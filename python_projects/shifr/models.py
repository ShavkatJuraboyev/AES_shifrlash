# myapp/models.py
from django.conf import settings
from django.db import models
from cryptography.fernet import Fernet

class UserText(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    encrypted_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk or getattr(self, '_updating', False):
            cipher_suite = Fernet(settings.FERNET_KEY)
            self.encrypted_text = cipher_suite.encrypt(self.encrypted_text.encode('utf-8')).decode('utf-8')
        super().save(*args, **kwargs)

    def get_decrypted_text(self):
        cipher_suite = Fernet(settings.FERNET_KEY)
        plain_text = cipher_suite.decrypt(self.encrypted_text.encode('utf-8'))
        return plain_text.decode('utf-8')

    def __str__(self):
        return self.first_name