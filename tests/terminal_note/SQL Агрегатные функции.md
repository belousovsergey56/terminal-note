---
Дата создания: 2025-04-14
ссылки:
  - "[[SQL]]"
  - "[[Ссылки/t0digital|t0digital]]"
  - "[[postgresql]]"
tags:
  - "#функции"
  - postgres
---
В PostgreSQL существует множество встроенных агрегатных функций, которые можно разделить на несколько категорий. Вот полный список основных агрегатных функций с пояснениями и примерами:

---

### **1. Основные агрегатные функции**
- **`COUNT(*)`** / **`COUNT(column)`**  
  Подсчитывает количество строк или ненулеых значений в колонке.  
  Пример: `SELECT COUNT(*) FROM table;`

- **`SUM(column)`**  
  Сумма значений в колонке.  
  Пример: `SELECT SUM(salary) FROM employees;`

- **`AVG(column)`**  
  Среднее арифметическое значений.  
  Пример: `SELECT AVG(age) FROM users;`

- **`MIN(column)`**  
  Минимальное значение.  
  Пример: `SELECT MIN(price) FROM products;`

- **`MAX(column)`**  
  Максимальное значение.  
  Пример: `SELECT MAX(temperature) FROM weather_data;`

---

### **2. Статистические функции**
- **`STDDEV(column)`**  
  Стандартное отклонение выборки.
- **`STDDEV_POP(column)`**  
  Стандартное отклонение генеральной совокупности.
- **`VAR_SAMP(column)`** / **`VARIANCE(column)`**  
  Дисперсия выборки.
- **`VAR_POP(column)`**  
  Дисперсия генеральной совокупности.
- **`CORR(Y, X)`**  
  Коэффициент корреляции Пирсона.
- **`COVAR_SAMP(Y, X)`** / **`COVAR_POP(Y, X)`**  
  Ковариация выборки/генеральной совокупности.

---

### **3. Строковые агрегаты**
- **`STRING_AGG(column, separator)`**  
  Объединяет строки через разделитель.  
  Пример: `SELECT STRING_AGG(name, ', ') FROM students;`

- **`ARRAY_AGG(column)`**  
  Объединяет значения в массив.  
  Пример: `SELECT ARRAY_AGG(email) FROM users;`

---

### **4. Бинарные/битовые функции**
- **`BIT_AND(column)`**  
  Побитовое И для всех значений.
- **`BIT_OR(column)`**  
  Побитовое ИЛИ для всех значений.

---

### **5. Булевы агрегаты**
- **`BOOL_AND(condition)`**  
  Возвращает `TRUE`, если все значения истинны.  
  Пример: `SELECT BOOL_AND(is_active) FROM accounts;`

- **`BOOL_OR(condition)`**  
  Возвращает `TRUE`, если хотя бы одно значение истинно.

---

### **6. JSON/XML агрегаты**
- **`JSON_AGG(column)`**  
  Собирает значения в JSON-массив.  
  Пример: `SELECT JSON_AGG(product) FROM orders;`

- **`JSON_OBJECT_AGG(key, value)`**  
  Создает JSON-объект из пар ключ-значение.
- **`XML_AGG(column)`**  
  Аналогично для XML.

---

### **7. Временные агрегаты**
- **`MIN(time_column)`** / **`MAX(time_column)`**  
  Минимальная/максимальная дата или время.

---

### **8. Специальные агрегаты**
- **`MODE() WITHIN GROUP (ORDER BY column)`**  
  Возвращает наиболее часто встречающееся значение (моду).  
  Пример: `SELECT MODE() WITHIN GROUP (ORDER BY age) FROM users;`

- **`PERCENTILE_CONT(fraction) WITHIN GROUP (ORDER BY column)`**  
  Вычисляет непрерывный процентиль (например, медиану).  
  Пример: `SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) FROM employees;`

- **`PERCENTILE_DISC(fraction) WITHIN GROUP (ORDER BY column)`**  
  Дискретный процентиль.

---

### **9. Агрегаты для массивов**
- **`ARRAY_AGG(column)`**  
  Собирает элементы в массив (см. выше).

---

### **10. Гистограммы**
- **`HISTOGRAM(column, min, max, nbuckets)`** (требует расширения, например, `tablefunc`)  
  Строит гистограмму значений.

---

### **Примечания**
1. **Пользовательские агрегаты**  
   PostgreSQL позволяет создавать собственные агрегатные функции с помощью `CREATE AGGREGATE`.

2. **Условия для агрегатов**  
   Можно комбинировать с `FILTER (WHERE condition)` для выборочного агрегирования:  
   Пример: `SELECT COUNT(*) FILTER (WHERE age > 30) FROM users;`

3. **Группировка**  
   Агрегаты часто используются с `GROUP BY` для групповой обработки данных.

4. **Расширения**  
   Некоторые функции доступны только при подключении расширений (например, `postgis`, `hstore`).

---

Это основные встроенные агрегатные функции. Для более специализированных задач рекомендуется обращаться к [официальной документации](https://www.postgresql.org/docs/current/functions-aggregate.html).

Самая часто встречающаяся агрегатная функция — `count`. С её помощью мы можем посчитать, сколько строк в наборе данных.

```sql
select * from book; -- видим 9 записей
select count(*) from book; -- 9
```

Когда мы вызываем функцию `count` с аргументом звездочка, то просим посчитать, сколько всего строк в наборе данных. Когда мы вместо звездочки указываем имя колонки, то просим посчитать, сколько в колонке значений, отличных от `NULL`:

```sql
select count(cover) from book; -- 3
```

Ещё есть агрегатные функции, которые считают сумму чисел:

```sql
select sum(some_int) from (
    select unnest(array[10, 20, 30]) some_int
);
```

Здесь я использую массив и функцию `unnest`, чтобы создать виртуальную таблицу с тремя строками со значениями строк 10, 20 и 30:

```sql
select unnest(array[10, 20, 30]) some_int;
```

На практике, конечно, у нас будет какая-то таблица, по которой мы суммируем данные. Или результаты объединения каких-то таблиц. Или подзапрос, о которых мы поговорим позже.

Аналогично можно считать среднее, минимальное и максимальное значение в наборе данных:

```sql
select avg(some_int) from (
    select unnest(array[10, 20, 30]) some_int
);

select min(some_int) from (
    select unnest(array[10, 20, 30]) some_int
);

select max(some_int) from (
    select unnest(array[10, 20, 30]) some_int
);
```

И ещё несколько более сложных агрегатных функций, которые могут агрегировать данные в массивы, в json или jsonb или в строку:

```sql
select array_agg(some_int) from (
    select unnest(array[10, 20, 30]) some_int
);

|array_agg |
|----------|
|{10,20,30}|


select string_agg(some_int::varchar, ', ') from (
    select unnest(array[10, 20, 30]) some_int
);

|string_agg|
|----------|
|10, 20, 30|

select string_agg(some_int, '; ') from (
    select unnest(array['Alex', 'Petr', 'Ivan']) some_int
);

|string_agg      |
|----------------|
|Alex; Petr; Ivan|

select json_agg(some_int) from (
    select unnest(array['Alex', 'Petr', 'Ivan']) some_int
);

select jsonb_agg(some_int) from (
    select unnest(array['Alex', 'Petr', 'Ivan']) some_int
);

select json_agg(t.*) from (
    select unnest(array['Alex', 'Petr', 'Ivan']) some_int
) t;

|json_agg||---------------------------------------------------------------------------------|
|"[{\"some_int\":\"Alex\"}, 
 {\"some_int\":\"Petr\"}, 
 {\"some_int\":\"Ivan\"}]"|
```