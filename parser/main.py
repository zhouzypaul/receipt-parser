"""
this file is meant to do optical character recognition
"""
import argparse

import easyocr
import cv2

from .text_model.word_box import Word
from .text_model.text_corpus import TextCorpus
from .language_models.gpt import gpt_parse_receipt


def optical_character_recognition(img_path):
    """
    given an image, return a concated raw string of all the text in the image
    """
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
    result = reader.readtext(img)
    raw_text = ''
    for points, text, confidence in result:
        raw_text += text + ' '
    return raw_text


def parse_receipt_with_ocr_gpt(img_path):
    """
    parse the content of the receipt by first doing OCR to extract the words
    then chatGPT is used to abstract it into mappings from food items to prices
    """
    raw_text = optical_character_recognition(img_path)
    print(raw_text)
    info_dict = gpt_parse_receipt(raw_text)
    print(info_dict)
    return info_dict


def parse_receipt_with_ocr_constraints(img_path):
    """
    parse the content of the receipt by first doing OCR to extract the words
    then we parse the result with hard rules
    and determine food with their prices according to how receipts are usually
    structrued and the bounding box location of the detected words
    """
    # read image
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)

    # OCR
    reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
    result = reader.readtext(img)
    words_list = []
    for points, text, conf in result:
        box = Word(*points, text, conf)
        words_list.append(box)

    # create the text corpus
    text_corpus = TextCorpus(words_list, y_delta=60)
    text_corpus.filter_by_confidence()
    lines = text_corpus.get_lines()
    text_corpus.print_lines(lines)
    info = text_corpus.get_info_dict(lines)
    print(info)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_path', '-p', type=str, default='./ItemizedReceipt.jpg')
    parser.add_argument('--parse_mode', type=str, default='gpt', choices=['gpt', 'constraints'])
    args = parser.parse_args()

    if args.parse_mode == 'constraints':
        parse_receipt_with_ocr_constraints(args.img_path)
    elif args.parse_mode == 'gpt':
        parse_receipt_with_ocr_gpt(args.img_path)
