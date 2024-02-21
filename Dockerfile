FROM python:3.11
ADD . /
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD ["python", "src/app.py"]