from django.http import HttpResponse
from ratelimit.decorators import ratelimit
from django.contrib.auth.decorators import login_required


@ratelimit(key='user_or_ip', rate='10/m', method='POST', block=True)
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def login_view(request):
    if getattr(request, 'limited', False):
        return HttpResponse("Rate limit exceeded", status=429)

    # login logic here
    return HttpResponse("Login successful")
