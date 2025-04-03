from nx_api.exc import ExcHttp


class ExcInvalidToken(ExcHttp):
    status_code = 400
    message = "Неверный url токен"


class ExcTokenExpired(ExcHttp):
    status_code = 400
    message = "Токен устарел"


class ExcTokenAlreadyUsed(ExcHttp):
    status_code = 400
    message = "Токен уже использован"
