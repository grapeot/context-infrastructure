#!/usr/bin/env python3
"""Local, provider-neutral benchmark records. Never invokes a model or a shell."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import secrets
import shutil
import sys
import tempfile
import uuid

MAX_FILE_BYTES = 8 * 1024 * 1024
STATUSES = {"completed", "error", "timeout", "cancelled"}
VERDICTS = {"satisfied", "gap", "failed", "unknown"}


def now():
    return datetime.now(timezone.utc).isoformat()


def encode(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_bytes(path):
    with Path(path).open("rb") as stream:
        data = stream.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        raise ValueError("File exceeds 8 MiB: " + str(path))
    return data


def read_json(path):
    return json.loads(read_bytes(path).decode("utf-8-sig"))


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}", value):
        raise ValueError("Invalid identifier")
    return value


def text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(name + " must be nonempty text")
    return value


def inside(base, relative):
    """Reject absolute paths, traversal, Windows alternate streams and symlinks."""
    if not isinstance(relative, str) or "\\" in relative or ":" in relative:
        raise ValueError("Use a relative forward-slash path")
    path = Path(relative)
    if path.is_absolute() or not path.parts or any(p in {".", ".."} for p in path.parts):
        raise ValueError("Path escapes its input directory")
    result = Path(base).resolve().joinpath(path)
    current = Path(base).resolve()
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("Symlink input is not supported")
    if not result.resolve().is_relative_to(Path(base).resolve()):
        raise ValueError("Path escapes its input directory")
    return result


def save_new(path, value):
    """Exclusive creation: a submitted record cannot be silently overwritten."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(encode(value))


def case_path(store, reference):
    parts = reference.split("/")
    if len(parts) != 2:
        raise ValueError("Case reference must be task_id/version")
    return inside(store, "cases/" + "/".join(identifier(p) for p in parts))


def verify(store, reference):
    path = case_path(store, reference)
    manifest = read_json(path / "manifest.json")
    files = manifest["files"]
    actual = {p.relative_to(path).as_posix() for p in path.rglob("*") if p.is_file()}
    if actual != set(files) | {"manifest.json"}:
        raise ValueError("Snapshot file inventory changed")
    for name, expected in files.items():
        if digest(read_bytes(inside(path, name))) != expected:
            raise ValueError("Snapshot changed: " + name)
    version = digest(encode(files))
    if reference.split("/")[1] != version or manifest["version"] != version:
        raise ValueError("Snapshot version does not match its contents")
    visible = {name: value for name, value in files.items() if name.startswith("input/")}
    if manifest["input_sha256"] != digest(encode(visible)):
        raise ValueError("Visible input digest changed")
    return manifest


