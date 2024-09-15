"""
Definition of views.
"""

import sys, os, json
from django.conf import settings
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .forms import MaterialForm, WaveForm, PlotForm, get_input_from_form

# TEMP
sys.path.append("../../WaveDispersion")
# temporary
from Tests import setup_shear_wave, setup_lamb_wave, plot_data, plot_close_all
from django.core.cache import cache
from django.http import JsonResponse
from .configs import DEFAULT_CONFIG_1, DEFAULT_CONFIG_2, MAX_CONFIGS


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        "app/index.html",
        {
            "title": "Home Page",
            "year": datetime.now().year,
        },
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        "app/contact.html",
        {
            "title": "Contact",
            "year": datetime.now().year,
        },
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        "app/about.html",
        {
            "title": "About",
            "year": datetime.now().year,
        },
    )


def app(request):
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        return process_form(request)
    else:
        request.session.pop("plots", None)  # Clear session data on GET request
        return show_form(request)


def process_form(request):
    material_form = MaterialForm(request.POST, prefix="material")
    wave_form = WaveForm(request.POST, prefix="wave")
    plot_form = PlotForm(request.POST, prefix="plot")
    if material_form.is_valid() and wave_form.is_valid() and plot_form.is_valid():
        plots, txt = get_input_from_form([material_form, wave_form, plot_form])

        # parse data
        return render(
            request,
            "app/result.html",
            {
                "title": "Result",
                "year": datetime.now().year,
                "plots": plots,
                "txt": txt,
            },
        )
    else:
        return show_form(request, material_form, wave_form, plot_form)


def show_form(request, material_form=None, wave_form=None, plot_form=None):
    units = {
        "density": "kg/m3",
        "youngs_modulus": "Pa",
        "thickness": "mm",
        "longitudinal_wave_velocity": "m/s",
        "shear_wave_velocity": "m/s",
        "rayleigh_wave_velocity": "m/s",
        "max_freq_thickness": "kHz*mm",
        "max_phase_velocity": "m/s",
        "wavestructure_frequencies": "kHz",
    }
    if material_form is None or wave_form is None or plot_form is None:
        material_form = MaterialForm(request.POST, prefix="material")
        wave_form = WaveForm(request.POST, prefix="wave")
        plot_form = PlotForm(request.POST, prefix="plot")
    return render(
        request,
        "app/app.html",
        {
            "title": "App",
            "year": datetime.now().year,
            "material_form": material_form,
            "wave_form": wave_form,
            "plot_form": plot_form,
            "plots": request.session.get("plots", None),  # Retrieve plots from session
            "units": units,
        },
    )


def validation(request):
    plot_files = [
        "Titanium_Shear_Phase.png",
        "Magnesium_Lamb_Phase.png",
        "Titanium_Shear_Group.png",
        "Magnesium_Lamb_Group.png",
    ]

    data_shear, shear_wave = setup_shear_wave(
        "../../WaveDispersion/validation/Titanium_Shear_Phase.txt"
    )
    plot_data(
        data_shear,
        shear_wave,
        "Phase",
        "Shear Wave Phase Velocity Test",
        os.path.join(settings.MEDIA_ROOT, plot_files[0]),
        True,
    )

    data_lamb, lamb_wave = setup_lamb_wave(
        "../../WaveDispersion/validation/Magnesium_Lamb_Phase.txt"
    )
    plot_data(
        data_lamb,
        lamb_wave,
        "Phase",
        "Lamb Wave Phase Velocity Test",
        os.path.join(settings.MEDIA_ROOT, plot_files[1]),
        True,
    )

    data_shear, shear_wave = setup_shear_wave(
        "../../WaveDispersion/validation/Titanium_Shear_Group.txt"
    )
    plot_data(
        data_shear,
        shear_wave,
        "Group",
        "Shear Wave Group Velocity Test",
        os.path.join(settings.MEDIA_ROOT, plot_files[2]),
        True,
    )

    data_lamb, lamb_wave = setup_lamb_wave(
        "../../WaveDispersion/validation/Magnesium_Lamb_Group.txt"
    )
    plot_data(
        data_lamb,
        lamb_wave,
        "Group",
        "Lamb Wave Group Velocity Test",
        os.path.join(settings.MEDIA_ROOT, plot_files[3]),
        True,
    )

    plots = [os.path.join(settings.MEDIA_URL, plot) for plot in plot_files]
    plot_close_all()

    return render(
        request,
        "app/validation.html",
        {"title": "Validation", "year": datetime.now().year, "plots": plots},
    )


def load_configuration(request, config_name):
    # Check for default configurations
    if config_name == "default1":
        return JsonResponse({"config": DEFAULT_CONFIG_1})
    elif config_name == "default2":
        return JsonResponse({"config": DEFAULT_CONFIG_2})

    # Check for custom configurations in cache
    config_data = cache.get(config_name)
    if config_data is None:
        return JsonResponse({"error": "Configuration not found"}, status=404)

    return JsonResponse({"config": config_data})


def save_configuration(request):
    if request.method == "POST":  # Ensure only POST requests are handled
        try:
            data = json.loads(
                request.body.decode("utf-8")
            )  # Parse JSON data from the request
            config_name = data.get("config_name")
            config_data = data.get("config_data")

            if not config_name or not config_data:
                return JsonResponse(
                    {"error": "Configuration name and data are required"}, status=400
                )

            # Save or overwrite the configuration in the cache
            cache.set(config_name, config_data)

            return JsonResponse({"success": f"Configuration {config_name} saved!"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def list_custom_configurations(request):
    configurations = []
    for i in range(1, MAX_CONFIGS + 1):
        config_name = f"config{i}"
        if cache.get(config_name):
            configurations.append(config_name)

    return JsonResponse({"configs": configurations})


def delete_configuration(request, config_name):
    if request.method == 'DELETE':
        if cache.get(config_name):  # Check if the configuration exists
            cache.delete(config_name)
            return JsonResponse({'success': f'Configuration {config_name} deleted!'})
        else:
            return JsonResponse({'error': 'Configuration not found!'}, status=404)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
