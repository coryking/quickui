import os
import shutil

class Project(object):
    '''
    A qb project: a collection of qui files that should be compiled and combined together.
    '''

    FILE_EXTENSION_QUI = ".qui"
    FILE_EXTENSION_JS = ".js"
    FILE_EXTENSION_CSS = ".css"
    BUILD_FOLDER_NAME = "build"
        
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.build_folder = os.path.join(path, self.BUILD_FOLDER_NAME)
        
    def build(self):
        '''
        Perform an incremental build of the project.
        '''
        print("Building")
        if (not os.path.exists(self.build_folder)):
            os.mkdir(self.build_folder)
        for filename in self.find_files():
            print(filename)
        
    def clean(self):
        '''
        Clean the project, including all compiled files and combined output files.
        '''
        print("Cleaning")
        if (os.path.exists(self.build_folder)):
            shutil.rmtree(self.build_folder)
            
    def find_files(self):
        results = []
        for path, directories, files in os.walk(self.path):
            results += [os.path.join(path, filename)
                        for filename in files if filename.endswith(self.FILE_EXTENSION_QUI)]
        return results

import unittest
class ProjectTests(unittest.TestCase):
    def test_clean(self):
        path = os.path.join(os.getcwd(), "tests")
        project = Project(path)
        project.build()
        buildFolderPath = os.path.join(path, "build")
        self.assertTrue(os.path.exists(buildFolderPath))
        project.clean()
        self.assertFalse(os.path.exists(buildFolderPath))