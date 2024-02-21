FROM python:3.11
ADD . /
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["python", "src/app.py"]