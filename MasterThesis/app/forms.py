"""
Definition of forms.
"""
import sys, os, shutil, ast
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
# temporary
sys.path.append("../../WaveDispersion")
# temporary
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
    density = forms.FloatField(initial=2700)            
    youngs_modulus = forms.FloatField(initial=68.9e9) 
    poissons_ratio = forms.FloatField(initial=0.33) 
    thickness = forms.FloatField(initial=1e-2) 
    longitudinal_wave_velocity = forms.FloatField(initial=6130)
    shear_wave_velocity = forms.FloatField(initial=3130)
    rayleigh_wave_velocity = forms.FloatField(initial=2881.6, required=False)
    name = forms.CharField(max_length=50, initial='Aluminum', required=False)

class WaveForm(forms.Form):
    wavetype = forms.ChoiceField(choices=WAVETYPE_CHOICES, initial=1)
    modes_number_sym = forms.IntegerField(initial=5)
    modes_number_anti = forms.IntegerField(initial=5)
    freq_thickness_max = forms.IntegerField(initial=10000)
    freq_thickness_points = forms.IntegerField(initial=100, required=False)
    cp_step = forms.IntegerField(initial=100, required=False)
    cp_max = forms.IntegerField(initial=12000)
    structure_mode = forms.CharField(initial='S_0', max_length=3, min_length=3, required=False)
    structure_frequencies = forms.CharField(initial=[500, 1000, 1500, 2000, 2500, 3000], max_length=50, required=False)
    structure_rows = forms.IntegerField(initial=3, required=False)  
    structure_columns = forms.IntegerField(initial=2, required=False) 

class PlotForm(forms.Form):
    plotted_modes = forms.ChoiceField(choices=MODETYPE_CHOICES, initial=1)	
    plots_chosen = forms.MultipleChoiceField(choices=PLOTTYPE_CHOICES, initial=1)
    cutoff_frequencies = forms.BooleanField(required=False)
    show_velocities = forms.BooleanField(required=False)
    symmetric_style = forms.CharField(max_length=150, required=False, initial="{'color': 'green', 'linestyle': '-'}")
    antisymmetric_style = forms.CharField(max_length=150, required=False, initial="{'color': 'purple', 'linestyle': '--'}")
    dashed_line_style = forms.CharField(max_length=150, required=False, initial="{'color': 'black', 'linestyle': '--', 'linewidth': 0.5}")
    continuous_line_style = forms.CharField(max_length=150, required=False, initial="{'color': 'black', 'linestyle': '-', 'linewidth': 0.75}")
    in_plane_style = forms.CharField(max_length=150, required=False, initial="{'color': 'green', 'linestyle': '-', 'label': 'In plane'}")
    out_of_plane_style = forms.CharField(max_length=150, required=False, initial="{'color': 'purple', 'linestyle': '--', 'label': 'Out of plane'}")
    velocity_style = forms.CharField(max_length=150, required=False, initial="{'color': 'black', 'va': 'center'}")
    padding_factor = forms.CharField(max_length=150, required=False, initial="{'x' : 1.00, 'y' : 1.05}")

def clear_media_directory():
    media_root = settings.MEDIA_ROOT
    try:
        shutil.rmtree(media_root)
        print(f"Media directory '{media_root}' cleared successfully.")
        os.makedirs(media_root)
    except FileNotFoundError:
        print(f"Media directory '{media_root}' not found.")
    except Exception as e:
        print(f"Error occurred while clearing media directory: {e}")


def get_input_from_form(form):
    # load Material data from input
    density = form[0].cleaned_data["density"]
    youngs_modulus = form[0].cleaned_data["youngs_modulus"]
    poissons_ratio  = form[0].cleaned_data["poissons_ratio"]
    thickness = form[0].cleaned_data["thickness"]
    velocities = (form[0].cleaned_data["longitudinal_wave_velocity"], form[0].cleaned_data["shear_wave_velocity"], form[0].cleaned_data["rayleigh_wave_velocity"])
    name = form[0].cleaned_data["name"]
    material = Material(density, youngs_modulus, poissons_ratio, thickness, *velocities, name)

    # load Wave data from input
    wavetype = dict(WAVETYPE_CHOICES).get(form[1].cleaned_data["wavetype"])
    modes_num = (form[1].cleaned_data["modes_number_sym"], form[1].cleaned_data["modes_number_anti"])
    cp_freq_params = (form[1].cleaned_data["freq_thickness_max"],form[1].cleaned_data["freq_thickness_points"], \
                      form[1].cleaned_data["cp_step"], form[1].cleaned_data["cp_max"])
    structure_mode  = form[1].cleaned_data["structure_mode"]
    structure_frequencies  = eval(form[1].cleaned_data["structure_frequencies"])
    structure_rows = form[1].cleaned_data["structure_rows"]
    structure_columns = form[1].cleaned_data["structure_columns"]
    if wavetype == "Lamb":
        wave = Lambwave(material, modes_num, *cp_freq_params, structure_mode, structure_frequencies, structure_rows, structure_columns)
    else: 
        wave = Shearwave(material, modes_num, *cp_freq_params, structure_mode, structure_frequencies, structure_rows, structure_columns)

    # load Plot data from input
    plotted_modes = dict(MODETYPE_CHOICES).get(form[2].cleaned_data["plotted_modes"])
    plots_chosen = form[2].cleaned_data["plots_chosen"]

    # Create a dictionary of kwargs excluding empty values
    kwargs = {
    field: ast.literal_eval(form[2].cleaned_data[field])
    for field in (
        "symmetric_style","antisymmetric_style", "dashed_line_style",
        "continuous_line_style","in_plane_style", "out_of_plane_style", 
        "velocity_style", "padding_factor" )
    if form[2].cleaned_data[field] and form[2].cleaned_data[field] != 'None'
    }

    # Setup plotter with no gui backend
    clear_media_directory()
    plotter = Plot(wave, plotted_modes, path=settings.MEDIA_ROOT, **kwargs)
    plotter.switch_backend()

    for choice in plots_chosen:
        plot = dict(PLOTTYPE_CHOICES).get(choice)
        plotter.add_plot(plot)

    # Save plots and txt 
    plot_files = plotter.save_plots()
    plotter.close_all_plots()
    txt_file = plotter.save_txt_results()
    plots = [os.path.join(settings.MEDIA_URL, plot) for plot in plot_files ]
    txt = os.path.join(settings.MEDIA_URL, os.path.basename(txt_file))

    # Return created objects
    return plots, txt

