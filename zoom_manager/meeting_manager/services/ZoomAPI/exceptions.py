class AccessTokenIsExpired(Exception):
    """Error that occurs when we request data from ZoomAPI
    with expired token"""

    def __init__(self):
        print(f"*ERROR* Expired token was use!!!")


class InvalidApiKeyOrSecret(Exception):
    """Error that occurs when invalid api key or secret"""

    def __init__(self):
        print(f"*ERROR* Invalid api key or secret!!!")


class InvalidTokenError(Exception):
    """Error that occurs when we request data from ZoomAPI
    with Invalid Token"""
    
    def __init__(self):
        print(f"*ERROR* Invailid token was use!!!")


class InvalidRefreshTokenError(Exception):
    """Error that occurs when we request data from ZoomAPI
    with Invalid Refresh Token"""
    
    def __init__(self):
        print(f"*ERROR* Invailid refresh_token was use!!!\n*INFO*Check your refresh_token for OAuth 2.0")