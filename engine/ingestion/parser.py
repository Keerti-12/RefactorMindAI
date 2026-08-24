import os
import json
import subprocess
import logging

logger = logging.getLogger(__name__)

def parse_java_file(file_path: str) -> dict:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    commands = ['java', '-jar', 'engine/ingestion/ASTExtractor.jar', file_path]

    result = subprocess.run(commands, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"AST Extraction failed for {result.stderr}")
        raise RuntimeError(f"AST Extraction failed for {file_path}")

    try:
        json_output = json.loads(result.stdout)
        logger.info(f"Successfully Parsed {file_path} (AST Size: {len(json_output)})")
    except json.JSONDecodeError as e:
        logger.error(f"JAR stdout was not valid JSON:\n{result.stdout[:500]}")
        raise RuntimeError("ASTExtractor produced non-JSON output")
    
    return json_output

if __name__ == '__main__':
    response = parse_java_file('tests/sample_java/OrderProcessor.java')
    print(response)