import os
from dotenv import load_dotenv

load_dotenv()

GRAPH_JSON_PATH = os.getenv("GRAPH_JSON_PATH", "graphify-out/graph.json")
SOURCE_DIR      = os.getenv("SOURCE_DIR", "source")
API_PORT        = int(os.getenv("API_PORT", "8005"))
MCP_PORT        = int(os.getenv("MCP_PORT", "8006"))
API_KEY         = os.getenv("API_KEY", "")
