from django.http import HttpResponse
import json


def event(request):
    if request.GET.get('challenge'):
        return HttpResponse(
            json.dumps({'challenge': request.GET.get('challenge')}),
            content_type='application/json'
        )
    print(request.GET)
