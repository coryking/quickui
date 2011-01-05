import os
from project import Project

class BuildUnit(object):
    '''
    Relates a QuickUI source file with its correspdonding generated JS and CSS output.
    '''
    
    def __init__(self, path_qui, path_build):
        basename = os.path.splitext(os.path.basename(path_qui))[0]
        self.filename_js = basename + Project.FILE_EXTENSION_JS
        self.filename_css = basename + Project.FILE_EXTENSION_CSS

import unittest
class BuildUnitTests(unittest.TestCase):
    def test_names(self):
        unit = BuildUnit("/project/Foo.qui", "/project/build")
        self.assertEqual("Foo.js", unit.filename_js)
        self.assertEqual("Foo.css", unit.filename_css)
