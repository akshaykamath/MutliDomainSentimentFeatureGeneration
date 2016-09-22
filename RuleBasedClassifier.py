__author__ = 'akshay'

import sys
from BinarySentimentClassifier import BinarySentiment
from nltk.tokenize import WhitespaceTokenizer
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import nltk

reload(sys)


class RuleBasedSentimentClassifier:
    sentences = []
    sentiment_dict = {}
    tokenizer = TweetTokenizer()

    def __init__(self, sentiment_dict, tokenize_method):
        self.sentiment_dict = sentiment_dict
        tokenizer = self.get_tokenize_strategy(tokenize_method)
        # self.sentences = sentences

    def perform_classification(self):
        for sentence in self.sentences:
            sentiment = self.classify_sentence(sentence)
            sentence_sentiment = sentence + " " + sentiment
            print sentence_sentiment

    def classify_sentence(self, sentence):

        sentiment_score = self.get_text_score(sentence)

        if sentiment_score >= 0:
            return BinarySentiment.Positive
        else:
            return BinarySentiment.Negative

        return BinarySentiment.Positive

    def get_text_score(self, sentence):
        sentence = sentence.lower()
        tokens = self.tokenizer.tokenize(sentence)

        #filtered_tokens = [token for token in tokens if token not in set(stopwords.words('english'))]
        #tagged_words = nltk.pos_tag(filtered_tokens)

        #filtered_words = [word[0] for word in tagged_words if word[1] == "JJ" or word[1] == "RB"]

        sentiment_score = 0
        for token in tokens:

            if self.sentiment_dict.has_key(token):
                sentiment_score += self.sentiment_dict[token]

        return sentiment_score

    def get_tokenize_strategy(self, method):

        if method == "T":
            return TweetTokenizer()

        return WhitespaceTokenizer()
