from typing import List, Dict
import re
from utils.logger import get_logger
from utils.openai_client import OpenAIClient
from config import MAX_CHUNK_LENGTH

logger = get_logger(__name__)

class ContentChunker:
    def __init__(self, use_openai=False):
        self.use_openai = use_openai
        self.openai_client = OpenAIClient() if use_openai else None

    def chunk_text(self, text: str, page_title: str) -> List[Dict[str, any]]:
        logger.info(f"Chunking text from page '{page_title}'")
        sections = re.split(r'(?=\n#{1,6}\s)', text)
        chunks = []
        chunk_count = 0
        
        for section in sections:
            lines = section.split('\n')
            header = lines[0].strip()
            content = '\n'.join(lines[1:]).strip()
            
            if len(content) > MAX_CHUNK_LENGTH:
                sub_chunks = self._split_large_chunk(content)
                for sub_chunk in sub_chunks:
                    chunks.append({
                        "id": f"chunk_{chunk_count:04d}",
                        "header": self._generate_header(sub_chunk),
                        "content": sub_chunk,
                        "page": page_title
                    })
                    chunk_count += 1
            else:
                chunks.append({
                    "id": f"chunk_{chunk_count:04d}",
                    "header": self._extract_header(header),
                    "content": content,
                    "page": page_title
                })
                chunk_count += 1
        
        logger.info(f"Created {len(chunks)} chunks for page '{page_title}'")
        return chunks

    def process_chunks(self, chunks: List[Dict[str, any]]) -> List[Dict[str, any]]:
        if self.use_openai:
            logger.info("Processing chunks with OpenAI")
            return [self._process_chunk_with_openai(chunk) for chunk in chunks]
        else:
            logger.info("Processing chunks with default formatting")
            return chunks

    def _split_large_chunk(self, content: str) -> List[str]:
        sub_chunks = []
        while content:
            split_index = self._find_split_index(content, MAX_CHUNK_LENGTH)
            sub_chunks.append(content[:split_index].strip())
            content = content[split_index:].strip()
        return sub_chunks

    def _find_split_index(self, text: str, max_length: int) -> int:
        if len(text) <= max_length:
            return len(text)
        split_index = text.rfind('\n', 0, max_length)
        if split_index == -1:
            split_index = text.rfind('. ', 0, max_length)
            if split_index == -1:
                split_index = max_length
            else:
                split_index += 2  # Include the period and space
        return split_index

    def _extract_header(self, header: str) -> str:
        return header.lstrip('#').strip()

    def _generate_header(self, content: str) -> str:
        first_sentence = content.split('.')[0].strip()
        if len(first_sentence) > 50:
            words = first_sentence.split()
            return ' '.join(words[:5]) + '...'
        return first_sentence

    def _process_chunk_with_openai(self, chunk: Dict[str, any]) -> Dict[str, any]:
        return self.openai_client.improve_text(chunk)