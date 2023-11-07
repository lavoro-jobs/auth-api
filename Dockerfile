FROM python:3.9

WORKDIR /devel

COPY ./lavoro-auth-api/requirements.txt /devel/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /devel/requirements.txt

RUN apt-get update && apt-get install -y curl

RUN curl -sS https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -o /wait-for-it.sh \
    && chmod +x /wait-for-it.sh

COPY ./lavoro-auth-api/lavoro_auth_api /devel/lavoro_auth_api


# Library
COPY ./lavoro-library/lavoro_library /devel/lavoro_library
COPY ./lavoro-library/pre_install.sh /devel/pre_install.sh

RUN chmod +x /devel/pre_install.sh
RUN /devel/pre_install.sh

ENV PYTHONPATH "${PYTHONPATH}:/devel"

ENTRYPOINT ["/wait-for-it.sh", "auth-db:5432", "--"]
CMD ["uvicorn", "lavoro_auth_api.auth_api:app", "--host", "0.0.0.0", "--port", "80"]
