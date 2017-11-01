# lib/env/init.py

import uptime
import socket

sh.env.core.version(sh.version)
sh.env.core.start(sh.now())

# hostname
hostname = socket.gethostname()
sh.env.system.name(hostname)

# system start
uptime = uptime.uptime()
start = sh.now() - datetime.timedelta(seconds=uptime)
sh.env.system.start(start)
