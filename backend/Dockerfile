FROM python:3.12

WORKDIR /usr/src/app/backend

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY  . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]
CMD ["daphne", "-b 0.0.0.0" , "-p 8000", "backend.asgi:application"]
CMD ["python", "change_stream_listener.py"]
