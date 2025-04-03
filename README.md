# cli
## help по cli
```shell
mg -h
```

## Инициализация
Устанавливает гит хук на пуш, выполняющий test, mypy, ruff проверки при коммите.

Делает глобально доступным cli проекта по имени mg.
```shell
sudo ./cli/run in
```

### Делает глобально доступным cli проекта по имени mg. Создает sim link на ./cli/run в /usr/local/bin
```shell
sudo ./cli/run in-link
```

### Устанавливает гит хук на пуш, выполняющий test, mypy, ruff, black проверки при коммите.
```shell
sudo mg in-hook
```

### Cнимает гит хук на пуш, выполняющий test, mypy, ruff, black проверки при коммите.
```shell
mg in-unhook
```

## docker compose
### mg dc ... - глобально доступный alias на докер композ проекта
### mg dc-attach <имя сервиса> подключение к контейнеру сервиса
### подключение к контейнеру базы
```shell
mg dc-attach db
```
### подключение к контейнеру api
```shell
mg dc-attach api
```

### Запуск проекта
```shell
mg dc up -d
```

### Стоп проекта
```shell
mg dc down
```

### Запуск базы
```shell
mg dc up -d db
```

### Стоп базы
```shell
mg dc up -d down
```

## git
### mg git - глобально доступный alias на git
### git статус
```shell
mg git status
```

## alembic
### mg al ... - глобально доступный alias на alembic
### История миграций:
```shell
mg al history
```
### al-rev <имя миграции> - создание миграции
### al-up <миграция | none> - апгрейд до head или до конкретной миграции или до n следующей миграции
```shell
mg al-up
```
#### al-down <миграция | none> - даунгрейд -1 или до конкретной миграции или до n предыдущей миграции
```shell
mg al-down
```

## Проверки chk
### Тесты
```shell
mg chk-test
```

### Mypy
```shell
mg chk-mypy
```
### Линтеры ruff
```shell
mg chk-style
```

## Форматирование
Форматирование ruff
```shell
mg fmt
```

## База
### Подключение к базе в контейнере по psql
```shell
mg db-shell
```
### Дамп базы project_root/db/dump
```shell
mg db-dump
```
### Восстановление базы до n дампа, по умолчанию до последнего -1
```shell
mg db-restore
```
### Сброс тестовой базы, удаляет public схему, создает ее заново, применяет миграции
```shell
mg db-reset_test
```

# Сервисы
## api swagger
https://localhost:42401/swagger
