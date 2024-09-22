"""
Definition of forms.
"""

import os, shutil, ast
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from Material import Plate
from Plot import Plot
from Wave import Lambwave, Shearwave


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""

    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput({"class": "form-control", "placeholder": "User name"}),
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            {"class": "form-control", "placeholder": "Password"}
        ),
    )


WAVETYPE_CHOICES = (
    ("1", "Lamb"),
    ("2", "Shear"),
)

MODETYPE_CHOICES = (
    ("1", "both"),
    ("2", "symmetric"),
    ("3", "antisymmetric"),
)

PLOTTYPE_CHOICES = (
    ("1", "Phase"),
    ("2", "Group"),
    ("3", "Wavenumber"),
    ("4", "Wavestructure"),
)


class MaterialForm(forms.Form):
    thickness = forms.FloatField(initial=10, help_text="Thickness of the plate [mm]")
    longitudinal_velocity = forms.FloatField(
        initial=6130, help_text="Longitudinal wave velocity of the material [m/s]"
    )
    shear_velocity = forms.FloatField(
        initial=3130, help_text="Shear wave velocity of the material [m/s]"
    )
    rayleigh_velocity = forms.FloatField(
        initial=2881.6,
        help_text="Rayleigh wave velocity of the material [m/s] (Optional)",
        required=False,
    )
    material_name = forms.CharField(
        max_length=50,
        initial="Aluminum",
        help_text="Name of the material (Optional)",
        required=False,
    )


class WaveForm(forms.Form):
    type_of_wave = forms.ChoiceField(
        choices=WAVETYPE_CHOICES, initial=1, help_text="Type of the wave, [Shear, Lamb]"
    )
    modes_symmetric = forms.IntegerField(
        initial=5, help_text="Number of symmetric modes to find"
    )
    modes_antisymmetric = forms.IntegerField(
        initial=5, help_text="Number of antisymmetric modes to find"
    )
    max_freq_thickness = forms.IntegerField(
        initial=10000, help_text="Max value pf Frequency x Thickness [kHz x mm]"
    )
    max_phase_velocity = forms.IntegerField(
        initial=12000, help_text="Max value pf Frequency x Thickness [m/s]"
    )
    wavestructure_mode = forms.CharField(
        initial="S_0",
        max_length=4,
        min_length=3,
        help_text="Which mode should be used for wavestructure plot \
   (Optional - Wavestructure Plot only)",
        required=False,
    )
    wavestructure_freq = forms.CharField(
        initial=[500, 1000, 1500, 2000, 2500, 3000],
        max_length=50,
        help_text="Frequencies at which to check Wavestructure (Optional - Wavestructure Plot only)",
        required=False,
    )
    wavestructure_rows = forms.IntegerField(
        initial=3,
        required=False,
        help_text="Number of rows for Wavestructure plot, rows x colums must equal to number of Wavestructure Frequencies values (Optional - Wavestructure Plot only)",
    )
    wavestructure_cols = forms.IntegerField(
        initial=2,
        required=False,
        help_text="Number of columns for Wavestructure plot, rows x colums must equal to number of Wavestructure Frequencies values (Optional - Wavestructure Plot only)",
    )
    number_of_fd_points = forms.IntegerField(
        initial=100,
        required=False,
        help_text="Number of frequency x thickness points to find",
    )
    phase_velocity_step = forms.IntegerField(
        initial=100,
        required=False,
        help_text="Step between phase velocity points checked",
    )


class PlotForm(forms.Form):
    type_of_modes = forms.ChoiceField(
        choices=MODETYPE_CHOICES,
        initial=1,
        help_text="Which wave types should be plotted [both, symmetric, antisymmetric]",
    )
    type_of_plots = forms.MultipleChoiceField(
        choices=PLOTTYPE_CHOICES,
        initial=1,
        help_text="Which plots should be plotted [Phase, Group, Wavenumber, Wavestrucure]",
    )
    show_cutoff_freq = forms.BooleanField(
        required=False,
        help_text="Display plate velocites: Longitudinal, Shear, Rayleigh of the material on the plot (Optional)",
    )
    show_velocities = forms.BooleanField(
        required=False, help_text="Display cutoff frequencies on the plot (Optional)"
    )
    symmetric_style = forms.CharField(
        max_length=150,
        required=False,
        initial="{'color': 'green', 'linestyle': '-'}",
        help_text="Matplotlib kwargs to set style for symmetric modes curves (Optional)",
    )
    antisymmetric_style = forms.CharField(
        max_length=150,
        required=False,
        initial="{'color': 'purple', 'linestyle': '--'}",
        help_text="Matplotlib kwargs to set style for antisymmetric modes curves (Optional)",
    )
    dashed_line_style = forms.CharField(
        max_length=150,
        required=False,
        initial="{'color': 'black', 'linestyle': '--', 'linewidth': 0.5}",
        help_text="Matplotlib kwargs to set style for dashed lines used for cutoff frequencies and plate velocites (Optional)",
    )
    continuous_line_style = forms.CharField(
        max_length=150,
        required=False,
        initial="{'color': 'black', 'linestyle': '-', 'linewidth': 0.75}",
        help_text="Matplotlib kwargs to set style for continous lines used as axis in Wavestructure plot (Optional)",
    )
    in_plane_style = forms.CharField(
        max_length=150,
        required=False,
        initial="{'color': 'green', 'linestyle': '-', 'label': 'In plane'}",
        help_text="Matplotlib kwargs to set style for Wavestructure in-plane curves (Optional)",
    )
    out_of_plane_style = forms.CharField(
        max_length=150,
        required=False,
        initial="{'color': 'purple', 'linestyle': '--', 'label': 'Out of plane'}",
        help_text="Matplotlib kwargs to set style for Wavestructure out-of-plane curves (Optional)",
    )
    velocity_style = forms.CharField(
        max_length=150,
        required=False,
        initial="{'color': 'black', 'va': 'center'}",
        help_text="Matplotlib kwargs to set style for plate velocities: Longitudinal, Shear, Rayleigh of the material (Optional)",
    )
    padding_factor = forms.CharField(
        max_length=150,
        required=False,
        initial="{'x' : 1.00, 'y' : 1.05}",
        help_text="X, Y padding values, how much space should be added on the right side of plots (Optional)",
    )


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


