#!/usr/bin/env python3
"""Resumable Batch Runner for Static-Guided Dynamic UTG Collection (ADB + OpenAI-compatible LLM)."""
from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR.parent) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR.parent))

from a11y_utg_agent.device_bridge import DEFAULT_ADB_PATH
from a11y_utg_agent.gui_agent import parse_args as parse_single_args, run_agent
from a11y_utg_agent.storyboard import build_storyboard_for_run, refine_refusal_outcome


def main() -> None:
    p = argparse.ArgumentParser(description="Batch run Mobile A11y UTG Agent over a directory of APKs.")
    p.add_argument("--apk-dir", required=True, help="Directory containing .apk files to analyze")
    p.add_argument("--static-dir", default=None, help="Optional directory containing per-APK static analysis JSONs")
    p.add_argument("--output-dir", default="./utg_output", help="Directory to store UTG traces, HarmonyOS JSONs, and storyboards")
    p.add_argument("--device", default=None, help="ADB serial (e.g. emulator-5554); optional if single device connected")
    p.add_argument("--adb-path", default=DEFAULT_ADB_PATH)
    p.add_argument("--model", default=None)
    p.add_argument("--base-url", default=None)
    p.add_argument("--api-key", default=None)
    p.add_argument("--mode", choices=("hybrid", "vision_only", "layout_only"), default="hybrid")
    p.add_argument("--max-steps", type=int, default=8)
    p.add_argument("--offline", action="store_true", help="Disable device Wi-Fi & mobile data (recommended for malware)")
    p.add_argument("--no-zh-captions", action="store_true", help="Skip LLM Chinese storyboard caption generation")
    p.add_argument("--resume", action="store_true", default=True)
    args = p.parse_args()

    apk_dir = Path(args.apk_dir)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ledger_p = out_dir / "batch_ledger.json"

    existing: dict[str, dict[str, Any]] = {}
    if args.resume and ledger_p.is_file():
        for rec in json.loads(ledger_p.read_text(encoding="utf-8")):
            existing[rec["apk_name"]] = rec

    apks = sorted(apk_dir.glob("*.apk"))
    print(f"[BATCH] Found {len(apks)} APKs in {apk_dir} | already completed={len(existing)}")

    for idx, apk_p in enumerate(apks, 1):
        if apk_p.name in existing:
            print(f"[SKIP {idx}/{len(apks)}] {apk_p.name}")
            continue
        static_json = None
        if args.static_dir:
            cand = Path(args.static_dir) / (apk_p.stem + ".json")
            if cand.is_file():
                static_json = str(cand)

        argv = [
            "--adb-path", args.adb_path,
            "--mode", args.mode,
            "--apk", str(apk_p),
            "--max_steps", str(args.max_steps),
            "--output_dir", str(out_dir),
            "--tag", apk_p.stem[:40],
            "--uninstall_after",
            "--clean_sandbox",
            "--stop_on_a11y_hook",
            "--capture_service_detail",
            "--probe_refusal",
            "--map_system_settings",
        ]
        if args.device:
            argv.extend(["--device", args.device])
        if args.model:
            argv.extend(["--model", args.model])
        if args.base_url:
            argv.extend(["--base-url", args.base_url])
        if args.api_key:
            argv.extend(["--api-key", args.api_key])
        if static_json:
            argv.extend(["--static_json", static_json, "--allow_activity_fallback"])
        if args.offline:
            argv.append("--offline")

        t0 = time.time()
        run_dir, trace = run_agent(parse_single_args(argv))
        ref = refine_refusal_outcome(trace)
        build_storyboard_for_run(
            run_dir, trace, ref,
            with_zh_captions=not args.no_zh_captions,
            model=args.model, base_url=args.base_url, api_key=args.api_key,
        )
        existing[apk_p.name] = {
            "apk_name": apk_p.name,
            "target_package": trace.get("target_package", ""),
            "final_status": trace.get("final_status", ""),
            "reached_a11y_hook": bool(trace.get("trigger_events")),
            "refusal_outcome": ref,
            "steps": len(trace.get("steps") or []),
            "elapsed_s": round(time.time() - t0, 1),
            "run_dir": run_dir.name,
            "updated_at": datetime.now().isoformat(timespec="seconds"),
        }
        ledger_p.write_text(json.dumps(list(existing.values()), indent=2, ensure_ascii=False), encoding="utf-8")

    csv_p = out_dir / "batch_ledger.csv"
    rows = list(existing.values())
    if rows:
        with csv_p.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    print(f"[BATCH DONE] {len(rows)} APKs processed -> {ledger_p}")


if __name__ == "__main__":
    main()
