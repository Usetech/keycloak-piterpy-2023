from django.conf import settings

from rest_framework_simplejwt.authentication import JWTAuthentication as _JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.utils.module_loading import import_string
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class JWTAuthentication(_JWTAuthentication):

    def get_user(self, validated_token):
        try:
            user_id = validated_token[settings.USER_ID_CLAIM]
            user = self.user_model.objects.get_or_create(**{settings.USER_ID_FIELD: user_id})
            # <UPDATE ПОЛЬЗОВАТЕЛЯ ПИСАТЬ ТУТ>
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed(_("User not found"), code="user_not_found")

        return user


class OIDCAuthenticationBackendUUID(OIDCAuthenticationBackend):
    def get_username(self, claims):
        """Использовать в качестве username UUID пользователя из Keycloak

        Если изменить email в keycloak, то при входе в Django будет создан новый
        пользователь. Однозначно мэтчим пользователя по UUID, чтобы избежать этого поведения
        """
        username_algo = self.get_settings("OIDC_USERNAME_ALGO", None)

        if username_algo:
            if isinstance(username_algo, str):
                username_algo = import_string(username_algo)
            return username_algo(claims.get("email"))

        # UUID instead of email
        return claims.get("sub")

    def update_user(self, user, claims):
        # TODO: см. в сторону keycloak spi event listener и http вебхуков
        changed = False
        claims_checklist = [("email", "email")]
        for claim_field, user_field in claims_checklist:
            if not getattr(user, user_field) != claims.get(claim_field):
                continue

            setattr(user, user_field, claims.get(claim_field))
            changed = True

        if changed:
            user.save()
            user.refresh_from_db()

        return user

    def filter_users_by_claims(self, claims):
        """Использование UUID пользователя вместо Email в качестве username"""
        login = claims.get("sub")
        if not login:
            return self.UserModel.objects.none()
        return self.UserModel.objects.filter(username=login)
