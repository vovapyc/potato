FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY ./requirements.txt /app/requirements.txt
RUN uv pip install --no-cache-dir  --system -r /app/requirements.txt

COPY ./*.onnx /app/
COPY ./*.py /app/

CMD ["fastapi", "run", "app.py", "--port", "80"]
