"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .forms import MaterialForm, WaveForm, PlotForm, get_input_from_form

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
            'title':'Contact Information',
            'message':'If any questions arise, the author can be contacted via AGH email.',
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
        return process_form(request)
    else:
        request.session.pop('plots', None)  # Clear session data on GET request
        return show_form(request)

def process_form(request):
    material_form = MaterialForm(request.POST, prefix='material')
    wave_form = WaveForm(request.POST, prefix='wave')
    plot_form = PlotForm(request.POST, prefix='plot')
    if material_form.is_valid() and wave_form.is_valid() and plot_form.is_valid():
        plotter = get_input_from_form([material_form, wave_form, plot_form])
        plots = plotter.get_plots_as_data()
        # Clear previous plots before adding new ones
        request.session.pop('plots', None)
        request.session['plots'] = plots
        # parse data
        return render(
            request,
            'app/result.html',
            {
                'title': 'Result',
                'message': 'Your result page.',
                'year': datetime.now().year,
                'plots': plots,
            }
        )
    else:
        return show_form(request, material_form, wave_form, plot_form)

def show_form(request, material_form=None, wave_form=None, plot_form=None):
    if material_form is None or wave_form is None or plot_form is None:
        material_form = MaterialForm(request.POST, prefix='material')
        wave_form = WaveForm(request.POST, prefix='wave')
        plot_form = PlotForm(request.POST, prefix='plot')
    return render(
        request,
        'app/app.html',
        {
            'title': 'App',
            'message': 'Your application page.',
            'year': datetime.now().year,
            'material_form': material_form, 'wave_form': wave_form, 'plot_form': plot_form,
            'plots': request.session.get('plots', None),  # Retrieve plots from session
        }
    )