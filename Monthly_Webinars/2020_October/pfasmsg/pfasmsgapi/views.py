"""
views.py - API functions for Django demo.

Terry N. Brown Brown.TerryN@epa.gov 09/04/2020
"""
import json

from django.http import HttpResponse

from pfasmsgui.models import PFASMsgRecord

# Create your views here.


def msgs(request):
    """Return all PFASMsgRecord objects for GET request.

    Should check request type (GET, POST, etc.)

    Real APIs usually support GET / POST / PUT / DELETE methods, so a
    Django Class Based View would be better, but for just a naive GET
    response, we use a function.
    """
    results = list(PFASMsgRecord.objects.values())
    for result in results:
        # add a field that's not in the DB
        result['valid'] = 'literally' not in result['message'].lower()
        # change to text so JSON can save it
        result['timestamp'] = str(result['timestamp'])

    return HttpResponse(
        json.dumps(results, indent=2, sort_keys=True),
        content_type='application/json',
    )
