"""
The Modpack class stores all information required to construct a modpack.
"""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
from .packer import Packer
import os
from copy import copy


SKIPABLE = True


class InplaceList(object):
    """
    This is a simple wrapper around a list that allows it to only be added to
    one element at a time through inplace addition but allows iterative and
    indexed value retreival.
    """
    def __init__(self):
        """Initialize an empty list."""
        self.list = []
        self.checked = False

    def __iadd__(self, other):
        """Allow inplace addition of elements."""
        if isinstance(other, str):
            for line in other.split('\n'):
                line = line.strip()
                if line and not line.isspace():
                    if line[0] == '@':
                        if SKIPABLE:
                            self.list.append(os.path.join("@components",
                                                          line[1:]))
                    elif line[0] == '#':
                        pass
                    else:
                        self.list.append(os.path.join("components", line))

        elif isinstance(other, (list, set, tuple)):
            for line in other:
                line = line.strip()
                if line[0] == '@':
                    if SKIPABLE:
                        self.list.append(os.path.join("@components", line[1:]))
                if line[0] == '#':
                    pass
                else:
                    self.list.append(os.path.join("components", line))
        else:
            self.list.append(other)
        return self

    def __getitem__(self, index):
        """Retreive a specific value."""
        return self.list.__getitem__(index)

    def __getslice__(self, start, stop):
        """Retreive a slice of values."""
        return self.list.__getslice__(start, stop)

    def __iter__(self):
        """Return an iterator over each value."""
        return self.list.__iter__()

    def __len__(self):
        """Return the number of stored values."""
        return len(self.list)

    def __call__(self):
        """Verify each path in the list as existing files."""
        if self.checked:
            return self.list

        missing = False
        for index, path in enumerate(self.list):
            if path[0] == '@':
                if os.path.exists(path[1:]):
                    self.list[index] = path[1:]
                else:
                    print("[WARNING]Skipping file: {0}".format(path[1:]))
                    self.list[index] = None
            elif not os.path.exists(path):
                missing = True
                print("[ERROR]Missing file: {0}".format(path))

        if missing:
            exit(1)
        else:
            self.checked = True
            return self.list


class Modpack(object):
    """Modpack stores all types of data on how to construct the modpack."""
    def __init__(self, basemodpack, baseserver, output="build/"):
        self.mods = "components/"
        self.output = output
        self.modpack = InplaceList()
        self.server = InplaceList()
        self.universal_mods = InplaceList()
        self.universal_coremods = InplaceList()
        self.universal_data = InplaceList()
        self.client_mods = InplaceList()
        self.client_coremods = InplaceList()
        self.client_data = InplaceList()
        self.server_mods = InplaceList()
        self.server_coremods = InplaceList()
        self.server_data = InplaceList()
        self.server += baseserver
        self.modpack += basemodpack
        self.launcher = "java -server -Xmx2G -jar server.jar nogui"

    def construct(self, client=True, server=True):
        """Construct the modpack using a packer."""
        pack = Packer(self.mods, self.output,
                      self.client_data(), self.server_data())
        clientmods = self.client_mods()
        clientmods.extend(self.universal_mods())
        clientcoremods = self.client_coremods()
        clientcoremods.extend(self.universal_coremods())
        clientdata = self.client_data()
        clientdata.extend(self.universal_data())
        servermods = self.server_mods()
        servermods.extend(self.universal_mods())
        servercoremods = self.server_coremods()
        servercoremods.extend(self.universal_coremods())
        serverdata = self.server_data()
        serverdata.extend(self.universal_data())

        if client:
            pack.construct_client(copy(self.modpack()), copy(clientmods),
                                  copy(clientcoremods), copy(clientdata))

        if server:
            pack.construct_server(copy(self.server()), copy(servermods),
                                  copy(servercoremods), copy(serverdata),
                                  self.launcher)

    def skipable(self, value):
        global SKIPABLE
        SKIPABLE = value
