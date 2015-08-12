#!/bin/python
#-*- coding=utf-8 -*-
import sys
import re

x = re.compile("(?P<IsValuationAccountCode>\()?(?P<AccountCode>\d\d\d\d)\)?,(?P<rest>.+)")

start_end = re.compile("\[(?P<start>\d\d\d\d)-(?P<end>\d\d\d\d)\]")


class IDNode(object):
    def __init__(self, code, title, start, end, note):
        self.children = []
        self.code = code
        self.start = start 
        self.end = end
        self.title = title

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

tree = IDNode(code=0, title="勘定科目", start=1, end=9999, note=None)

for line in sys.stdin.readlines():
    m = x.match(line)
    if m:
        d = m.groupdict()
        assert(d['AccountCode'] is not None)
        start = None
        end = None
        title = d['rest']
        code = int(d['AccountCode'])
        for part in d["rest"].split(","):
            m = start_end.match(part)
            if m is not None:
                d = m.groupdict()
                start = int(d["start"])
                end = int(d["end"])
        print code, start, end
        
        if start is None:
            m = code
            r = 1000
            while r > 0:
                n, m = divmod(m, r)
                print n, m
                if n == 0:
                    start = code + 1
                    end = code + r*10 -1
                    break
                r = r / 10
            print code, start, end, "default"

        tree.add(IDNode(code, title, start, end, None))


def foo(n, node):
    print '  '*n, node.code, node.title

tree.visit(foo)

