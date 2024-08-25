# MasterThesis
## Topic: 
Dispersion in ultrasonic wave propagation - numerical investigations
## Decription:
Ultrasonic wave have found various engineering applications. This includes the work for structural damage detection. The major problem in these investigations is the fact that many ultrasonic waves are dispersive i.e., the relevant wave speed depends on the frequency of propagating waves. Examples include Lamb waves propagating in plate-like structures. The project will investigate dispersion in ultrasonic waves. The literature on the subject will be provided. The student will be asked to create a numerical library that provides dispersion characteristics for different wave types and boundaries.
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
All instalation will be done automatically by building the docker, which can be done buy running the script:
```
./build_docker.sh
```
### Run
Running the app can also done using a simple script:
```
./run_docker.sh
```
### Usage
The app supports plotting dispersion curves for Lamb and SH waves for isotropic plates and waves in Hollow Cylinders. 
The available plots are Wavenumber, Phase Velocity, Group Velocity and Wavestructure plots.

#### Methods

### Results
### Validation
### References 
This repository was created as master thesis made by Mechatronic Engineering student at Faculty of Mechanical Engineering and Robotics. 
Project was done at AGH University of Science and Technology in Cracow under the supervision of Dr hab. inż. Wiesław Staszewski. 
The equations and algorithms were obtained from the great book: Rose, J. L., Ultrasonic Guided Waves in Solid Media, Cambridge University Press, 1999. 
The results were validated using Disperse Software.
