ENGLISH_FREQ = {
    "A": 8.08, "B": 1.67, "C": 3.18, "D": 3.99, "E": 12.56, "F": 2.17,
    "G": 1.80, "H": 5.27, "I": 7.24, "J": 0.14, "K": 0.63, "L": 4.04,
    "M": 2.60, "N": 7.38, "O": 7.47, "P": 1.91, "Q": 0.09, "R": 6.42,
    "S": 6.59, "T": 9.15, "U": 2.79, "V": 1.00, "W": 1.89, "X": 0.21,
    "Y": 1.65, "Z": 0.07,
}


def shift_text(text: str, shift: int) -> str:
    """Зсуває лише літери A-Z / a-z на shift (може бути додатним або від'ємним)."""
    result = []
    for ch in text:
        if "A" <= ch <= "Z":
            idx = (ord(ch) - ord("A") + shift) % 26
            result.append(chr(ord("A") + idx))
        elif "a" <= ch <= "z":
            idx = (ord(ch) - ord("a") + shift) % 26
            result.append(chr(ord("a") + idx))
        else:
            result.append(ch)
    return "".join(result)


def score_candidate(candidate: str) -> float:
    """Оцінюємо, наскільки частоти літер в тексті близькі до еталонних (менше = краще)."""
    letters = [ch.upper() for ch in candidate if ch.isalpha()]
    if not letters:
        return float("inf")

    total = len(letters)
    error = 0.0
    for letter, expected_pct in ENGLISH_FREQ.items():
        actual_pct = (letters.count(letter) / total) * 100.0
        error += (actual_pct - expected_pct) ** 2
    return error


def decode_by_frequency(encoded_text: str) -> str:
    best_text = encoded_text
    best_error = float("inf")

    # Перебираємо зсув шифрування k у межах 0..25; для декодування зсуваємо на -k
    for k in range(26):
        decoded = shift_text(encoded_text, -k)
        err = score_candidate(decoded)
        if err < best_error:
            best_error = err
            best_text = decoded

    return best_text


def main():
    encoded_message = input()
    print(decode_by_frequency(encoded_message))


if __name__ == "__main__":
    main()
