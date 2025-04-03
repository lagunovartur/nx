# cli
## help по cli
```shell
nx -h
```

## Инициализация
Устанавливает гит хук на пуш, выполняющий test, mypy, ruff проверки при коммите.

Делает глобально доступным cli проекта по имени nx.
```shell
sudo ./cli/run in
```

### Делает глобально доступным cli проекта по имени nx. Создает sim link на ./cli/run в /usr/local/bin
```shell
sudo ./cli/run in-link
```

### Устанавливает гит хук на пуш, выполняющий test, mypy, ruff, black проверки при коммите.
```shell
sudo nx in-hook
```

### Cнимает гит хук на пуш, выполняющий test, mypy, ruff, black проверки при коммите.
```shell
nx in-unhook
```

## docker compose
### nx dc ... - глобально доступный alias на докер композ проекта
### nx dc-attach <имя сервиса> подключение к контейнеру сервиса
### подключение к контейнеру базы
```shell
nx dc-attach db
```
### подключение к контейнеру api
```shell
nx dc-attach api
```

### Запуск проекта
```shell
nx dc up -d
```

### Стоп проекта
```shell
nx dc down
```

### Запуск базы
```shell
nx dc up -d db
```

### Стоп базы
```shell
nx dc up -d down
```

## git
### nx git - глобально доступный alias на git
### git статус
```shell
nx git status
```

## alembic
### nx al ... - глобально доступный alias на alembic
### История миграций:
```shell
nx al history
```
### al-rev <имя миграции> - создание миграции
### al-up <миграция | none> - апгрейд до head или до конкретной миграции или до n следующей миграции
```shell
nx al-up
```
#### al-down <миграция | none> - даунгрейд -1 или до конкретной миграции или до n предыдущей миграции
```shell
nx al-down
```

## Проверки chk
### Тесты
```shell
nx chk-test
```

### Mypy
```shell
nx chk-mypy
```
### Линтеры ruff
```shell
nx chk-style
```

## Форматирование
Форматирование ruff
```shell
nx fmt
```

## База
### Подключение к базе в контейнере по psql
```shell
nx db-shell
```
### Дамп базы project_root/db/dump
```shell
nx db-dump
```
### Восстановление базы до n дампа, по умолчанию до последнего -1
```shell
nx db-restore
```
### Сброс тестовой базы, удаляет public схему, создает ее заново, применяет миграции
```shell
nx db-reset_test
```

# Сервисы
## api swagger
https://localhost:42401/swagger
