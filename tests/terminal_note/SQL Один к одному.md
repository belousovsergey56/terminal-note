---
Дата создания: 2025-04-14
ссылки:
  - "[[SQL]]"
  - "[[Ссылки/t0digital|t0digital]]"
  - "[[postgresql]]"
tags:
  - "#связи"
  - онтологии
  - "#1to1"
  - "#один_к_одному"
---
### Создание связи
```sql
create table book_detail(
    book_id bigint primary key references book(book_id),
    description text check (length(description) >= 30),
    isbn char(17),
    toc text,
    publisher varchar(255),
    publication_year smallint,
    publisher_series text,
    age_limit smallint
);
```

### Вставка данных
```sql
insert into book_detail (book_id, description, isbn) values(
    1,
    'Одно из наиболее значительных, масштабных и талантливых произведений русскоязычной литературы, принесшее автору Нобелевскую премию.',
    '978-5-389-16579-3'
);
```

### Выборка данных
```sql
select * from book b join book_detail bd using(book_id);
```