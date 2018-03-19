FROM python:3.5
ADD backend /backend
WORKDIR /backend
RUN pip install -r requirements.txt
CMD ["python", "main.py"]