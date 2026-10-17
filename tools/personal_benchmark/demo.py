"""Offline synthetic lifecycle; no model calls and no personal source reads."""
import argparse
import json
from pathlib import Path
import tempfile

import bench


def run(store):
    examples = Path(__file__).parent / "examples"
    case = bench.freeze(store, examples / "case.json")
    experiment = bench.plan(store, case["case"], bench.read_json(examples / "configurations.json"),
                            repeats=1, max_attempts=2, event="Synthetic offline demonstration")
    with tempfile.TemporaryDirectory() as temporary:
        source = Path(temporary)
        for attempt in experiment["attempts"]:
            bench.export_input(store, experiment["plan_id"], attempt["id"], source / attempt["id"])
            (source / "answer.txt").write_text(
                "项目暂停。2025-01-03记录软件修复完成，2025-01-04因设备未到而暂停；设备验收未知。",
                encoding="utf-8")
            bench.save_new(source / (attempt["id"] + ".json"), {
                "status": "completed", "input_sha256": experiment["input_sha256"],
                "output_file": "answer.txt", "runtime": "Synthetic fixture, not a model run",
                "resolved_model": None, "assistance": "Prewritten demonstration answer"})
            bench.record(store, experiment["plan_id"], attempt["id"], source / (attempt["id"] + ".json"))
    queue = bench.blind(store, experiment["plan_id"])
    for answer in queue["answers"]:
        bench.review(store, experiment["plan_id"], answer["label"], {
            "reviewer_kind": "ai", "reviewer": "synthetic-demo-fixture", "verdict": "satisfied",
            "rationale": "Prewritten fixture judgment for checking the recording lifecycle only.",
            "prior_exposure": "Demo generated both answers; this is not an independent evaluation.",
            "next_evidence": "Replace this fixture with a real, attributed task and independent review.",
            "personal_value": "unknown"})
    bench.unblind(store, experiment["plan_id"])
    return bench.report(store, experiment["plan_id"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store", type=Path, default=Path(".personal_benchmark/demo"))
    args = parser.parse_args()
    print(json.dumps(run(args.store.resolve()), ensure_ascii=False, indent=2))
