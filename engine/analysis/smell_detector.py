import json
import logging
from engine.llm.caller import call_llm
from engine.ingestion.parser import parse_java_file

logger = logging.getLogger(__name__)

def analyze_semantic_smells(ast_dict: dict) -> dict:
    """
    Takes AST dictionary and transform it to string and the pass the string to LLM to identify semantic code smells like GOD class, tight Coupling, dependencies, etc.
    """

    ast_context = json.dumps(ast_dict, indent=2)

    prompt = f"""
        You are a strict java program analyzer, not a motivational coach. You single goal is to strictly analyze the Java class, field and method for each of the classes found in the ast. 

        Identify the followings smells in code :-
            - GOD class
            - Tight Coupling
            - HardCoded magic strings and logic
            - Outdated API usage
            - Large classes/methods that can be broken decomposed
            - Direct DB call 
            - Improper exception handling
        
        For each of the identified smells, provide a short description of the smell, the class in which it is found and the method in which it is found.

        ASK to analyze: {ast_context}
        
        Critical Instruction: 
        1. You must return only a raw answer in JSON array of objects.
        2. Do NOT wrap the response in markdown blocks (e.g. do no use ```).
        3. Do NOT include any converstaional text, greetings or explainations outside json.

        Expected JSON Schema:
        [
            {{
                "className":  "Name of the class",
                "methodName": "Name of the method (or null if it's a class-level smell)",
                "smellType": "Type of the smell identified",
                "description": "Short description of the smell, why it is a smell and what rules are violated",
            }}
        ]
    """

    logger.info("Sending the stringified AST to LLM")

    raw_result = call_llm(prompt)

    try: 
        parsed_json = json.loads(raw_result)
        logger.info(f"Successfully detected {len(parsed_json)} code smells")
        return parsed_json

    except json.JSONDecodeError as e:
        logger.err("Failed to Parse LLM ouput. The LLM hallucinated converstation text. Error: {e}")
        logger.err(f"Raw result: {raw_result}")
        raise RuntimeError("LLM didn't returned the valid json")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    logger.info("\n---- Starting Pipeline ----\n")

    logger.info("Step1: Ingestion Running....")
    ast_dict = parse_java_file("tests/sample_java/OrderProcessor.java")

    logger.info("Step2: Semantic Analysis Running....")
    analysis = analyze_semantic_smells(ast_dict)

    print("\n------ LLM Analysis Result -------\n")
    print(analysis)
    print("\n--------- Analysis End -----------\n")