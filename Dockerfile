FROM python:3.11-slim
WORKDIR /app
RUN mkdir -p /workspace
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .
EXPOSE 8000
CMD ["uvicorn", "devassure.api:app", "--host", "0.0.0.0", "--port", "8000"]
