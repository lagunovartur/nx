from fastapi import Request, Response


class DiProxy:

    def __call__(self, request: Request, response: Response) -> None:
        request.state.response = response

