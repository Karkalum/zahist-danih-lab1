import os
import numpy as np
from PIL import Image

class LFSR16:
    """16-бітний регістр зсуву з лінійним зворотним зв'язком (відводи 16, 14, 13, 11)."""
    def __init__(self, seed: int):
        if not (1 <= seed <= 0xFFFF):
            raise ValueError("Seed має бути в діапазоні 1..65535")
        self.state = seed

    def next_bit(self) -> int:
        # 0-based індекси бітів для [16, 14, 13, 11] -> [15, 13, 12, 10]
        feedback = (
            ((self.state >> 15) & 1)
            ^ ((self.state >> 13) & 1)
            ^ ((self.state >> 12) & 1)
            ^ ((self.state >> 10) & 1)
        )
        self.state = ((self.state << 1) & 0xFFFF) | feedback
        return feedback

    def next_int(self, bits: int) -> int:
        value = 0
        for _ in range(bits):
            value = (value << 1) | self.next_bit()
        return value

def make_permutation(count: int, seed: int) -> list[int]:
    """Генерує зворотну перестановку індексів [0..count-1] на базі LFSR."""
    lfsr = LFSR16(seed)
    order = list(range(count))
    bits = max(1, count.bit_length())

    for i in range(count - 1, 0, -1):
        while True:
            idx = lfsr.next_int(bits)
            if idx <= i:
                break
        order[i], order[idx] = order[idx], order[i]
    return order


def split_image(arr: np.ndarray, rows: int, cols: int):
    h, w, c = arr.shape
    h = (h // rows) * rows
    w = (w // cols) * cols
    arr = arr[:h, :w]

    bh, bw = h // rows, w // cols
    blocks = [
        arr[r * bh : (r + 1) * bh, c * bw : (c + 1) * bw].copy()
        for r in range(rows)
        for c in range(cols)
    ]
    return blocks, rows, cols, bh, bw, c


def merge_image(blocks: list[np.ndarray], rows: int, cols: int, bh: int, bw: int, channels: int) -> np.ndarray:
    result = np.zeros((rows * bh, cols * bw, channels), dtype=np.uint8)
    k = 0
    for r in range(rows):
        for c in range(cols):
            result[r * bh : (r + 1) * bh, c * bw : (c + 1) * bw] = blocks[k]
            k += 1
    return result


def scramble(arr: np.ndarray, seed: int, rows: int, cols: int) -> np.ndarray:
    blocks, r, c, bh, bw, ch = split_image(arr, rows, cols)
    perm = make_permutation(len(blocks), seed)
    shuffled = [blocks[i] for i in perm]
    return merge_image(shuffled, r, c, bh, bw, ch)


def unscramble(arr: np.ndarray, seed: int, rows: int, cols: int) -> np.ndarray:
    blocks, r, c, bh, bw, ch = split_image(arr, rows, cols)
    perm = make_permutation(len(blocks), seed)
    restored = [None] * len(blocks)
    for pos, src_idx in enumerate(perm):
        restored[src_idx] = blocks[pos]
    return merge_image(restored, r, c, bh, bw, ch)


def correlation_pct(a: np.ndarray, b: np.ndarray) -> float:
    h = min(a.shape[0], b.shape[0])
    w = min(a.shape[1], b.shape[1])
    va = a[:h, :w].astype(np.float64).flatten()
    vb = b[:h, :w].astype(np.float64).flatten()
    return abs(float(np.corrcoef(va, vb)[0, 1])) * 100.0


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, "Donor.png")
    out_dir = os.path.join(base_dir, "output")
    os.makedirs(out_dir, exist_ok=True)

    seed = 44257
    rows, cols = 12, 16

    orig = np.array(Image.open(input_path).convert("RGB"))
    enc = scramble(orig, seed=seed, rows=rows, cols=cols)
    dec = unscramble(enc, seed=seed, rows=rows, cols=cols)

    Image.fromarray(enc).save(os.path.join(out_dir, "Donor_enc.png"))
    Image.fromarray(dec).save(os.path.join(out_dir, "Donor_dec.png"))

    print(f"Seed: {seed}, сітка: {rows}x{cols}")
    print(f"Схожість оригінал <-> зашифроване: {correlation_pct(orig, enc):.2f}%")
    print(f"Схожість оригінал <-> розшифроване: {correlation_pct(orig, dec):.2f}%")


if __name__ == "__main__":
    main()
