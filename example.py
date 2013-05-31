from pakpak import Modpack

forge = "minecraftforge-universal-1.5.2-7.8.0.716.zip"

test = Modpack(forge,
               "minecraft_server.jar")
test.server += forge
#test.universal_mods += "mca.zip"

test.construct(server=False)
