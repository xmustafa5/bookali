from ninja.security import HttpBearer
from jose import jwt, JWTError
from config import settings


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            user_email = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms='HS256')
        except JWTError:
            return None
        if user_email:
            return {'email': str(user_email['email'])}


def create_token_for_user(user):
    token = jwt.encode({'email': str(user.email)}, key=settings.SECRET_KEY, algorithm='HS256')
    return {
        'access': str(token)
    }

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXJhYUBleGFtcGxlLmNvbSJ9.dgd8H48QJOOXdbbp6M_vAgmfpx59lADRvyM4ThycqYc
