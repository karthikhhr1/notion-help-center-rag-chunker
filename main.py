import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from scraper.article_scraper import ArticleScraper
from scraper.content_processor import ContentProcessor
from utils.logger import get_logger
from config import USE_OPENAI_PRETTIFICATION, OUTPUT_FILE, MAX_ARTICLES, MAX_WORKERS, CHUNK_WRITE_INTERVAL

logger = get_logger(__name__)

def process_article(scraper, processor, link):
    content, page_title = scraper.scrape_article(link)
    if content:
        processed_chunks = processor.process(content, page_title)
        logger.info(f"Processed {len(processed_chunks)} chunks for {link}")
        return processed_chunks
    else:
        logger.warning(f"No content found for {link}")
        return []

def write_chunks_to_file(chunks, file, is_first_write):
    for i, chunk in enumerate(chunks):
        if not is_first_write or i > 0:
            file.write(',\n')
        json.dump(chunk, file, ensure_ascii=False, indent=2)
    file.flush()  # Ensure data is written to disk

def main():
    logger.info("Starting Notion Help Center scraping process")
    scraper = ArticleScraper()
    processor = ContentProcessor(use_openai=USE_OPENAI_PRETTIFICATION)

    article_links = scraper.get_article_links()
    if MAX_ARTICLES:
        article_links = article_links[:MAX_ARTICLES]

    chunk_count = 0
    is_first_write = True

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('[\n')  # Start of the JSON array
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_link = {executor.submit(process_article, scraper, processor, link): link for link in article_links}
            
            buffer = []
            for future in as_completed(future_to_link):
                link = future_to_link[future]
                try:
                    chunks = future.result()
                    buffer.extend(chunks)
                    chunk_count += len(chunks)

                    if len(buffer) >= CHUNK_WRITE_INTERVAL:
                        write_chunks_to_file(buffer, f, is_first_write)
                        is_first_write = False
                        buffer = []

                except Exception as exc:
                    logger.error(f"{link} generated an exception: {exc}")

            # Write any remaining chunks
            if buffer:
                write_chunks_to_file(buffer, f, is_first_write)
        
        f.write('\n]')  # End of the JSON array

    logger.info(f"Scraping and processing completed. Total chunks: {chunk_count}")
    logger.info(f"Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
    