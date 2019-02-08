FROM eyqs/process-dynamics-engine
WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/app"
COPY ./requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt
COPY . .
CMD ["python", "server/app.py"]
