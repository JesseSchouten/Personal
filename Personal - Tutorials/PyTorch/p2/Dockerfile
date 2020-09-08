FROM python:3.7

EXPOSE 8000

WORKDIR /usr/src/app

COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

COPY . /usr/src/app

CMD ["python","./tutorial_2.py"]
