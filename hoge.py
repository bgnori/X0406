#!/bin/python
#-*- coding=utf-8 -*-
import sys
import re
import json

DEBUG = False

x = re.compile("(?P<IsValuationAccountCode>\()?(?P<AccountCode>\d\d\d\d)\)?,(?P<rest>.+)")

start_end = re.compile("\[(?P<start>\d\d\d\d)-(?P<end>\d\d\d\d)\]")


class IDNode(object):
    def __init__(self, code, title, isvaluation, start, end, note):
        self.children = []
        self.code = code
        self.title = title
        self.isvaluation = isvaluation
        self.start = start 
        self.end = end
        self.note = note

    def add(self, node): 
        for c in self.children:
            if c.start <= node.code and node.code <= c.end:
                c.add(node)
                return
        self.children.append(node)

    def visit(self, f, n=None):
        if n is None:
            n = 0
        f(n, self)
        for c in self.children:
            c.visit(f, n+1)

    def findByCode(self, code):
        if self.code == code:
            return self
        for c in self.children:
            if c.code == code:
                return c
            if c.start <= code and code <= c.end:
                return c.findByCode(code)
        return None

    def findByTitle(self, title):
        if self.title == title:
            return self
        for c in self.children:
            found = c.findByTitle(title)
            if found is not None:
                return found
        return None



tree = IDNode(code=0, title="勘定科目", isvaluation=False, start=1, end=9999, note=None)

for line in sys.stdin.readlines():
    m = x.match(line)
    if m:
        d = m.groupdict()
        assert(d['AccountCode'] is not None)
        start = None
        end = None
        isvaluation = d['IsValuationAccountCode'] is not None
        code = int(d['AccountCode'])
        note = None
        for i, part in enumerate(d["rest"].split(",")):
            if i == 0:
                title = part
            else:
                m = start_end.match(part)
                if m is not None:
                    d = m.groupdict()
                    start = int(d["start"])
                    end = int(d["end"])
                else:
                    note = part
        if DEBUG:
            print code, start, end
        
        if start is None:
            m = code
            r = 1000
            while r > 0:
                n, m = divmod(m, r)
                if DEBUG:
                    print n, m
                if n == 0:
                    start = code + 1
                    end = code + r*10 -1
                    break
                r = r / 10
            if DEBUG:
                print code, start, end, "default"

        tree.add(IDNode(code, title, isvaluation, start, end, note))


def foo(n, node):
    print '  '*n, node.code, node.title, node.isvaluation, node.note

#tree.visit(foo)

print "find 0", tree.findByCode(0)
print "find 8000", tree.findByCode(8000)
print "find 8221", tree.findByCode(8221)
print "find 仕入割引", tree.findByTitle("仕入割引")

