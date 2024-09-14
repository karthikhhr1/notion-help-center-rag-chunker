# Scraper settings
BASE_URL = 'https://www.notion.so'
HELP_CENTER_URL = 'https://www.notion.so/help'
MAX_WORKERS = 20
MAX_ARTICLES = None # Set to None to scrape all articles
CHUNK_WRITE_INTERVAL = 1000  # Number of chunks to process before writing to file

# Chunker settings
MAX_CHUNK_LENGTH = 750

# File paths
OUTPUT_FILE = 'data/formatted_chunks.json'

# Logging
LOG_LEVEL = 'INFO'

# Selenium settings
SELENIUM_TIMEOUT = 10
SELENIUM_IMPLICIT_WAIT = 1

# OpenAI settings
USE_OPENAI_PRETTIFICATION = True  # Set to False to use default formatting
OPENAI_RATE_LIMIT_DELAY = 60  # Delay in seconds when rate limit is hit