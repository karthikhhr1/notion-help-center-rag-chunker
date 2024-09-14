import re
from utils.logger import get_logger

logger = get_logger(__name__)

class TextCleaner:
    def clean(self, text):
        logger.info("Cleaning text content")
        unwanted_sections = [
            'IN THIS ARTICLE',
            'CONTENTS',
            'Jump to FAQs',
            'FAQs',
            'Play',
            'Still have more questions? Message support',
        ]
        for section in unwanted_sections:
            text = text.replace(section, '')
        
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        def preserve_list(match):
            list_items = match.group(1).split('\n')
            return '\n'.join([f"• {item.strip()}" for item in list_items if item.strip()])
        
        text = re.sub(r'(?<=\n)([•-] .*(?:\n[•-] .*)*)', preserve_list, text, flags=re.MULTILINE)
        
        lines = text.split('\n')
        filtered_lines = [line for line in lines if not re.match(r'^\d+[:\d]*\s*(min video)?$', line.strip())]
        
        cleaned_text = '\n'.join(filtered_lines).strip()
        logger.info("Text cleaning completed")
        return cleaned_text