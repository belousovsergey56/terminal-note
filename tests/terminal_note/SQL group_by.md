---
Дата создания: 2025-04-26
ссылки:
  - "[[t0digital]]"
  - "[[SQL]]"
  - "[[postgresql]]"
tags:
  - group_by
  - psql
  - postgres
---
Для группировки используется оператор `GROUP BY`, он группирует строки, имеющие одинаковые значения в указанных столбцах, и позволяет выполнять агрегатные функции для каждой из групп.

Например, что если нам нужно найти не общее количество книг в таблице книг, а количество книг в каждой категории? Как мы это можем сделать?

Для начала давайте получим сводную таблицу, в которой есть имя идентификатор и название категории, а также идентификатор и название книги.

Я начну писать запрос с категорий, потому что нам категории ведь нужны в первую очередь.



```sql
select bc.category_id, bc.name
from book_category bc;
```

Добавим идентификатор книги к каждой категории:



```sql
select bc.category_id, bc.name as category_name, b.book_id, b.name as book_name
from book_category bc
left join book_to_category btc using(category_id)
left join book b using(book_id);

-- 13 rows
```

Мы видим здесь большее количество строк, потому что некоторые книги входят в несколько категорий. И для таких строк у нас колонки с данными книги повторяются, а колонки с данными категории разнятся.

Обратите внимание, что мы используем здесь `left join` вместо `inner join`. Потому что есть категории без книг. Если мы используем `join`, то мы в результатах потеряем такие категории, а мы этого не хотим!

Напомню, мы хотим посчитать количество книг в каждой категории. Значит, нам надо сгруппировать полученные результаты по категории и в каждой группе посчитать количество строк. Группировка происходит с помощью `group by`, а подсчет количества строк в группе с помощью агрегатной функции `count`, которую мы уже знаем.



```sql
select bc.category_id, bc.name as category_name, count(b.book_id) as books_count
from book_category bc
left join book_to_category btc using(category_id)
left join book b using(book_id)
group by bc.category_id, bc.name
order by books_count desc;

|category_id|category_name                 |books_count|
|-----------|------------------------------|-----------|
|1          |Художественая литература      |8          |
|3          |Научная фантастика            |4          |
|2          |Литература по программированию|1          |
|4          |Литература по фотографии      |0          |
```

Что здесь важно. В `group by` указываются те колонки, по которым мы группируем. Можно указать имена колонок или их порядковые номера в выборе:



```sql
select bc.category_id, bc.name as category_name, count(b.book_id) as books_count
from book_category bc
left join book_to_category btc using(category_id)
left join book b using(book_id)
group by 1, 2
order by books_count desc;

|category_id|category_name                 |books_count|
|-----------|------------------------------|-----------|
|1          |Художественая литература      |8          |
|3          |Научная фантастика            |4          |
|2          |Литература по программированию|1          |
|4          |Литература по фотографии      |0          |
```

В `select`-части запроса мы указываем те поля, которые нам необходимо достать в результирующую таблицу. И в случае использования группировок — и это очень важно! — мы можем указывать в этой части только те поля, которые входят в группировку, а также агрегатные функции, и всё. Потому что если мы добавим туда поля, по которым не выполняется группировка, то непонятно, какое именно значение брать из колонки:



```sql
select bc.category_id, bc.name as category_name, b.book_id
from book_category bc
left join book_to_category btc using(category_id)
left join book b using(book_id)
group by 1, 2;
-- SQL Error [42803]: ОШИБКА: столбец "b.book_id" должен фигурировать в предложении
-- GROUP BY или использоваться в агрегатной функции
```

PostgreSQL нам услужливо подсказывает, в чём дело. Действительно, давайте ещё раз внимательно посмотрим на таблицу, которую мы пытаемся сгруппировать:



```sql
select bc.category_id, bc.name as category_name, b.book_id, b.name as book_name
from book_category bc
left join book_to_category btc using(category_id)
left join book b using(book_id)
order by category_name;
```

Мы группируем по первым двум колонкам — идентификатор и название категории. То есть все строки, у которых первые две колонки одинаковые, попадают в 1 группу, то есть в одну строку в финальной выборке. И если мы в эту же финальную выборку просим добавить колонку `b.name`, то какое именно значение должно попасть в выборку? Вот в научной фантастике у нас 4 разные книги. Название какой книги должно попасть в единственную строку по научной фантастике? Непонятно. Вот и постгресу непонятно.

Поэтому он просит либо убрать эту колонку из выдачи, либо взять от неё любую доступную для неё агрегатную функцию. Как мы помним, агрегатная функция переводит набор данных в одно значение. И тогда не будет возникать вопрос — какое значение вставить, потому что все 4 книги как-то упакуются в одно значение и это одно значение добавится отдельной колонкой к одной строке конкретной категории.

Мы здесь в качестве агрегатной функции выбираем `count(b.book_id)`, эта функция как раз вернёт количество заполненных значений в колонке `b.book_id` в каждой группе.



```sql
select bc.category_id, bc.name as category_name, count(b.book_id) as books_count
from book_category bc
left join book_to_category btc using(category_id)
left join book b using(book_id)
group by 1, 2
order by books_count desc;

|category_id|category_name                 |books_count|
|-----------|------------------------------|-----------|
|1          |Художественая литература      |8          |
|3          |Научная фантастика            |4          |
|2          |Литература по программированию|1          |
|4          |Литература по фотографии      |0          |
```

Причём использовать `count(*)` здесь будет неправильно — потому что для каждой группы просто посчитается количество строк в ней, а это не то, что нам нужно. Скажем, у нас 0 книг по фотографии, а в такой выборке получится, что якобы у нас одна книга по фотографии есть. Потому что в выборке есть 1 строка в группе, в которой название категории «Литература по фотографии».



```sql
select bc.category_id, bc.name as category_name, count(*) as books_count
from book_category bc
left join book_to_category btc using(category_id)
left join book b using(book_id)
group by 1, 2
order by books_count desc;

|category_id|category_name                 |books_count|
|-----------|------------------------------|-----------|
|1          |Художественая литература      |8          |
|3          |Научная фантастика            |4          |
|4          |Литература по фотографии      |1          |
|2          |Литература по программированию|1          |
```

Собственно вот так работает группировка! Ничего больше. Повторюсь, что для колонок, которые не входят в `GROUP BY`, мы можем выполнять любую агрегатную функцию:


```sql
select bc.category_id, bc.name as category_name, json_agg(b.*) as books
from book_category bc
left join book_to_category btc using(category_id)
left join book b using(book_id)
group by 1, 2;

select bc.category_id, bc.name as category_name, string_agg(b.name, ', ') as books
from book_category bc
left join book_to_category btc using(category_id)
left join book b using(book_id)
group by 1, 2;
```
