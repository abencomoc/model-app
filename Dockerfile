FROM rayproject/ray:2.44.0

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy your application code
COPY src/finbert_ray.py /app/finbert_ray.py

WORKDIR /app

