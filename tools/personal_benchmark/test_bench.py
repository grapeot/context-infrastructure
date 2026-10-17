import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).parent))
import bench
import demo


class BenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        shutil.copytree(Path(__file__).parent / "examples", self.source)
        self.store = self.root / "store"

    def draft(self, **changes):
        value = bench.read_json(self.source / "case.json")
        value.update(changes)
        (self.source / "case.json").write_bytes(bench.encode(value))

    def experiment(self):
        case = bench.freeze(self.store, self.source / "case.json")
        return bench.plan(self.store, case["case"], bench.read_json(self.source / "configurations.json"),
                          1, 2, "Test event")

    def attempt(self, plan, attempt_id, status="completed", **changes):
        (self.source / "answer.txt").write_text("Synthetic answer", encoding="utf-8")
        value = {"status": status, "input_sha256": plan["input_sha256"], "output_file": "answer.txt"}
        value.update(changes)
        path = self.source / "receipt.json"
        path.write_bytes(bench.encode(value))
        return bench.record(self.store, plan["plan_id"], attempt_id, path)

    def judgment(self, **changes):
        value = {"reviewer_kind": "ai", "reviewer": "test-reviewer", "verdict": "unknown",
                 "rationale": "Insufficient evidence", "next_evidence": "A real independent task",
                 "prior_exposure": "Synthetic test", "personal_value": "unknown"}
        value.update(changes)
        return value

    def test_freeze_idempotent_but_new_content_new_version(self):
        first = bench.freeze(self.store, self.source / "case.json")
        self.assertEqual(first, bench.freeze(self.store, self.source / "case.json"))
        (self.source / "input.txt").write_text("Changed input", encoding="utf-8")
        second = bench.freeze(self.store, self.source / "case.json")
        self.assertNotEqual(first["case"], second["case"])
        bench.verify(self.store, first["case"])

    def test_missing_provenance_and_hold_are_rejected(self):
        for changes in ({"sources": []}, {"status": "hold"}, {"criteria": []}):
            with self.subTest(changes=changes):
                original = (self.source / "case.json").read_bytes()
                self.draft(**changes)
                with self.assertRaises(ValueError):
                    bench.freeze(self.store, self.source / "case.json")
                (self.source / "case.json").write_bytes(original)

    def test_escaping_and_symlink_sources_rejected(self):
        for path in ("../secret.txt", "C:/secret.txt", "sub\\secret.txt", "/secret.txt"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                bench.inside(self.source, path)
        target = self.root / "secret.txt"
        target.write_text("private", encoding="utf-8")
        try:
            (self.source / "link.txt").symlink_to(target)
        except OSError:
            self.skipTest("Host does not permit symlink creation")
        with self.assertRaises(ValueError):
            bench.inside(self.source, "link.txt")

    def test_hidden_files_do_not_enter_export(self):
        plan = self.experiment()
        output = self.root / "export"
        bench.export_input(self.store, plan["plan_id"], "a001", output)
        self.assertEqual({p.name for p in output.iterdir()}, {"prompt.txt"})
        with self.assertRaises(ValueError):
            bench.export_input(self.store, plan["plan_id"], "a001", output)

    def test_snapshot_and_plan_drift_rejected(self):
        plan = self.experiment()
        path = bench.case_path(self.store, plan["case"]) / "hidden/rubric.txt"
        original = path.read_bytes()
        path.write_text("Changed rubric", encoding="utf-8")
        with self.assertRaises(ValueError):
            bench.load_plan(self.store, plan["plan_id"])
        path.write_bytes(original)
        plan_path = self.store / "plans" / plan["plan_id"] / "plan.json"
        changed = copy.deepcopy(plan)
        changed["configurations"][0]["requested_model"] = "different-model"
        plan_path.write_bytes(bench.encode(changed))
        with self.assertRaises(ValueError):
            bench.load_plan(self.store, plan["plan_id"])

    def test_budget_and_unknown_attempt_rejected(self):
        plan = self.experiment()
        with self.assertRaises(ValueError):
            bench.plan(self.store, plan["case"], plan["configurations"], 2, 3, "Too large")
        with self.assertRaises(ValueError):
            self.attempt(plan, "a999")

    def test_duplicate_attempt_and_wrong_input_rejected(self):
        plan = self.experiment()
        with self.assertRaises(ValueError):
            self.attempt(plan, "a001", input_sha256="wrong")
        self.attempt(plan, "a001")
        with self.assertRaises(FileExistsError):
            self.attempt(plan, "a001")

    def test_all_attempts_required_failure_retained(self):
        plan = self.experiment()
        self.attempt(plan, "a001")
        with self.assertRaises(ValueError):
            bench.blind(self.store, plan["plan_id"])
        self.attempt(plan, "a002", "timeout", output_file=None)
        queue = bench.blind(self.store, plan["plan_id"])
        self.assertEqual(queue, bench.blind(self.store, plan["plan_id"]))
        self.assertEqual((queue["attempt_count"], queue["non_completed_count"]), (2, 1))
        self.assertNotIn("example-baseline", json.dumps(queue))
        bench.review(self.store, plan["plan_id"], "A001", self.judgment())
        bench.unblind(self.store, plan["plan_id"])
        report = bench.report(self.store, plan["plan_id"])
        self.assertEqual(report["results"][1]["receipt"]["status"], "timeout")
        self.assertIsNone(report["results"][1]["review"])

    def test_review_attribution_reveal_gate_and_immutability(self):
        plan = self.experiment()
        for attempt in plan["attempts"]:
            self.attempt(plan, attempt["id"])
        bench.blind(self.store, plan["plan_id"])
        with self.assertRaises(ValueError):
            bench.unblind(self.store, plan["plan_id"])
        with self.assertRaises(ValueError):
            bench.review(self.store, plan["plan_id"], "A001", self.judgment(personal_value="useful"))
        review = bench.review(self.store, plan["plan_id"], "A001", self.judgment())
        self.assertEqual(review["reviewer_kind"], "ai")
        with self.assertRaises(FileExistsError):
            bench.review(self.store, plan["plan_id"], "A001", self.judgment())
        bench.review(self.store, plan["plan_id"], "A002", self.judgment(reviewer_kind="human", personal_value="unknown"))
        first = bench.unblind(self.store, plan["plan_id"])
        self.assertEqual(first, bench.unblind(self.store, plan["plan_id"]))
        with self.assertRaises(ValueError):
            bench.review(self.store, plan["plan_id"], "A001", self.judgment())

    def test_tampered_record_is_rejected(self):
        plan = self.experiment()
        self.attempt(plan, "a001")
        self.attempt(plan, "a002")
        path = self.store / "plans" / plan["plan_id"] / "attempts/a001.json"
        value = bench.read_json(path)
        value["resolved_model"] = "changed-identity"
        path.write_bytes(bench.encode(value))
        with self.assertRaises(ValueError):
            bench.blind(self.store, plan["plan_id"])

    def test_offline_demo_has_no_personal_or_real_model_claim(self):
        report = demo.run(self.store)
        self.assertEqual(len(report["results"]), 2)
        self.assertEqual(report["case"]["sources"][0]["kind"], "synthetic")
        self.assertEqual(report["case"]["importance"]["value"], "unknown")
        for result in report["results"]:
            self.assertIsNone(result["receipt"]["resolved_model"])
            self.assertEqual(result["review"]["personal_value"], "unknown")

    def test_cli_lifecycle_and_error_exit(self):
        def cli(*args):
            result = subprocess.run([sys.executable, str(Path(__file__).parent / "bench.py"),
                                     "--store", str(self.store), *map(str, args)],
                                    capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)
        case = cli("freeze", self.source / "case.json")
        cli("verify", case["case"])
        plan = cli("plan", case["case"], self.source / "configurations.json",
                   "--repeats", "1", "--max-attempts", "2", "--event", "CLI smoke")
        for attempt in plan["attempts"]:
            cli("export", plan["plan_id"], attempt["id"], self.root / attempt["id"])
            (self.source / "answer.txt").write_text("Synthetic answer", encoding="utf-8")
            (self.source / "receipt.json").write_bytes(bench.encode({
                "status": "completed", "input_sha256": plan["input_sha256"], "output_file": "answer.txt"}))
            cli("record", plan["plan_id"], attempt["id"], self.source / "receipt.json")
        queue = cli("blind", plan["plan_id"])
        (self.source / "judgment.json").write_bytes(bench.encode(self.judgment()))
        for answer in queue["answers"]:
            cli("review", plan["plan_id"], answer["label"], self.source / "judgment.json")
        cli("unblind", plan["plan_id"])
        self.assertEqual(len(cli("report", plan["plan_id"])["results"]), 2)
        invalid = subprocess.run([sys.executable, str(Path(__file__).parent / "bench.py"),
                                  "--store", str(self.store), "verify", "../bad"],
                                 capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(invalid.returncode, 2)
        self.assertIn("error", json.loads(invalid.stderr))


if __name__ == "__main__":
    unittest.main()
