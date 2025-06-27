---
Дата создания: 2025-04-27
ссылки:
  - "[[SQL]]"
  - "[[postgresql]]"
  - "[[t0digital]]"
tags:
  - psql
  - sql
  - postgres
  - distinct
---
Есть в языке SQL ещё ключевое слово `DISTINCT`, которое используется для удаления дубликатов из результирующего набора данных.

`GROUP BY` тоже используется для удаления дубликатов, но сценарии использования `GROUP BY` как правило связаны с использованием агрегатных функций, в то время как задача `DISTINCT` просто в удалении дубликатов и здесь не идёт речи об использовании агрегатных функций.

Например, у нас есть таблица `book_to_category`. Что если нам надо найти идентификаторы всех книг, которые привязаны хотя бы к одной категории? Это можно сделать двумя способами:



```sql
select book_id from book_to_category group by book_id order by book_id;

select distinct book_id from book_to_category order by book_id;
```

Результат идентичен. Однако в этом случае я бы воспользовался именно `distinct`, потому что здесь задача просто убрать дубликаты.

В уроке «json_agg vs ORM» фигурировал такой запрос:



```sql
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
ORDER BY b.name;
```

Здесь тоже есть `DISTINCT`. Если мы его уберём, то в JSON появятся дубликаты:



```sql
SELECT
b.name AS book_name,
json_agg(a.*) AS authors,
json_agg(c.*) AS categories
FROM book___ b
LEFT JOIN book____authors USING(book_id)
LEFT JOIN author___ a USING(author_id)
LEFT JOIN book____categories USING(book_id)
LEFT JOIN category___ c USING(category_id)
GROUP by b.name
ORDER BY b.name;
```

С чем это связано? С тем, что собственно дубликаты присутствуют там:)

Если мы уберем группировку, то увидим это:



```sql
SELECT
b.name AS book_name,
a.name AS author,
c.name AS category
FROM book___ b
LEFT JOIN book____authors USING(book_id)
LEFT JOIN author___ a USING(author_id)
LEFT JOIN book____categories USING(book_id)
LEFT JOIN category___ c USING(category_id)
ORDER BY b.name;

|book_name |author |category |
|------------------------|----------------|-------------------------|
|Ариэль |Александр Беляев|Художественная литература|
|Ариэль |Александр Беляев|Научная фантастика |
|Голова профессора Доуэля|Александр Беляев|Научная фантастика |
|Голова профессора Доуэля|Александр Беляев|Художественная литература|
|Капитанская дочка |Александр Пушин |Художественная литература|
|Человек-амфибия |Александр Беляев|Научная фантастика |
|Человек-амфибия |Александр Беляев|Художественная литература|
```

Когда мы группируем эту таблицу по колонке `book_name` и просто собираем строки `author` и `category` в json, то в json появляются дубликаты. Чтобы убрать их — просто используем `distinct`. В этом его задача.