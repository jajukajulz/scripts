# check for patched source code files with a specific extension

import os
import logging
import sys
import optparse

def run_check(path_to_check, extension):
    for root, dirs, files in os.walk(path_to_check):
        for file in files:
            if file.endswith(extension):
                 print(os.path.join(root, file))

if __name__ == '__main__':

    args = sys.argv[1:]
    parser = optparse.OptionParser('usage: python %prog --path <path> --loglevel <loglevel> '
                                   'e.g. python %prog --path "/Users/juliank/dev/utils" --ext ".py"  --loglevel DEBUG')

    parser.add_option("-p", "--path", dest="path", default='C:/Program Files (x86)/appname', help="The top level directory to check for py files")
    parser.add_option("-e", "--ext", dest="ext", default='.py', help="The file extension to look for")
    parser.add_option("", "--loglevel", type="string", dest="loglevel", default="info",
                      help="Logging level. Options are: notset, debug, info, warn, error, fatal.")

    (options, args) = parser.parse_args(args)
    try:
        loglevel = getattr(logging, options.loglevel.upper())
        logging.getLogger().setLevel(loglevel)
    except AttributeError:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.error("Unknown logging level '%s', switching to DEBUG loglevel." % options.loglevel)

    logging.info("Checking started - " + options.path + " " + options.ext)

    run_check(options.path, options.ext)

    logging.info("Checking finished")
