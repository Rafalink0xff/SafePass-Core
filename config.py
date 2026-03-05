import os
from dotenv import load_dotenv

load_dotenv()

PEPPER = os.getenv("SECRET_PEPPER")

# Se o PEPPER for None ou vazio, paramos tudo imediatamente
if not PEPPER:
    raise ValueError("ERRO CRÍTICO: Variável SECRET_PEPPER não encontrada no ambiente!")