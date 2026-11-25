import hashlib

def crack(hash: str) -> str:
  target = hash.strip().lower()
  for i in range(100_000):
    pin = f"{i:05d}"
    if hashlib.md5(pin.encode("utf-8")).hexdigest() == target:
      return pin
  return ""
