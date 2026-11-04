from django.db import models
from django.urls import reverse


class Author(models.Model):
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    name = models.CharField(max_length=100, blank=False, verbose_name='Имя')
    bio = models.TextField(blank=True, verbose_name='Биография')

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(max_length=40, blank=False, verbose_name='Заголовок')

    def __str__(self):
        return self.name


class Tag(models.Model):
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    name = models.CharField(max_length=20, blank=False, verbose_name='Заголовок')

    def __str__(self):
        return self.name


class Article(models.Model):
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    title = models.CharField(max_length=200, blank=False, verbose_name='Заголовок')
    content = models.TextField(blank=True, verbose_name='Текст')
    pub_date = models.DateTimeField(auto_now=True, blank=False, verbose_name='Дата публикации')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles', verbose_name='Теги')

    def get_absolute_url(self):
        return reverse("blogapp:article", kwargs={'pk': self.pk})

    def __str__(self):
        return self.title