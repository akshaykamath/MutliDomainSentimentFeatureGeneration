from __future__ import division
import xml.etree.ElementTree as ET
import csv
import sys
from SentWordNetDataCleaner import SentWordNetDataCleaner
from RuleBasedClassifier import RuleBasedSentimentClassifier

reload(sys)
sys.setdefaultencoding("utf-8")


def get_helpful_score(text):
    try:
        mod_text = text.replace('of', '|')
        numbers = mod_text.split('|')
        helpful_score = float(numbers[0].replace("\n", "").replace("\t", "").replace(" ", "")) / float(
            numbers[1].replace("\n", "").replace("\t", "").replace(" ", ""))
        helpful_score *= 100

        return int(helpful_score)
    except:
        return 0


def get_word_net_score(sentence, sentiment_dict):
    rule_based_classifier = RuleBasedSentimentClassifier(sentiment_dict, "T")
    score = rule_based_classifier.get_text_score(sentence)

    return score


# Assume white space to be a delimiter between words
def get_review_length(text):
    words = text.split(' ')
    return len(words)


def write_reviews_to_csv_file(reviews, sentiment):


    count = 0
    # Write all the positive reviews into the csv file.
    while count < 500:
        try:
            review = reviews[count + 1]
            product_name = review[2].text.strip()
            review_text = review[10].text.strip()
            review_summary = review[6].text.strip()
            helpful_score = get_helpful_score(review[4].text)
            review_rating = int(float(review[5].text.replace("\n", "").replace("\t", "").replace(" ", "")))
            word_net_score_review = get_word_net_score(review_text, sentiment_dict)
            word_net_score_summary = get_word_net_score(review_summary, sentiment_dict)
            review_length = get_review_length(review_text)
            sentiment = sentiment

            writer.writerow({'product_name': product_name,
                             'review_text': review_text,
                             'review_summary': review_summary,
                             'helpful_score': helpful_score,
                             'review_rating': review_rating,
                             'word_net_score_review': word_net_score_review,
                             'word_net_score_summary': word_net_score_summary,
                             'review_length': review_length,
                             'sentiment': sentiment})

        except:
            print("Unexpected error:", sys.exc_info()[0])
            continue

        count += 1




if __name__ == "__main__":
    positive_file = 'Dataset/positive-review.xml'
    negative_file = 'Dataset/negative-review.xml'

    cleaned_data_set_file = 'Dataset/cleaned-dataset-file.csv'
    csv_file = open(cleaned_data_set_file, 'wb')
    csv_field_names = ['product_name', 'review_text', 'review_summary', 'helpful_score', 'review_rating', 'word_net_score_review', 'word_net_score_summary', 'review_length', 'sentiment']
    writer = csv.DictWriter(csv_file, fieldnames=csv_field_names)

    writer.writerow({'product_name': "Name",
                             'review_text': "review_text",
                             'review_summary': "review_summary",
                             'helpful_score': "helpful_score",
                             'review_rating': "review_rating",
                             'word_net_score_review': "word_net_score_review",
                             'word_net_score_summary': "word_net_score_summary",
                             'review_length': "review_length",
                             'sentiment': "sentiment"})

    # Prepare senti word net dictionary
    sent_word_cleaner = SentWordNetDataCleaner()
    sentiment_dict = sent_word_cleaner.get_sent_word_dict()

    with open(positive_file, 'r') as pos_file:
        positive_xml_string = pos_file.read()

    pos_file.close()

    with open(negative_file, 'r') as neg_file:
        negative_xml_string = neg_file.read()

    neg_file.close()

    pos_parser = ET.XMLParser(encoding="UTF-8")
    neg_parser = ET.XMLParser(encoding="UTF-8")

    positive_root = ET.fromstring(positive_xml_string, parser=pos_parser)
    negative_root = ET.fromstring(negative_xml_string, parser=neg_parser)

    positive_reviews = positive_root.findall('review')
    negative_reviews = negative_root.findall('review')

    write_reviews_to_csv_file(positive_reviews, "POSITIVE")
    write_reviews_to_csv_file(negative_reviews, "NEGATIVE")

    csv_file.close()

