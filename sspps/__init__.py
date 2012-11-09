import logging
import collections
import os
import sys

class Plugin(object):
    '''Base class for all plugins
       to create a plugin, subclass this and place in the plugins
       directory.'''

    enabled = True # Set to false in subclasses to disable that plugin

    def activate(self):
        '''Called after plugin is loaded but before added to event
           loop'''
        pass

    def deactivate(self):
        '''Called before plugin is unloaded'''
        pass

class PluginLoader(object):
    def __init__(self, plugins_dir, parent_class=Plugin):
        self.plugins_dir = plugins_dir
        self.parent_class = parent_class
        if self.plugins_dir[-1:] != '/':
            self.plugins_dir += '/'
        self.plugins = collections.deque()

    def load_all(self):
        logging.debug('Starting plugin loading')
        plugins_dir = os.listdir(self.plugins_dir)
        found_driver = False
        if self.plugins_dir not in sys.path:
            sys.path.insert(0, self.plugins_dir)
        for poss_plugin in plugins_dir:
            full_path = self.plugins_dir + poss_plugin
            if poss_plugin[-3:] == '.py':
                logging.debug('loading %s' % full_path)
                module=__import__(poss_plugin[:-3])
                mod_dict = module
            elif os.path.isdir(full_path) and os.path.isfile(full_path+'/__init__.py'):
                module=__import__(poss_plugin)
                mod_dict = module
            else:
                logging.debug('skipping %s due to invalid path (No __init__.py or not .py)' % full_path)
                continue
            mod_dict = mod_dict.__dict__
            self.plugins = []
            for key, value in mod_dict.items():
                try:
                    is_subclass = issubclass(value, self.parent_class)
                except TypeError:
                    continue
                if is_subclass:
                    try:
                        enabled = value.enabled
                    except AttributeError:
                        enabled = True

                    if enabled:
                        try:
                            is_driver = value.driver
                        except AttributeError:
                            is_driver = False

                        if is_driver:
                            if found_driver:
                                logging.error("More than one driver detected. Exiting.")
                                sys.exit(1)
                            found_driver = True
                                
                        logging.debug('Initializing %s' % value.__name__)
                        instance = value()
                        instance.activate()
                        self.plugins.append(instance)
                    else:
                        logging.debug('Skipping %s, not enabled' % value.__name__)
            
        logging.debug('Finished plugin loading')

