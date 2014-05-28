#!/usr/bin/env python

import os
import sys
import tests
import unittest

sys.path.insert(0, os.path.dirname(__file__) + "/pybindxml")

loader = unittest.TestLoader()
tests = loader.discover("tests")
runner = unittest.runner.TextTestRunner(verbosity=2)
runner.run(tests)
 
