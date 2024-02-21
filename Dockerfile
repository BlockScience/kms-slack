FROM python:3.11
ADD . /
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python", "src/app.py"]