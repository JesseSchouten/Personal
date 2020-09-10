FROM python:3.7

EXPOSE 8000

WORKDIR /usr/src/app

COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

CMD ["python","./tutorial_2.py"]

