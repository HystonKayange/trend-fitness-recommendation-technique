from allauth.account.adapter import DefaultAccountAdapter


class MyAccountAdapter(DefaultAccountAdapter):

    def get_signup_redirect_url(self, request):
        path = "/account/profile/{username}/"
        return path.format(username=request.user.username)
