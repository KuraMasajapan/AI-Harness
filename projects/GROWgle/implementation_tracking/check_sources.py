#!/usr/bin/env python3
"""Detect new/updated Markdown in GROWgle and report intake status.
Run: python3 projects/GROWgle/implementation_tracking/check_sources.py
Optional: GITHUB_TOKEN=... (for API rate limits). No writes to GitHub.
"""
import json, os, pathlib, urllib.request, sys
ROOT=pathlib.Path(__file__).resolve().parent
DATA=json.loads((ROOT/"source_inventory.json").read_text(encoding="utf-8"))
URL="https://api.github.com/repos/KuraMasajapan/AI-Harness/git/trees/main?recursive=1"
headers={"User-Agent":"GROWgle-source-tracking","Accept":"application/vnd.github+json"}
if os.getenv("GITHUB_TOKEN"): headers["Authorization"]="Bearer "+os.environ["GITHUB_TOKEN"]
with urllib.request.urlopen(urllib.request.Request(URL,headers=headers),timeout=25) as resp:
    tree=json.load(resp)
if tree.get("truncated"): sys.exit("ERROR: GitHub tree truncated; cannot audit safely.")
other={"HIROSHIMA","HYOGO","OSAKA","KYOTO","SHIKOKU"}
def selected(p):
    return p.startswith("projects/GROWgle/") and p.endswith(".md") and p.split("/")[2] not in other and "implementation_tracking/" not in p
latest={r["path"]:r["sha"] for r in tree["tree"] if r.get("type")=="blob" and selected(r["path"])}
baseline={r["path"]:r for r in DATA["files"] if selected(r["path"])}
new=sorted(set(latest)-set(baseline))
changed=sorted(p for p in latest.keys() & baseline.keys() if latest[p]!=baseline[p]["blob_sha"])
removed=sorted(set(baseline)-set(latest))
pending=sorted(p for p in latest.keys() & baseline.keys() if latest[p]==baseline[p]["blob_sha"] and baseline[p]["document_status"] in ("UNASSESSED","PARTIAL_PROTOTYPE"))
for title,paths in [("NEW MD",new),("UPDATED MD",changed),("DELETED/MOVED",removed),("PENDING REVIEW OR PARTIAL",pending)]:
    print("\n"+title+" ("+str(len(paths))+")")
    for p in paths: print(" - "+p)
print("\nNOTE: No unchanged/partially indexed MD is automatically considered fully implemented.")
print("NOTE: This script does not publish content, nor change the ledger.")
