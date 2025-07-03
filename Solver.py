import json, random


def get_possible_words() -> list[str]:
    with open("possible_words.json", "r", encoding="utf8") as f:
        possible_words: list[str] = json.loads(f.read())
    return possible_words


def get_usable_words() -> list[str]:
    with open("usable_words.json", "r", encoding="utf8") as f:
        usable_words: list[str] = json.loads(f.read())
    return usable_words


type letter_number = dict[str, tuple[int, bool]]


def get_well_placed_letters(solution: str, attempt: str) -> list[str | bool]:
    return [a if a == b else False for a, b in zip(solution, attempt)]


def get_colors_from_attempt(solution: str, attempt: str) -> str:
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
            colors.append("G")
        elif letter_number[l]:
            letter_number[l] -= 1
            colors.append("Y")
        else:
            colors.append("B")
    return "".join(colors)


def get_well_placed_letters_wrong_place_letters_and_letter_number_from_colors(
    attempt: str, colors: str
) -> tuple[list[str | bool], list[str | bool], letter_number]:
    well_placed_letters: list[str | bool] = [
        l if color == "G" else False for l, color in zip(attempt, colors)
    ]
    wrong_placed_letters: list[str | bool] = [
        l if color == "Y" else False for l, color in zip(attempt, colors)
    ]

    letter_number = get_empty_letter_number()
    for l, color in zip(attempt, colors):
        if color == "B":
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


def evaluate_word(possible_words: list[str], word: str) -> float:
    # possible_words = possible_words[:10]
    sequences: dict[str, int] = {}
    # print(word)
    for w in possible_words:
        colors = get_colors_from_attempt(w, word)
        sequences[colors] = (sequences.get(colors) or 0) + 1
        # print(w, colors)
    # print(sequences)

    scores = []
    for colors, number in sequences.items():
        # (number of word eliminated by color sequence) * probability of getting the sequence
        scores.append((len(possible_words) - number) * (number / len(possible_words)))
    # print(scores)
    # print(sum(scores))
    # exit()
    return sum(scores)


def get_best_word(possible_words: list[str], usable_words: list[str]) -> str:
    if len(possible_words) <= 2:
        return possible_words[0]
    best_words = [
        (word, evaluate_word(possible_words, word)) for word in usable_words[:3]
    ]
    best_words.sort(key=lambda a: a[1], reverse=True)

    for word in usable_words[3:]:
        score = evaluate_word(possible_words, word)
        best_words.append((word, score))
        best_words.sort(key=lambda a: a[1], reverse=True)
        best_words.pop()

    # print(best_words)
    return best_words[0][0]


def terminal_game():
    possible_words = get_possible_words()
    attempt = "roate"

    while True:
        print(f"the word is {attempt}")
        colors = input("enter the colors\n")
        if colors == "GGGGG":
            break

        possible_words = [
            word
            for word in possible_words
            if get_colors_from_attempt(word, attempt) == colors
        ]
        print(f"there is {len(possible_words)} possible words left")
        attempt = get_best_word(possible_words, get_usable_words())
    print("word found")


def main():
    terminal_game()


if __name__ == "__main__":
    main()
