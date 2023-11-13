# PiterPy 2023: Python + Keycloak: доверь аутентификацию профессионалам

## Поддержка 3 вариантов аутентификации с помощью Keycloak

1. Сессионная
2. Токенная: stateless
3. Токенная: stateful

см. `kc.settings.kc_type`


## Примеры апдейта и создания пользователей

см. `kc.authentication`


## Настройки

Добавить `127.0.0.1 keycloak` в `/etc/hosts `


## Запуск

`docker compose up`

_Docker Compose version v2.20.2_

## Доступ

__Keycloak:__ http://keycloak:8080

__Django:__ http://localhost:8000

