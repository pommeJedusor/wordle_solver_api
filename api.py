from flask import Flask, Request, request

from Solver import (
    get_possible_words,
    get_usable_words,
    get_colors_from_attempt,
    get_best_word,
)


app = Flask(__name__)

usable_words = get_usable_words()
first_word = "roate"


def is_request_valid(request: Request) -> bool:
    if not request.is_json:
        return False

    words: list[dict[str, str]] = request.get_json()

    if not type(words) is list:
        return False
    for word in words:
        if not type(word) is dict or not word.get("word") or not word.get("colors"):
            return False
    return True


@app.route("/get_next_attempt")
def get_next_attempt():
    if not is_request_valid(request):
        return "#request not valid"
    words: list[dict[str, str]] = request.get_json()
    if not words:
        return first_word

    possible_words = get_possible_words()

    for word_colors in words:
        word = word_colors["word"]
        colors = word_colors["colors"]
        possible_words = [
            possible_word
            for possible_word in possible_words
            if get_colors_from_attempt(possible_word, word) == colors
        ]

    return get_best_word(possible_words, usable_words)
