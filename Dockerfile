FROM graphblas/pygraphblas-minimal:v3.3.3

COPY . /formal-languages-practice

WORKDIR /formal-languages-practice
RUN pip3 install -r requirements.txt
CMD ["/usr/bin/python3.8", "-m", "pytest", "-vv", "-s"]