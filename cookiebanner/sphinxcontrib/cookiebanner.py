#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sphinx.errors import ExtensionError


def add_cb_javascript(app, pagename, templatename, context, doctree):
    if not app.config.cookiebanner_enabled:
        return
    
    # Embed code into the header, using the "metatags" space.
    headercode = """
       <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/cookieconsent@3/build/cookieconsent.min.css" />
    """
    context['metatags'] += headercode
    
    # Embed code into the body, using the "body" space.
    bodycode = """
       <script src="https://cdn.jsdelivr.net/npm/cookieconsent@3/build/cookieconsent.min.js" data-cfasync="false"></script>
       <script>
          window.cookieconsent.initialise({
             "palette": {
                "popup": {
                   "background": "#000000",
                   "text": "#ffffff"
                },
                "button": {
                   "background": "#ffffff",
                   "text": "#000000"
                }
             },
             "theme": "classic",
             "position": "top",
             "content": {
                "message": "This website uses cookies to improve user experience. By using our website you consent to all cookies in accordance with the &lt;i&gt;FIRST&lt;/i&gt; Privacy Policy.",
                "href": "https://www.firstinspires.org/about/privacy-policy"
             }
          });
       </script>
    """
    context['body'] += bodycode

def setup(app):
    app.add_config_value('cookiebanner_enabled', True, 'html')
    app.connect('html-page-context', add_cb_javascript)

