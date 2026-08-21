import os
import logging
from dotenv import load_dotenv
from groq import Groq
import re

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
primary_model = os.getenv("MODEL")
fallback_model = os.getenv("FALLBACK_MODEL")

client = Groq(api_key=api_key)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def call_llm(prompt: str, context: str = "") -> str:
    full_prompt = f"{prompt}\n\n{context}".strip()

    for model in [primary_model, fallback_model]:
        try:
            logger.info(f"Calling LLM - model: {model}")
            response = client.chat.completions.create(
                model = model,
                messages = [
                    {
                        "role": "system",
                        "content": "You are an expert Java software engineer "
                                "specializing in legacy code modernization "
                                "and refactoring. Be precise and technical."
                    },
                    {
                        "role": "user",
                        "content": full_prompt
                    }
                ],
                temperature=0.2,
                max_tokens=4096
            )

            result = response.choices[0].message.content
            result = re.sub(r'<think>.*?</think>\n*', '', result, flags=re.DOTALL)
            result = result.strip()
            logger.info(f"LLM call successful - model: {model},"f"character retruned: {len(result)}")

            return result

        except Exception as e:
            logger.warning(f"LLM Call failed - model: {model}, error: {e}")

    raise RuntimeError(
        "Both Primary and fallback LLM models failed."
        "Check your Groq api key and model availability."   
    )

if __name__ == "__main__":
    response = call_llm("Say hello and confirm you are ready to help with java refactoring.")
    print(f'\n{response}\n')