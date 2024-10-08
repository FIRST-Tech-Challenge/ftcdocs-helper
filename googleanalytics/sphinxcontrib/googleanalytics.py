#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sphinx.errors import ExtensionError


def add_ga_javascript(app, pagename, templatename, context, doctree):

    # Do this regardless of whether this module is enabled or disabled
    metatags = context.get('metatags', '')
    metatags += """ <meta name="google-site-verification" content="75RBwHq1pWFvK2E7wuVgAeq_LOOJrU4q1wRIjXqPpqg" /> """
    context['metatags'] = metatags
    
    if not app.config.googleanalytics_enabled:
        metatags = context.get('metatags', '')
        metatags += """ <!-- Google Analytics Intentionally Disabled --> """
        context['metatags'] = metatags
        return

    metatags = context.get('metatags', '')
    metatags += """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>""" % app.config.googleanalytics_id
    metatags += """
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', '%s');
    </script>
    """ % app.config.googleanalytics_id
    context['metatags'] = metatags


def check_config(app):
    if not app.config.googleanalytics_id and app.config.googleanalytics_enabled == True:
        raise ExtensionError("'googleanalytics_id' config value must be set for ga statistics to function properly.")


def setup(app):
    app.add_config_value('googleanalytics_id', '', 'html')
    app.add_config_value('googleanalytics_enabled', True, 'html')
    app.connect('html-page-context', add_ga_javascript)
    app.connect('builder-inited', check_config)

