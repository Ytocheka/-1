import random
import string
from cryptography.fernet import Fernet


def test_password_generator():


    chars = string.ascii_letters + string.digits + "!@#$%"
    password = ''.join(random.choice(chars) for _ in range(12))

    print(f"✅ Пароль сгенерирован: {password}")
    print(f"✅ Длина: {len(password)} символов")


    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%" for c in password)

    print(f"✅ Заглавные буквы: {'Да' if has_upper else 'Нет'}")
    print(f"✅ Строчные буквы: {'Да' if has_lower else 'Нет'}")
    print(f"✅ Цифры: {'Да' if has_digit else 'Нет'}")
    print(f"✅ Спецсимволы: {'Да' if has_special else 'Нет'}")


def test_cryptography():
    print("\n🔒 Тест cryptography...")


    key = Fernet.generate_key()
    cipher_suite = Fernet(key)


    test_message = b"cvb45644"
    encrypted = cipher_suite.encrypt(test_message)
    decrypted = cipher_suite.decrypt(encrypted)

    print(f"✅ Сообщение зашифровано: {encrypted[:20]}...")
    print(f"✅ Сообщение расшифровано: {decrypted.decode()}")

    return test_message == decrypted


if __name__ == "__main__":

    try:
        test_password_generator()
        crypto_works = test_cryptography()

        if crypto_works:
            print("\nБиблиотеки работают корректно")
        else:
            print("\n⚠Есть проблемы с шифрованием")

    except Exception as e:
        print(f"\n❌ Ошибка: {e}")