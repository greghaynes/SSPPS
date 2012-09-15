SSPS
====

A super simple plugin system for python

Installing
----------

pip install ssps


Using
-----

Load plugins from directory 'plugins':
<pre><code>import ssbs

pl = ssbs.PluginLoader('plugins')
pl.load_all() </code></pre>

Create a plugin by putting a module in plugins directory:
<pre><code>import ssbs

class MyPlugin(ssbs.Plugin):
    enabled = True
    def __init__(self):
        print 'init!'
    def activate(self):
        print 'Activated!' </code></pre>
