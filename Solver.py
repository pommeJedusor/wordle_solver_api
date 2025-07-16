import json, time, heapq
import cython

MAX_SIZE_POSSIBLE_WORDS = 40
NUMBER_BEST_WORDS = 100


def get_possible_words() -> list[str]:
    with open("possible_words.json", "r", encoding="utf8") as f:
        possible_words: list[str] = json.loads(f.read())
    return possible_words


def get_usable_words() -> list[str]:
    with open("usable_words.json", "r", encoding="utf8") as f:
        usable_words: list[str] = json.loads(f.read())
    return usable_words


@cython.cfunc
def get_well_placed_letters(solution: str, attempt: str) -> list[str | bool]:
    return [a if a == b else False for a, b in zip(solution, attempt)]


@cython.cfunc
def get_colors(solution: str, attempt: str) -> str:
    well_placed_letters = get_well_placed_letters(solution, attempt)

    letter_number = {}
    for letter in attempt:
        letter_number[letter] = min(
            len([l for l in attempt if l == letter]),
            len([l for l in solution if l == letter]),
        )

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


@cython.cfunc
def evaluate_word(possible_words: list[str], word: str) -> float:
    sequences: dict[str, int] = {}
    for w in possible_words:
        colors = get_colors(w, word)
        sequences[colors] = (sequences.get(colors) or 0) + 1

    scores = []
    for colors, number in sequences.items():
        scores.append((len(possible_words) - number) * (number / len(possible_words)))
    return sum(scores)


@cython.cfunc
def get_best_words(possible_words: list[str], usable_words: list[str]) -> list[str]:
    if len(possible_words) <= 2:
        return [possible_words[0]]
    possible_words = possible_words[:MAX_SIZE_POSSIBLE_WORDS]

    scores: list[tuple[float, str]] = []

    for word in usable_words:
        score = evaluate_word(possible_words, word)
        heapq.heappush(scores, (score, word))
        if len(scores) > NUMBER_BEST_WORDS:
            heapq.heappop(scores)

    return [score[1] for score in scores]


@cython.cfunc
def get_best_word(
    possible_words: list[str], usable_words: list[str]
) -> tuple[bool, str]:
    if len(possible_words) <= 2:
        return len(possible_words) == 1, possible_words[0]

    best_word = "pomme"
    best_score = 0

    for word in usable_words:
        score = evaluate_word(possible_words, word)
        if score > best_score:
            best_word, best_score = word, score

    return False, best_word


def get_next_guess(
    possible_words: list[str], usable_words: list[str]
) -> tuple[bool, str]:
    best_words = get_best_words(possible_words, usable_words)

    return get_best_word(possible_words, best_words)


# @cython.cfunc
# def terminal_game():
#    possible_words = get_possible_words()
#    attempt = "roate"
#
#    while True:
#        print(f"the word is {attempt}")
#        colors = input("enter the colors\n")
#        if colors == "GGGGG":
#            break
#
#        possible_words = [
#            word for word in possible_words if get_colors(word, attempt) == colors
#        ]
#        print(f"there is {len(possible_words)} possible words left")
#        start = time.time()
#        _, attempt = get_best_word(possible_words, get_usable_words())
#        end = time.time()
#        print(end - start, "seconds")
#    print("word found")


@cython.cfunc
def main():
    start = time.time()
    _, attempt = get_next_guess(get_possible_words(), get_usable_words())
    end = time.time()

    print(attempt)
    print(end - start)


def get_colors_interface(solution: str, attempt: str) -> str:
    return get_colors(solution, attempt)


if __name__ == "__main__":
    main()
