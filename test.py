import time
from Solver import (
    get_colors_interface,
    get_next_guess,
    get_possible_words,
    get_usable_words,
)
from second_word import second_word

usable_words = get_usable_words()
first_word = "salet"


def simulation(
    possible_words: list[str],
    scores: list[int],
    depth=1,
    previous_color: str | None = None,
):
    if depth == 1:
        attempt = first_word
    elif depth == 2 and previous_color:
        attempt = second_word[previous_color]
    else:
        _, attempt = get_next_guess(possible_words, usable_words)

    sequences: dict[str, int] = {}
    for w in possible_words:
        colors = get_colors_interface(w, attempt)
        sequences[colors] = (sequences.get(colors) or 0) + 1

    for colors, _ in sequences.items():
        if colors == "GGGGG":
            scores[depth] += 1
            continue

        next_possible_words = [
            word
            for word in possible_words
            if get_colors_interface(word, attempt) == colors
        ]
        simulation(next_possible_words, scores, depth + 1, colors)
    return scores


def get_average(scores: list[int]) -> float:
    total = 0
    for i in range(10):
        total += i * scores[i]
    return total / sum(scores)


def main():
    possible_words = get_possible_words()
    scores = [0] * 10
    # scores = [0, 0, 37, 1028, 1205, 39, 0, 0, 0, 0] # before heuristic 3.5396275443915113 avg
    # score2 = [0, 0, 37, 1027, 1206, 39, 0, 0, 0, 0] # after heuristic
    # salet 3.5119099177132957 [0, 0, 57, 1060, 1146, 45, 1, 0, 0, 0]
    # [0, 0, 8, 1170, 1092, 39, 0, 0, 0, 0]
    # [0, 0, 9, 1177, 1084, 39, 0, 0, 0, 0] 3.499350368124729

    simulation(possible_words, scores)

    # calcul avg
    total = 0
    for i in range(10):
        total += i * scores[i]
    avg = total / len(possible_words)
    print(scores)
    print(avg, "avg")

    # calcul aggregate percentage
    for i in range(9):
        scores[i + 1] += scores[i]
    # print([score / len(possible_words) for score in scores])

    start = time.time()
    _, attempt = get_next_guess(possible_words, usable_words)
    end = time.time()
    print(end - start, "seconds")
    print(attempt)


if __name__ == "__main__":
    main()
