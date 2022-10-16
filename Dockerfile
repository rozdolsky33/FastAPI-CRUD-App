FROM python:3.9-alpine

RUN pip install pipenv
RUN mkdir -p /user/src/app/app

WORKDIR /user/src/app

COPY Pipfile Pipfile.lock main.py ./
COPY app ./app

RUN pipenv install --system

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]