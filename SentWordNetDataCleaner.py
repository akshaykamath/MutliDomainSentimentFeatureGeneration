__author__ = 'Akshay'

import codecs
import re


class SentWordNetDataCleaner:

    __sent_word_net_file__ = "WordNetData\SentiWordNet_3.0.0_20130122.txt"

    def __init__(self):
        pass

    def get_sent_word_dict(self):
        sent_dict = {}

        pos_word = codecs.open("WordNetData\\positive_words.txt", "r", "UTF-8")
        neg_word = codecs.open("WordNetData\\neg_words.txt", "r", "UTF-8")

        while True:
            read_line = pos_word.readline()
            if not read_line:
                break

            lines = read_line.split()
            word = re.sub("#.*", "", lines[0]).lower()

            if word not in sent_dict:
                sent_dict[word] = float(lines[1])
            else:
                sent_dict[word] += float(lines[1])

        while True:
            read_line = neg_word.readline()
            if not read_line:
                break

            lines = read_line.split()
            word = str(re.sub("#.*", "", lines[0]))

            if word not in sent_dict:
                sent_dict[word] = float(lines[1])
            else:
                sent_dict[word] += float(lines[1])

        return sent_dict

    def prepare_sent_word_data(self):

        sent_word_file = codecs.open(self.__sent_word_net_file__, "r", "UTF-8")

        positive_file = codecs.open("Data\\positive_words.txt", "a", "utf-8")
        negative_file = codecs.open("Data\\neg_words.txt", "a", "utf-8")
        neutral_file = codecs.open("Data\\neutral_words.txt", "a", "utf-8")

        while True:
            read_line = sent_word_file.readline()
            if not read_line:
                break

            line = read_line.split('\t')

            print line[2]
            pos_score = float(line[2])
            neg_score = float(line[3])
            sentiment_score = pos_score - neg_score

            words = line[4].split(' ')
            word_split = []

            for word in words:
                lin = word+ " "+ str(sentiment_score) +"\n"
                print lin
                word_split.append(lin)

            if sentiment_score > 0:
                positive_file.writelines(word_split)
            elif sentiment_score < 0:
                negative_file.writelines(word_split)
            else:
                neutral_file.writelines(word_split)

        sent_word_file.close()
        negative_file.close()
        positive_file.close()

    def prepare_sentiword_negative_data(self):
        return "classified"
