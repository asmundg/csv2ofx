import csv
from datetime import datetime
from StringIO import StringIO
import sys
import time

from lxml import etree
from lxml.etree import HTML, XPath

row_selector = XPath('//table[@id="repeatertable"]//tr[td]')

def parse(source, output):
    """
     source: file-like
     output: file-like

     returns the output object
    """
    page = HTML(source.read())
    writer = csv.writer(output)
    for row in row_selector(page):
        date, memo, debit, credit = [el.text.strip() for el in row.xpath('td')]
        date = datetime(*time.strptime('30.11.2009', '%d.%m.%Y')[:6]).isoformat()
        payment = debit
        if not payment:
            payment = credit
        payment = float(payment.replace(' ', '').replace(',', '.'))
        writer.writerow((date, memo, payment))
    return output

if __name__ == '__main__':
    print parse(sys.stdin, StringIO()).getvalue()
