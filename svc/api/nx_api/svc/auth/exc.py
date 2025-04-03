from fr_lib.exc.http import ExcHttp


class ExcNotAuth(ExcHttp):
    message = "Пользователь не авторизован"
    status_code = 401


class ExcAlreadyAuth(ExcHttp):
    message = "Пользователь уже авторизован"
    status_code = 409


class ExcInvalidCreds(ExcHttp):
    message = "Введены неверные учетные данные"
    status_code = 401


class ExcRefreshTokenNotSent(ExcHttp):
    message = "Токен обновления не передан"
    status_code = 401


class ExcAccessTokenNotSent(ExcHttp):
    message = "Токен доступа не передан"
    status_code = 401
