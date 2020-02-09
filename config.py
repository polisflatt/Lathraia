import func
import Server.configuration

# There's not too much here.
# The directory will be created if it does not already exist.
build_dir = "builds/"



# You do not need to worry about this, unless you're doing translations.
options_menu = """
[0]: Client
[1]: Server
"""

client_options_menu = """
[0]: Launch the client (you need to know the IP Address and the callsign (user) you're looking for!)
[1]: Launch the listener. You need this to find out who's currently online and what their IP and callsign is.
[2]: Help!
"""

client_help = """
This is the client menu. You may choose 0-2 in order to select an option.
You need to open the listener first, in order to select who you wish to connect to, then you will launch the client and do whatever from there.
Additionally, if you already know the IP of the server, you may run Client/main.py with the args IP and CALLSIGN, since this program is modular.
"""

server_options_menu = """
[0]: Package Server (build it, in other words)
[1]: Help!
"""

server_builder_text = """
Welcome to the Lathraia server builder - where you can compile a stub that can neatly run!
This is not like the traditional server builder. You are not configuring anything here.

In order to use the server, you need to configure it. Head into the Server/ folder, and look in
configuration.py and constants.py and then head back here.
"""

server_help_text = """
This is the server menu. You may choose to build and compress the server here, into a simple file.
As of now, the only method of compression made avaliable is through ZIP (namely, zipapp).
You need to configure the server to your needs before you use/make it. You also need to configure the client.
The configuration files can be found at Server/configuration.py and Client/conf.py.
"""

server_information_text = """
Version: {version}
Callsign: {callsign}
IP Address is: {ip}
Port is: {port}
Data port is: {data_port}
Video port is: {video_port}
Audio port is: {audio_port}
"""