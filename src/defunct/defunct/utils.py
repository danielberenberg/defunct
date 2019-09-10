#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
defunct utils
"""

def text_dumper(output_text, dump_station):
    """
    Dump a collection of text to the dump_station

    args:
        :output_text   (str) - text to write to disk
        :dump_station  (file object) - place to write
    returns:
        :None
    """
    dump_station.writelines(output_text)

def text_loader(load_station):
    """
    Load up text from the specified file buffer

    args:
        :load_station (file object)
    returns:
        :(str) - the text
    """
    return load_station.readlines()

