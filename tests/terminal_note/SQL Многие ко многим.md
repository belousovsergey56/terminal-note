---
Дата создания: 2025-04-11
ссылки:
  - "[[SQL]]"
  - "[[Ссылки/t0digital|t0digital]]"
  - "[[postgresql]]"
tags:
  - "#связи"
  - "#онтологии"
  - "#m2m"
  - "#многие_ко_многим"
---
> Связь многие ко многим реализуется через отдельную, промежуточную таблицу, которая хранит в себе ссылки на связываемые сущности.

```sql
drop table if exists
book,
book_category,
author,
book_to_author,
book_to_category cascade;

create table book_category (
category_id bigint generated always as identity primary key,
name varchar(150) not null check (length(name) >= 2)
);

create table author (
author_id bigint generated always as identity primary key,
name varchar(150) not null check (length(name) >= 3),
description text check (length(description) >= 30)
);

create table book (
book_id bigint generated always as identity primary key,
created_at timestamp,
name varchar(255) not null check (length(name) >= 2),
description text check (length(description) >= 30),
cover varchar(255)
);

create table book_to_category (
book_id bigint references book(book_id),
category_id bigint references book_category(category_id),
primary key (book_id, category_id)
);

create table book_to_author (
book_id bigint references book(book_id),
author_id bigint references author(author_id),
primary key (book_id, author_id)
);

insert into book_category ("name") values
('Художественая литература'),
('Литература по программированию'),
('Научная фантастика'),
('Литература по фотографии');

insert into author ("name",description) values
('Михаил Шолохов','Великий русский советский писатель, журналист и киносценарист.'),
('Лусиану Рамальо','Автор замечательных книг по языку программирования Python.'),
('Александр Пушкин','Русский поэт, драматург и прозаик, рассматривается как основоположник современного русского литературного языка.'),
('Александр Беляев','Русский писатель-фантаст, один из основоположников советской научно-фантастической литературы.'),
('Жюль Верн','Французский писатель, классик приключенческой литературы, один из основоположников жанра научной фантастики.'),
('Борис Пастернак', 'Один из крупнейших русских поэтов XX века.');

insert into book ("name",description,cover,created_at) values
('Тихий Дон','Одно из наиболее значительных, масштабных и талантливых произведений русскоязычной литературы, принесшее автору Нобелевскую премию.','https://cdn.rroom.io/17558b4d-59dd-4f8e-b2c7-51b0d7da5216.png','2024-01-01 00:00:00'),
('Python. К вершинам мастерства','Лучшая книга по углубленному изучению Python.','https://cdn.rroom.io/2bee8345-a535-4fe3-add9-8db804ea89ae.png','2024-01-02 00:00:00'),
('Судьба человека','Пронзительный рассказ о временах Великой Отечественной войны, одно из первых произведений советской литературы, в котором война показана правдиво и наглядною.','https://cdn.rroom.io/271755e5-046f-4842-85cf-4e22cb17b294.png','2024-01-03 00:00:00'),
('Капитанская дочка',NULL,NULL,'2024-01-04 00:00:00'),
('Сказка о рыбаке и рыбке',NULL,NULL,'2024-01-05 00:00:00'),
('Голова профессора Доуэля',NULL,NULL,'2024-01-06 00:00:00'),
('Остров погибших кораблей',NULL,NULL,'2024-01-07 00:00:00'),
('Путешествие к центру Земли',NULL,NULL,'2024-01-08 00:00:00'),
('Дети капитана Гранта',NULL,NULL,'2024-01-09 00:00:00');

insert into book_to_author(book_id, author_id) values
(1, 1),
(2, 2),
(3, 1),
(4, 3),
(5, 3),
(6, 4),
(7, 4),
(8, 5),
(9, 5);

insert into book_to_category(book_id, category_id) values
(1, 1),
(2, 2),
(3, 1),
(4, 1),
(5, 1),
(6, 1),
(7, 1),
(8, 1),
(9, 1),
(6, 3),
(7, 3),
(8, 3),
(9, 3);
```

Здесь таблицы книг и авторов связаны через промежуточную таблицу `book_to_author`. Эта таблица хранит ссылку на автора и на книгу. И она может содержать много строк, которые ссылаются на одну и ту же книгу или на одну и ту же категорию. Связь многие ко многим, книга может написана несколькими авторами и один автор мог написать несколько книг.

Аналогично таблица книг связана с таблицей категорий через промежуточную таблицу `book_to_category`. Одна книга может быть в разных категориях и категория может содержать разные книги. Связь снова многие ко многим.

Как достать все категории одной книги? Например, книги с идентификатором 6, это книга «Голова профессора Доуэля» Александра Беляева. Эта книга принадлежит категории Художественная литература и Научная фантастика.

```sql
select b.name book_name, c.name category_id
from book b
join book_to_category bc using(book_id)
join book_category c using(category_id)
where b.book_id = 6;

|book_name |category_id |
|------------------------|------------------------|
|Голова профессора Доуэля|Художественая литература|
|Голова профессора Доуэля|Научная фантастика |
```

> Если мы хотим получить книги с категориями? Просто убираем ограничение `where`, и можно для удобства добавить сортировку

```sql
select b.name book_name, c.name category
from book b
join book_to_category bc using(book_id)
join book_category c using(category_id)
order by book_name, category_id;
```

А если нам хочется, чтобы одна книга была представлена в результатах одной строкой, а не несколькими? Для этого можно воспользоваться группировкой, о которой мы поговорим дальше в этой главе, но пример можно показать уже сейчас

```sql
select b.name book_name, array_agg(c.name) category
from book b
join book_to_category bc using(book_id)
join book_category c using(category_id)
group by 1
order by book_name;
```

Здесь у нас колонка `category` в результатах представлена массивом. Можно сделать строкой
```sql
select b.name book_name, string_agg(c.name, ', ') category_id
from book b
join book_to_category bc using(book_id)
join book_category c using(category_id)
group by 1
order by book_name, category_id;
```