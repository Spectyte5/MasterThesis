# MasterThesis

## Topic 
Dispersion in ultrasonic wave propagation - numerical investigations

## Decription
Ultrasonic wave have found various engineering applications. This includes the work for structural damage detection. The major problem in these investigations is the fact that many ultrasonic waves are dispersive i.e., the relevant wave speed depends on the frequency of propagating waves. Examples include Lamb waves propagating in plate-like structures. The project will investigate dispersion in ultrasonic waves. The literature on the subject will be provided. The student will be asked to create a numerical library that provides dispersion characteristics for different wave types and boundaries.

## Goal 
Project idea was to create a alternative numerical libary for providing dispersion characteristics for different wave types and boundaries.
Dispersion curves show a relation between relevant wave speed and its frequency. They are commonly used in different field of engineering and science
for mode identification, solution optimization and generally representing the behavior of waves in given medium.

## Features and Functionality
This application, allows user to visualize dispersion curves for different wave types (Lamb waves, Shear-Horizontal waves, etc.)
and in different mediums (such traction-free isotropic plates, hollow cyllinders from different materials, etc.)
User has many options and parameters that allow checking wave behavior under desired condition and also changing visual side of plots.

## Technology Stack and Implementation
The application was build using the Django framwork as backend, which allowed for efficent data managment and processing.
The frontend intreafce was designed using HTML, CSS and JavaScript with the addition of bootstrap library for styling.
All calculations where done using Numpy and Sympy libraries and then the results where plotted using matplotlib.

## Setup
### Creating a .env file
1. Generate a secret key using django:
  - Secret key is then used in the django app
```python
# importing the function from utils
from django.core.management.utils import get_random_secret_key

# generating and printing the SECRET_KEY
print(get_random_secret_key())
```
2. Set Allowed hosts:
  - Which is a list of strings representing the host/domain names that this Django site can serve.
3. Put all information in .env file
  - Example will be show below
```
# Examplary .env file
SECRET_KEY=34030197126181789620087796727370 
DEBUG=False
ALLOWED_HOSTS = '*'
```
4. Make sure .env is located in the root of the project
### Install
The app was dockerized for ease of use and was written as a webapp to allow cross-compatibilty (Windows, Linux, Mac, etc.)
All instalation will be done automatically by building the docker, which can be done buy running the script:
```
./build_docker.sh
```
### Run
Running the app can also done using a simple script:
```
./run_docker.sh
```

## Usage
The app supports plotting dispersion curves for Lamb and SH waves for isotropic plates and waves in Hollow Cylinders. 
The available plots are Wavenumber, Phase Velocity, Group Velocity and Wavestructure plots. Input of parameters is handled through Django form.

### Material
Material Information part of the form.
#### Parameters
- **Shape**
  Plate of Cylinder are supported options. Example: - 
- **Thickness** (`float`):  
  The thickness of the material plate, measured in millimeters (mm). Example: *10*
- **Longitudinal velocity** (`float`):  
  The velocity of longitudinal waves in the material, measured in meters per second (m/s). Example: *6130*
- **Shear velocity** (`float`):  
  The velocity of shear waves in the material, measured in meters per second (m/s). Example: *3130*
- **Rayleigh velocity** (`float`, optional):  
  The velocity of Rayleigh waves in the material, measured in meters per second (m/s). Example: *2881.6*
- **Material name ** (`str`, optional):  
  The name of the material. Defaults to `"no_material"` if not provided. Example: *Aluminium*
- **inner_radius** (`float`):
  Inner radius of the cylinder, in mm (*Cylinder*). Example: *15.24*
  
### Wave
Wave Information part of the form.
#### Parameters
- **Type of wave** (`bool`)
  Lamb, Shear and Axial are supported options. Example: - 

- **Modes symmetric** (`float`):  
  Number of symmetric  modes (*Plate*). Example: *5*

- **Modes antisymmetric** (`float`):  
  Number of antisymmetric modes (*Plate*). Example: *5*

- **Circumfential order** (`float`):  
  Number of circumferencial order. Example: *5*

