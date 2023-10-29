FROM python:3.9

WORKDIR /devel

COPY ./requirements.txt /devel/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /devel/requirements.txt

COPY ./lavoro_auth_api /devel/lavoro_auth_api

CMD ["uvicorn", "lavoro_auth_api.auth_api:app", "--host", "0.0.0.0", "--port", "80"]
