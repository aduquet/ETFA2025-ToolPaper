FROM python:3.11.7-slim

# Set environment variables to prevent Python from buffering stdout
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.5.1

# Set the working directory
WORKDIR /app

# Install system dependencies for Python and tkinter
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk \
    libxcb-xinerama0 \
    && apt-get clean

# Install Poetry
RUN pip install --no-cache poetry==$POETRY_VERSION

# Copy only dependency files for caching
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of the application
COPY . /app/

# Expose the port used by the app
EXPOSE 8080

# Run the app
CMD ["poetry", "run", "python", "app_fb.py"]
