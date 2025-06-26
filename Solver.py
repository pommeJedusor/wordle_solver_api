from enum import Enum
import json, random


def get_possible_words():
    with open("possible_words.json", "r", encoding="utf8") as f:
        possible_words: list[str] = json.loads(f.read())
    return possible_words


def get_usable_words():
    with open("usable_words.json", "r", encoding="utf8") as f:
        usable_words: list[str] = json.loads(f.read())
    return usable_words


class Color(Enum):
    GREEN = 1
    YELLOW = 2
    BLACK = 3


type letter_number = dict[str, tuple[int, bool]]


def get_well_placed_letters(solution: str, attempt: str) -> list[str | bool]:
    return [a if a == b else False for a, b in zip(solution, attempt)]


def get_colors_from_attempt(solution: str, attempt: str) -> list[Color]:
    well_placed_letters = get_well_placed_letters(solution, attempt)

    letter_number = {}
    for letter in attempt:
        nb_letter_occurences_in_attempt = len([l for l in attempt if l == letter])
        nb_letter_occurences_in_solution = len([l for l in solution if l == letter])
        if nb_letter_occurences_in_attempt <= nb_letter_occurences_in_solution:
            letter_number[letter] = nb_letter_occurences_in_attempt
        else:
            letter_number[letter] = nb_letter_occurences_in_solution

    for letter in [l for l in well_placed_letters if l]:
        letter_number[letter] -= 1

    colors = []
    for l, well_placed_letter in zip(attempt, well_placed_letters):
        if well_placed_letter:
            colors.append(Color.GREEN)
        elif letter_number[l]:
            letter_number[l] -= 1
            colors.append(Color.YELLOW)
        else:
            colors.append(Color.BLACK)
    return colors


def get_well_placed_letters_wrong_place_letters_and_letter_number_from_colors(
    attempt: str, colors: list[Color]
) -> tuple[list[str | bool], list[str | bool], letter_number]:
    well_placed_letters: list[str | bool] = [
        l if color == Color.GREEN else False for l, color in zip(attempt, colors)
    ]
    wrong_placed_letters: list[str | bool] = [
        l if color == Color.YELLOW else False for l, color in zip(attempt, colors)
    ]

    letter_number = get_empty_letter_number()
    for l, color in zip(attempt, colors):
        if color == Color.BLACK:
            letter_number[l] = (letter_number[l][0], True)
        else:
            letter_number[l] = (letter_number[l][0] + 1, letter_number[l][1])

    return (well_placed_letters, wrong_placed_letters, letter_number)


def get_empty_letter_number() -> letter_number:
    letter_number = {}
    for i in range(26):
        letter_number[chr(i + 97)] = (0, False)
    return letter_number


def is_word_valid(
    word: str,
    well_placed_letters: list[str | bool],
    wrong_placed_letters: list[str | bool],
    letter_number: letter_number,
) -> bool:
    letter_number_word: dict[str, int] = {}
    for i in range(26):
        letter_number_word[chr(97 + i)] = 0

    for i, letter in enumerate(word):
        if well_placed_letters[i] and well_placed_letters[i] != letter:
            return False
        if wrong_placed_letters[i] and wrong_placed_letters[i] == letter:
            return False

        if letter in letter_number_word:
            letter_number_word[letter] += 1
    for l, (number, is_max) in letter_number.items():
        if number > letter_number_word[l] or is_max and letter_number_word[l] != number:
            return False

    return True


def main():
    possible_words = get_possible_words()
    word_to_find = "reset" or random.choice(possible_words)
    first_word = "salet"
    colors = get_colors_from_attempt(word_to_find, first_word)
    print(word_to_find)
    print(first_word)
    print(colors)
    print(len(possible_words))
    well_placed_letters, wrong_placed_letters, letter_number = (
        get_well_placed_letters_wrong_place_letters_and_letter_number_from_colors(
            first_word, colors
        )
    )
    filtered_words = [
        word
        for word in possible_words
        if is_word_valid(word, well_placed_letters, wrong_placed_letters, letter_number)
    ]
    print(len(filtered_words))
    for word in filtered_words:
        print(word)


if __name__ == "__main__":
    main()
