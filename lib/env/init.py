# lib/env/init.py

import psutil
import socket

sh.env.core.version(sh.version)
sh.env.core.start(sh.now())

# hostname
hostname = socket.gethostname()
sh.env.system.name(hostname)

# system start
start = sh.now() - datetime.timedelta(seconds=psutil.boot_time())
sh.env.system.start(start)
