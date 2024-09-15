DEFAULT_COMMON = {
    "thickness": 10,
    "longitudinal_velocity": 6130,
    "shear_velocity": 3130,
    "rayleigh_velocity": 2881.6,
    "material_name": "Aluminum",
    "modes_symmetric": 5,
    "modes_antisymmetric": 5,
    "max_freq_thickness": 10000,
    "max_phase_velocity": 12000,
    "wavestructure_freq": "[500, 1000, 1500, 2000, 2500, 3000]",
    "wavestructure_rows": 3,
    "wavestructure_cols": 2,
    "number_of_fd_points": 100,
    "phase_velocity_step": 100,
    "type_of_modes": 1,
    "type_of_plots": 1,
    "show_cutoff_freq": True,
    "show_velocities": False,
    "symmetric_style": "{'color': 'green', 'linestyle': '-'}",
    "antisymmetric_style": "{'color': 'purple', 'linestyle': '--'}",
    "dashed_line_style": "{'color': 'black', 'linestyle': '--', 'linewidth': 0.5}",
    "continuous_line_style": "{'color': 'black', 'linestyle': '-', 'linewidth': 0.75}",
    "in_plane_style": "{'color': 'green', 'linestyle': '-', 'label': 'In plane'}",
    "out_of_plane_style": "{'color': 'purple', 'linestyle': '--', 'label': 'Out of plane'}",
    "velocity_style": "{'color': 'black', 'va': 'center'}",
    "padding_factor": "{'x' : 1.00, 'y' : 1.05}",
}

DEFAULT_CONFIG_1 = dict(
    DEFAULT_COMMON,
    **{
        "wavestructure_freq": "[500, 1000, 1500, 2000, 2500, 3000]",
        "type_of_wave": 1,
        "wavestructure_mode": "S_0",
    }
)
DEFAULT_CONFIG_2 = dict(
    DEFAULT_COMMON,
    **{
        "wavestructure_freq": "[2000, 3500, 5000, 7500, 9000, 10000]",
        "type_of_wave": 2,
        "wavestructure_mode": "SH_1",
    }
)
MAX_CONFIGS = 20
