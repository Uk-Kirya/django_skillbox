from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile


class UserBioForm(forms.Form):
    name = forms.CharField(label="Your Name")
    age = forms.IntegerField(label="Your Age")
    bio = forms.CharField(label="Your BIO", widget=forms.Textarea)


def validate_file_form(file: InMemoryUploadedFile) -> None:
    if file.size > (1024 * 1024 * 10):
        raise ValidationError("Max filesize 10MB")


class FileUploadForm(forms.Form):
    my_file = forms.FileField(validators=[validate_file_form])
