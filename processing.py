from flashtext import KeywordProcessor
import unidecode
import re

def preprocess_text(text, flag):
    text = str(text)
    
    #remove image link and url associated with teams
    text = re.sub(r'\[\S+]', '', text, flags=re.MULTILINE)
    text = re.sub(r'https\S+teams\S+', '', text, flags=re.MULTILINE)

    # Replacing all the occurrences of \n,\\n,\t,\\ with a space.
    keyword_processor = KeywordProcessor()
    keyword_processor.add_keyword('\n', ' ')
    keyword_processor.add_keyword('\\n', ' ')
    keyword_processor.add_keyword('\t',' ')
    keyword_processor.add_keyword('\\', ' ')
    
    text = keyword_processor.replace_keywords(text)
    
    #Remove whitespaces
    text = " ".join(text.split())

    # Remove accented characters from text using unidecode.
    # Unidecode() - It takes unicode data & tries to represent it to ASCII characters. 
    if(flag):
        text = unidecode.unidecode(text)

    #Remove some of the punctuation
    text = re.sub(r'^\"', '', text)
    text = re.sub(r'\,$', '', text)
    text = re.sub(r'\"$', '', text)
    if(flag):
        text = re.sub(r'[^\w\s]', '', text)

    #lower case
    if(flag):
        text = text.lower()
    
    return text