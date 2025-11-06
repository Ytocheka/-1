
import argparse
import sys
from passgen import commands


def main():
    parser = argparse.ArgumentParser(
        description="Генератор безопасных паролей",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python main.py generate -l 16 --special
  python main.py generate --multiple 5 -l 12
  python main.py save -s example.com -u user@example.com -p "password123"
  python main.py get -s example.com
  python main.py search "google"
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Команды')
    gen_parser = subparsers.add_parser('generate', help='Генерация пароля')
    gen_parser.add_argument('-l', '--length', type=int, default=12,
                            help='Длина пароля (по умолчанию: 12)')
    gen_parser.add_argument('--no-lowercase', action='store_true',
                            help='Исключить строчные буквы')
    gen_parser.add_argument('--no-uppercase', action='store_true',
                            help='Исключить заглавные буквы')
    gen_parser.add_argument('--no-digits', action='store_true',
                            help='Исключить цифры')
    gen_parser.add_argument('--special', action='store_true',
                            help='Включить специальные символы')
    gen_parser.add_argument('--multiple', type=int,
                            help='Сгенерировать несколько паролей')
    gen_parser.add_argument('--save', action='store_true',
                            help='Сохранить пароль в хранилище')


    save_parser = subparsers.add_parser('save', help='Сохранение пароля')
    save_parser.add_argument('-s', '--service', required=True,
                             help='Название сервиса')
    save_parser.add_argument('-u', '--username', required=True,
                             help='Имя пользователя')
    save_parser.add_argument('-p', '--password', required=True,
                             help='Пароль для сохранения')
    save_parser.add_argument('-n', '--notes',
                             help='Заметки')


    get_parser = subparsers.add_parser('get', help='Получение пароля')
    get_parser.add_argument('-s', '--service', required=True,
                            help='Название сервиса')


    search_parser = subparsers.add_parser('search', help='Поиск паролей')
    search_parser.add_argument('query', help='Поисковый запрос')


    subparsers.add_parser('init', help='Инициализация хранилища паролей')


    subparsers.add_parser('list', help='Список всех сервисов')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)


    command_handlers = {
        'generate': commands.generate_password_command,
        'save': commands.save_password_command,
        'get': commands.get_password_command,
        'search': commands.search_passwords_command,
        'init': commands.init_storage_command,
        'list': commands.list_services_command,
    }

    handler = command_handlers.get(args.command)
    if handler:
        handler(args)
    else:
        print(f"Неизвестная команда: {args.command}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()