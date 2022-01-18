import json
import os
from collections import Counter
from unicodedata import normalize

import arabic_reshaper
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
from hazm import Normalizer, word_tokenize
from wordcloud import WordCloud
from src.data import DATA_DIR
from loguru import logger

class ChatStatistics:
    def __init__(self, chat_json):

        #load chat data
        logger.info(f"Generating chat data from {chat_json}")
        with open(chat_json) as f:
            self.chat_data=json.load(f)

        #load stopwords
        logger.info(f"Loading stop words from {DATA_DIR/ 'stopwords.tx'}")
        self.normalizer=Normalizer()
        stop_words=open(str(DATA_DIR/ 'stopwords.txt')).readlines()
        stop_words=list(map(str.strip, stop_words))
        self.stop_words=list(map(self.normalizer.normalize, stop_words))



    def generate_word_cloud(self, output_dir):
        """ Generating word cloud from a chat data json file"""
        logger.info("Loading text content... ")
        text_content = " "

        for msg in self.chat_data['messages']:
            if type(msg['text']) is str:
                tokens = word_tokenize(msg['text'])
                tokens = filter(lambda item: item not in self.stop_words, tokens)
                text_content += f' {" ".join(tokens)}'  

        logger.info("Generating word cloud...")
        #normalize, reshape for final word cloud
        text_content=self.normalizer.normalize(text_content)
        text_content = arabic_reshaper.reshape(text_content)
        #text_content = get_display(text_content)

        Counter(text_content.split(" ")).most_common()
        wordcloud = WordCloud(
            font_path=str(DATA_DIR/'BHoma.ttf'),
            width=1200, height=1200,
            max_words=120,
            background_color="white"
            ).generate(text_content)

        logger.info(f"Saving word cloud fo {output_dir}")
        wordcloud.to_file(output_dir/ "persian_ex.png")


if __name__ == '__main__':
    chat_stats = ChatStatistics(chat_json=str(DATA_DIR/ 'result.json'))
    chat_stats.generate_word_cloud(output_dir= DATA_DIR)


    print("Done!")

