from cryptography.fernet import Fernet
from django.db import models
from django.conf import settings

class EncryptedCharField(models.CharField):
    def decrypt(self, value, expression, connection):
        if value:
            decrypted_value = settings.CIPHER_SUITE.decrypt(value.encode())
            return decrypted_value.decode()
        return value

    def encrypt(self, value):
        if value:
            encrypted_value = settings.CIPHER_SUITE.encrypt(value.encode())
            return encrypted_value.decode()
        return value