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


def copydirectory(root_src_dir, root_dst_dir):
    """Copy one directory to another location and overwrite."""
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir)
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy2(src_file, dst_dir)


def copyfilelist(filelist, destination):
    """Copy all files in filelist to the destination directory."""
    ensure(destination)
    if filelist:
        for single in [path for path in filelist if path is not None]:
            if os.path.isdir(single):
                copydirectory(single,
                              os.path.join(destination,
                                           single.split(os.sep)[-1]))
            else:
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
        files.extend([path for path in filelist if path is not None])
    for single in files:
        with zipfile.ZipFile(single, "r") as basezip:
            for member in basezip.namelist():
                path = os.path.join(".tmp", member)
                if member.endswith('/') and not os.path.exists(path):
                    os.makedirs(path)
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

    def construct_client(self, modpack, mods, coremods, data):
        """Construct the client modpack."""
        path = os.path.join(self.output, "client")
        if os.path.exists(path):
            shutil.rmtree(path)
        self.construct_client_modpack(modpack[0], modpack[1:])
        self.construct_client_mods(mods)
        self.construct_client_coremods(coremods)
        self.construct_client_data(data)

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

    def construct_client_data(self, data):
        """Copy all client data over to the client output."""
        copyfilelist(data, os.path.join(self.output, "client/"))

    def construct_server(self, server, mods, coremods, data, launcher):
        """Construct the client modpack."""
        path = os.path.join(self.output, "server")
        if os.path.exists(path):
            shutil.rmtree(path)
        self.construct_server_server(server[0], server[1:])
        self.construct_server_launcher(launcher)
        self.construct_server_mods(mods)
        self.construct_server_coremods(coremods)
        self.construct_server_data(data)

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
        copyfilelist(modlist, os.path.join(self.output, "server/mods"))

    def construct_server_coremods(self, modlist=None):
        """Construct the coremods for the server modspack."""
        copyfilelist(modlist, os.path.join(self.output, "server/coremods"))

    def construct_server_data(self, data):
        """Copy all server data over to the server output."""
        copyfilelist(data, os.path.join(self.output, "server/"))
