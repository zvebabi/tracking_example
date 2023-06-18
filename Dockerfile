FROM nvidia/cuda:10.2-cudnn8-devel-ubuntu18.04 as unzipper
SHELL ["/bin/bash", "-c"] 

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub && \
    apt update && \
    apt install -y --no-install-recommends \
      wget \
      unzip \
      python3 \
      python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget -O HallWayTracking.zip https://www.dropbox.com/s/kije4lyl8torf3q/HallWayTracking.zip?dl=0 && \
    unzip HallWayTracking.zip && \
    rm HallWayTracking.zip

FROM nvidia/cuda:10.2-cudnn8-devel-ubuntu18.04 as deploy
SHELL ["/bin/bash", "-c"] 

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub && \
    apt update && \
    apt install -y --no-install-recommends \
      git \
      ffmpeg \
      python3 \
      python3-dev \
      python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install wheel torch==1.7.0 torchvision==0.8.0 torchaudio==0.7.0 \
      cython \
      setuptools \
      gdown

WORKDIR /app

#download deps
RUN git clone -b pytorch_1.7 https://github.com/ifzhang/DCNv2.git && \
    cd DCNv2 && \
    sed -i '/.*if torch.cuda.is_available() and CUDA_HOME is not None:.*/c\    if 1: #torch.cuda.is_available() and CUDA_HOME is not None:' ./setup.py && \
    ./make.sh

RUN git clone https://github.com/ifzhang/FairMOT.git && \
    cd FairMOT && \
    python3 -m pip install -r requirements.txt
    # gdown --fuzzy https://drive.google.com/open?id=1iqRQjsG9BawIl8SlFomMg5iwkb6nqSpi&authuser=0

RUN python3 -m pip install ffmpegcv

#download sample videos
COPY --from=unzipper /HallWayTracking HallWayTracking/

#download app and model
COPY ./weights/ /app/FairMOT/models/
COPY ./images/ /app/images
COPY ./src/ /app/
COPY ./runApp.sh /app/

#test demo
CMD ["/app/runApp.sh", "100"]
