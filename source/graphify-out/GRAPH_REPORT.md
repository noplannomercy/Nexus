# Graph Report - source  (2026-05-11)

## Corpus Check
- 5 files · ~2,726 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 66 nodes · 72 edges · 9 communities (2 shown, 7 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]

## God Nodes (most connected - your core abstractions)
1. `InMemoryJobStore` - 14 edges
2. `PostgresJobStore` - 13 edges
3. `HCS Code2Rule PoC2 — 추진 방향 요약` - 6 edges
4. `ForgeClient` - 5 edges
5. `NexusClient` - 5 edges
6. `CitadelClient` - 4 edges
7. `LightRAGClient` - 4 edges
8. `_maybe_close_job()` - 4 edges
9. `advance_pipeline()` - 3 edges
10. `dispatch_code_file()` - 3 edges

## Surprising Connections (you probably didn't know these)
- `create_app()` --calls--> `InMemoryJobStore`  [INFERRED]
  app.py → job_store.py

## Communities (9 total, 7 thin omitted)

### Community 2 - "Community 2"
Cohesion: 0.31
Nodes (5): advance_pipeline(), dispatch_code_file(), dispatch_text_doc(), LightRAGClient, _maybe_close_job()

### Community 3 - "Community 3"
Cohesion: 0.25
Nodes (7): 1. 과제 현황, 2. 제안하는 방향, 3. HCA Code2Rule과의 관계, 4. 확정이 필요한 사항 (HCS 측 결정), 5. 다음 단계, code:block1 (┌─────────────────────────────────┐), HCS Code2Rule PoC2 — 추진 방향 요약

## Knowledge Gaps
- **5 isolated node(s):** `1. 과제 현황`, `code:block1 (┌─────────────────────────────────┐)`, `3. HCA Code2Rule과의 관계`, `4. 확정이 필요한 사항 (HCS 측 결정)`, `5. 다음 단계`
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `InMemoryJobStore` connect `Community 0` to `Community 8`?**
  _High betweenness centrality (0.149) - this node is a cross-community bridge._
- **Why does `PostgresJobStore` connect `Community 1` to `Community 0`?**
  _High betweenness centrality (0.135) - this node is a cross-community bridge._
- **Why does `ForgeClient` connect `Community 4` to `Community 2`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **What connects `1. 과제 현황`, `code:block1 (┌─────────────────────────────────┐)`, `3. HCA Code2Rule과의 관계` to the rest of the system?**
  _5 weakly-connected nodes found - possible documentation gaps or missing edges._