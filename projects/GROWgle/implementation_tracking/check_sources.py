#!/usr/bin/env python3
"""Check growing GROWgle Markdown inventory without changing publication status."""
import argparse
import json
import os
from pathlib import Path
import re
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
REPO = "KuraMasajapan/AI-Harness"
PREFIX = "projects/GROWgle/"
OTHER = {"HIROSHIMA", "HYOGO", "OSAKA", "KYOTO", "SHIKOKU"}

def is_source(path):
    return (path.startswith(PREFIX) and path.endswith(".md") and
            not path.startswith(PREFIX + "implementation_tracking/"))

def get_scope(path, previous):
    if previous:
        return previous.get("scope", "NEEDS_SCOPE_REVIEW")
    if path[len(PREFIX):].split("/")[0] in OTHER:
        return "FUTURE_REGION"
    return "NEEDS_SCOPE_REVIEW"

def analyze(manifest, tree):
    if tree.get("truncated") or not isinstance(tree.get("tree"), list):
        raise ValueError("Incomplete GitHub tree; audit cannot be trusted")
    previous = {r["path"]: r for r in manifest["files"] if is_source(r["path"])}
    current = {r["path"]: r["sha"] for r in tree["tree"]
               if r.get("type") == "blob" and is_source(r.get("path", ""))}
    if not current:
        raise ValueError("No GROWgle MD files returned; refusing false empty report")
    changed = []
    for path in sorted(set(previous) | set(current)):
        old = previous.get(path)
        if old is None:
            action = "NEW"
        elif path not in current:
            action = "REMOVED_OR_MOVED"
        elif old["blob_sha"] != current[path]:
            action = "UPDATED"
        else:
            continue
        changed.append({"path": path, "change": action,
                        "scope": get_scope(path, old),
                        "previous_status": old.get("document_status") if old else None})
    pending = [{"path": path, "status": previous[path]["document_status"],
                "sample_cards": len(previous[path].get("prototype_record_ids", []))}
               for path in sorted(set(previous) & set(current))
               if previous[path]["blob_sha"] == current[path]
               and previous[path].get("scope") == "OKAYAMA_PILOT"
               and previous[path].get("document_status") in ("UNASSESSED", "PARTIAL_PROTOTYPE")]
    return {"scanned_md": len(current), "changes": changed, "pending": pending,
            "baseline_date": manifest.get("snapshot_date", "unknown")}

def markdown(data, ref):
    ref = ref if re.fullmatch(r"[0-9a-fA-F]{40}", ref) else "main"
    def link(path):
        safe_text = path.replace("[", "\\[").replace("]", "\\]")
        return f"[{safe_text}](https://github.com/{REPO}/blob/{ref}/{quote(path, safe='/')})"
    lines = ["# GROWgle MD取り込みチェック", "",
             "**注意：差分検出は実装済み・公開承認済みの判定ではありません。**", "",
             f"- GitHub内のMD：{data['scanned_md']}件（追跡用ファイルを除く）",
             f"- 新規・更新・削除：{len(data['changes'])}件",
             f"- 未精査または一部実装：{len(data['pending'])}件",
             f"- 基準日：{data['baseline_date']}", ""]
    for action, title in (("NEW", "新規MD"), ("UPDATED", "更新MD"), ("REMOVED_OR_MOVED", "削除・移動の疑い")):
        rows = [r for r in data["changes"] if r["change"] == action]
        lines += [f"## {title}（{len(rows)}件）", ""]
        lines += [f"- {link(r['path'])} — {r['scope']}（確認待ち）" for r in rows[:100]] or ["- なし"]
        if len(rows) > 100:
            lines += [f"- 残り{len(rows)-100}件は添付JSONを参照"]
        lines += [""]
    lines += [f"## 既存の未精査・一部実装資料（{len(data['pending'])}件）", ""]
    lines += [f"- {link(r['path'])} — {r['status']}（v0.5参考抽出 {r['sample_cards']}件）" for r in data["pending"][:100]] or ["- なし"]
    lines += ["", "### 運用上の注意", "",
              "- 1ファイルの一部だけが試作に入っても実装完了ではありません。",
              "- 将来対象の他県資料は岡山県の未実装項目に混ぜません。",
              "- ファイルの差分しか自動判定しません。個別企画の重複・掲載状況は別途照合します。",
              "- 読み取り専用。既存の原文・サイト・台帳・公開承認状態は変更しません。", ""]
    return "\n".join(lines)

def fetch_tree(ref):
    if not re.fullmatch(r"[0-9a-fA-F]{40}|main", ref):
        raise ValueError("Invalid GitHub ref")
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "GROWgle-MD-intake"}
    token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    url = f"https://api.github.com/repos/{REPO}/git/trees/{ref}?recursive=1"
    with urlopen(Request(url, headers=headers), timeout=35) as response:
        return json.load(response)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", default=os.getenv("GITHUB_SHA") or "main")
    parser.add_argument("--manifest", type=Path, default=ROOT/"source_inventory.json")
    parser.add_argument("--tree-json", type=Path, help="Offline test fixture")
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--markdown-out", type=Path)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    tree = json.loads(args.tree_json.read_text(encoding="utf-8")) if args.tree_json else fetch_tree(args.ref)
    data = analyze(manifest, tree)
    report = markdown(data, args.ref)
    print(report)
    for target, output in ((args.json_out, json.dumps(data, indent=2, ensure_ascii=False)+"\n"),
                           (args.markdown_out, report)):
        if target:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(output, encoding="utf-8")

if __name__ == "__main__":
    main()
