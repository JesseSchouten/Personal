FROM ubuntu:latest

RUN apt-get update && apt-get -y update

RUN apt-get install -y build-essential python3.6 python3-pip python3-dev

ENV TZ=Europe/Amsterdam
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -yq libgtk2.0-dev
RUN apt-get install -y libgl1-mesa-dev

RUN mkdir src
WORKDIR src/
COPY . .

RUN pip3 install -r requirements.txt
RUN pip3 install matplotlib
RUN pip3 install jupyter
RUN pip3 install opencv-python
RUN pip3 install tqdm

WORKDIR /src/notebooks

# Add Tini. Tini operates as a process subreaper for jupyter. This prevents kernel crashes.
ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]