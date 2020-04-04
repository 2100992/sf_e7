# sf_e7

Учебный проект SkillFactory.

Запущен тут - http://94.103.94.xxx/

Для того, что бы развернуть проект, нужно выполнить следующее:

-установить docker и docker compose

-git clone https://github.com/2100992/sf_e7.git

-cd sf_e7

-docker-compose build

-docker-compose up -d


### Описание

1.
Отображение всех объявлений: `/posts/`

JSON со списком всех объявлений со статистикой и тегами: `/api/posts/`

        Можно сделать некоторую фильтрацию по объявлениям. Например:
        - /posts/?slug=car_sale
        - /api/posts/?slug=car_sale


2.
Отображение детальной информации по объявлению. Вместе с комментариями и тегами: `/posts/<_id>/`

Аналогичный JSON: `/api/posts/<_id>/`



### Задание:

    - добавление объявления (возможно с тегами и комментариями) с помощью POST запроса к серверу;
    - получение существующего объявления (с тегами и комментариями) по ID с помощью GET запроса к серверу;
    - добавление тега к существующему объявлению с помощью POST запроса к серверу;
    - добавление комментария к существующему объявлению с помощью POST запроса к серверу;
    - статистика для данного объявления: сколько у него тегов и комментариев с помощью GET запроса к серверу.
