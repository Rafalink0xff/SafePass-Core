from config import PEPPER
from argon2 import PasswordHasher

# Aplicando as configurações de hardware (RNF02)
ph = PasswordHasher(
    memory_cost=65536, # 64MB
    time_cost=3,       # 3 iterações
    parallelism=4      # 4 threads
)

def hash_password(password: str):
    senha_com_pepper = f"{password}{PEPPER}"
    return ph.hash(senha_com_pepper)

def verify_password(password: str, hashed_p: str):
    senha_com_pepper = f"{password}{PEPPER}"
    try:
        return ph.verify(hashed_p, senha_com_pepper)
    except Exception:
        return False