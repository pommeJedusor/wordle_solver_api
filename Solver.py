import json, time


def get_possible_words() -> list[str]:
    with open("possible_words.json", "r", encoding="utf8") as f:
        possible_words: list[str] = json.loads(f.read())
    return possible_words


def get_usable_words() -> list[str]:
    with open("usable_words.json", "r", encoding="utf8") as f:
        usable_words: list[str] = json.loads(f.read())
    return usable_words


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


def evaluate_word(possible_words: list[str], word: str) -> float:
    sequences: dict[str, int] = {}
    for w in possible_words:
        colors = get_colors_from_attempt(w, word)
        sequences[colors] = (sequences.get(colors) or 0) + 1

    scores = []
    for colors, number in sequences.items():
        scores.append((len(possible_words) - number) * (number / len(possible_words)))

    return sum(scores)


def get_best_word(
    possible_words: list[str], usable_words: list[str]
) -> tuple[bool, str]:
    if len(possible_words) == 1:
        return True, possible_words[0]
    elif len(possible_words) == 2:
        return False, possible_words[0]

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
    return False, best_words[0][0]


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
        _, attempt = get_best_word(possible_words, get_usable_words())
    print("word found")


def main():
    start = time.time()
    _, attempt = get_best_word(get_possible_words(), get_usable_words())
    print(time.time() - start)
    print(attempt)


if __name__ == "__main__":
    main()
