def hex_xor(h1: str, h2: str) -> bytes:
    b1 = bytes.fromhex(h1.strip())
    b2 = bytes.fromhex(h2.strip())
    return bytes(x ^ y for x, y in zip(b1, b2))


def solve_robber_city(m1_hex: str, m2_hex: str, m3_hex: str) -> str:
    b1 = bytes.fromhex(m1_hex.strip())
    b2 = bytes.fromhex(m2_hex.strip())
    b3 = bytes.fromhex(m3_hex.strip())

    # 1. Відновлюємо ключ Аліси: K_A = M2 XOR M3
    key_alice = bytes(x ^ y for x, y in zip(b2, b3))

    # 2. Відновлюємо відкритий текст: M = M1 XOR K_A
    plain_bytes = bytes(x ^ y for x, y in zip(b1, key_alice))
    return plain_bytes.decode("ascii")


def main():
    m1 = input().strip()
    m2 = input().strip()
    m3 = input().strip()
    print(solve_robber_city(m1, m2, m3))


if __name__ == "__main__":
    main()
