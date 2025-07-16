import heapq
import json
from Solver import (
    get_best_words,
    get_best_words_with_scores,
    get_next_guess,
    get_possible_words,
    get_usable_words,
    get_colors_from_attempt,
)

usable_words = get_usable_words()
first_word = "salet"


def simulation(possible_words: list[str], scores: list[int], depth=1):
    if depth == 1:
        attempt = first_word
    else:
        _, attempt = get_next_guess(possible_words, usable_words)

    sequences: dict[str, int] = {}
    for w in possible_words:
        colors = get_colors_from_attempt(w, attempt)
        sequences[colors] = (sequences.get(colors) or 0) + 1

    for colors, _ in sequences.items():
        if colors == "GGGGG":
            scores[depth] += 1
            continue

        next_possible_words = [
            word
            for word in possible_words
            if get_colors_from_attempt(word, attempt) == colors
        ]
        simulation(next_possible_words, scores, depth + 1)
    return scores


def get_average(scores: list[int]) -> float:
    total = 0
    for i in range(10):
        total += i * scores[i]
    return total / sum(scores)


def main():
    global first_word
    possible_words = get_possible_words()
    usable_words = get_usable_words()
    # scores = [0] * 10
    # scores = [0, 0, 37, 1028, 1205, 39, 0, 0, 0, 0] # before heuristic 3.5396275443915113 avg
    # score2 = [0, 0, 37, 1027, 1206, 39, 0, 0, 0, 0] # after heuristic
    # salet 3.5119099177132957 [0, 0, 57, 1060, 1146, 45, 1, 0, 0, 0]
    # [0, 0, 8, 1170, 1092, 39, 0, 0, 0, 0]
    # [0, 0, 9, 1177, 1084, 39, 0, 0, 0, 0] 3.499350368124729

    possible_colors = set()
    for word in possible_words:
        possible_colors.add(get_colors_from_attempt(word, first_word))

    colors_word_scores: dict[str, tuple[str, float, list[int]]] = {}
    for color in possible_colors:
        local_possible_words = [
            word
            for word in get_possible_words()
            if get_colors_from_attempt(word, "salet") == color
        ]

        best_word = "pomme"
        best_score = 10
        best_scores = [0] * 10
        best_words = get_best_words_with_scores(local_possible_words, usable_words)
        while len(best_words) > 30:
            heapq.heappop(best_words)
        for word in [word[1] for word in best_words]:
            first_word = word
            scores = [0] * 10
            simulation(local_possible_words, scores)
            score = get_average(scores)
            if score < best_score:
                best_word, best_score, best_scores = (word, score, scores)

        colors_word_scores[color] = (best_word, best_score, best_scores)
        print("salet", color, best_word, best_score, best_scores)
    print(colors_word_scores)
    with open("test.json", "w", encoding="utf8") as f:
        f.write(json.dumps(colors_word_scores))
    exit()

    for word in get_best_words(possible_words, get_usable_words())[10:100]:
        first_word = word
        scores = [0] * 10
        simulation(possible_words, scores)
        print(word, get_average(scores), scores)
    exit()

    # calcul avg
    total = 0
    for i in range(10):
        total += i * scores[i]
    avg = total / len(possible_words)
    print(avg)

    # calcul aggregate percentage
    for i in range(9):
        scores[i + 1] += scores[i]
    print([score / len(possible_words) for score in scores])


if __name__ == "__main__":
    main()
