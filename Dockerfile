FROM python:3.9

WORKDIR /devel

COPY ./requirements.txt /devel/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /devel/requirements.txt

COPY ./auth_api /devel/auth_api

CMD ["uvicorn", "auth_api.auth_api:app", "--host", "0.0.0.0", "--port", "80"]
