#!/bin/python
#-*- coding=utf-8 -*-

from peewee import *
import datetime

db = SqliteDatabase(':memory:')

class JournalEntry(Model):
    key = PrimaryKeyField()
    dt = DateTimeField(default=datetime.datetime.now)

class Title(Model):
    title_id = PrimaryKeyField()
    name = CharField()

class JournalField(Model):
    key = PrimaryKeyField()
    amount = IntegerField()
    title = ForeignKeyField(Title)
    journalentry = ForeignKeyField(JournalEntry, related_name="fields")
    """ for f in entry.journal_fields"""
    iscredit = BooleanField()


def setupTitles():
    Title.create(name=u"材料")
    Title.create(name=u"賃金・給料")
    Title.create(name=u"経費")
    Title.create(name=u"仕掛品")
    Title.create(name=u"製品")
    Title.create(name=u"製造間接費")
    Title.create(name=u"現金預金")
    Title.create(name=u"売掛金")
    Title.create(name=u"買掛金")
    Title.create(name=u"売上")
    Title.create(name=u"売上原価")
    Title.create(name=u"販売費及び一般管理費")
    Title.create(name=u"月次損益")
    
classes = [JournalEntry, Title, JournalField]


def make_entry(debit, credit):
    with db.transaction():
        e = JournalEntry.create()
        print e
        for c in credit:
            t = Title.select().where(Title.name == c["name"])
            JournalField.create(amount=c["amount"], title=t, journalentry=e, iscredit=True)
        for d in debit:
            t = Title.select().where(Title.name == d["name"])
            JournalField.create(amount=d["amount"], title=t, journalentry=e, iscredit=False)


def story(reset):
    if reset:
        db.drop_tables(classes)
        db.create_tables(classes)
        with db.transaction():
            setupTitles()

    for t in Title.select():
        print t.title_id, t.name
    
    make_entry(
            [{"name":u"材料", "amount":720000}],
            [{"name":u"買掛金", "amount":720000}])
