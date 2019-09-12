#!/usr/bin/python
import subprocess
import sys
import optparse

#Usage: /etc/init.d/postgresql {start|stop|restart|reload|force-reload|status} [version ...]
def run_postgres_action(proc):
    if proc == "start":
        subprocess.call('pg_ctl -D /usr/local/var/postgres start',shell=True)
        print("Postgres started successfully")
    elif proc == "stop":
        subprocess.call('pg_ctl -D /usr/local/var/postgres stop',shell=True)
        print("Postgres stopped successfully")
    elif proc == "restart":
        subprocess.call('pg_ctl -D /usr/local/var/postgres restart',shell=True)
        print("Postgres restarted successfully")
    else:
        print("error: give any mode")
    print("Thank you")

if __name__ == '__main__':

    args = sys.argv[1:]
    parser = optparse.OptionParser()

    parser.add_option("-a", "--action", dest="action", default='start', help="action - start, stop, restart, reload, force-reload, status}")

    (options, args) = parser.parse_args(args)
    if not options.action:
        parser.error('no action given')

    run_postgres_action(options.action)
