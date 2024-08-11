FROM python:3.10.12

SHELL [ "/bin/bash", "-c" ]

ENV PYTHONUNBUFFERED 1 
ENV PYTHONDONTWRITEBYTECODE 1 

RUN pip install --upgrade pip
RUN apt update && apt -qy install libpq-dev gettext cron flake8 locales neovim
RUN useradd -rms /home andrey && chmod 777 /opt /run
WORKDIR /kithenland-project

COPY requirements.txt .

RUN pip install -r requirements.txt
COPY --chown=andrey:andrey . .

USER andrey

CMD ["python3", "manage.py", "runserver", "0.0.0.0:7000"]

# docker build -t online-market-image . && docker compose up --build