#!/usr/bin/python
import subprocess
import sys
import optparse

#For the MySQL version 5.7 and newer:

#start $launchctl load -F /Library/LaunchDaemons/com.oracle.oss.mysql.mysqld.plist
#stop $launchctl unload -F /Library/LaunchDaemons/com.oracle.oss.mysql.mysqld.plist

def run_db_action(proc):
    if proc == "start":
        subprocess.call('launchctl load -F /Library/LaunchDaemons/com.oracle.oss.mysql.mysqld.plist',shell=True)
        print("MySQL started successfully")
    elif proc == "stop":
        subprocess.call('launchctl unload -F /Library/LaunchDaemons/com.oracle.oss.mysql.mysqld.plist',shell=True)
        print("MySQL stopped successfully")
    else:
        print("error: give any mode")
    print("Thank you")

if __name__ == '__main__':

    args = sys.argv[1:]
    parser = optparse.OptionParser()

    parser.add_option("-a", "--action", dest="action", default='start', help="action - start, stop")

    (options, args) = parser.parse_args(args)
    if not options.action:
        parser.error('no action given')

    run_db_action(options.action)
