from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def event(request):
    print(request.POST.get('body'))
    challenge = request.POST.get('body').get('challenge')
    if challenge:
        return HttpResponse(
            json.dumps({'challenge': challenge}),
            content_type='application/json',
        )
    return HttpResponse(challenge)
