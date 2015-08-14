#!/bin/python
# -*- coding=utf-8 -*-
import json
from collections import namedtuple


def loadfromjson(j):
    return json.loads(j)


class Journal(object):
    def __init__(self):
        self.entries = []
    def append(self, e):
        self.entries.append(e)

    def getTAccount(self, title):
        dr = {}
        cr = {}
        for e in self.entries:
            for t, v  in e["debit"].items():
                if t == title:
                    dr[e['date']] = v
            for t, v  in e["credit"].items():
                if t == title:
                    cr[e['date']] = v
        return dr, cr


