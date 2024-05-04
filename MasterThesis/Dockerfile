# Dockerfile

# The official Python runtime as a parent image
FROM python:3.11

# Cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Wavedispersion package
RUN pip install ./WaveDispersion

# Mounts the application code
COPY . code
WORKDIR /code

EXPOSE 8000

# Run the production server
ENTRYPOINT ["python", "MasterThesis/manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
