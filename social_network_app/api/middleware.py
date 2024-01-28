from social_network_app.models import UserProfile


class LastRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
            user_profile.update_last_request()
        return response