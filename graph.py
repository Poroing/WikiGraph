#!/usr/bin/python3

import networkx as nx
import json
import sys
import argparse

class Graph(nx.DiGraph):

    def topologicalSort(self):
        if not nx.is_directed_acyclic_graph(self):
            print('The graph contains cycles and cannot be processed')
            return
        topological_order = nx.topological_sort(self)
        for node in topological_order:
            print(node)

    def getNMinOutDegree(self, n):
        sorted_nodes = sorted(self.nodes(), key=lambda node: self.out_degree(node))
        if n > len(sorted_nodes):
            n = len(sorted_nodes)
        for node in sorted_nodes[:n]:
            print(node)

    def getNMaxOutDegree(self, n):
        sorted_nodes = sorted(self.nodes(), key=lambda node: -self.out_degree(node))
        if n > len(sorted_nodes):
            n = len(sorted_nodes)
        for node in sorted_nodes[:n]:
            print(node)

    def stronglyConnectedComponent(self):
        for strongly_connected_component in nx.strongly_connected_components(self):
            print(strongly_connected_component)

    def doNothing(self):
        pass

def generateEdgeFromDictionary(dictionary):
    for key in dictionary:
        for item in dictionary[key]:
            yield (key, item)

def createDiGraphFromDictionary(dictionary):
    graph = Graph()
    graph.add_edges_from(generateEdgeFromDictionary(dictionary))
    return graph

def createDiGraphFromJsonFile(json_file):
    return createDiGraphFromDictionary(json.load(json_file))

def createDiGraphFromSTDIN():
    return createDiGraphFromJsonFile(sys.stdin)

graph = createDiGraphFromSTDIN()

parser = argparse.ArgumentParser(
    description='Apply graph operations on json object from the stdin.')
parser.add_argument('-t', '--topological-sort', action='store_const',
    const=graph.topologicalSort, default=graph.doNothing)
parser.add_argument('-m', '--min-out-degree', nargs='?', const=1, default=0, type=int)
parser.add_argument('-M', '--max-out-degree', nargs='?', const=1, default=0, type=int)
parser.add_argument('-r', '--remove-node', nargs='*')
parser.add_argument('-s', '--strongly-connected-component', action='store_const',
    const=graph.stronglyConnectedComponent, default=graph.doNothing)
parser.add_argument('-rf', '--remove-node-from-file', nargs='+', type=argparse.FileType('r'))

args = parser.parse_args()

if args.remove_node is not None:
    graph.remove_nodes_from(args.remove_node)
if args.remove_node_from_file is not None:
    for f in args.remove_node_from_file:
        graph.remove_nodes_from(map(lambda s: s.strip('\n'), f.readlines()))

if args.min_out_degree is not None:
    graph.getNMinOutDegree(args.min_out_degree)
if args.max_out_degree is not None:
    graph.getNMaxOutDegree(args.max_out_degree)

args.topological_sort()
args.strongly_connected_component()
