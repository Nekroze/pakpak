"""The packer performs the movements of a modpack as defined by a config."""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
import os


def CopyFilelistTo(filelist, destination):
    """Copy all files in filelist to the destination directory."""
    pass


def CompressFilelistTo(base, filelist, destination):
    """
    Copy the base to the destination and copy the contents of filelist into the
    destination.
    """
    pass


class Packer(object):
    """
    Stores the location of the mod database and output directories and can take
    a configuration file to retreive the correct mods and store them correctly
    in the output.
    """
    def __init__(self, mods, output, clientdata=None, serverdata=None):
        """
        Store mods database and output directories along with the client and
        server data lists which are added to the output for each.
        """
        self.mods = mods
        self.output = output
        self.clientdata = clientdata
        self.serverdata = serverdata

    def construct_client_modpack(self, base, additions=None):
        """
        Construct a modpack.jar with the given base and all additions added
        into the base.
        """
        CompressFilelistTo(base, additions,
                           os.path.join(self.output, "client/bin/modpack.jar"))

    def construct_client_mods(self, modlist=None):
        """Construct the mods for the client modpack."""
        CopyFilelistTo(modlist, os.path.join(self.output, "client/mods"))

    def construct_client_coremods(self, modlist=None):
        """Construct the coremods for the client modspack."""
        CopyFilelistTo(modlist, os.path.join(self.output, "client/coremods"))

    def construct_client_data(self):
        """Copy all client data over to the client output."""
        CopyFilelistTo(self.clientdata, os.path.join(self.output, "client/"))

    def construct_server_server(self, base, additions=None):
        """
        Construct a server.jar with the given base and all additions added
        into the base.
        """
        CompressFilelistTo(base, additions,
                           os.path.join(self.output, "server/server.jar"))

    def construct_server_launcher(self, command):
        """Construct the server launcher scripts."""
        with open(os.path.join(self.output, "server/start.bat") as bat:
                  bat.write(command)
        with open(os.path.join(self.output, "server/start.sh") as bash:
                  bash.write(command)

    def construct_server_mods(self, modlist=None):
        """Construct the mods for the server modpack."""
        CopyFilelistTo(modlist, os.path.join(self.output, "client/mods"))

    def construct_server_coremods(self, modlist=None):
        """Construct the coremods for the server modspack."""
        CopyFilelistTo(modlist, os.path.join(self.output, "client/mods"))

    def construct_server_data(self):
        """Copy all server data over to the server output."""
        CopyFilelistTo(self.clientdata, os.path.join(self.output, "server/"))
