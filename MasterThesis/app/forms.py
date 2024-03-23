"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
# temporary
import sys
sys.path.append("../../WaveDispersion")
from Material import Material
from Plot import Plot
from Wave import Lambwave, Shearwave

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

WAVETYPE_CHOICES =( 
    ("1", "Lamb"), 
    ("2", "Shear"), 
)

MODETYPE_CHOICES =( 
    ("1", "both"), 
    ("2", "symmetric"), 
    ("3", "antisymmetric"), 
)

PLOTTYPE_CHOICES =( 
    ("1", "Phase"), 
    ("2", "Group"), 
    ("3", "Wavenumber"), 
    ("4", "Wavestructure"), 
)

class WaveDispersionForm(forms.Form):
    # Material
    density = forms.FloatField()            
    youngs_modulus  = forms.FloatField() 
    poissons_ratio  = forms.FloatField() 
    thickness  = forms.FloatField() 
    wavetype = forms.ChoiceField(choices = WAVETYPE_CHOICES)
    # Wave
    increasing_mode  = forms.CharField(max_length=3, min_length=3)
    structure_frequencies  = forms.CharField(max_length=50)
    structure_rows = forms.IntegerField()  
    structure_columns = forms.IntegerField() 
    # Plot
    plotted_modes = forms.ChoiceField(choices = MODETYPE_CHOICES)	
    plots_chosen = forms.MultipleChoiceField(choices = PLOTTYPE_CHOICES)


def get_input_from_form(form):

    # load Material data from input
    density = form.cleaned_data["density"]
    youngs_modulus = form.cleaned_data["youngs_modulus"]
    poissons_ratio  = form.cleaned_data["poissons_ratio"]
    thickness  = form.cleaned_data["thickness"]
    material = Material(density, youngs_modulus, poissons_ratio, thickness)

    # load Wave data from input
    wavetype = dict(WAVETYPE_CHOICES).get(form.cleaned_data["wavetype"])
    increasing_mode  = form.cleaned_data["increasing_mode"]
    structure_frequencies  = eval(form.cleaned_data["structure_frequencies"])
    structure_rows = form.cleaned_data["structure_rows"]
    structure_columns = form.cleaned_data["structure_columns"]
    if wavetype == "Lamb":
        wave = Lambwave(material, increasing_mode, structure_frequencies, structure_rows, structure_columns)
    else: 
        wave = Shearwave(material, increasing_mode, structure_frequencies, structure_rows, structure_columns)

    # load Plot data from input
    plotted_modes = dict(MODETYPE_CHOICES).get(form.cleaned_data["plotted_modes"])
    plots_chosen = form.cleaned_data["plots_chosen"]
    plotter = Plot(wave, plotted_modes)
    for choice in plots_chosen:
        plot = dict(PLOTTYPE_CHOICES).get(choice)
        plotter.add_plot(plot)
    # Return created objects
    return plotter
