# -*- coding: utf-8 -*-

"""
 Eat Skandiabanken csv export and output OFX
"""

import StringIO
import sys

from lxml import etree

from ofx import OFX
from base import CSV2OFX

class SkandiabankenCSV2OFX(CSV2OFX):
    encoding = 'latin1'
    key_posted = 'BOKF\xd8RINGSDATO'
    key_out_amount = 'UT FRA KONTO'
    key_in_amount = 'INN P\xc5 KONTO'
    key_name = 'TEKST'
    key_id = 'ARKIVREFERANSE'

    def amount(self, row):
        out_amount = row.get(self.key_out_amount)
        if not out_amount:
            return float(row.get(self.key_in_amount).replace(',', '.'))
        else:
            return -float(out_amount.replace(',', '.'))

    def id(self, row):
        return CSV2OFX.id(self, row) + str(self.posted(row))

def main():
    parser = SkandiabankenCSV2OFX(u'Skandiabanken', sys.argv[1], 'NOK')
    lines = sys.stdin.readlines()
    source = StringIO.StringIO()
    source.write(''.join(lines[2:-2]))
    source.seek(0)
    ofx = parser.build_ofx(source)
    return ofx

if __name__ == '__main__':
    print main()