def freeze(store, draft_path):
    draft_path = Path(draft_path).resolve()
    draft = read_json(draft_path)
    task_id = identifier(draft["task_id"])
    if draft.get("status") != "ready":
        raise ValueError("Only ready cases can be frozen; preserve holds and evidence gaps")
    for field in ("title", "start_point", "independence_group"):
        text(draft.get(field), field)
    sources = draft.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("At least one attributed source is required")
    for source in sources:
        if source.get("kind") not in {"record", "recollection", "inference", "synthetic"}:
            raise ValueError("Unknown source kind")
        text(source.get("locator"), "source locator")
    criteria = draft.get("criteria")
    if not isinstance(criteria, list) or not criteria:
        raise ValueError("Task-specific criteria are required")
    ids = set()
    for criterion in criteria:
        cid = identifier(criterion["id"])
        if cid in ids:
            raise ValueError("Duplicate criterion")
        ids.add(cid)
        text(criterion.get("description"), "criterion description")
        if criterion.get("origin") not in {"original", "clarification", "retrospective"}:
            raise ValueError("Criterion origin must be explicit")
    if not isinstance(draft.get("limitations"), list):
        raise ValueError("List known limitations, including an empty list when appropriate")
    payload = {
        "input/prompt.txt": read_bytes(inside(draft_path.parent, draft["prompt_file"])),
        "hidden/rubric.txt": read_bytes(inside(draft_path.parent, draft["rubric_file"])),
    }
    for group, prefix in (("attachments", "input/attachments"), ("evidence_files", "hidden/evidence")):
        for item in draft.get(group, []):
            name = item["name"]
            if not re.fullmatch(r"[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)?", name):
                raise ValueError("Use a simple portable attachment name")
            dest = prefix + "/" + name
            if dest.casefold() in {key.casefold() for key in payload}:
                raise ValueError("Duplicate attachment name")
            payload[dest] = read_bytes(inside(draft_path.parent, item["file"]))
    metadata = {key: draft[key] for key in (
        "task_id", "title", "start_point", "independence_group", "sources", "criteria", "limitations"
    )}
    metadata["importance"] = draft.get("importance", {"value": "unknown", "basis": None})
    payload["case.json"] = encode(metadata)
    hashes = {name: digest(data) for name, data in payload.items()}
    version = digest(encode(hashes))
    reference = task_id + "/" + version
    target = case_path(store, reference)
    if target.exists():
        return {"case": reference, **verify(store, reference)}
    manifest = {"version": version, "files": hashes, "created_at": now(),
                "input_sha256": digest(encode({k: v for k, v in hashes.items() if k.startswith("input/")}))}
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=target.parent) as temporary:
        stage = Path(temporary) / "snapshot"
        for name, data in payload.items():
            output = stage / name
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(data)
        save_new(stage / "manifest.json", manifest)
        stage.rename(target)
    return {"case": reference, **verify(store, reference)}


def load_plan(store, plan_id):
    path = inside(store, "plans/" + identifier(plan_id))
    plan = read_json(path / "plan.json")
    content = {k: v for k, v in plan.items() if k != "plan_sha256"}
    if plan.get("plan_sha256") != digest(encode(content)):
        raise ValueError("Plan changed after registration")
    if plan["plan_id"] != plan_id:
        raise ValueError("Plan identity mismatch")
    manifest = verify(store, plan["case"])
    if plan["input_sha256"] != manifest["input_sha256"]:
        raise ValueError("Plan input mismatch")
    return path, plan


def plan(store, reference, configurations, repeats, max_attempts, event):
    manifest = verify(store, reference)
    if not isinstance(configurations, list) or not configurations:
        raise ValueError("At least one model configuration is required")
    for config in configurations:
        if not isinstance(config, dict):
            raise ValueError("Each configuration must be an object")
        text(config.get("requested_model"), "requested_model")
        text(config.get("conditions"), "conditions (effort, tools, environment and budget)")
    if type(repeats) is not int or repeats < 1 or type(max_attempts) is not int:
        raise ValueError("Specify positive repetitions and an integer attempt ceiling")
    count = repeats * len(configurations)
    if not 1 <= count <= max_attempts <= 100:
        raise ValueError("Plan exceeds the explicit attempt ceiling (maximum 100)")
    plan_id = "p-" + uuid.uuid4().hex
    value = {"plan_id": plan_id, "case": reference, "created_at": now(),
             "event": text(event, "event"), "input_sha256": manifest["input_sha256"],
             "configurations": configurations, "max_attempts": max_attempts,
             "attempts": [{"id": "a%03d" % (i * repeats + r + 1), "configuration": i,
                           "repeat": r + 1} for i in range(len(configurations)) for r in range(repeats)]}
    value["plan_sha256"] = digest(encode(value))
    save_new(inside(store, "plans/" + plan_id + "/plan.json"), value)
    return value


def export_input(store, plan_id, attempt_id, destination):
    _, value = load_plan(store, plan_id)
    attempt = next((a for a in value["attempts"] if a["id"] == attempt_id), None)
    if attempt is None:
        raise ValueError("Unknown attempt")
    destination = Path(destination)
    if destination.exists():
        raise ValueError("Input export requires a new directory")
    shutil.copytree(case_path(store, value["case"]) / "input", destination)
    return {"directory": str(destination), "input_sha256": value["input_sha256"],
            "configuration": value["configurations"][attempt["configuration"]]}


