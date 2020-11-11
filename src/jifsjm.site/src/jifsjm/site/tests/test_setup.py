# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from jifsjm.site.testing import JIFSJM_SITE_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that jifsjm.site is properly installed."""

    layer = JIFSJM_SITE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if jifsjm.site is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'jifsjm.site'))

    def test_browserlayer(self):
        """Test that IJifsjmSiteLayer is registered."""
        from jifsjm.site.interfaces import (
            IJifsjmSiteLayer)
        from plone.browserlayer import utils
        self.assertIn(IJifsjmSiteLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = JIFSJM_SITE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['jifsjm.site'])

    def test_product_uninstalled(self):
        """Test if jifsjm.site is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'jifsjm.site'))

    def test_browserlayer_removed(self):
        """Test that IJifsjmSiteLayer is removed."""
        from jifsjm.site.interfaces import IJifsjmSiteLayer
        from plone.browserlayer import utils
        self.assertNotIn(IJifsjmSiteLayer, utils.registered_layers())
