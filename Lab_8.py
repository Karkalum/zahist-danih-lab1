import math

def discrete_log(g: int, h: int, q: int) -> int:
    h %= q
    if h == 1:
        return 0

    m = math.isqrt(q) + 1

    baby: dict[int, int] = {}
    cur = 1
    for j in range(m):
        if cur == h:
            return j
        if cur not in baby:
            baby[cur] = j
        cur = (cur * g) % q

    gm = pow(g, m, q)
    factor = pow(gm, -1, q)

    gamma = h
    best: int | None = None
    for i in range(1, m + 1):
        gamma = (gamma * factor) % q
        if gamma in baby:
            cand = i * m + baby[gamma]
            if best is None or cand < best:
                best = cand

    return best if best is not None else -1

def main() -> None:
    g, h, q = map(int, input().split())
    print(discrete_log(g, h, q))

if __name__ == "__main__":
    main()
