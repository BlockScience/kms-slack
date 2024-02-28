FROM python:3.11
ADD . .
RUN pip install --no-cache-dir -r requirements.txt
ENV HOST 0.0.0.0
EXPOSE 8080
ENTRYPOINT ["python", "src/app.py"]
