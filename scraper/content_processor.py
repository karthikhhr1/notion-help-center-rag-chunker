from utils.text_cleaner import TextCleaner
from scraper.content_chunker import ContentChunker
from utils.logger import get_logger

logger = get_logger(__name__)

class ContentProcessor:
    def __init__(self, use_openai=False):
        self.cleaner = TextCleaner()
        self.chunker = ContentChunker(use_openai)

    def process(self, content, page_title):
        logger.info(f"Processing content for page: {page_title}")
        cleaned_content = self.cleaner.clean(content)
        chunks = self.chunker.chunk_text(cleaned_content, page_title)
        processed_chunks = self.chunker.process_chunks(chunks)
        final_chunks = [self._clean_chunk_content(chunk) for chunk in processed_chunks]
        logger.info(f"Processed {len(final_chunks)} chunks for page: {page_title}")
        return final_chunks

    def _clean_chunk_content(self, chunk):
        content = chunk['content']
        if content.startswith("CONTENT:") or content.startswith("Content:"):
            content = content.split("\n", 1)[1] if "\n" in content else content[8:].strip()
        chunk['content'] = content.strip()
        return chunk