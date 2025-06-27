---
Дата создания: 2025-04-26
ссылки:
  - "[[t0digital]]"
  - "[[SQL]]"
  - "[[postgresql]]"
tags:
  - filter
  - where
  - postgres
  - psql
---
В запросах с `GROUP BY` мы можем использовать фильтрацию с `WHERE` так же, как и обычно.

Например, если нас интересует только научная фантастика, мы можем отфильтровать все остальные записи, убрав их из выборки:



```sql
select bc.category_id, bc.name as category_name, count(b.book_id) as books_count
from book_category bc
left join book_to_category btc using(category_id)
left join book b using(book_id)
where bc.name = 'Научная фантастика'
group by 1, 2
order by books_count desc;

|category_id|category_name     |books_count|
|-----------|------------------|-----------|
|3          |Научная фантастика|4          |
```

А что если нам нужно использовать критерий фильтрации по агрегатной функции? Например, что, если нам нужны категории книг, в которых больше одной книги, как это можно сделать? Использовать это условие в `where` не получится:



```sql
select bc.category_id, bc.name as category_name, count(b.book_id) as books_count
from book_category bc
left join book_to_category btc using(category_id)
left join book b using(book_id)
where count(b.book_id) > 1
group by 1, 2
order by books_count desc;

-- SQL Error [42803]: ОШИБКА: агрегатные функции нельзя применять
-- в конструкции WHERE
```

Для фильтрации по агрегатной функции есть слово `HAVING`. Оно всегда идёт после `GROUP BY`.



```sql
select bc.category_id, bc.name as category_name, count(b.book_id) as books_count
from book_category bc
left join book_to_category btc using(category_id)
left join book b using(book_id)
group by 1, 2
having count(b.book_id) > 1
order by books_count desc;

|category_id|category_name           |books_count|
|-----------|------------------------|-----------|
|1          |Художественая литература|8          |
|3          |Научная фантастика      |4          |
```

Фильтрация с `WHERE` работает до группировки, а фильтрация с `HAVING` после группировки.

И есть ещё ключевое слово `FILTER`. Не все о нём знают, но штука очень удобная, наглядная и читаемая. `FILTER` позволяет выполнять агрегатные функции на поднаборе из группы. Звучит сложно, но на деле просто. Допустим, мы хотим понять, сколько в каждой книжной категории книг из разных веков, из 20 и 21.



```sql
select
    bc.name as category_name,
    count(*) as all_category_books,
    count(*) filter (where bd.publication_year between 1900 and 1999) as books_of_20_century,
    count(*) filter (where bd.publication_year > 2000) as books_of_21_century
from book_category bc
join book_to_category btc using(category_id)
join book_detail bd using(book_id)
group by bc.name;

|category_name                 |all_category_books|books_of_20_century|books_of_21_century|
|------------------------------|------------------|-------------------|-------------------|
|Художественая литература      |7                 |4                  |0                  |
|Литература по программированию|1                 |0                  |1                  |
|Научная фантастика            |3                 |2                  |0                  |
```

Здесь в колонке `all_category_books` возвращается общее количество книг в этой категории, в колонке `books_of_20_century` количество книг в этой категории, которые вышли в 20м веке, в колонке `books_of_21_century` количество книг в этой категории, которые вышли в 21м веке. А количество книг, вышедших в 18, 19 и других веках, мы тут отдельно не считаем. Круть вообще!