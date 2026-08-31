import os
import json
import subprocess
import logging

logger = logging.getLogger(__name__)

def build_graph(dir_path: str) -> dict:
    if not os.path.exists(dir_path):
        raise FileNotFoundError(f"Directory not found: {dir_path}")

    commands = ['java', '-cp', 'engine/ingestion/ASTExtractor.jar', 'com.refactormind.GraphBuilder', dir_path]

    anlaysis_engine = subprocess.run(commands, capture_output=True, text = True)
    if(anlaysis_engine.returncode != 0):
        logger.error(f"Building AST Graph Extaction failed for {anlaysis_engine.stderr}")
        raise RuntimeError(f"AST Extaction Graph Building Failed for {dir_path}")

    try:
        json_output = json.loads(anlaysis_engine.stdout)
        logger.info(f"Successfully built graph for {dir_path} — "
            f"{len(json_output.get('nodes', []))} nodes, "
            f"{len(json_output.get('edges', []))} edges")
        return json_output
    except json.JSONDecodeError as e:
        logger.error(f"ASTExtractor produced non-JSON output: {anlaysis_engine.stdout[:500]}")
        raise RuntimeError(f"AST Graph Building Failed for {dir_path}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format ="%(asctime)s - %(levelname)s - %(message)s")
    graph = build_graph('tests')
    print(json.dumps(graph, indent=2))