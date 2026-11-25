def encode(string: str) -> str:
  tripled = []
  for ch in string:
    bits8 = f"{ord(ch):08b}"
    for b in bits8:
      tripled.append(b * 3)
  return "".join(tripled)


def decode(bits: str) -> str:
  # 1. Виправляємо помилки у кожній трійці бітів
  corrected_bits = []
  for i in range(0, len(bits), 3):
    triplet = bits[i : i + 3]
    if len(triplet) < 3:
      break
    bit = "1" if triplet.count("1") >= 2 else "0"
    corrected_bits.append(bit)

  stream = "".join(corrected_bits)

  # 2. Збираємо 8-бітні блоки у символи ASCII
  chars = []
  for i in range(0, len(stream) - (len(stream) % 8), 8):
    byte_str = stream[i : i + 8]
    chars.append(chr(int(byte_str, 2)))

  return "".join(chars)
