# Cервис по расчёту стоимости страхования в зависимости от типа груза и объявленной стоимости

## Задание

Тариф должен загружаться из файла JSON или должен принимать подобную JSON структуру:

```
{
        "2020-06-01": [
            {
                "cargo_type": "Glass",
                "rate": 0.04
            },
            {
                "cargo_type": "Other",
                "rate": 0.01
            }
        ],
        "2020-07-01": [
            {
                "cargo_type": "Glass",
                "rate": 0.035
            },
            {
                "cargo_type": "Other",
                "rate": 0.015
            }
        ]
    }
```

- Сервис должен посчитать стоимость страхования для запроса используя актуальный тариф.(Загружается через API)
- Сервис возвращает (объявленную стоимость * rate) в зависимости от указанного в запросе типа груза и даты.
- Сервис должен разворачиваться внутри Docker.
- Сервис должен разрабатываться через GIT (Файл Readme с подробным описанием развертывания)
- Данные должны храниться в базе данных

## Технологии, которые были использованы:
- FastApi - framework
- Tortoise ORM
- Postgresql (основная бд),  Sqlite (тестовая бд)
- Docker
- Docker-compose

## Запуск и установка
Перед запуском в корневой папке и папке backend необходимо создать .env файлы в корневой папке и папке backend, примеры находятся там же (env_example).

Для запуска приложения необходим docker-compose. 
Выполните следующие команды

```sh
docker-compose build
docker-compose up
```

Для тестирования используется PyTest
Запуск тестов:

```sh
pytest ./backend/tests/tests.py
```

## Реализованый функционал

- Авторизация (Админ создается при запуске, логин и пароль задаются в .env файле)
- Загрузка тарифов по датам в json
- Получение типов грузов с пагинацией
- Расчет стоимости страховки на определенную дату (для расчета актуальной стоимости не передовать параметр date)
