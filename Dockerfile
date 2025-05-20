FROM python:3.12

WORKDIR /usr/local/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && rm -rf ~/.cache

COPY src ./src
EXPOSE 8080

# Setup app user
RUN useradd -m -d /home/app -s /bin/bash app \
  && chown -R app:app /usr/local/app
USER app

ENV PYTHONPATH=/usr/local/app/src

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
