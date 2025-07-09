import re
from flask import Flask, Request, request
from flask_cors import CORS, cross_origin

from second_word import second_word

from Solver import (
    get_possible_words,
    get_usable_words,
    get_colors_from_attempt,
    get_best_word,
)


app = Flask(__name__)

usable_words = get_usable_words()
first_word = "roate"

cors = CORS(app)


def is_request_valid(words: list[list[str]]) -> bool:
    for row in words:
        if len(row) != 2:
            return False
        if not re.search("^[a-z]{5}$", row[0]):
            return False
        if not re.search("^(G|Y|B){5}$", row[1]):
            return False

    if len(words) == 0 or words[0][0] != "roate":
        return False

    if len(words) > 1 and second_word[words[0][1]] != words[1][0]:
        return False

    return True


@app.route("/get_next_attempt", methods=["GET"])
@cross_origin()
def get_next_attempt():
    words = request.args.get("words")
    if words == None:
        return "#request not valid"
    words = [row.split("|") for row in words.split("||")]

    if not is_request_valid(words):
        return "#request not valid"

    if len(words) == 1:
        return second_word.get(words[0][1]) or ""

    possible_words = get_possible_words()

    for row in words:
        word = row[0]
        colors = row[1]
        possible_words = [
            possible_word
            for possible_word in possible_words
            if get_colors_from_attempt(possible_word, word) == colors
        ]
        print(len(possible_words))

    if (
        not possible_words
        or len(possible_words) == 1
        and words[-1][0] == possible_words[0]
    ):
        return ""
    return get_best_word(possible_words, usable_words)


@app.after_request
def add_header(response):
    response.cache_control.max_age = 3600
    return response
