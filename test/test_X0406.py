#!/bin/python
# -*- coding=utf-8 -*-

from nose.tools import with_setup, raises
from X0406 import load

t = None

def setup_tree():
    global t
    t = load(file("X0406.txt"))

def teardown_tree():
    global t
    t = None

@with_setup(setup_tree, teardown_tree)
def test_findByCode0():
    found = t.findByCode(0)
    assert found.code == 0

@with_setup(setup_tree, teardown_tree)
def test_findByCode8000():
    found = t.findByCode(8000)
    assert found.code == 8000

@with_setup(setup_tree, teardown_tree)
def test_findByCode82211():
    t = load(file("X0406.txt"))
    found = t.findByCode(8221)
    assert found.code == 8221
    assert found.title == "当期商品仕入高"

@with_setup(setup_tree, teardown_tree)
def test_findByTitle():
    found = t.findByTitle("仕入割引")
    assert found.code == 8640