def record(store, plan_id, attempt_id, receipt_path):
    directory, value = load_plan(store, plan_id)
    attempt_id = identifier(attempt_id)
    if not any(a["id"] == attempt_id for a in value["attempts"]):
        raise ValueError("Unknown attempt")
    if (directory / "review_snapshot").exists():
        raise ValueError("Attempt population is frozen for review")
    receipt_path = Path(receipt_path).resolve()
    receipt = read_json(receipt_path)
    if receipt.get("status") not in STATUSES:
        raise ValueError("Record a terminal status, including failures")
    if receipt.get("input_sha256") != value["input_sha256"]:
        raise ValueError("Receipt must declare the exact exported input digest")
    answer = None
    if receipt.get("output_file"):
        answer = read_bytes(inside(receipt_path.parent, receipt["output_file"])).decode("utf-8-sig")
    if receipt["status"] == "completed" and not (answer and answer.strip()):
        raise ValueError("Completed attempts require an answer")
    result = {"attempt_id": attempt_id, "status": receipt["status"], "recorded_at": now(),
              "input_sha256": value["input_sha256"], "answer": answer,
              "output_sha256": digest(answer.encode("utf-8")) if answer is not None else None,
              "provenance": "imported_receipt_not_independently_attested"}
    for key in ("resolved_model", "runtime", "assistance", "usage", "error", "checks"):
        result[key] = receipt.get(key)
    result["record_sha256"] = digest(encode(result))
    save_new(directory / "attempts" / (attempt_id + ".json"), result)
    return result


def records(directory, value):
    result = []
    for attempt in value["attempts"]:
        path = directory / "attempts" / (attempt["id"] + ".json")
        if not path.exists():
            raise ValueError("Record every planned attempt, including failures, before review")
        record_value = read_json(path)
        content = {k: v for k, v in record_value.items() if k != "record_sha256"}
        if record_value.get("record_sha256") != digest(encode(content)):
            raise ValueError("Attempt record changed")
        answer = record_value["answer"]
        expected = digest(answer.encode("utf-8")) if answer is not None else None
        if (record_value["attempt_id"] != attempt["id"] or
                record_value["input_sha256"] != value["input_sha256"] or
                record_value["output_sha256"] != expected):
            raise ValueError("Attempt integrity mismatch")
        result.append(record_value)
    return result


def blind(store, plan_id):
    directory, value = load_plan(store, plan_id)
    attempts = records(directory, value)
    if (directory / "review_snapshot").exists():
        return read_json(directory / "review_snapshot/queue.json")
    completed = [r for r in attempts if r["status"] == "completed"]
    secrets.SystemRandom().shuffle(completed)
    mapping = {"A%03d" % (i + 1): r["attempt_id"] for i, r in enumerate(completed)}
    case = case_path(store, value["case"])
    result = {"plan_id": plan_id, "title": read_json(case / "case.json")["title"],
              "prompt": read_bytes(case / "input/prompt.txt").decode("utf-8-sig"),
              "rubric": read_bytes(case / "hidden/rubric.txt").decode("utf-8-sig"),
              "criteria": read_json(case / "case.json")["criteria"],
              "answers": [{"label": label, "text": r["answer"]}
                          for label, r in zip(mapping, completed)],
              "attempt_count": len(attempts), "non_completed_count": len(attempts) - len(completed)}
    # Separate the entire review snapshot from its identity mapping in one directory rename.
    with tempfile.TemporaryDirectory(dir=directory) as temporary:
        stage = Path(temporary) / "review"
        save_new(stage / "mapping.json", mapping)
        save_new(stage / "queue.json", result)
        stage.rename(directory / "review_snapshot")
    return result


