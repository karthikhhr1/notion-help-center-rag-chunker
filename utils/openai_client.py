import os
import time
from openai import OpenAI
from typing import Dict
from utils.logger import get_logger
from config import OPENAI_RATE_LIMIT_DELAY

logger = get_logger(__name__)

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def improve_text(self, chunk: Dict[str, str]) -> Dict[str, str]:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                prompt = self._create_prettify_prompt(chunk)
                response = self._get_openai_response(prompt)
                improved_text = response.choices[0].message.content.strip()
                improved_header, improved_content = self._parse_improved_text(improved_text)
                return {
                    "id": chunk["id"],
                    "header": improved_header,
                    "content": improved_content,
                    "page": chunk["page"]
                }
            except Exception as e:
                logger.warning(f"Error in OpenAI API call (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(OPENAI_RATE_LIMIT_DELAY)
                else:
                    logger.error("Max retries reached. Returning original chunk.")
                    return chunk

    def _create_prettify_prompt(self, chunk: Dict[str, str]) -> str:
        return f"""
        Improve the formatting and clarity of the following text while preserving its meaning:

        Header: {chunk['header']}

        Content:
        {chunk['content']}

        Please return the improved text in the following format:
        HEADER: [Improved header]

        [Improved content]
        """

    def _get_openai_response(self, prompt: str):
        return self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that improves the formatting and clarity of text."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            n=1,
            temperature=0.3,
        )

    def _parse_improved_text(self, improved_text: str) -> tuple:
        improved_lines = improved_text.split('\n')
        improved_header = improved_lines[0].replace('HEADER: ', '').strip()
        improved_content = '\n'.join(improved_lines[1:]).strip()
        return improved_header, improved_content