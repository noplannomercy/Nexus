import subprocess
import threading
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path

import config
import core.graph_queries as graph_queries

router = APIRouter()


def _do_rebuild(rebuild_flag: dict) -> None:
    rebuild_flag["running"] = True
    try:
        graph_queries.init(config.GRAPH_JSON_PATH)
    finally:
        rebuild_flag["running"] = False


@router.post("/")
def trigger_rebuild():
    from api.main import rebuild_flag
    t = threading.Thread(target=_do_rebuild, args=(rebuild_flag,), daemon=True)
    t.start()
    return {"status": "ok", "message": "Rebuild started"}


@router.post("/upload")
def upload_and_update(file: UploadFile = File(...)):
    source_dir = Path(config.SOURCE_DIR)
    source_dir.mkdir(parents=True, exist_ok=True)
    dest = source_dir / file.filename

    with dest.open("wb") as f:
        f.write(file.file.read())

    result = subprocess.run(
        ["graphify", str(source_dir), "--update", "--no-viz"],
        capture_output=True,
        text=True,
        cwd="/app",
    )
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=result.stderr[:500])

    graph_json = Path(config.GRAPH_JSON_PATH)
    if not graph_json.exists():
        raise HTTPException(status_code=500, detail="graph.json not generated")

    graph_queries.init(config.GRAPH_JSON_PATH)
    stats = graph_queries.graph_stats()
    return {"status": "ok", "file": file.filename, "nodes": stats["nodes"], "edges": stats["edges"]}