- **Modes wavenumber** (`float`):  
  Number of wavenumber modes (*Cylinder*) Example: *5*

- **Max freq thickness** (`int`):  
  Maximum value of Frequency x Thickness [kHz x mm]. Example: *10000*

- **Max phase velocity** (`int`):  
  Maximum value of phase velocity [m/s]. Example: *12000*

- **Wavestructure mode** (`str`, optional):  
  Specifies the mode to be used for the wavestructure plot. Example: *S_0/SH_0/T_(0,1)*

- **Wavestructure freq** (`str`, optional):  
  Array of frequencies at which to check wavestructure. Example: *[500, 1000, 1500, 2000, 2500, 3000]*

- **Wavestructure rows** (`int`, optional):  
  Number of rows for the wavestructure plot. Example: *3*

- **Wavestructure cols** (`int`, optional):  
  Number of columns for the wavestructure plot. Example: *2*

- **Number of fd points** (`int`, optional):  
  Number of frequency x thickness points to calculate. Example: *100*

- **Phase velocity step** (`int`, optional):  
  Step size between phase velocity points to be checked. Example: *100*

### Plot
Plot Information part of the form.
#### Parameters

- **Type of modes** (`str`):  
  Types of the modes shown on the plot: `sym`, `anti`, `torsional`, `longitudinal`, `flexural`, `all`. Example: -

- **Show cutoff freq** (`bool`, optional): Example: -
  Show cutoff frequencies on the plot.

- **Show velocities** (`bool`, optional):  Example: -
  Show plate velocities on the plot.

- **Symmetric style** (`str`, optional):  
  Dictionary with style keyword arguments for symmetric modes. Example: *{'color': 'green', 'linestyle': '-'}*

- **Antisymmetric style** (`str`, optional):  
  Dictionary with style keyword arguments for antisymmetric modes. Example: *{'color': 'purple', 'linestyle': '--'}*

- **Torsional style** (`str`, optional):  
  Dictionary with style keyword arguments for torsional modes. Example: *{'color': 'green', 'linestyle': '-'}*

- **Longitudinal style** (`str`, optional):  
  Dictionary with style keyword arguments for longitudinal modes. Example: *{'color': 'purple', 'linestyle': '--'}*

- **Flexural style** (`str`, optional):  
  Dictionary with style keyword arguments for flexural modes. Example: *{'color': 'purple', 'linestyle': '--'}*

- **Dashed line style** (`str`, optional):  
  Dictionary with style keyword arguments for all dashed lines on plots. Example: *{'color': 'black', 'linestyle': '--', 'linewidth': 0.5}*

- **Continuous line style** (`str`, optional):  
  Dictionary with style keyword arguments for all continuous lines on plots. Example: *{'color': 'black', 'linestyle': '-', 'linewidth': 0.75}*

- **In plane style** (`str`, optional):  
  Dictionary with style keyword arguments for the in-plane component on wavestructure plots. Example: *{'color': 'green', 'linestyle': '-', 'label': 'In plane'}*

- **Out of plane style** (`str`, optional):  
  Dictionary with style keyword arguments for the out-of-plane component on wavestructure plots. Example: *{'color': 'purple', 'linestyle': '--', 'label': 'Out of plane'}*

- **Velocity style** (`str`, optional):  
  Dictionary with style keyword arguments for the plate velocity option. Example: *{'color': 'black', 'va': 'center'}*

- **Padding factor** (`str`, optional):  
  Padding thickness for plots. Example: *{'x' : 1.00, 'y' : 1.05}*

## References 
1. This repository was created as master thesis made by Mechatronic Engineering student at Faculty of Mechanical Engineering and Robotics. 
2. Project was done at AGH University of Science and Technology in Cracow under the supervision of Dr hab. inż. Wiesław Staszewski. 
3. The equations and algorithms were obtained from the great book: Rose, J. L., Ultrasonic Guided Waves in Solid Media, Cambridge University Press, 1999.
4. The algorithm was based on the one from [LambWaveDispersion](https://github.com/franciscorotea/Lamb-Wave-Dispersion/tree/master).
5. The results were validated using [Disperse Software](http://www.disperse.software).
