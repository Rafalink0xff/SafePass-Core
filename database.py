import json
import os
from typing import Optional

ARQUIVO = "users.json"


def _carregar_usuarios() -> list[dict]:
    if not os.path.exists(ARQUIVO):
        return []
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def _salvar_usuarios(usuarios: list[dict]) -> bool:
    try:
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, indent=2, ensure_ascii=False)
        return True
    except IOError:
        return False


def salvar_usuario(email: str, hash_senha: str) -> bool:
    """
    Salva um novo usuário no arquivo users.json.
    Retorna False se o email já existir ou se houver erro.
    """
    if not email or not email.strip() or not hash_senha or not hash_senha.strip():
        return False

    email = email.strip().lower()

    usuarios = _carregar_usuarios()

    # Verifica se já existe
    if any(u.get("email", "").lower() == email for u in usuarios):
        return False

    usuarios.append({"email": email, "hash_senha": hash_senha})

    return _salvar_usuarios(usuarios)


def buscar_usuario(email: str) -> Optional[str]:
    """
    Retorna o hash da senha do usuário com o email informado,
    ou None se não encontrado ou email inválido.
    """
    if not email or not email.strip():
        return None

    email = email.strip().lower()
    usuarios = _carregar_usuarios()

    for usuario in usuarios:
        if usuario.get("email", "").lower() == email:
            return usuario.get("hash_senha")

    return None

def verificar_email(email: str) -> Optional[str]:
    """
    Retorna o hash da senha do usuário com o email informado,
    ou None se não encontrado ou email inválido.
    """
    if not email or not email.strip():
        return None

    email = email.strip().lower()
    usuarios = _carregar_usuarios()

    for usuario in usuarios:
        if usuario.get("email", "").lower() == email:
            return usuario.get("email")

    return None