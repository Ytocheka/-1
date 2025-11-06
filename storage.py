import json
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from typing import Dict, List, Optional
from .utils import hash_password, verify_password


class PasswordStorage:
    def __init__(self, storage_file: str = "passwords.enc"):
        self.storage_file = storage_file
        self.fernet = None

    def _derive_key(self, password: str, salt: bytes) -> bytes:

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def initialize_storage(self, master_password: str):

        salt = os.urandom(16)
        key = self._derive_key(master_password, salt)
        self.fernet = Fernet(key)


        data = {
            'salt': base64.b64encode(salt).decode(),
            'passwords': {}
        }

        encrypted_data = self.fernet.encrypt(json.dumps(data).encode())
        with open(self.storage_file, 'wb') as f:
            f.write(encrypted_data)

    def _load_data(self, master_password: str) -> Dict:

        if not os.path.exists(self.storage_file):
            raise FileNotFoundError("Хранилище не инициализировано")

        with open(self.storage_file, 'rb') as f:
            encrypted_data = f.read()


        try:
            temp_data = json.loads(Fernet(base64.urlsafe_b64encode(os.urandom(32))).decrypt(encrypted_data))
            salt = base64.b64decode(temp_data['salt'])
        except:

            with open(self.storage_file, 'rb') as f:
                encrypted_data = f.read()


            salt = os.urandom(16)

        key = self._derive_key(master_password, salt)
        self.fernet = Fernet(key)

        try:
            decrypted_data = self.fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data)
        except Exception as e:
            raise ValueError("Неверный мастер-пароль") from e

    def save_password(self, master_password: str, service: str, username: str,
                      password: str, notes: str = ""):

        data = self._load_data(master_password)

        data['passwords'][service] = {
            'username': username,
            'password': password,
            'notes': notes,
            'service': service
        }

        encrypted_data = self.fernet.encrypt(json.dumps(data).encode())
        with open(self.storage_file, 'wb') as f:
            f.write(encrypted_data)

    def get_password(self, master_password: str, service: str) -> Optional[Dict]:

        data = self._load_data(master_password)
        return data['passwords'].get(service)

    def list_services(self, master_password: str) -> List[str]:

        data = self._load_data(master_password)
        return list(data['passwords'].keys())

    def search_passwords(self, master_password: str, query: str) -> List[Dict]:

        data = self._load_data(master_password)
        results = []

        for service, info in data['passwords'].items():
            if (query.lower() in service.lower() or
                    query.lower() in info['username'].lower() or
                    query.lower() in info.get('notes', '').lower()):
                results.append(info)

        return results