FROM ubuntu:focal

# install debian packages
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -qq \
 && apt-get install -y \
    # install essentials
    build-essential \
    wget \
    git \
    cython \
    ffmpeg \
    libsm6 \
    libxext6 \
    python3-pip \
    ttf-mscorefonts-installer \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# avoid getting font from internet https://github.com/ultralytics/yolov5/issues/5159
RUN wget https://ultralytics.com/assets/Arial.ttf && mkdir -p /root/.config/Ultralytics/ && mv Arial.ttf /root/.config/Ultralytics/Arial.ttf
RUN fc-cache -f

RUN mkdir -p /app/model/snapshotes
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
WORKDIR /app/model
RUN git clone https://github.com/ultralytics/yolov5
RUN wget -q -t 3 -O ./snapshotes/yolo5_fullDS_native.pt https://lacmus-dvc.fra1.digitaloceanspaces.com/public/weights/yolo5_fullDS_native.pt
WORKDIR /app

EXPOSE 5000
CMD uvicorn server:app --host 0.0.0.0 --port 5000