# Use an official ubuntu runtime as a parent image
FROM ubuntu:latest

# get python / pip
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

# We copy just the requirements.txt first to leverage Docker cache
COPY app/requirements.txt /app/requirements.txt

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY app /app

# Create sqlite db file
RUN python create_db_tables.py --db_name=sqlite.db

# Make ports available to the world outside this container
EXPOSE 8081

# Run app.py when the container launches
CMD ["python", "app.py"]