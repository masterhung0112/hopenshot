#!/usr/bin/env python3

import sys

try:
    from classes import info
    print("Loaded modules from current directory: %s" % info.PATH)    
except ImportError:
    from openshot_qt.classes import info
    sys.path.append(info.PATH)
    print("Loaded modules from installed directory: %s" % info.PATH)

from classes.app import OpenShotApp
from classes.logger import log

def main():
    if "--version" in sys.argv:
        print("OpenShot version %s" % info.SETUP['version'])
        exit()

    log.info("------------------------------------------------")
    log.info("   OpenShot (version %s)" % info.SETUP['version'])
    log.info("------------------------------------------------")
        
    app = OpenShotApp(sys.argv)
    
    sys.exit(app.run())

if __name__ == "__main__":
    main()
