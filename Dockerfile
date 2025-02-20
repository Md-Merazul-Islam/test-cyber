# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . /app/

# Expose the port your app will run on
EXPOSE 8000

# Run Gunicorn with your project’s WSGI entry point
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
