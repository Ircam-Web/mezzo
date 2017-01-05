# -*- coding: utf-8 -*-
try:
    from local_settings import *
except ImportError:
    pass
# Test runner with no database creation
TEST_RUNNER = 'organization.core.tests.NoDbTestRunner'
