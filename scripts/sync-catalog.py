#!/usr/bin/env python3
"""
sync-catalog.py  —  sync packwiz packs → catalog.json

Czyta pack.toml z każdego folderu paczki w repo,
aktualizuje pola packwiz w catalog.json.
Metadane Notion (notion_id, title, status itd.) są zachowywane.
Nowe paczki dostają puste pola Notion.

Użycie:
  python scripts/sync-catalog.py
  GITHUB_TOKEN=ghp_xxx python scripts/sync-catalog.py
"""

import json, requests, base64, datetime, os, sys

REPO = "karolkuter-boop/fftv-modpacks"
SKIP = {"_template", "scripts", "mods-cdn"}
PACKWIZ_BASE = "https://karolkuter-boop.github.io/fftv-modpacks"


def parse_pack_toml(content):
    result = {}
    section = None
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and not line.startswith("[["):
            section = line.strip("[]").strip()
        elif "=" in line:
            k, _, v = line.partition("=")
            k, v = k.strip(), v.strip().strip('"')
            result[(f"{section}.{k}" if section else k)] = v
    return result


def main():
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print("ERROR: Ustaw GITHUB_TOKEN", file=sys.stderr)
        sys.exit(1)

    hdrs = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}

    # Pobierz aktualny catalog.json
    r = requests.get(f"https://api.github.com/repos/{REPO}/contents/catalog.json", headers=hdrs)
    r.raise_for_status()
    cat_meta = r.json()
    catalog = json.loads(base64.b64decode(cat_meta["content"]).decode())
    cat_sha = cat_meta["sha"]
    existing = {p["id"]: p for p in catalog.get("packs", [])}

    # Pobierz listę folderów z root repo
    r = requests.get(f"https://api.github.com/repos/{REPO}/contents/", headers=hdrs)
    r.raise_for_status()
    dirs = sorted(f["name"] for f in r.json() if f["type"] == "dir" and f["name"] not in SKIP)

    updated = []
    for d in dirs:
        r = requests.get(f"https://api.github.com/repos/{REPO}/contents/{d}/pack.toml", headers=hdrs)
        if r.status_code != 200:
            continue
        fields = parse_pack_toml(base64.b64decode(r.json()["content"]).decode())

        loader = next((k.split(".")[1] for k in fields if k.startswith("versions.") and k != "versions.minecraft"), "")
        loader_ver = next((v for k, v in fields.items() if k.startswith("versions.") and k != "versions.minecraft"), "")

        entry = dict(existing.get(d, {
            "id": d,
            "notion_id": "",
            "notion_url": "",
            "icon": "📦",
            "title": fields.get("name", d),
            "status": "WIP",
            "series": [],
            "channel": "",
            "recording_date": "",
        }))
        entry.update({
            "id": d,
            "packwiz_url": f"{PACKWIZ_BASE}/{d}/pack.toml",
            "pack_version": fields.get("version", ""),
            "mc": fields.get("versions.minecraft", ""),
            "index_hash": fields.get("index.hash", ""),
            "loader": loader,
            "loader_version": loader_ver,
        })
        updated.append(entry)
        marker = "NEW" if d not in existing else "upd"
        print(f"  [{marker}] {d}: {entry['mc']} {loader} {loader_ver}  hash={entry['index_hash'][:12]}…")

    catalog["packs"] = updated
    catalog["updated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

    new_content = json.dumps(catalog, ensure_ascii=False, indent=2) + "\n"
    r = requests.put(
        f"https://api.github.com/repos/{REPO}/contents/catalog.json",
        headers=hdrs,
        json={
            "message": "sync: update catalog.json from pack.toml",
            "content": base64.b64encode(new_content.encode()).decode(),
            "sha": cat_sha,
        }
    )
    r.raise_for_status()
    print(f"\n✓ catalog.json zaktualizowany ({len(updated)} paczek)")


if __name__ == "__main__":
    main()
