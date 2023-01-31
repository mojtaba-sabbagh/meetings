FROM python:3.9

WORKDIR /app

RUN pip install --upgrade pip

COPY . .
RUN pip install -r requirments.txt
RUN pip install gunicorn

EXPOSE 8000

ENTRYPOINT ["sh","entrypoint.sh"]
