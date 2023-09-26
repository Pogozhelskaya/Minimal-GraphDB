[![Build Status](https://travis-ci.com/Pogozhelskaya/formal-languages-practice.svg?branch=Task01)](https://travis-ci.com/Pogozhelskaya/formal-languages-practice)
# Implementation of a simple graph database in Python

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
To run with your own examples:
````
main.py --graph {path_to_graph} --query {path_to_query} [--sources {path_to_source_set}]
               [--destinations {path_to_destination_set}]
````
For help:
````
main.py -h
````
### Transitive closure comparison
To get data(graphs and regular expressions) for benchmarks download the archive:
````
gdown https://drive.google.com/uc?id=158g01o2rpdq5eL3Ari8e5SPbbeZTJspr
````
To run benchmarks:
`````
chmod +x run.sh
/bin/bash run.sh
`````
### Experimental analyses
* After testing LUBM graphs dataset, there has been detected no difference between calculating transitive closure with squaring and transitive closure with multiplying by adjacency matrix. More detailed analysis report can be found at report.pdf. 
* Report about time comparison of different CFPQ-algorithms can be found at report_cfpq.ipynb.

### Query Language Grammar
```
S (Stmt) (Stmt)*
Stmt c o n n e c t Blank Path Blank ;
Stmt s e l e c t Blank Result Blank f r o m Blank Graph Blank ;
Path ((Word | /)) ((Word | /)*)
Result p a i r s
Result c o u n t
Graph i n t e r s e c t Blank o f Blank Graph Blank a n d Blank Graph
Graph Query
Graph Word
Query Word
Query ( \( ) Query ( \) )
Query ( Query Query )
Query ( \( )  Query ( \| ) Query ( ( \| ) Query )* ( \) )
Query ( \( ) Query ( \* ) ( \) )
Query ( \( ) Query ( \? ) ( \) )
Query ( \( ) Query ( \+ ) ( \) )
Word (Char) (Char)*
Char (a|(b|(c|(d|(e|(f|(g|(h|(i|(j|(k|(l|(m|(n|(o|(p|(q|(r|(s|(t|(u|(v|(w|(x|(y|(z|(0|(1|(2|(3|(4|(5|(6|(7|(8|(9|_))))))))))))))))))))))))))))))))))))
Blank @
```

### How to run analyzer
```
analyzer.py --script {path_to_script)
```

### Example of script

```
connect db/db_name ;
select pairs from graph ;
select count from intersect of graph and (((((3?)6)*)+)(5|4)*) ;
```

