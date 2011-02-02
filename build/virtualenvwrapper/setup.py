#!/usr/bin/env python

PROJECT = 'virtualenvwrapper'
VERSION = '2.5.3'

# Bootstrap installation of Distribute
import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages

from distutils.util import convert_path
from fnmatch import fnmatchcase
import os
import sys

try:
    long_description = open('README.txt', 'rt').read()
except IOError:
    long_description = ''

################################################################################
# find_package_data is an Ian Bicking creation.

# Provided as an attribute, so you can append to these instead
# of replicating them:
standard_exclude = ('*.py', '*.pyc', '*~', '.*', '*.bak', '*.swp*')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build',
                                './dist', 'EGG-INFO', '*.egg-info')

def find_package_data(
    where='.', package='',
    exclude=standard_exclude,
    exclude_directories=standard_exclude_directories,
    only_in_packages=True,
    show_ignored=False):
    """
    Return a dictionary suitable for use in ``package_data``
    in a distutils ``setup.py`` file.

    The dictionary looks like::

        {'package': [files]}

    Where ``files`` is a list of all the files in that package that
    don't match anything in ``exclude``.

    If ``only_in_packages`` is true, then top-level directories that
    are not packages won't be included (but directories under packages
    will).

    Directories matching any pattern in ``exclude_directories`` will
    be ignored; by default directories with leading ``.``, ``CVS``,
    and ``_darcs`` will be ignored.

    If ``show_ignored`` is true, then all the files that aren't
    included in package data are shown on stderr (for debugging
    purposes).

    Note patterns use wildcards, or can be exact paths (including
    leading ``./``), and all searching is case-insensitive.
    
    This function is by Ian Bicking.
    """

    out = {}
    stack = [(convert_path(where), '', package, only_in_packages)]
    while stack:
        where, prefix, package, only_in_packages = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        if show_ignored:
                            print >> sys.stderr, (
                                "Directory %s ignored by pattern %s"
                                % (fn, pattern))
                        break
                if bad_name:
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                    stack.append((fn, '', new_package, False))
                else:
                    stack.append((fn, prefix + name + '/', package, only_in_packages))
            elif package or not only_in_packages:
                # is a file
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        if show_ignored:
                            print >> sys.stderr, (
                                "File %s ignored by pattern %s"
                                % (fn, pattern))
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out
################################################################################
    

setup(
    name = PROJECT,
    version = VERSION,
    
    description = 'Enhancements to virtualenv',
    long_description = long_description,
    
    author = 'Doug Hellmann',
    author_email = 'doug.hellmann@gmail.com',

    url = 'http://www.doughellmann.com/projects/%s/' % PROJECT,
#     download_url = 'http://www.doughellmann.com/downloads/%s-%s.tar.gz' % \
#                     (PROJECT, VERSION),

    classifiers = [ 'Development Status :: 5 - Production/Stable',
                    'License :: OSI Approved :: BSD License',
                    'Programming Language :: Python',
                    'Intended Audience :: Developers',
                    'Environment :: Console',
                    ],

    platforms = ['Any'],

    scripts = ['virtualenvwrapper.sh', 
               ],

    provides=['virtualenvwrapper',
              'virtualenvwrapper.user_scripts',
              ],
    requires=['virtualenv'],

    namespace_packages = [ 'virtualenvwrapper' ],
    packages = find_packages(),
    include_package_data = True,
    # Scan the input for package information
    # to grab any data files (text, images, etc.) 
    # associated with sub-packages.
    package_data = find_package_data(PROJECT, 
                                     package=PROJECT,
                                     only_in_packages=False,
                                     ),

    entry_points = {
        #'console_scripts': [ 'venvw_hook = virtualenvwrapper.hook_loader:main' ],
        'virtualenvwrapper.initialize': [
            'user_scripts = virtualenvwrapper.user_scripts:initialize',
            ],
        'virtualenvwrapper.initialize_source': [
            'user_scripts = virtualenvwrapper.user_scripts:initialize_source',
            ],

        'virtualenvwrapper.pre_mkvirtualenv': [
            'user_scripts = virtualenvwrapper.user_scripts:pre_mkvirtualenv',
            ],
        'virtualenvwrapper.post_mkvirtualenv_source': [
            'user_scripts = virtualenvwrapper.user_scripts:post_mkvirtualenv_source',
            ],

        'virtualenvwrapper.pre_cpvirtualenv': [
            'user_scripts = virtualenvwrapper.user_scripts:pre_cpvirtualenv',
            ],
        'virtualenvwrapper.post_cpvirtualenv_source': [
            'user_scripts = virtualenvwrapper.user_scripts:post_cpvirtualenv_source',
            ],

        'virtualenvwrapper.pre_rmvirtualenv': [
            'user_scripts = virtualenvwrapper.user_scripts:pre_rmvirtualenv',
            ],
        'virtualenvwrapper.post_rmvirtualenv': [
            'user_scripts = virtualenvwrapper.user_scripts:post_rmvirtualenv',
            ],

        'virtualenvwrapper.pre_activate': [
            'user_scripts = virtualenvwrapper.user_scripts:pre_activate',
            ],
        'virtualenvwrapper.post_activate_source': [
            'user_scripts = virtualenvwrapper.user_scripts:post_activate_source',
            ],

        'virtualenvwrapper.pre_deactivate_source': [
            'user_scripts = virtualenvwrapper.user_scripts:pre_deactivate_source',
            ],
        'virtualenvwrapper.post_deactivate_source': [
            'user_scripts = virtualenvwrapper.user_scripts:post_deactivate_source',
            ],

        'virtualenvwrapper.get_env_details': [
            'user_scripts = virtualenvwrapper.user_scripts:get_env_details',
            ],
        },

    zip_safe=False,
    )
