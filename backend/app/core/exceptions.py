from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    """リソースが見つからない"""
    def __init__(self, detail: str = "リソースが見つかりません"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ForbiddenException(HTTPException):
    """権限エラー"""
    def __init__(self, detail: str = "この操作を実行する権限がありません"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class UnauthorizedException(HTTPException):
    """認証エラー"""
    def __init__(self, detail: str = "認証が必要です"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ValidationException(HTTPException):
    """バリデーションエラー"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )