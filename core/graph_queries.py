import json
import networkx as nx
from pathlib import Path

_graphs: dict[str, nx.DiGraph] = {}
_DEFAULT = "default"


def init(graph_json_path: str, project_id: str = _DEFAULT) -> None:
    data = json.loads(Path(graph_json_path).read_text(encoding="utf-8"))
    G = nx.DiGraph()
    for node in data.get("nodes", []):
        G.add_node(node["id"], **node)
    for link in data.get("links", []):
        G.add_edge(link["source"], link["target"], **link)
    _graphs[project_id] = G


def _get_graph(project_id: str = _DEFAULT) -> nx.DiGraph:
    g = _graphs.get(project_id) or _graphs.get(_DEFAULT)
    if g is None:
        raise RuntimeError("Graph not initialized")
    return g


def _resolve_id(node_id: str, project_id: str = _DEFAULT) -> str | None:
    G = _get_graph(project_id)
    if node_id in G:
        return node_id
    normalized = node_id.lower().replace("_", "").replace(" ", "").replace("-", "")
    for n, data in G.nodes(data=True):
        if n.lower().replace("_", "").replace(" ", "").replace("-", "") == normalized:
            return n
        norm = data.get("norm_label", "").replace("_", "").replace(" ", "")
        if norm == normalized:
            return n
    return None


def get_node(node_id: str, project_id: str = _DEFAULT) -> dict | None:
    resolved = _resolve_id(node_id, project_id)
    if resolved is None:
        return None
    return dict(_get_graph(project_id).nodes[resolved])


def get_neighbors(node_id: str, depth: int = 1, project_id: str = _DEFAULT) -> list[dict]:
    G = _get_graph(project_id)
    resolved = _resolve_id(node_id, project_id)
    if resolved is None:
        return []
    results = []
    seen = {resolved}
    frontier = [resolved]
    for _ in range(depth):
        next_frontier = []
        for n in frontier:
            for neighbor in set(list(G.successors(n)) + list(G.predecessors(n))):
                if neighbor not in seen:
                    seen.add(neighbor)
                    next_frontier.append(neighbor)
                    edge = (
                        dict(G.edges[n, neighbor])
                        if G.has_edge(n, neighbor)
                        else dict(G.edges[neighbor, n])
                    )
                    results.append({"node": dict(G.nodes[neighbor]), "edge": edge})
        frontier = next_frontier
    return results


def get_community(community_id: int, project_id: str = _DEFAULT) -> list[dict]:
    G = _get_graph(project_id)
    return [
        dict(data)
        for _, data in G.nodes(data=True)
        if data.get("community") == community_id
    ]


def god_nodes(limit: int = 10, project_id: str = _DEFAULT) -> list[dict]:
    G = _get_graph(project_id)
    by_degree = sorted(
        ((n, G.degree(n)) for n in G.nodes()),
        key=lambda x: x[1],
        reverse=True,
    )[:limit]
    return [dict(G.nodes[n]) for n, _ in by_degree]


def graph_stats(project_id: str = _DEFAULT) -> dict:
    G = _get_graph(project_id)
    return {"nodes": G.number_of_nodes(), "edges": G.number_of_edges()}


def shortest_path(src_id: str, dst_id: str, project_id: str = _DEFAULT) -> list[dict] | None:
    G = _get_graph(project_id)
    src = _resolve_id(src_id, project_id)
    dst = _resolve_id(dst_id, project_id)
    if src is None or dst is None:
        return None
    try:
        path = nx.shortest_path(G, src, dst)
        return [dict(G.nodes[n]) for n in path]
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None


def keyword_search(keywords: list[str], hops: int = 1, project_id: str = _DEFAULT) -> list[dict]:
    G = _get_graph(project_id)
    kw_lower = [k.lower() for k in keywords]
    seen: set[str] = set()
    results: list[dict] = []
    seeds: list[str] = []

    for node_id, data in G.nodes(data=True):
        label = data.get("label", "").lower()
        norm = data.get("norm_label", "").lower()
        if any(kw in label or kw in norm or kw in node_id.lower() for kw in kw_lower):
            if node_id not in seen:
                seen.add(node_id)
                results.append(dict(data))
                seeds.append(node_id)

    frontier = seeds[:]
    for _ in range(hops):
        next_frontier = []
        for n in frontier:
            for neighbor in set(list(G.successors(n)) + list(G.predecessors(n))):
                if neighbor not in seen:
                    seen.add(neighbor)
                    next_frontier.append(neighbor)
                    results.append(dict(G.nodes[neighbor]))
        frontier = next_frontier

    return results
