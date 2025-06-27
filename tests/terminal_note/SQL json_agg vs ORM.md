---
Дата создания: 2025-04-14
ссылки:
  - "[[Ссылки/t0digital|t0digital]]"
  - "[[SQL]]"
tags:
  - "#Примеры"
---
Проект на GitHub: [https://github.com/alexey-goloburdin/django-orm-vs-json_agg](https://github.com/alexey-goloburdin/django-orm-vs-json_agg)

Вот так может описываться структура моделей Django:

```python
from django.db import models

class Author(models.Model):
    author_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "author___"

class Category(models.Model):
    category_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "category___"

class Book(models.Model):
    book_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    authors = models.ManyToManyField(to=Author, related_name='books')
    categories = models.ManyToManyField(to=Category, related_name='books')

    class Meta:
        db_table = "book___"
```

Вот так мы можем создать несколько записей (это Django management command):


```python
# books/management/commands/init_db_records.py
from books.models import Book, Category

from django.core.management.base import BaseCommand

from books.models import Author, Book, Category

class Command(BaseCommand):
    def handle(self, *args, **options):
        Category.objects.all().delete()
        Author.objects.all().delete()
        Book.objects.all().delete()
        
        authors = (
            Author.objects.create(author_id=1, name='Александр Пушин'),
            Author.objects.create(author_id=2, name='Александр Беляев')
        )
        
        categories = (
            Category.objects.create(category_id=1, name='Художественная литература'),
            Category.objects.create(category_id=2, name='Научная фантастика')
        )
        
        book = Book.objects.create(
            book_id=1,
            name="Капитанская дочка"
        )
        book.categories.add(categories[0])
        book.authors.add(authors[0])
        
        book = Book.objects.create(
            book_id=2,
            name="Ариэль",
        )
        book.categories.add(categories[0], categories[1])
        book.authors.add(authors[1])

        book = Book.objects.create(
            book_id=3,
            name="Человек-амфибия",
        )
        book.categories.add(categories[0], categories[1])
        book.authors.add(authors[1])

        book = Book.objects.create(
            book_id=4,
            name="Голова профессора Доуэля",
        )
        book.categories.add(categories[0], categories[1])
        book.authors.add(authors[1])
```

И теперь предположим, что нам надо достать и напечатать все книги с их категориями.

С Django ORM это можно сделать так. Предварительно только включим логирование всех запросов в `books/settings.py`, чтобы мы видели все SQL-запросы, которые генерирует и отправляет в PostgreSQL Django:


```sh
# settings.py
import logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

И теперь решаем задачу вывода книг:

```python
# books/management/commands/print_books_naive_method.py
from django.core.management.base import BaseCommand

from books.models import Book

def print_books_naive_method():
    books = Book.objects.all()
    for book in books:
        book_name = book.name
        category_names = ", ".join([
            c.name.lower() for c in book.categories.all()
        ])
        author_names = ", ".join([
            a.name for a in book.authors.all()
        ])
        print(f"«{book_name}», авторы: {author_names}, категории: {category_names}")

class Command(BaseCommand):
    def handle(self, *args, **options):
        print_books_naive_method()
```

Что получаем? 9 SQL-запросов.

Можно сократить количество SQL-запросов, если использовать `prefetch`:

```python
# books/management/commands/print_books_with_prefetch.py
from django.core.management.base import BaseCommand

from books.models import Book

def print_books_with_prefetch():
    books = Book.objects.prefetch_related("authors", "categories").all()
    for book in books:
        book_name = book.name
        category_names = ", ".join([
            c.name.lower() for c in book.categories.all()
        ])
        author_names = ", ".join([
            a.name for a in book.authors.all()
        ])
        print(f"«{book_name}», авторы: {author_names}, категории: {category_names}")

class Command(BaseCommand):
    def handle(self, *args, **options):
        print_books_with_prefetch()
```

Воу! Результат тот же, а уже 3 запроса. Да, стало лучше... Но 3 запроса это не 1 один запрос. И, если будет больше связей — больше запросов будет. Будет 10 связей — будет 10 запросов. Этот способ лучше, потому что с ростом количества записей в таблице книг не увеличивается количество запросов, но количество запросов будет увеличиваться с ростом количества связей.

Есть ли способ ещё лучше? Конечно.

Например, `json_agg`. Сколько бы ни было записей или связей — всё достанем одним запросом:

```python
# books/management/commands/print_books_with_json.py
from django.core.management.base import BaseCommand

from django.db import connection

def print_books_with_json():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                b.name AS book_name,
                json_agg(distinct a.*) AS authors,
                json_agg(distinct c.*) AS categories
            FROM book___ b
            LEFT JOIN book____authors USING(book_id)
            LEFT JOIN author___ a USING(author_id)
            LEFT JOIN book____categories USING(book_id)
            LEFT JOIN category___ c USING(category_id)
            GROUP by b.name
            ORDER BY b.name""")
        books = cursor.fetchall()
    for book in books:
        book_name = book[0]
        category_names = ", ".join([
            c["name"].lower() for c in book[2]
        ])
        author_names = ", ".join([
            a["name"] for a in book[1]
        ])
        print(f"«{book_name}», авторы: {author_names}, категории: {category_names}")


class Command(BaseCommand):
    def handle(self, *args, **options):
        print_books_with_json()
```

Уопчки! Всего 1 запрос. Отлично!

1 запрос вместо 9 запросов на старте.

Причём с помощью `json_agg` мы достаём все данные всех нужных нам дополнительных сущностей и точно так же можем инициализировать питоновские классы с ними. В данном случае класс книга, класс категория, класс автор. Без проблем. Просто вместо тонны запросов забираем все данные одним запросом.