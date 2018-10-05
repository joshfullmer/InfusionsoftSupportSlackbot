from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


# csrf_exempt
def event(request):
    if request.POST.get('challenge'):
        return HttpResponse(
            json.dumps({'challenge': request.POST.get('challenge')}),
            content_type='application/json'
        )
    return HttpResponse(request.POST.get('challenge'))
