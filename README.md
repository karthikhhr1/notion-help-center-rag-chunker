# Notion Help Center RAG Chunker

## Overview

This project is a Python-based web scraper designed to extract and process content from the Notion Help Center. It scrapes articles, processes the content, chunks it into manageable pieces, and optionally improves the text using OpenAI's GPT model. The scraped and processed content is then saved as a JSON file.

## Features

- Multi-threaded scraping for improved performance
- Content cleaning and processing
- Chunking of content with intelligent header generation
- Optional text improvement using OpenAI's GPT model
- Periodic saving of processed chunks to manage memory usage
- Configurable settings for customization

## Prerequisites

- Python 3.7+
- pip (Python package manager)
- Chrome browser (for Selenium WebDriver)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/notion-help-center-scraper.git
   cd notion-help-center-scraper
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. If you plan to use the OpenAI text improvement feature, set up your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Configuration

Edit the `config.py` file to customize the scraper's behavior:

- `MAX_ARTICLES`: Maximum number of articles to scrape (set to None for all articles)
- `MAX_WORKERS`: Number of threads for parallel processing
- `CHUNK_WRITE_INTERVAL`: Number of chunks to process before writing to file
- `MAX_CHUNK_LENGTH`: Maximum character length for each chunk
- `USE_OPENAI_PRETTIFICATION`: Set to True to use OpenAI for text improvement, False for default formatting

## Usage

Run the main script to start the scraping and processing:

```
python main.py
```

The script will:
1. Scrape articles from the Notion Help Center
2. Clean and process the scraped content
3. Chunk the content into smaller pieces
4. Optionally improve the text using OpenAI (if enabled)
5. Save the processed chunks to `data/formatted_chunks.json`

## Project Structure

```
notion-help-center-scraper/
├── main.py
├── config.py
├── requirements.txt
├── README.md
├── scraper/
│   ├── __init__.py
│   ├── article_scraper.py
│   └── content_processor.py
├── utils/
│   ├── __init__.py
│   ├── text_cleaner.py
│   ├── content_chunker.py
│   ├── openai_client.py
│   └── logger.py
└── data/
    └── formatted_chunks.json
```

## Customization

- To modify scraping behavior, edit `scraper/article_scraper.py`
- To adjust content processing, edit `scraper/content_processor.py`
- To change chunking logic, edit `utils/content_chunker.py`
- To modify text cleaning rules, edit `utils/text_cleaner.py`
- To change OpenAI integration, edit `utils/openai_client.py`

## Output

The scraped and processed content is saved as a JSON file (`data/formatted_chunks.json`) with the following structure:

```json
[
  {
    "id": "chunk_0001",
    "header": "Example Header",
    "content": "Example content...",
    "page": "Original Page Title"
  },
  ...
]
```

## Troubleshooting

- If you encounter issues with Selenium, ensure you have the latest version of Chrome installed and that your ChromeDriver is compatible.
- If you're using OpenAI text improvement and encounter rate limit errors, try increasing the `OPENAI_RATE_LIMIT_DELAY` in `config.py`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This scraper is for educational purposes only. Ensure you comply with Notion's terms of service and robots.txt when using this tool.
