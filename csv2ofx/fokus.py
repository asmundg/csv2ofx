# -*- coding: utf-8 -*-

"""
 Eat Skandiabanken csv export and output OFX
"""

from datetime import datetime
import re
import sys

from csv2ofx.base import CSV2OFX


class FokusBankCSV2OFX(CSV2OFX):
    encoding = 'latin1'
    key_posted = 'Bokf\xf8rt dato'
    key_amount = 'Bel\xf8p i NOK'
    key_name = 'Tekst'
    key_id = 'Bankens arkivreferanse:'
    delimiter = ','

    def name(self, row):
        name = re.sub(' +', ' ', super(FokusBankCSV2OFX, self).name(row))
        # Drop unusable prefix, to get some interesting data into the
        # allowed 32 characters
        name = re.sub(u'Overføring( [0-9]+) ', '', name)
        name = re.sub(u'Overføring( [0-9]+)?<br/>Avsender:<br/>', '', name)
        name = re.sub(u'Overføring med melding <br/>', '', name)
        name = re.sub(u'Overførsel strukturert <br/>', '', name)
        name = name[:32]
        return name

    def posted(self, row):
        return datetime.strptime(row.get(self.key_posted), '%d.%m.%Y')

    def amount(self, row):
        return (float(row.get(self.key_amount)
                      .replace('.', '').replace(',', '.')))

    def id(self, row):
        return super(FokusBankCSV2OFX, self).id(row) + str(self.posted(row))


def main():
    parser = FokusBankCSV2OFX(u'Fokus Bank', sys.argv[1], 'NOK')
    ofx = parser.build_ofx(sys.stdin)
    sys.stdout.write(ofx)
