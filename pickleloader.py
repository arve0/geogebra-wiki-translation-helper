#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
File: pickleloader.py
Author: Arve Seljebu
Email: arve.seljebu@gmail.com
Github: arve0
Description: Loads data from pickle.
"""


import pickle


def main():
    """ Runs upon script execution """
    file_ = open('data/pages-en.pickle')
    pages = pickle.load(file_)
    file_.close()

    for page in pages:
        print page['title']


if __name__ == '__main__':
    main()
