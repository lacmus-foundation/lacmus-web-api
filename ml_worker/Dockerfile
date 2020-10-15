FROM tensorflow/tensorflow:2.1.1-gpu

# install debian packages
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -qq \
 && apt-get install --no-install-recommends -y \
    # install essentials
    build-essential \
    wget \
    git \
    g++ \
    cython \
    # requirements for numpy
    libopenblas-base \
    python3-numpy \
    python3-scipy \
    # requirements for keras
    python3-h5py \
    python3-yaml \
    python3-pydot \
    libgl1-mesa-glx \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# install application
ARG KERAS_VERSION=2.3.1
ENV KERAS_BACKEND=tensorflow

RUN mkdir /app
WORKDIR /app
COPY requirements.txt .

RUN git clone https://github.com/lacmus-foundation/lacmus.git \
    && pip3 install --upgrade setuptools \
    && pip3 --no-cache-dir install --no-dependencies git+https://github.com/fchollet/keras.git@${KERAS_VERSION} \
    && pip3 install opencv-python \
    && cd /app/lacmus && pip3 install . --user \
    && python3 setup.py build_ext --inplace \
    && cd /app && pip install -r requirements.txt

COPY . .

CMD uvicorn server:app --host 0.0.0.0 --port 5000