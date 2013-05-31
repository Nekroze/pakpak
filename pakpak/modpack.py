"""
The Modpack class stores all information required to construct a modpack.
"""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
from .packer import Packer
import os


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
                    self.list.append(os.path.join("mods", line.strip()))
        elif isinstance(other, (list, set, tuple)):
            for data in other:
                self.list.append(os.path.join("mods", data))
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


class Modpack(object):
    """Modpack stores all types of data on how to construct the modpack."""
    def __init__(self, basemodpack, baseserver, output="build/"):
        self.mods = "mods/"
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
        self.server.list += baseserver
        self.modpack.list += basemodpack
        self.launcher = "java -server -Xmx1024M -jar server.jar nogui"

    def check_files(self):
        """Check if all specified files exist."""
        files = self.modpack.list
        files.extend(self.server.list)
        files.extend(self.universal_mods.list)
        files.extend(self.universal_coremods.list)
        files.extend(self.universal_data.list)
        files.extend(self.client_mods.list)
        files.extend(self.client_coremods.list)
        files.extend(self.client_data.list)
        files.extend(self.server_mods.list)
        files.extend(self.server_coremods.list)
        files.extend(self.server_data.list)
        missing = False
        for single in files:
            if not os.path.exists(single):
                missing = True
                print("[ERROR]Missing file: {0}".format(single))
        if missing:
            exit(1)

    def construct(self, client=True, server=True):
        """Construct the modpack using a packer."""
        self.check_files()
        pack = Packer(self.mods, self.output,
                      self.client_data.list, self.server_data.list)
        clientmods = self.client_mods.list
        clientmods.extend(self.universal_mods.list)
        clientcoremods = self.client_coremods.list
        clientcoremods.extend(self.universal_coremods.list)
        servermods = self.server_mods.list
        servermods.extend(self.universal_mods.list)
        servercoremods = self.server_coremods.list
        servercoremods.extend(self.universal_coremods.list)

        if client:
            pack.construct_client(self.modpack.list, clientmods,
                                  clientcoremods)

        if server:
            pack.construct_server(self.server.list, servermods,
                                  servercoremods, self.launcher)
