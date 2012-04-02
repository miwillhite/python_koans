#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Based on AboutSandwichCode in the Ruby Koans
#

from runner.koan import *

import re  # For regular expression string comparisons
import os  # So I can make this run with watchr

class AboutWithStatements(Koan):
    def count_lines(self, file_name):
        try:
            f = open(file_name)
            try:
                count = 0
                for line in f.readlines():
                    count += 1
                return count
            finally:
                f.close()
        except IOError as e:
            # should never happen
            self.fail()
    
    def test_counting_lines(self):
        path = os.path.join(os.path.dirname(__file__), '..', "example_file.txt")
        self.assertEqual(4, self.count_lines(path))
    
    # ------------------------------------------------------------------
        
    def find_line(self, file_name):
        try:
            f = open(file_name)
            try:
                for line in f.readlines():
                    match = re.search('e', line)
                    if match:
                        return line
            finally:
                f.close()
        except IOError:
            # should never happen
            self.fail()
    
    def test_finding_lines(self):
        path = os.path.join(os.path.dirname(__file__), '..', "example_file.txt")
        self.assertEqual('test\n', self.find_line(path))
    
    ## ------------------------------------------------------------------
    ## THINK ABOUT IT:
    ##
    ## The count_lines and find_line are similar, and yet different.
    ## They both follow the pattern of "sandwich code".
    ##
    ## Sandwich code is code that comes in three parts: (1) the top slice
    ## of bread, (2) the meat, and (3) the bottom slice of bread.  The
    ## the bread part of the sandwich almost always goes together, but
    ## the meat part changes all the time.
    ##
    ## Because the changing part of the sandwich code is in the middle,
    ## abstracting the top and bottom bread slices to a library can be
    ## difficult in many languages.
    ##
    ## (Aside for C++ programmers: The idiom of capturing allocated
    ## pointers in a smart pointer constructor is an attempt to deal with
    ## the problem of sandwich code for resource allocation.)
    ##
    ## Python solves the problem using Context Managers. Consider the
    ## following code:
    ##
    
    class FileContextManager():
        def __init__(self, file_name):
            self._file_name = file_name
            self._file = None
        
        def __enter__(self):
            self._file = open(self._file_name)
            return self._file
        
        def __exit__(self, cls, value, tb):
            self._file.close()
    
    # Now we write:
    
    def count_lines2(self, file_name):
        with self.FileContextManager(file_name) as f:
            count = 0
            for line in f.readlines():
                count += 1
        return count
    
    def test_counting_lines2(self):
        path = os.path.join(os.path.dirname(__file__), '..', "example_file.txt")
        self.assertEqual(4, self.count_lines2(path))
    
    # ------------------------------------------------------------------
    
    def find_line2(self, file_name):
        with self.FileContextManager(file_name) as f:
            for line in f.readlines():
                match = re.search('e', line)
                if match:
                    return line
    
    def test_finding_lines2(self):
        path = os.path.join(os.path.dirname(__file__), '..', "example_file.txt")
        self.assertEqual('test\n', self.find_line2(path))
        self.assertNotEqual(None, self.find_line2(path))
    
    # ------------------------------------------------------------------
    
    def count_lines3(self, file_name):
        with open(file_name) as f:
            count = 0
            for line in f.readlines():
                count += 1
            return count
    
    def test_open_already_has_its_own_built_in_context_manager(self):
        path = os.path.join(os.path.dirname(__file__), '..', "example_file.txt")
        self.assertEqual(4, self.count_lines3(path))
