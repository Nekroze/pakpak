"""
The Modpack class stores all information required to construct a modpack.
"""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
from .packer import Packer


class InplaceList(object):
    """
    This is a simple wrapper around a list that allows it to only be added to
    one element at a time through inplace addition but allows iterative and
    indexed value retreival.
    """
    def __init__(self):
        """Initialize an empty list."""
        self.list = []

    def __iadd__(self, other):
        """Allow inplace addition of elements."""
        if isinstance(other, str):
            for line in other.split('\n'):
                if line and not line.isspace():
                    self.list.append(line.strip())
        elif isinstance(other, (list, set, tuple)):
            for data in other:
                self.list.append(data)
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


def Modpack(object):
    """Modpack stores all types of data on how to construct the modpack."""

    def __init__(self, basemodpack, baseserver, mods="mods/", output="build/"):
        self.mods = mods
        self.output = output
        self.modpack = InplaceList()
        self.server = InplaceList()
        self.universal_mods = InplaceList()
        self.universal_coremods = InplaceList()
        self.client_mods = InplaceList()
        self.client_coremods = InplaceList()
        self.server_mods = InplaceList()
        self.server_coremods = InplaceList()
        self.client_data = InplaceList()
        self.server_data = InplaceList()
        self.server += baseserver
        self.modpack += basemodpack
        self.launcher = "java -server -Xmx1024M -jar server.jar nogui"

    def construct(self, client=True, server=True):
        """Construct the modpack using a packer."""
        pack = Packer(self.mods, self.output,
                      self.client_data, self.server_data)
        clientmods = self.client_mods.list + self.universal_mods
        clientcoremods = self.client_coremods.list + self.universal_coremods
        servermods = self.server_mods.list + self.universal_mods
        servercoremods = self.server_coremods.list + self.universal_coremods

        if client:
            pack.construct_client(self.modpack, clientmods, clientcoremods)

        if server:
            pack.construct_server(self.modpack, servermods, servercoremods,
                                  self.launcher)
