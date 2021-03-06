#!/bin/python
# -*- coding=utf-8 -*-

from nose.tools import with_setup, raises
from journal import loadfromjson, Journal


sample_json = """{
    "debit": {"建物": 100000},
    "credit":  {"現金": 100000},
    "issuer": "bgnori@gmail.com",
    "date": 1439517320
}"""


def test_loadfromjson():
    j = loadfromjson(sample_json)
    assert j["debit"][u"建物"] == 100000
    assert j["credit"][u"現金"] == 100000
    assert j["issuer"]== "bgnori@gmail.com"
    assert j["date"] == 1439517320


def test_Journal():
    j = Journal()
    e = loadfromjson(sample_json)

    j.append(e)
    dr, cr = j.getTAccount(u"現金")
    assert cr[1439517320] == 100000




