import os.path
import uuid

from django.contrib.auth.models import User
from django.db import models


def path_to_user(instance: "User", filename: str):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('users', str(instance.user.id), 'profile-photo', filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(null=True, upload_to=path_to_user)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
