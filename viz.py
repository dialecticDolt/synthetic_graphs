
import time

import numpy as np
import argparse

from synthetic.core import *

import networkx as nx
import pydot 
import matplotlib.image as mpimg
import io 
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph

import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Plot graph file')
parser.add_argument('--data', metavar='data', type=bool, default=False, help="Bool: whether to include data dependencies in plot")
parser.add_argument('-backend', metavar='backend', type=int, default=0, help='What plotting backed to use. networkx=0, pydot=1')
parser.add_argument('-graph', metavar='graph', type=str, help='the input graph file to run', required=True, default='graph/independent.gph')
parser.add_argument('-output', metavar='output', type=str, help='the output png file name', required=False, default='graph_output.png')
args = parser.parse_args()

def plot_graph_nx(depend_dict, data_dict):
    G = nx.DiGraph()

    dep_dict = depend_dict[0]

    for target, deps in dep_dict.items():
        for source in deps:
            G.add_edge(source, target, color='black')

    for target, deps in data_dict.items():
        for source in deps:
            G.add_edge(source, target, color='red')

    #nx.draw(G, with_labels=True, font_weight='bold')
    #plt.show()

    pg = nx.drawing.nx_pydot.to_pydot(G)
    
    png_str = pg.create_png(prog="dot")
    sio = io.BytesIO()
    sio.write(png_str)
    sio.seek(0)
    img = mpimg.imread(sio)

    implot = plt.imshow(img, aspect='equal')
    plt.show()

    pg.write_png(args.output)

    #A = to_agraph(G)
    #A.layout('dot')
    #A.draw('output.png')


def plot_graph_pydot(depend_dict, data_dict):
    G = pydot.Dot("graph", graph_type="graph")

    dep_dict = depend_dict[0]

    for target, deps in dep_dict.items():
        target = str(target)
        for source in deps:
            source = str(source)
            G.add_edge(pydot.Edge(source, target, color='black'))

    for target, deps in data_dict.items():
        target = str(target)
        for source in deps:
            source = str(source)
            G.add_edge(pydot.Edge(source, target, color='red'))

    #G.write_png("output.png")


if __name__ == '__main__':
    #Throwaway data information
    G = read_graph(args.graph)
    G.pop(0)
    depend_dict = convert_to_dict(G)
    data_dict = find_data_edges(depend_dict)
    
    #print(depend_dict)
    print(data_dict)

    plot_graph_nx(depend_dict, data_dict)


