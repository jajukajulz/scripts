#!/usr/bin/python
import os
import subprocess
import sys
import optparse

def run_tomcat_action(proc):
    #proc = input("Enter the mode :")
    #os.environ["JAVA_HOME"] = '/usr/lib/jvm/java-7-openjdk-amd64'
    #os.environ["CATALINA_HOME"] = '/export/apps/tomcat7'
    if proc == "start":
        os.getcwd()
        os.chdir("/Library/Tomcat/bin/")
        os.getcwd()
        subprocess.call('sh startup.sh',shell=True)
        print("Tomcat started successfully")
    elif proc == "stop":
        os.getcwd()
        os.chdir("/Library/Tomcat/bin/")
        os.getcwd()
        subprocess.call('sh shutdown.sh',shell=True)
        print("Tomcat stopped successfully")
    elif proc == "restart":
        os.getcwd()
        os.chdir("/Library/Tomcat/bin/")
        os.getcwd()
        subprocess.call('sh shutdown.sh',shell=True)
        subprocess.call('sh startup.sh',shell=True)
        print("tomcat restarted successfully")
    else:
        print("error: give any mode")
    print("Thank you")

if __name__ == '__main__':

    args = sys.argv[1:]
    parser = optparse.OptionParser()

    parser.add_option("-a", "--action", dest="action", default='start', help="action - start, stop or restart")

    (options, args) = parser.parse_args(args)
    if not options.action:
        parser.error('no action given')

    run_tomcat_action(options.action)
