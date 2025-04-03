from nx_api.exc import ExcHttp


class ExcAccessTokenExpired(ExcHttp):
    status_code = 403
    message = "Токен доступа устарел"


class ExcRefreshTokenExpired(ExcHttp):
    status_code = 401
    message = "Токен обновления устарел"
