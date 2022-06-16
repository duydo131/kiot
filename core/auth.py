from datetime import datetime

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header


class UserAuthentication(BaseAuthentication):
    keyword = "Bearer"

    TOKEN_ID = "id"
    NULL_TOKEN = "null"

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth:
            return (AnonymousUser(), None)
        elif len(auth) == 1:
            raise exceptions.AuthenticationFailed(
                _("Invalid token header. No credentials provided.")
            )
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed(_("Invalid token header"))
        elif auth[0].lower() != b"bearer":
            raise exceptions.AuthenticationFailed(_("Invalid token header"))

        try:
            token = auth[1]
            if token == self.NULL_TOKEN:
                return (AnonymousUser(), None)
        except UnicodeError:
            raise exceptions.AuthenticationFailed(
                _("Invalid token header. Token string should not contain invalid characters.")
            )
        try:
            return self.authenticate_credentials(token)
        except Exception:
            return

    def authenticate_credentials(self, token):
        UserModel = get_user_model()
        try:
            payload = jwt.decode(token, settings.OIDC_RP_IDP_SIGN_KEY, verify=False, algorithms=['RS256'])
            user_id = payload[self.TOKEN_ID]
            user = UserModel.objects.filter(id=user_id).first()
            if user and not user.avatar_url:
                user.avatar_url = payload.get("picture", None)
                if user.avatar_url:
                    user.save()
        except (jwt.ExpiredSignature, jwt.DecodeError, jwt.InvalidTokenError) as ex:
            raise exceptions.AuthenticationFailed(_(f"Token is invalid: {ex}"))
        except UserModel.DoesNotExist:
            raise exceptions.AuthenticationFailed(_("User does not exist"))
        except Exception as e:
            return None
        exp = datetime.fromtimestamp(payload["exp"])
        now = datetime.now().replace(microsecond=0)
        if now > exp:
            raise exceptions.AuthenticationFailed(_("Token is expired"))
        return user, token
