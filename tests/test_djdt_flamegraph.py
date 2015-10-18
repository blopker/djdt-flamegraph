"""
test_djdt_flamegraph
----------------------------------

Tests for `djdt_flamegraph` module.
"""

import unittest

from djdt_flamegraph import djdt_flamegraph
from djdt_flamegraph import FlamegraphPanel
from djdt_flamegraph import flamegraph


class TestDjdtFlamegraph(unittest.TestCase):

    def setUp(self):
        pass

    def test_subprocess(self):
        stack = 'unix`_sys_sysenter_post_swapgs;genunix`close 5'
        res = flamegraph.stats_to_svg(stack)
        self.assertIn('svg version="1.1"', res)

    def test_000_something(self):
        pass
