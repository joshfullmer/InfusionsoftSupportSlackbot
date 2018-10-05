from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def event(request):
    if request.GET.get('challenge'):
        return HttpResponse(
            json.dumps({'challenge': request.GET.get('challenge')}),
            content_type='application/json'
        )
    return HttpResponse(request.GET.get('challenge'))
