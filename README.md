# WikiGraph

Create a graph of the Wiki http://awoiaf.westeros.org and provide some operation
on this graph.

## Dependency

- Python 3
- Scrapy
- NetworkX
- JQ

## How to use it

Generate the JSON file that represent the wiki with
```
$ ./generate_adjacency_dictionary.sh
```
The pipe the JSON file into `graph.py`
```
$ cat adjacency_dictionary.json | ./graph.py
```

## Graph of another Wiki

The program can easily be modified to be used on another Wiki. for that
the value of `urls` in the class `TitleSpider` in the file
`WikiGraph/ScapyProject/spiders/title_spider.py` has to be change to
the main page of the wiki.

For example to create a graph of the wiki http://crawl.chaosforge.org/Crawl_Wiki 
change
```python
urls = ['http://awoiaf.westeros.org/index.php/Main_Page']
```
to
```python
urls = ['http://crawl.chaosforge.org/Crawl_Wiki']
```

I might implement a way to change this from the CLI. But if anybody
ask me to implement it, it will be done almost immediatly. 

## How it work

The program use a web spider created with the help of the python module scrapy to
find all the pages of the Wiki. The pages are found by a Depth First Search which
start at the main page of the wiki, during the Depth First Search the web spider
create an adjacency list of the pages. The adjacency list is stored in a JSON file.

To apply the opeartions on the graph the adjacency list is converted in a
networkx graph,
networkx is python module that provide a crazy lot of operations on graphs, therefore
implementing any other operation is quite trivial when the networkx graph has been created.
