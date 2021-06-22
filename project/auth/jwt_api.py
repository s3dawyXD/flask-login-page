from jose import jwt
import datetime


class AuthError(Exception):
    """for formating error messages"""

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


class JWT_API:
    """
    JWT module 

    for generating Json Web Token (jwt) and validate them 
    """

    def __init__(self):
        self.key = "secret"
        self.algorithm = "HS256"
        self.iss_domain = "my_domain.com"

    def verify_decode_jwt(self, token: str) -> dict:
        """
        it validate all the claims in the token

        @params: jwt String 
        returns: payload: dictionary with all the data in jwt
        """
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                self.key,
                algorithms=self.algorithm,
                issuer='https://' + self.iss_domain + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    def create_jwt(self, data:dict={})->str:
        """
        Create jwt with data

        this jwt is easy to decode so DO NOT put sensitive inforation within
        all data in jwt should be encrypted

        @params: data: dictionary of the data we need to attach with the jwt
        returns: jwt token :str 
        """
        payload = {'iss': 'https://' +
                   self.iss_domain + '/', 'iat': self.get_iat(), 'exp': self.get_exp(), 'data': data}
        jwt_token = jwt.encode(payload, self.key, algorithm=self.algorithm)
        return jwt_token

    def get_exp(self):
        """ returns expiry data for the jwt """
        return datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)

    def get_iat(self):
        """get the issue date for jwt """
        return datetime.datetime.now(datetime.timezone.utc)

    def check_jwt_exp(self, token):
        """check if jwt is expired"""
        try:
            payload = jwt.decode(token, 'wrong key', options={
                                 "verify_signature": False})
            now = datetime.datetime.now(datetime.timezone.utc)
            now = datetime.datetime.timestamp(now)
            try:
                exp = payload['exp']
                if exp > now:
                    return False
                else:
                    return True
            except Exception:
                return True
        except jwt.ExpiredSignatureError:
            return True
        except Exception:
            return True

    def refresh_token(self, token):
        
        return self.create_jwt(self.get_token_data(token))

    def get_token_data(self, token):
        try:
            payload = jwt.decode(token, self.key, options={
                                 "verify_exp": False})
            return payload['data']

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
