FROM python:3.12.0

WORKDIR /app

RUN pip install --upgrade pip "poetry==2.5.1"
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY . .

CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]