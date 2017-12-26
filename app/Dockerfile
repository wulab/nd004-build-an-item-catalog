FROM python:alpine

WORKDIR /usr/src/app

COPY ./ ./
RUN pip install --no-cache-dir -e .

CMD [ "flask", "run", "--host=0.0.0.0", "--port=8000" ]
