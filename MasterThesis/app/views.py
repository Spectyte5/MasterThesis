"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .forms import WaveDispersionForm, get_input_from_form

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def app(request):
    assert isinstance(request, HttpRequest)
    request.session.pop('plots', None)
    if request.method == "POST":
        form = WaveDispersionForm(request.POST)
        if form.is_valid():
            plotter = get_input_from_form(form)
            plots = plotter.get_plots_as_data()
            # parse data
            return render(
                request,
                'app/result.html',
                    {   
                        'title':'Result',
                        'message':'Your result page.',
                        'year':datetime.now().year,
                        'plots': plots,
                    }
            )
    else:
        form = WaveDispersionForm()
    return render(
        request,
        'app/app.html',
        {   
            'title':'App',
            'message':'Your application page.',
            'year':datetime.now().year,
            'form':form,
        }
    )