ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def caesar_shift_encode(text: str, start_shift: int) -> str:
    result = []
    for i, ch in enumerate(text):
        idx = ALPHABET.index(ch)
        shifted_idx = (idx + start_shift + i) % 26
        result.append(ALPHABET[shifted_idx])
    return "".join(result)


def caesar_shift_decode(text: str, start_shift: int) -> str:
    result = []
    for i, ch in enumerate(text):
        idx = ALPHABET.index(ch)
        orig_idx = (idx - start_shift - i) % 26
        result.append(ALPHABET[orig_idx])
    return "".join(result)


def rotor_forward(text: str, rotor: str) -> str:
    # A -> rotor[0], B -> rotor[1], ...
    return "".join(rotor[ALPHABET.index(ch)] for ch in text)


def rotor_backward(text: str, rotor: str) -> str:
    # Зворотна заміна: знаходимо літеру в rotor і беремо відповідну з ALPHABET
    return "".join(ALPHABET[rotor.index(ch)] for ch in text)


def enigma_process(mode: str, shift: int, rotors: list[str], message: str) -> str:
    mode = mode.strip().upper()
    if mode == "ENCODE":
        text = caesar_shift_encode(message, shift)
        for r in rotors:
            text = rotor_forward(text, r)
        return text

    if mode == "DECODE":
        text = message
        for r in reversed(rotors):
            text = rotor_backward(text, r)
        return caesar_shift_decode(text, shift)

    raise ValueError(f"Невідомий режим: {mode}")


def main():

    mode = input().strip()
    shift = int(input().strip())
    rotors = [input().strip() for _ in range(3)]
    message = input().strip()

    print(enigma_process(mode, shift, rotors, message))


if __name__ == "__main__":
    main()
