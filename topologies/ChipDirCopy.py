from __future__ import print_function
from __future__ import absolute_import

from m5.params import *
from m5.objects import *

from topologies.BaseTopology import SimpleTopology


class ChipDirCopy(SimpleTopology):
    description = 'ChipDirCopy'

    def __init__(self, controllers):
        self.nodes = controllers

    def makeTopology(self, options, network, IntLink, ExtLink, Router):
        nodes = self.nodes

        # default values for link latency and router latency.
        # Can be over-ridden on a per link/router basis
        link_latency = options.link_latency  # used by simple and garnet
        router_latency = options.router_latency  # only used by garnet

        # chip1
        routers = [Router(router_id=i, latency=router_latency)
                   for i in range(len(nodes))]
        network.routers = routers

        # First determine which nodes are cache cntrls vs. dirs vs. dma
        cache_nodes = []
        dir_nodes = []
        dma_nodes = []
        for node in nodes:
            if node.type == 'L1Cache_Controller' or \
                    node.type == 'L2Cache_Controller':
                cache_nodes.append(node)
            elif node.type == 'Directory_Controller':
                dir_nodes.append(node)
            elif node.type == 'DMA_Controller':
                dma_nodes.append(node)

        link_count = 0
        cache_router_count = 0

        ext_links = []
        for (i, n) in enumerate(cache_nodes):
            ext_links.append(ExtLink(link_id=link_count, ext_node=n,
                                     int_node=routers[i], latency=link_latency))
            link_count += 1
            cache_router_count += 1

        dir_router = 0
        for (i, n) in enumerate(dir_nodes):
            ext_links.append(ExtLink(link_id=link_count, ext_node=n,
                                     int_node=routers[dir_router], latency=link_latency))
            link_count += 1
            dir_router += 2

        dma_router = 0

        for (i, n) in enumerate(dma_nodes):
            ext_links.append(ExtLink(link_id=link_count, ext_node=n,
                                     int_node=routers[dma_router], latency=link_latency))
            dma_router += 1
            link_count += 1

        network.ext_links = ext_links

        link_count = len(nodes)
        int_links = []
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                if (i != j):
                    link_count += 1
                    int_links.append(IntLink(link_id=link_count,
                                             src_node=routers[i],
                                             dst_node=routers[j],
                                             latency=link_latency))

        network.int_links = int_links
