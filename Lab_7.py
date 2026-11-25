def scanner(qrcode: list[list[int]]) -> str:
  # Збираємо бітовий потік змійкою по 2 стовпці справа наліво (20-19, 18-17, 16-15, 14-13)
  bits: list[int] = []
  going_up = True

  for right_col in (20, 18, 16, 14):
    rows = range(20, 8, -1) if going_up else range(9, 21)
    for r in rows:
      for c in (right_col, right_col - 1):
        val = qrcode[r][c]
        # Знімаємо маску 0: (r + c) % 2 == 0 -> інвертуємо біт
        if (r + c) % 2 == 0:
          val ^= 1
        bits.append(val)
    going_up = not going_up

  def read_byte(offset: int) -> int:
    b = 0
    for bit in bits[offset : offset + 8]:
      b = (b << 1) | bit
    return b

  # Перші 4 біти (0..3) — індикатор режиму (0100), далі 8 бітів (4..11) — довжина тексту
  length = read_byte(4)

  # Далі йдуть length байтів по 8 бітів, починаючи з індексу 12
  chars = []
  for i in range(length):
    code = read_byte(12 + i * 8)
    chars.append(chr(code))

  return "".join(chars)
