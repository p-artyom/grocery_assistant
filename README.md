# Продуктовый помощник

- website: https://partyoms.sytes.net/; 
- login: yc-user@mail.ru; 
- password: yc-user123456789.

## Описание

Проект представляет из себя онлайн-сервис, на котором пользователи могут
публиковать рецепты, подписываться на публикации других пользователей,
добавлять понравившиеся рецепты в список "Избранное", а перед походом в
магазин скачивать сводный список продуктов, необходимых для приготовления
одного или нескольких выбранных блюд. Это полностью рабочий проект, который
состоит из бэкенд-приложения на _Django_ и фронтенд-приложения на _React_.
Проект готов к запуску в контейнерах и _CI/CD_ с помощью _GitHub Actions_.
В данном проекте мной был разработан бэкенд, тесты для моделей и эндпоинтов,
настроен _CI/CD_.

## Технологии

- Python 3.9;
- PostgreSQL 13;
- Django 3.2.3;
- Django REST framework 3.12.4;
- Gunicorn 20.1.0;
- Nginx 1.22.1;
- Node.js 13.12.0.

## Деплой проекта на удалённый сервер 

Инструкция написана для сервера с установленной _ОС Ubuntu 22.04.1 LTS_.

- Подключитесь к удалённому серверу;

- Установите _Docker Compose_ на сервер. Поочерёдно выполните на сервере
команды для установки _Docker_ и _Docker Compose_ для _Linux_. Выполнять их
лучше в домашней директории пользователя:

```text
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt-get install docker-compose-plugin
```

- Находясь на удалённом сервере, из любой директории выполните команду:

```text
sudo apt install nginx -y
```

- А потом запустите _Nginx_ командой:

```text
sudo systemctl start nginx
```

- На сервере в редакторе _nano_ откройте конфиг _Nginx_:
`sudo nano/etc/nginx/sites-enabled/default`. Измените настройки `location`
в секции `server`:

```text
location / {
    proxy_pass http://127.0.0.1:9000;
    client_max_body_size 20M;
}
```

- Для проверки файла конфигурации на ошибки выполните команду:

```text
sudo nginx -t
``` 

- Далее перезагрузите конфигурацию _Nginx_:

```text
sudo systemctl reload nginx
``` 

- Форкните и клонируйте к себе на компьютер
[репозиторий](https://github.com/p-artyom/foodgram-project-react);

- В корне проекта перейдите в директорию `.github/workflows` и в ней откройте 
файл `main.yml`;

- В строках `75, 98, 121` замените в поле `tags` значение `partyom` на свой
логин в _DockerHub_;

Для автоматического развёртывания контейнеров на удалённом сервере при помощи
_GitHub Actions_ необходимо создать _secrets_ в собственном репозитории.

- Перейдите в настройки репозитория — _Settings_, выберите на панели слева
_Secrets and Variables_ → _Actions_, нажмите _New repository secret_ и
создайте следующие переменные с необходимыми значениями:

  - в переменной `DOCKER_USERNAME` введите имя пользователя в _Docker Hub_;

  - в переменной `DOCKER_PASSWORD` введите пароль пользователя в _Docker Hub_;

  - в переменной `SSH_KEY` должно быть содержимое файла с закрытым _SSH_-ключом
  для доступа к серверу;

  - в переменной `SSH_PASSPHRASE` должно быть значение _passphrase_ для
  доступа к серверу;

  - в переменной `USER` должно быть ваше имя пользователя на сервере;

  - в переменной `HOST` должно быть значение _IP_-адреса вашего сервера;

  - в переменной `TELEGRAM_TO` сохраните _ID_ своего телеграм-аккаунта. Узнать
  свой _ID_ можно у телеграм-бота _@userinfobot_. Бот станет отправлять
  уведомления в аккаунт с указанным _ID_;

  - в переменной `TELEGRAM_TOKEN` сохраните токен вашего бота. Получить этот
  токен можно у телеграм-бота _@BotFather_.

- Сделайте коммит и запушьте изменения на _GitHub_;

- Пуш в ветку _main_ запускает тестирование и деплой _Foodgram_ на удалённый
сервер, а после успешного деплоя вам приходит сообщение в Телеграм.

Текущий _Workflow_ состоит из четырёх фаз:

- Тестирование проекта;

- Сборка и публикация образа;

- Автоматический деплой;

- Отправка уведомления в персональный чат.

## Запуск приложения локально в docker-контейнерах

Инструкция написана для компьютера с установленной _ОС Windows 10 или 11_.

- Установите _Windows Subsystem for Linux_ по инструкции с официального сайта
[Microsoft](https://learn.microsoft.com/ru-ru/windows/wsl/install);

- Зайдите на
[официальный сайт Docker](https://www.docker.com/products/docker-desktop/),
скачайте и установите файл Docker Desktop;

- Проверьте, что Docker работает:

```text
sudo systemctl status docker
``` 

- В терминале в папке с `docker-compose.yml` выполните команду:

```text
docker compose up
```

- Перейдите в новом терминале в директорию, где лежит файл
`docker-compose.yml`, и выполните команды:

```text
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py importcsv
docker compose exec backend python manage.py collectstatic
docker compose exec backend cp -r /app/collected_static/. /backend_static/static/
```

- Откройте в браузере страницу `http://localhost:9000/`;

- На странице `http://localhost:9000/api/docs/` можно ознакомиться с
документацией проекта.

## Автор

Пилипенко Артем
