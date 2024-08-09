# ToolRI
ARG PROJECT=ToolRI

# linux image
FROM python:3.10-bookworm

# working directory in the container
WORKDIR /$PROJECT

# copy the current directory contents into the container
COPY . /$PROJECT

# install some apt packages
RUN apt update
RUN apt install git wget -y

# install Tesseract
RUN apt install tesseract-ocr tesseract-ocr-eng tesseract-ocr-por -y

## install Python packages
RUN pip install -r $PROJECT/requirements.txt

## install ToolRI as editable for development
RUN pip install -e $PROJECT/
