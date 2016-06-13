#!/usr/bin/env python

#############################################################################
##
# This file is part of Taurus
##
# http://taurus-scada.org
##
# Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
# Taurus is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# Taurus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
##
# You should have received a copy of the GNU Lesser General Public License
# along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################

"""
This module defines the test suite for the whole Taurus package
Usage::

  from taurus.test import testsuite
  testsuite.run()

"""

__docformat__ = 'restructuredtext'

import os
from taurus.external import unittest
import taurus

def get_suite():
    loader = unittest.defaultTestLoader
    start_dir = os.path.dirname(taurus.__file__)
    return loader.discover(start_dir, top_level_dir=os.path.dirname(start_dir))

def run(disableLogger=True):
    """Runs all tests for the taurus package"""
    # disable logging messages
    if disableLogger:
        taurus.disableLogOutput()
    # discover all tests within the taurus/lib directory
    suite = get_suite()
    # use the basic text test runner that outputs to sys.stderr
    runner = unittest.TextTestRunner(descriptions=True, verbosity=2)
    # run the test suite
    return runner.run(suite)


if __name__ == '__main__':
    import sys
    from taurus.external import argparse
    parser = argparse.ArgumentParser(description='Main test suite for Taurus')
    parser.add_argument('--skip-gui-tests', dest='skip_gui',
                        action='store_true', default=False,
                        help='Do not perform tests requiring GUI')
    args = parser.parse_args()

    if args.skip_gui:
        import taurus.test.skip
        taurus.test.skip.GUI_TESTS_ENABLED = False
    ret = run()

    # calculate exit code (0 if OK and 1 otherwise)
    if ret.wasSuccessful():
        exit_code = 0
    else:
        exit_code = 1
    sys.exit(exit_code)
