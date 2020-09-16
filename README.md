[![Build Status](https://travis-ci.com/Pogozhelskaya/formal-languages-practice.svg?branch=Task01)](https://travis-ci.com/Pogozhelskaya/formal-languages-practice)
# SPbU Formal Languages course assignments

 ### Required libraries:
 * [pygraphblas](https://github.com/michelp/pygraphblas)

 * [pyformlang](https://pypi.org/project/pyformlang/)
 
 * [pytest](https://docs.pytest.org/en/stable/getting-started.html#install-pytest)
 
 * [networkx](https://github.com/networkx/networkx)
 
 
### How to run tests
```
git clone https://github.com/Pogozhelskaya/formal-languages-practice
cd formal-languages-practice
python3 -m pytest -v -s
```
### Running tests with Docker
An alternative way of building and running tests is using Docker container:

```
git clone https://github.com/Pogozhelskaya/formal-languages-practice
cd formal-languages-practice
docker build -t formal-languages-practice .
docker run formal-languages-practice  
```
### How to use with command line
````
git clone https://github.com/Pogozhelskaya/formal-languages-practice
cd formal-languages-practice
main.py --graph {path_to_graph} --query {path_to_query} [--sources {path_to_source_set}]
               [--destinations {path_to_destination_set}]
````
For help:
````
main.py -h
