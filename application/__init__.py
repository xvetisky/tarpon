#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import json
import os

import appdirs

from application.docsets import Docset
import application.info


def ensure(path):
    """
    Ensures that a path exists by creating it if necessary.

    Note: ``os.makedirs()`` in Python 3 has the option ``exist_ok`` which will
    not throw an error if the directory already exist (making this function
    unnecessary). However, Python 2 has no such option.

    :type path: str
    :param path: path to be created if necessary
    :rtype: str
    :returns: input path (allowing functions like os.path.join to be wrapped)
    """
    if not os.path.exists(path):
        os.makedirs(path)
    return path


class Application:
    data_dir = ensure(appdirs.user_data_dir(appname=info.SHORT_NAME))
    cache_dir = ensure(appdirs.user_cache_dir(appname=info.SHORT_NAME))
    # log_dir = ensure(appdirs.user_log_dir(appname=info.SHORT_NAME))
    docsets = {}
    def __init__(self):
        search_paths = glob.glob(self.data_dir + "/*.docset")
        search_paths.extend(glob.glob(self.cache_dir + "/*.json"))
        self.load_docsets(search_paths)

    def load_docsets(self, paths):
        for path in paths:
            if path.endswith(".docset"):  # load from disk
                docset = Docset.frompath(path)
                self.docsets[docset.name] = docset
            elif path.endswith(".json"):  # load from cache files
                with open(path) as cache_file:
                    for name, url in json.load(cache_file).iteritems():
                        if name in self.docsets:
                            self.docsets[name].url = url
                        else:
                            self.docsets[name] = Docset(name, url=url)

    @property
    def docsets_on_disk(self):
        return filter(lambda x: x[1].on_disk, self.docsets.iteritems())
