from django import http
from django.contrib.auth import login, logout, get_user_model


class SSOLoginMiddleware(object):

    def process_request(self, request):
        User = get_user_model()

        if request.path.startswith('/logout') and "HTTP_X_LOGOUT_URL" in request.META and request.META["HTTP_X_LOGOUT_URL"]:
            logout(request)
            return http.HttpResponseRedirect(request.META["HTTP_X_LOGOUT_URL"])

        if not request.user.is_authenticated() and "HTTP_REMOTE_USER" in request.META:
            attributemap = {
                "username": "HTTP_REMOTE_USER",
                "last_name": "HTTP_X_LAST_NAME",
                "first_name": "HTTP_X_FIRST_NAME",
                "email": "HTTP_X_EMAIL",
            }

            for key, value in attributemap.items():
                attributemap[key] = request.META[value]

            if attributemap["email"] and User.objects.filter(email__iexact=attributemap["email"]).exists():
                user = User.objects.filter(email__iexact=attributemap["email"])[0]
            elif (User.__name__ != "EmailUser") and User.objects.filter(username__iexact=attributemap["username"]).exists():
                user = User.objects.filter(username__iexact=attributemap["username"])[0]
            else:
                user = User()

            user.__dict__.update(attributemap)
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
