from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def event(request):
    challenge = request.POST.get('challenge').get('challenge')
    print(request.POST)
    print(challenge)
    if challenge:
        return HttpResponse(
            json.dumps({'challenge': challenge}),
            content_type='application/json',
        )
    return HttpResponse(challenge)
