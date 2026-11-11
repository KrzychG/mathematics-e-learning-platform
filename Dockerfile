FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    FLASK_APP=run.py \
    FLASK_CONFIG=docker

WORKDIR /app

# Użytkownik bez uprawnień roota katalogi zapisu dostaną właściwego właściciela
# przed podpięciem nazwanych wolumenów Dockera.
RUN groupadd --system appgroup && useradd --system --gid appgroup --create-home appuser

# Instalacja zależności w osobnej warstwie dla szybszego cache'owania buildów
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Kopiowanie kodu aplikacji
COPY . .

# Przygotowanie katalogów trwałych i skryptu startowego
RUN mkdir -p /app/instance /app/app/static/uploads/avatars \
    && sed -i 's/\r$//' /app/docker/entrypoint.sh \
    && chmod +x /app/docker/entrypoint.sh \
    && chown -R appuser:appgroup /app

USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import sys, urllib.request; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:5000/healthz', timeout=3).status == 200 else 1)"

ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "4", "--timeout", "120", "run:app"]
