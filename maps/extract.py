#!/usr/bin/env python3

import sys
import argparse

import osmnx as ox

# %matplotlib inline
ox.config(log_file=True, log_console=True, use_cache=True)


def save_shp(centre, distance=1000, name=None):
    if name is not None:
        place_name = name
    else:
        place_name = '%s-%s' % centre

    G = ox.graph_from_point(centre, network_type='walk', distance=distance, simplify=False)
    fig, ax = ox.plot_graph(G, node_color='b', node_zorder=3)

    G2 = G.copy()
    G2 = ox.simplify_graph(G2)
    # fig, ax = ox.plot_graph(G)

    # project the network to an appropriate UTM (automatically determined)
    G_projected = ox.project_graph(G2)
    # ox.save_graphml(G_projected, filename='worthing.graphml')
    ox.save_load.save_graph_shapefile(G2, filename='%s.shp' % place_name, folder=None, encoding='utf-8')

    # print ox.basic_stats(G)

    # ec = ox.get_edge_colors_by_attr(G_projected, attr='length')
    # ox.plot_graph(G_projected, edge_color=ec)

    # you can also plot/save figures as SVGs to work with in Illustrator later
    # fig, ax = ox.plot_graph(G_projected, save=True, file_format='svg')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", type=float, help="Start latitude")
    parser.add_argument("--lon", type=float, help="Start longitude")
    parser.add_argument("--name", type=str, help="Name")
    parser.add_argument("--distance", help="Map distance meters",
        type=float, default=1000)
    args = parser.parse_args()

    save_shp((args.lat, args.lon), distance=args.distance, name=args.name)
