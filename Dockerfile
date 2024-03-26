# QuestionAnswerGenerator/Dockerfile

FROM python:3.10-slim

WORKDIR ./

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     curl \
#     software-properties-common \
#     git \
#     && rm -rf /var/lib/apt/lists/*

# RUN git clone https://github.com/streamlit/streamlit-example.git .

# RUN pip3 install -r requirements.txt

RUN mkdir ./
COPY . /
WORKDIR ./

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501

ENTRYPOINT ["streamlit", "run", "main.py", 'langchain_helper.py',"--server.port=8501", "--server.address=0.0.0.0"]