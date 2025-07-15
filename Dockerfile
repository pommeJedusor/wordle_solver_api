FROM python:3.13.5-alpine3.21

WORKDIR /app
COPY . /app

RUN apk add --no-cache gcc musl-dev

RUN pip install -r requirements.txt

RUN python setup.py build_ext --inplace

EXPOSE 5000  

CMD ["python", "api.py"]
