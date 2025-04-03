from nx_api.errors.http import ExcHttp


class ExcAccessTokenExpired(ExcHttp):
    status_code = 403
    message = "Токен доступа устарел"


class ExcRefreshTokenExpired(ExcHttp):
    status_code = 401
    message = "Токен обновления устарел"
