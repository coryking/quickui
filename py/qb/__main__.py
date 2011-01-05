import sys
import getopt
import os

from project import Project

def main(argv):
    
    # Crack args
    try:                                
        opts, paths = getopt.getopt(argv, "chr", ["clean", "help", "rebuild"]) 
    except getopt.GetoptError:           
        usage()
        sys.exit(2)

    # Check options
    doBuild = True
    doClean = False
    for opt, arg in opts:
        if opt in ("-c", "--clean"):
            doBuild = False
            doClean = True
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        if opt in ("-r", "--rebuild"):
            doBuild = True
            doClean = True

    if (len(paths) == 0):
        # No projects explicitly listed; process current directory as a project.
        paths = [ os.getcwd() ]

    # Process projects
    for path in paths:
        project = Project(path)
        # TODO: Look for a build.qb file in the given folder
        if (doClean):
            project.clean()
        if (doBuild):
            project.build()

def usage():
    print("usage: qb [--clean | --rebuild] [project1] ... [projectN]")

if __name__ == "__main__":
    main(sys.argv[1:])
