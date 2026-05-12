from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from pathlib import Path

import config
import core.graph_queries as graph_queries

router = APIRouter()


class KeywordSearchRequest(BaseModel):
    keywords: list[str]
    hops: int = 1
    project_id: str = "default"


@router.get("/node/{node_id}")
def get_node(node_id: str, project_id: str = "default"):
    node = graph_queries.get_node(node_id, project_id)
    if node is None:
        raise HTTPException(status_code=404, detail="Node not found")
    return node


@router.get("/neighbors/{node_id}")
def get_neighbors(node_id: str, depth: int = 1, project_id: str = "default"):
    return graph_queries.get_neighbors(node_id, depth=depth, project_id=project_id)


@router.get("/community/{community_id}")
def get_community(community_id: int, project_id: str = "default"):
    return graph_queries.get_community(community_id, project_id)


@router.get("/god-nodes")
def god_nodes(limit: int = 10, project_id: str = "default"):
    return graph_queries.god_nodes(limit=limit, project_id=project_id)


@router.get("/stats")
def graph_stats(project_id: str = "default"):
    return graph_queries.graph_stats(project_id)


@router.get("/path")
def shortest_path(src: str, dst: str, project_id: str = "default"):
    path = graph_queries.shortest_path(src, dst, project_id)
    if path is None or path == []:
        raise HTTPException(status_code=404, detail="No path found")
    return path


@router.post("/search")
def keyword_search(body: KeywordSearchRequest):
    return graph_queries.keyword_search(body.keywords, hops=body.hops, project_id=body.project_id)


@router.get("/html")
def serve_graph_html(project_id: str = "default"):
    html_path = Path(config.GRAPH_JSON_PATH).parent / project_id / "graph.html"
    if not html_path.exists():
        # 하위 호환: default는 루트 경로도 확인
        if project_id == "default":
            fallback = Path(config.GRAPH_JSON_PATH).parent / "graph.html"
            if fallback.exists():
                return FileResponse(str(fallback), media_type="text/html")
        return HTMLResponse(f"<h2>graph.html not found for project '{project_id}'.</h2>", status_code=404)
    return FileResponse(str(html_path), media_type="text/html")
