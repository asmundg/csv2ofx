# -*- coding: utf-8 -*-

"""
 Eat Skandiabanken csv export and output OFX
"""

import csv
from datetime import datetime
import logging
import sys

from lxml import etree

from ofx import OFX, OFXStatement

class CSV2OFX(object):
    encoding = None
    key_posted = None
    key_amount = None
    key_name = None
    key_id = None
    delimiter = '\t'

    def __init__(self, bank_id, account_id, currency):
        self.bank_id = bank_id
        self.account_id = account_id
        self.currency = currency

    def posted(self, row):
        return datetime.strptime(row.get(self.key_posted), '%Y-%m-%d')

    def amount(self, row):
        return float(row.get(self.key_amount))

    def name(self, row):
        return row.get(self.key_name).decode(self.encoding)

    def id(self, row):
        return row.get(self.key_id)

    def parse_csv(self, source):
        reader = csv.DictReader(source, delimiter=self.delimiter)
        statements = []
        for row in reader:
            statement = OFXStatement(posted=self.posted(row),
                                     amount=self.amount(row),
                                     name=self.name(row),
                                     fitid=self.id(row))
            statements.append(statement)
        return statements

    def build_ofx(self, source):
        statements = self.parse_csv(source)
        ofx = OFX()
        ofx.currency = self.currency
        ofx.bank_id = self.bank_id
        ofx.account_id = self.account_id
        ofx.account_type = 'CHECKING'
        ofx.statements = statements
        now = datetime.utcnow()
        ofx.start = now
        ofx.end = now
        return \
            'OFXHEADER:100\n' \
            'DATA:OFXSGML\n' \
            'VERSION:102\n' \
            'SECURITY:NONE\n' \
            'ENCODING:UTF-8\n' \
            'CHARSET:CSUNICODE\n' \
            'COMPRESSION:NONE\n' \
            'OLDFILEUID:NONE\n' \
            'NEWFILEUID:NONE\n\n' \
            + etree.tostring(ofx.output(),
                             encoding='utf-8',
                             xml_declaration=False,
                             pretty_print=True)