def review(store, plan_id, label, judgment):
    directory, _ = load_plan(store, plan_id)
    if (directory / "unblinded.json").exists():
        raise ValueError("Anonymous review is closed after identity reveal")
    queue = read_json(directory / "review_snapshot/queue.json")
    if label not in {a["label"] for a in queue["answers"]}:
        raise ValueError("Unknown anonymous label")
    if judgment.get("verdict") not in VERDICTS or judgment.get("reviewer_kind") not in {"ai", "human"}:
        raise ValueError("Explicit verdict and reviewer_kind (ai/human) are required")
    for field in ("reviewer", "rationale", "next_evidence", "prior_exposure"):
        text(judgment.get(field), field)
    personal_value = judgment.get("personal_value", "unknown")
    if judgment["reviewer_kind"] == "ai" and personal_value != "unknown":
        raise ValueError("AI review cannot supply personal value calibration")
    result = {key: judgment[key] for key in
              ("verdict", "reviewer_kind", "reviewer", "rationale", "next_evidence", "prior_exposure")}
    result.update(label=label, recorded_at=now(), personal_value=personal_value)
    save_new(directory / "reviews" / (identifier(label) + ".json"), result)
    return result


def unblind(store, plan_id):
    directory, value = load_plan(store, plan_id)
    records(directory, value)
    queue = read_json(directory / "review_snapshot/queue.json")
    for answer in queue["answers"]:
        if not (directory / "reviews" / (answer["label"] + ".json")).exists():
            raise ValueError("Review every completed answer before revealing identities")
    mapping = read_json(directory / "review_snapshot/mapping.json")
    result = {"revealed_at": now(), "mapping": mapping}
    path = directory / "unblinded.json"
    if not path.exists():
        save_new(path, result)
    return read_json(path)


def report(store, plan_id):
    directory, value = load_plan(store, plan_id)
    if not (directory / "unblinded.json").exists():
        raise ValueError("Complete anonymous review and reveal before the comparison report")
    attempts = {r["attempt_id"]: r for r in records(directory, value)}
    revealed = read_json(directory / "unblinded.json")
    labels = {attempt: label for label, attempt in revealed["mapping"].items()}
    results = []
    for attempt in value["attempts"]:
        record_value = attempts[attempt["id"]]
        label = labels.get(attempt["id"])
        judgment = read_json(directory / "reviews" / (label + ".json")) if label else None
        results.append({"attempt_id": attempt["id"], "repeat": attempt["repeat"],
                        "configuration": value["configurations"][attempt["configuration"]],
                        "receipt": record_value, "review": judgment})
    return {"case": read_json(case_path(store, value["case"]) / "case.json"),
            "plan": value, "results": results,
            "scope": "One task condition; repeated attempts are not independent tasks. No overall model rank.",
            "verification": "Imported execution/check receipts are declarations, not runtime attestation.",
            "personal_value": "Use attributed human calibration; unknown remains unknown."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store", type=Path, default=Path(".personal_benchmark"))
    commands = parser.add_subparsers(dest="command", required=True)
    p = commands.add_parser("freeze"); p.add_argument("draft", type=Path)
    p = commands.add_parser("verify"); p.add_argument("case")
    p = commands.add_parser("plan"); p.add_argument("case"); p.add_argument("configurations", type=Path)
    p.add_argument("--repeats", type=int, default=2); p.add_argument("--max-attempts", type=int, required=True)
    p.add_argument("--event", required=True)
    p = commands.add_parser("export"); p.add_argument("plan"); p.add_argument("attempt"); p.add_argument("destination", type=Path)
    p = commands.add_parser("record"); p.add_argument("plan"); p.add_argument("attempt"); p.add_argument("receipt", type=Path)
    for command in ("blind", "unblind", "report"):
        commands.add_parser(command).add_argument("plan")
    p = commands.add_parser("review"); p.add_argument("plan"); p.add_argument("label"); p.add_argument("judgment", type=Path)
    args = parser.parse_args(argv)
    store = args.store.resolve()
    try:
        if args.command == "freeze": result = freeze(store, args.draft)
        elif args.command == "verify": result = verify(store, args.case)
        elif args.command == "plan": result = plan(store, args.case, read_json(args.configurations), args.repeats, args.max_attempts, args.event)
        elif args.command == "export": result = export_input(store, args.plan, args.attempt, args.destination)
        elif args.command == "record": result = record(store, args.plan, args.attempt, args.receipt)
        elif args.command == "review": result = review(store, args.plan, args.label, read_json(args.judgment))
        else: result = {"blind": blind, "unblind": unblind, "report": report}[args.command](store, args.plan)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"error": type(exc).__name__, "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
