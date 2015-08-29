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

# print cpu usage
def cpu():
    print "CPU Usage: " + str(psutil.cpu_percent(interval=1)) + "%"

# print ram
def ram():
    print "Free RAM: " + bytes2human(psutil.virtual_memory().available)

# print load
def load():
    # print "Load Average: " + str(os.getloadavg()[0])
    print "Load Average: " + str(os.getloadavg()[0]) + " (" + str(multiprocessing.cpu_count()) + " CPUs)"

# print network
def network():
    pnic_before = psutil.net_io_counters(pernic=True)
    # sleep some time (one second)
    interval = 1
    time.sleep(interval)
    pnic_after = psutil.net_io_counters(pernic=True)
    stats_before = pnic_before['eth1']
    stats_after = pnic_after['eth1']
    bytes_sent = bytes2human(stats_after.bytes_sent - stats_before.bytes_sent) + '/s'
    bytes_rcvd = bytes2human(stats_after.bytes_recv - stats_before.bytes_recv) + '/s'
    print "Network: " + bytes_sent + " sent"
    print "Network: " + bytes_rcvd + " received"

# print disk
def disk():
    statvfs = os.statvfs('/')
    # Size of filesystem in bytes
    # disk_size = bytes2human(statvfs.f_frsize * statvfs.f_blocks)
    # Actual number of free bytes
    # disk_free = bytes2human(statvfs.f_frsize * statvfs.f_bfree)
    # Number of free bytes that ordinary users are allowed to use (excl. reserved space)
    disk_real_free = bytes2human(statvfs.f_frsize * statvfs.f_bavail)
    # print "Disk Usage: " + disk_size
    # print "Disk Usage: " + disk_free
    print "Disk Usage: " + disk_real_free

# main
def main():
    try:
        while True:
            cpu()
            ram()
            load()
            network()
            disk()
            print " "
            interval = 10
            time.sleep(interval)
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == '__main__':
    main()