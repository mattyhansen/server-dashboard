#!/usr/bin/python3

### USAGE:
# sudo python monitor.py

### INSTALL:
#if no pip: command not found, install:
#sudo apt-get install python-dev
#sudo apt-get install python-pip
#sudo pip install psutil
#sudo pip install psutil --upgrade

### IMPORT
import os
import multiprocessing
import psutil #https://code.google.com/p/psutil/wiki/Documentation
import time
import json

# convert bytes to human readable
def bytes2human(n):
    symbols = ('KB', 'MB', 'GB', 'TB')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f %s' % (value, s)
    return '%.2f B' % (n)

# cpu percent usage
def cpu():
    return str(psutil.cpu_percent(interval=1)) + "%"

# ram usage
def ram():
    return bytes2human(psutil.virtual_memory().available)

# server load
def load():
    # print "Load Average: " + str(os.getloadavg()[0])
    return str(os.getloadavg()[0])

# cpu count
def cpu_count():
    return str(multiprocessing.cpu_count())

# network stats
def network_stats():
    pnic_before = psutil.net_io_counters(pernic=True)
    # sleep some time (one second)
    interval = 1
    time.sleep(interval)
    pnic_after = psutil.net_io_counters(pernic=True)
    # return stats
    stats = {}
    stats['before'] = pnic_before['eth1']
    stats['after'] = pnic_after['eth1']
    return stats

# network sent
def network_sent():
    stats = network_stats()
    bytes_sent = bytes2human(stats['after'].bytes_sent - stats['before'].bytes_sent) + '/s'
    return bytes_sent

# network received
def network_received():
    stats = network_stats()
    bytes_rcvd = bytes2human(stats['after'].bytes_recv - stats['before'].bytes_recv) + '/s'
    return bytes_rcvd

# free disk space
def disk_free():
    statvfs = os.statvfs('/')
    # Size of filesystem in bytes
    # disk_size = bytes2human(statvfs.f_frsize * statvfs.f_blocks)
    # Actual number of free bytes
    # disk_free = bytes2human(statvfs.f_frsize * statvfs.f_bfree)
    # Number of free bytes that ordinary users are allowed to use (excl. reserved space)
    disk_real_free = bytes2human(statvfs.f_frsize * statvfs.f_bavail)
    # print "Disk Usage: " + disk_size
    # print "Disk Usage: " + disk_free
    return disk_real_free

# disk used as percentage
def disk():
    vfs = os.statvfs('/')
    usedPercentage = 100.0 * float(vfs.f_blocks - vfs.f_bfree) / float(vfs.f_blocks - vfs.f_bfree + vfs.f_bavail)
    return '%.2f% %' % (usedPercentage)

# main
def main():
    try:
        while True:
            monitor_json = json.dumps({
                "cpu": cpu(),
                "ram": ram(),
                "load": load(),
                "cpu_count": cpu_count(),
                "network_sent": network_sent(),
                "network_received": network_received(),
                "disk": disk(),
                #"disk_free": disk_free(),
            })
            with open("monitor.json", "w") as text_file:
                text_file.write(monitor_json)
            # print monitor_json
            # print " "
            interval = 2
            time.sleep(interval)
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == '__main__':
    main()