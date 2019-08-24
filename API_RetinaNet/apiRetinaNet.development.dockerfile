FROM tensorflow/tensorflow:1.12.0-py3

# install debian packages
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -qq \
 && apt-get install --no-install-recommends -y \
    # install essentials
    build-essential \
    g++ \
    git \
    wget \
    apt-transport-https \
    curl \
    cython \
    # requirements for numpy
    libopenblas-base \
    python3-numpy \
    python3-scipy \
    # requirements for keras
    python3-h5py \
    python3-yaml \
    python3-pydot \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

ARG KERAS_VERSION=2.2.4
ENV KERAS_BACKEND=tensorflow

# install application
EXPOSE 5001
WORKDIR /var/www/apiRetinaNet
COPY . .

RUN ls -a && pip3 --no-cache-dir install --no-dependencies git+https://github.com/fchollet/keras.git@${KERAS_VERSION} \
    && pip3 --no-cache-dir install -U numpy==1.13.3 --user \
    && pip3 --no-cache-dir install opencv-python flask \
    && pip3 install --upgrade setuptools \
    && pip3 install . --user \
    && python3 setup.py build_ext --inplace

# quick test and dump package lists
RUN python3 -c "import tensorflow; print(tensorflow.__version__)"

ENTRYPOINT ["python3", "web_api.py", "--model", "./snapshots/resnet50_liza_alert_v3_interface.h5"]