from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from config import BASE_URL, HELP_CENTER_URL, SELENIUM_TIMEOUT, SELENIUM_IMPLICIT_WAIT
from utils.logger import get_logger

logger = get_logger(__name__)

class ArticleScraper:
    def __init__(self):
        self.driver = self._get_driver()

    def _get_driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(SELENIUM_IMPLICIT_WAIT)
        return driver

    def get_article_links(self):
        logger.info("Fetching article links")
        self.driver.get(HELP_CENTER_URL)
        time.sleep(SELENIUM_IMPLICIT_WAIT)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SELENIUM_IMPLICIT_WAIT)

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        article_links = soup.select('a.toggleList_link__safdF')

        links = [urljoin(BASE_URL, a.get('href')) for a in article_links if a.get('href')]
        links = [link for link in links if '/help/notion-academy/course/' not in link]

        logger.info(f"Found {len(links)} article links")
        return list(set(links))

    def scrape_article(self, url):
        logger.info(f"Scraping article: {url}")
        self.driver.get(url)
        time.sleep(SELENIUM_IMPLICIT_WAIT)

        try:
            accept_button = WebDriverWait(self.driver, SELENIUM_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="Accept"]'))
            )
            accept_button.click()
        except Exception:
            pass

        try:
            content_div = WebDriverWait(self.driver, SELENIUM_TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'article'))
            )
            article_text = content_div.text.strip()
            page_title = self.driver.title.strip()
            return article_text, page_title
        except Exception as e:
            logger.warning(f"Could not find content element for {url}: {e}")
            return '', ''

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()