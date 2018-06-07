import argparse
import sys
import django
import os
from django.test.runner import DiscoverRunner
from django.core import management

class MezzoTestsRunner(DiscoverRunner):
	
	
	def __init__(self, pattern=None, top_level=None, verbosity=1,
                 interactive=True, failfast=False, keepdb=True,
                 reverse=False, debug_mode=False, debug_sql=False, parallel=0,
                 tags=None, exclude_tags=None, **kwargs):

		if kwargs['front']:
			pattern='tests_front.py'
		if kwargs['back']:
			pattern='tests.py'
		super(MezzoTestsRunner,self).__init__(keepdb=not kwargs['destroydb'],pattern=pattern)

	def run_tests(self, test_labels, extra_tests=None, **kwargs):
		if not test_labels:
			test_labels+=('organization','/srv/lib/mezzanine-organization/')
			test_labels+=('agenda','/srv/lib/mezzanine-agenda/')
			test_labels+=('cartridge','/srv/lib/cartridge/')
			test_labels+=('mezzanine','/srv/lib/mezzanine/')
		super(MezzoTestsRunner,self).run_tests(test_labels,extra_tests, **kwargs)
	
	@classmethod
	def add_arguments(cls, parser):
		parser.add_argument('--front' , help="Only run front tests (selenium)",action="store_true")		
		parser.add_argument('--back' , help="Only run back tests (faster)",action="store_true")		
		parser.add_argument("--destroydb",help="Execute test on a new database (may be very long).",action="store_true")
		super(MezzoTestsRunner,cls).add_arguments(parser)
