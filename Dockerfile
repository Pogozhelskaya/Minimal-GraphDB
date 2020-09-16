FROM graphblas/pygraphblas-minimal:latest

RUN mkdir /formal-languages-practice
WORKDIR /formal-languages-practice

COPY . /formal-languages-practice

RUN pip3 install -r requirements.txt
CMD ["/usr/bin/python3.8", "-m", "pytest", "-v", "-s"]