"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .forms import CreateNewList
from .graph import graph

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
    if request.method == "POST":
        form = CreateNewList(request.POST)
        if form.is_valid():
            # load data from input
            Num = form.cleaned_data["Numerator"]
            Den = form.cleaned_data["Denominator"]
            figure = graph()
            # parse data
            return render(
                request,
                'app/result.html',
                    {   
                        'title':'Result',
                        'message':'Your result page.',
                        'year':datetime.now().year,
                        'graph': figure.draw_figure(),
                        'num': Num,
                        'den': Den
                    }
            )
    else:
        form = CreateNewList()
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