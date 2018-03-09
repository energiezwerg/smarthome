# lib/env/init.py

import psutil
import socket

sh.env.core.version(sh.version, logic.lname)
#sh.env.core.start(sh.now())
sh.env.core.start(shtime.now(), logic.lname)

# hostname
hostname = socket.gethostname()
sh.env.system.name(hostname, logic.lname)

# system start
#start = sh.now() - datetime.timedelta(seconds=psutil.boot_time())
start = shtime.now() - datetime.timedelta(seconds=psutil.boot_time())
sh.env.system.start(start, logic.lname)
