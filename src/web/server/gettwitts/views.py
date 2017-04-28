from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import LoginField


def get_name(request):
    if request.method == 'POST':
        form = LoginField(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginField()

    return render(request, 'gettwitts/inputform.html', {'form': form})
