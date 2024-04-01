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

class MaterialForm(forms.Form):
    density = forms.FloatField()            
    youngs_modulus = forms.FloatField() 
    poissons_ratio = forms.FloatField() 
    thickness = forms.FloatField() 
    longitudinal_wave_velocity = forms.FloatField()
    shear_wave_velocity = forms.FloatField()
    rayleigh_wave_velocity = forms.FloatField(required=False)
    name = forms.CharField(max_length=50, required=False)

class WaveForm(forms.Form):
    wavetype = forms.ChoiceField(choices=WAVETYPE_CHOICES)
    modes_nums = forms.CharField(max_length=50)
    freq_thickness_max = forms.IntegerField()
    freq_thickness_points = forms.IntegerField()
    cp_step = forms.IntegerField()
    cp_max = forms.IntegerField()
    structure_mode = forms.CharField(max_length=3, min_length=3)
    structure_frequencies = forms.CharField(max_length=50)
    structure_rows = forms.IntegerField()  
    structure_columns = forms.IntegerField() 

class PlotForm(forms.Form):
    plotted_modes = forms.ChoiceField(choices=MODETYPE_CHOICES)	
    plots_chosen = forms.MultipleChoiceField(choices=PLOTTYPE_CHOICES)
    cutoff_frequencies = forms.BooleanField()
    show_velocities = forms.BooleanField()
    symmetric_style = forms.CharField(max_length=150, required=False)
    antisymmetric_style = forms.CharField(max_length=150, required=False)
    dashed_line_style = forms.CharField(max_length=150, required=False)
    continuous_line_style = forms.CharField(max_length=150, required=False)
    in_plane_style = forms.CharField(max_length=150, required=False)
    out_of_plane_style = forms.CharField(max_length=150, required=False)
    velocity_style = forms.CharField(max_length=150, required=False)
    padding_factor = forms.CharField(max_length=150, required=False)

def get_input_from_form(form):
    # load Material data from input
    density = form[0].cleaned_data["density"]
    youngs_modulus = form[0].cleaned_data["youngs_modulus"]
    poissons_ratio  = form[0].cleaned_data["poissons_ratio"]
    thickness = form[0].cleaned_data["thickness"]
    velocities = (form[0].cleaned_data["longitudinal_wave_velocity"], form[0].cleaned_data["shear_wave_velocity"], form[0].cleaned_data["rayleigh_wave_velocity"])
    name = form[0].cleaned_data["name"]
    material = Material(density, youngs_modulus, poissons_ratio, thickness, velocities, name)

    # load Wave data from input
    wavetype = dict(WAVETYPE_CHOICES).get(form[1].cleaned_data["wavetype"])
    cp_freq_params = (form[1].cleaned_data["modes_nums"], form[1].cleaned_data["freq_thickness_max"], \
                     form[1].cleaned_data["freq_thickness_points"], form[1].cleaned_data["cp_step"], form[1].cleaned_data["cp_max"])
    structure_mode  = form[1].cleaned_data["increasing_mode"]
    structure_frequencies  = eval(form[1].cleaned_data["structure_frequencies"])
    structure_rows = form[1].cleaned_data["structure_rows"]
    structure_columns = form[1].cleaned_data["structure_columns"]
    if wavetype == "Lamb":
        wave = Lambwave(material, cp_freq_params, structure_mode, structure_frequencies, structure_rows, structure_columns)
    else: 
        wave = Shearwave(material, cp_freq_params, structure_mode, structure_frequencies, structure_rows, structure_columns)

    # load Plot data from input
    plotted_modes = dict(MODETYPE_CHOICES).get(form.cleaned_data["plotted_modes"])
    plots_chosen = form[2].cleaned_data["plots_chosen"]
    kwargs = (form[2].cleaned_data["cutoff_frequencies"], form[2].cleaned_data["show_velocities"], form[2].cleaned_data["symmetric_style"], \
              form[2].cleaned_data["antisymmetric_style"], form[2].cleaned_data["dashed_line_style"], form[2].cleaned_data["continuous_line_style"], \
              form[2].cleaned_data["in_plane_style"], form[2].cleaned_data["out_of_plane_style"], form[2].cleaned_data["velocity_style"], \
              form[2].cleaned_data["padding_factor"])
    plotter = Plot(wave, plotted_modes, kwargs)
    for choice in plots_chosen:
        plot = dict(PLOTTYPE_CHOICES).get(choice)
        plotter.add_plot(plot)
    # Return created objects
    return plotter
