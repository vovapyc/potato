FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY ./requirements.txt /app/requirements.txt
RUN uv pip install --no-cache-dir  --system -r /app/requirements.txt

# Preload embeddings model to include it in the image
RUN python -c "import timm; timm.create_model('nextvit_small.bd_ssld_6m_in1k_384', pretrained=True)"

COPY ./app.py /app/app.py
COPY potato_logreg.pkl /app/potato_logreg.pkl

CMD ["fastapi", "run", "app.py", "--port", "80"]
