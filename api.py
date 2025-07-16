import re
from flask import Flask, request
from flask_cors import CORS, cross_origin
import requests

from second_word import second_word

from Solver import (
    get_next_guess,
    get_possible_words,
    get_usable_words,
    get_colors_interface,
)


app = Flask(__name__)

usable_words = get_usable_words()
first_word = "salet"

cors = CORS(app)


def is_request_valid(words: list[list[str]]) -> bool:
    for row in words:
        if len(row) != 2:
            return False
        if not re.search("^[a-z]{5}$", row[0]):
            return False
        if not re.search("^(G|Y|B){5}$", row[1]):
            return False

    return True


@app.route("/get_todays_word/<string:date>", methods=["GET"])
@cross_origin()
def get_todays_word(date: str):
    is_date_valid = len(date) == 10 and re.search("^\d{4}-\d{2}-\d{2}$", date)
    if not is_date_valid:
        return "pomme"

    r = requests.get(f"https://www.nytimes.com/svc/wordle/v2/{date}.json")
    return r.json()["solution"]


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
            if get_colors_interface(possible_word, word) == colors
        ]
        print(len(possible_words))

    if (
        not possible_words
        or len(possible_words) == 1
        and words[-1][0] == possible_words[0]
    ):
        return ""
    is_final_word, word = get_next_guess(possible_words, usable_words)
    if is_final_word:
        return word + "Y"
    return word


@app.after_request
def add_header(response):
    response.cache_control.max_age = 3600
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
