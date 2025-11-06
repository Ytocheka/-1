import hashlib
import secrets
import json
from typing import Dict, Any, Optional
import getpass


def hash_password(password: str) -> str:

    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return f"{salt}${password_hash.hex()}"


def verify_password(password: str, hashed: str) -> bool:

    try:
        salt, stored_hash = hashed.split('$')
        new_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        return secrets.compare_digest(new_hash, stored_hash)
    except:
        return False


def calculate_entropy(password: str) -> float:

    char_pool = 0
    if any(c.islower() for c in password):
        char_pool += 26
    if any(c.isupper() for c in password):
        char_pool += 26
    if any(c.isdigit() for c in password):
        char_pool += 10
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        char_pool += 20

    if char_pool == 0:
        return 0

    return len(password) * (char_pool ** 0.5).bit_length()


def get_master_password() -> str:

    return getpass.getpass("Введите мастер-пароль: ")


def strength_check(password: str) -> Dict[str, Any]:

    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Пароль слишком короткий")

    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Добавьте строчные буквы")

    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Добавьте заглавные буквы")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Добавьте цифры")

    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 1
    else:
        feedback.append("Добавьте специальные символы")

    entropy = calculate_entropy(password)

    strength_levels = {
        0: "Очень слабый",
        1: "Слабый",
        2: "Средний",
        3: "Хороший",
        4: "Сильный",
        5: "Очень сильный"
    }

    return {
        "score": score,
        "strength": strength_levels.get(score, "Неизвестно"),
        "entropy": f"{entropy:.2f} бит",
        "feedback": feedback
    }