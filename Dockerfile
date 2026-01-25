FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY shareable_url.txt .
COPY shareable_url_compressed.txt .

EXPOSE 7860

CMD ["python", "app.py"]
