from Solver import (
    get_possible_words,
    get_usable_words,
    get_best_word,
    get_colors_from_attempt,
)

usable_words = get_usable_words()
first_word = "roate"


def simulation(possible_words: list[str], scores: list[int], depth=1):
    if depth == 1:
        attempt = first_word
    else:
        attempt = get_best_word(possible_words, usable_words)

    sequences: dict[str, int] = {}
    for w in possible_words:
        colors = get_colors_from_attempt(w, attempt)
        sequences[colors] = (sequences.get(colors) or 0) + 1

    for colors, number in sequences.items():
        if colors == "GGGGG":
            scores[depth] += 1
            continue

        next_possible_words = [
            word
            for word in possible_words
            if get_colors_from_attempt(word, attempt) == colors
        ]
        simulation(next_possible_words, scores, depth + 1)
    print(scores)
    return scores


def main():
    possible_words = get_possible_words()
    scores = [0, 0, 37, 1028, 1205, 39, 0, 0, 0, 0]
    # simulation(possible_words, scores)
    print(scores)

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
