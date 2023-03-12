# 

from __future__ import print_function
from __future__ import absolute_import

import m5

class BaseTopology(object):
    description = "BaseTopology"

    def __init__(self):
        """ When overriding place any objects created in
            configs/ruby/<protocol>.py that are needed in
            makeTopology (below) here. The minimum is usually
            all of the controllers created in the above file.
        """

    def makeTopology(self, options, network, IntLink, ExtLink, Router):
        """ Called from configs/ruby/Ruby.py
            The return value is ( list(Router), list(IntLink), list(ExtLink))
            The API of this function cannot change when subclassing!!
            Any additional information needed to create this topology should
            be passed into the constructor when it's instantiated in
            configs/ruby/<protocol>.py
        """
        m5.util.fatal("BaseTopology should have been overridden!!")

    def registerTopology(self, options):
        """ Called from configs/ruby/Ruby.py
            There is no return value. This should only be called in
            SE mode. It is used by some topology objects to populate
            the faux filesystem with accurate file contents.
            No need to implement if not using FilesystemRegister
            functionality.
        """

class SimpleTopology(BaseTopology):
    """ Provides methods needed for the topologies included in Ruby before
        topology changes.
        These topologies are "simple" in the sense that they only use a flat
        list of controllers to construct the topology.
    """
    description = "SimpleTopology"

    def __init__(self, controllers):
        self.nodes = controllers

    def addController(self, controller):
        self.nodes.append(controller)

    def __len__(self):
        return len(self.nodes)
