FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src/ .
RUN python -m compileall -q -f -b .
RUN find . -name '*.py' | xargs rm

EXPOSE 8000

CMD ["uvicorn", "tds.calculator.main:app", "--host", "0.0.0.0", "--port", "8000"]
