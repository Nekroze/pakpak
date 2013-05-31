"""The packer performs the movements of a modpack as defined by a config."""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'
import os
import shutil
import zipfile


def ensure(directory):
    """Ensure that the given directory exists or make it recursively."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def copyfilelist(filelist, destination):
    """Copy all files in filelist to the destination directory."""
    ensure(destination)
    if filelist:
        for single in filelist:
            shutil.copy2(single, destination)


def compressfilelist(base, filelist, destination):
    """
    Copy the base to the destination and copy the contents of filelist into the
    destination.
    """
    ensure(os.path.dirname(destination))
    ensure(".tmp/")
    files = [base]
    if filelist:
        files.extend(filelist)
    for single in files:
        with zipfile.ZipFile(single, "r") as basezip:
            basezip.extractall(".tmp/")

    with zipfile.ZipFile(destination, "w") as destzip:
        for root, _, files in os.walk(".tmp/"):
            for single in files:
                path = os.path.join(root, single)
                arcpath = path.split(os.sep)[1:]
                arcpath = os.path.join(*arcpath)
                destzip.write(path, arcpath)
    shutil.rmtree(".tmp/")


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

    def construct_client(self, modpack, mods, coremods):
        """Construct the client modpack."""
        self.construct_client_modpack(modpack[0], modpack[1:])
        print "construct", mods
        self.construct_client_mods(mods)
        self.construct_client_coremods(coremods)
        self.construct_client_data()

    def construct_client_modpack(self, base, additions=None):
        """
        Construct a modpack.jar with the given base and all additions added
        into the base.
        """
        compressfilelist(base, additions,
                         os.path.join(self.output, "client/bin/modpack.jar"))

    def construct_client_mods(self, modlist=None):
        """Construct the mods for the client modpack."""
        copyfilelist(modlist, os.path.join(self.output, "client/mods"))

    def construct_client_coremods(self, modlist=None):
        """Construct the coremods for the client modspack."""
        copyfilelist(modlist, os.path.join(self.output, "client/coremods"))

    def construct_client_data(self):
        """Copy all client data over to the client output."""
        copyfilelist(self.clientdata, os.path.join(self.output, "client/"))

    def construct_server(self, server, mods, coremods, launcher):
        """Construct the client modpack."""
        self.construct_server_server(server[0], server[1:])
        self.construct_server_launcher(launcher)
        self.construct_server_mods(mods)
        self.construct_server_coremods(coremods)
        self.construct_server_data()

    def construct_server_server(self, base, additions=None):
        """
        Construct a server.jar with the given base and all additions added
        into the base.
        """
        compressfilelist(base, additions,
                         os.path.join(self.output, "server/server.jar"))

    def construct_server_launcher(self, command):
        """Construct the server launcher scripts."""
        with open(os.path.join(self.output, "server/start.bat"), 'w') as bat:
            bat.write(command)
        with open(os.path.join(self.output, "server/start.sh"), 'w') as bash:
            bash.write(command)

    def construct_server_mods(self, modlist=None):
        """Construct the mods for the server modpack."""
        copyfilelist(modlist, os.path.join(self.output, "client/mods"))

    def construct_server_coremods(self, modlist=None):
        """Construct the coremods for the server modspack."""
        copyfilelist(modlist, os.path.join(self.output, "client/mods"))

    def construct_server_data(self):
        """Copy all server data over to the server output."""
        copyfilelist(self.clientdata, os.path.join(self.output, "server/"))
