FROM jupyter/base-notebook:1fbaef522f17

COPY . .
RUN pip install -r requirements.txt
# lulz
RUN echo $'#!/bin/bash\npython app.py' > ${CONDA_DIR}/bin/jupyter
