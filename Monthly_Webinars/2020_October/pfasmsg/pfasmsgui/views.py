from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.utils import timezone

# Create your views here.

from .models import PFASMsgRecord
from .forms import PFASMsgForm


def simple_test(request):
    """Simple function based view"""
    return HttpResponse("Too simple.")


class MessageBoard(View):
    """A class based view that handles multiple request types (GET and POST)"""

    def get(self, request):
        """Render template to return page content, what the user sees"""

        # get a selected subset of messages from DB
        msgs = PFASMsgRecord.objects.exclude(message__icontains='literally')
        # a blank form object for entering new data
        msg_form = PFASMsgForm()
        # context data for the template
        context = dict(messages=msgs, msg_form=msg_form)
        # process template and return result as response
        return render(request, "pfasmsgui/main.html", context=context)

    def post(self, request):
        """Add incoming data to the DB"""
        
        msg_form = PFASMsgForm(data=request.POST)
        if not msg_form.is_valid():
            pass
            # should really handle this
        # get a PFASMsgRecord from the form, but don't save to DB yet
        model_instance = msg_form.save(commit=False)
        model_instance.timestamp = timezone.now()
        model_instance.ip = request.META.get('REMOTE_ADDR')
        # could check for HTTP_X_FORWARDED_FOR header as well
        model_instance.save()  # now save it
        return redirect('main_page')
