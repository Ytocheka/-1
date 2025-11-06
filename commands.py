import argparse
import sys
from typing import List
from .generator import PasswordGenerator
from .storage import PasswordStorage
from .utils import strength_check, get_master_password


def generate_password_command(args):

    generator = PasswordGenerator()

    try:
        if args.multiple:
            passwords = generator.generate_multiple(
                count=args.multiple,
                length=args.length,
                use_lowercase=not args.no_lowercase,
                use_uppercase=not args.no_uppercase,
                use_digits=not args.no_digits,
                use_special=args.special
            )

            print(f"Сгенерировано {args.multiple} паролей:")
            for i, password in enumerate(passwords, 1):
                strength = strength_check(password)
                print(f"{i}. {password} [{strength['strength']}]")

        else:
            password = generator.generate_password(
                length=args.length,
                use_lowercase=not args.no_lowercase,
                use_uppercase=not args.no_uppercase,
                use_digits=not args.no_digits,
                use_special=args.special
            )

            print(f"Сгенерированный пароль: {password}")
            strength = strength_check(password)
            print(f"Надежность: {strength['strength']}")
            print(f"Энтропия: {strength['entropy']}")

            if strength['feedback']:
                print("Рекомендации:")
                for feedback in strength['feedback']:
                    print(f"  - {feedback}")


            if args.save:
                master_password = get_master_password()
                storage = PasswordStorage()

                service = input("Введите название сервиса: ")
                username = input("Введите имя пользователя: ")
                notes = input("Введите заметки (опционально): ")

                storage.save_password(master_password, service, username, password, notes)
                print(f"Пароль для {service} сохранен!")

    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


def save_password_command(args):

    storage = PasswordStorage()
    master_password = get_master_password()

    try:
        storage.save_password(
            master_password,
            args.service,
            args.username,
            args.password,
            args.notes or ""
        )
        print(f"Пароль для {args.service} сохранен!")
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


def get_password_command(args):

    storage = PasswordStorage()
    master_password = get_master_password()

    try:
        password_info = storage.get_password(master_password, args.service)
        if password_info:
            print(f"Сервис: {password_info['service']}")
            print(f"Имя пользователя: {password_info['username']}")
            print(f"Пароль: {password_info['password']}")
            if password_info.get('notes'):
                print(f"Заметки: {password_info['notes']}")
        else:
            print(f"Пароль для сервиса '{args.service}' не найден")
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


def search_passwords_command(args):

    storage = PasswordStorage()
    master_password = get_master_password()

    try:
        results = storage.search_passwords(master_password, args.query)
        if results:
            print(f"Найдено {len(results)} результатов:")
            for i, result in enumerate(results, 1):
                print(f"{i}. Сервис: {result['service']}")
                print(f"   Пользователь: {result['username']}")
                print(f"   Пароль: {result['password']}")
                if result.get('notes'):
                    print(f"   Заметки: {result['notes']}")
                print()
        else:
            print("Ничего не найдено")
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


def init_storage_command(args):

    storage = PasswordStorage()
    master_password = get_master_password()
    confirm_password = getpass.getpass("Подтвердите мастер-пароль: ")

    if master_password != confirm_password:
        print("Пароли не совпадают!", file=sys.stderr)
        sys.exit(1)

    try:
        storage.initialize_storage(master_password)
        print("Хранилище успешно инициализировано!")
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


def list_services_command(args):

    storage = PasswordStorage()
    master_password = get_master_password()

    try:
        services = storage.list_services(master_password)
        if services:
            print("Сохраненные сервисы:")
            for service in services:
                print(f"  - {service}")
        else:
            print("Нет сохраненных паролей")
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)