from rest_framework_simplejwt.authentication import JWTAuthentication


class SimpleUser:
    def __init__(self, payload):
        self.payload = payload
        self.id = payload.get('id')
        self.role = payload.get('role')
        self.is_authenticated = True

    def get(self, key, default=None):
        return self.payload.get(key, default)

class CustomJWTAuthentication(JWTAuthentication):
    
    def get_user(self, validated_token):
        return SimpleUser(validated_token)