def validate_wave(form):
    structure_mode = form[1].cleaned_data["wavestructure_mode"]
    structure_frequencies = (
        eval(form[1].cleaned_data["wavestructure_freq"])
        if form[1].cleaned_data["wavestructure_freq"]
        else None
    )
    structure_rows = form[1].cleaned_data["wavestructure_rows"]
    structure_columns = form[1].cleaned_data["wavestructure_cols"]
    expected_size = structure_rows * structure_columns
    if structure_frequencies and len(structure_frequencies) != expected_size:
        raise forms.ValidationError(
            f"The size of the array ({len(structure_frequencies)}) does not match the product of rows ({structure_rows}) and columns ({structure_columns})."
        )
    return (structure_mode, structure_frequencies, structure_rows, structure_columns)


def get_input_from_form(form):
    # load Material data from input
    thickness = form[0].cleaned_data["thickness"]
    velocities = (
        form[0].cleaned_data["longitudinal_velocity"],
        form[0].cleaned_data["shear_velocity"],
    )
    rayleigh = form[0].cleaned_data["rayleigh_velocity"]
    name = form[0].cleaned_data["material_name"]
    material = Plate(thickness, *velocities, rayleigh_wave_velocity=rayleigh, name=name)

    # load Wave data from input
    wavetype = dict(WAVETYPE_CHOICES).get(form[1].cleaned_data["type_of_wave"])
    modes_num = (
        form[1].cleaned_data["modes_symmetric"],
        form[1].cleaned_data["modes_antisymmetric"],
    )
    cp_freq_max = (
        form[1].cleaned_data["max_freq_thickness"],
        form[1].cleaned_data["max_phase_velocity"],
    )
    structure_args = validate_wave(form)
    cp_freq_steps = (
        form[1].cleaned_data["number_of_fd_points"],
        form[1].cleaned_data["phase_velocity_step"],
    )
    if wavetype == "Lamb":
        wave = Lambwave(
            material, modes_num, *cp_freq_max, *structure_args, *cp_freq_steps
        )
    else:
        wave = Shearwave(
            material, modes_num, *cp_freq_max, *structure_args, *cp_freq_steps
        )

    # load Plot data from input
    plotted_modes = dict(MODETYPE_CHOICES).get(form[2].cleaned_data["type_of_modes"])
    plots_chosen = form[2].cleaned_data["type_of_plots"]
    show_optional = (
        form[2].cleaned_data["show_cutoff_freq"],
        form[2].cleaned_data["show_velocities"],
    )

    # Create a dictionary of kwargs excluding empty values
    kwargs = {
        field: ast.literal_eval(form[2].cleaned_data[field])
        for field in (
            "symmetric_style",
            "antisymmetric_style",
            "dashed_line_style",
            "continuous_line_style",
            "in_plane_style",
            "out_of_plane_style",
            "velocity_style",
            "padding_factor",
        )
        if form[2].cleaned_data[field] and form[2].cleaned_data[field] != "None"
    }

    # Setup plotter with no gui backend
    clear_media_directory()
    plotter = Plot(
        wave, plotted_modes, *show_optional, path=settings.MEDIA_ROOT, **kwargs
    )
    plotter.switch_backend()

    for choice in plots_chosen:
        plot = dict(PLOTTYPE_CHOICES).get(choice)
        plotter.add_plot(plot)

    # Save plots and txt
    plot_files = plotter.save_plots()
    plotter.close_all_plots()
    txt_file = plotter.save_txt_results()
    plots = [os.path.join(settings.MEDIA_URL, plot) for plot in plot_files]
    txt = os.path.join(settings.MEDIA_URL, os.path.basename(txt_file))

    # Return created objects
    return plots, txt
