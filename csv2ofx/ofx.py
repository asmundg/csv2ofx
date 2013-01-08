from datetime import datetime
import time

from lxml import etree
from lxml.etree import Element
from lxml.builder import E


class OFXStatement(object):
    def __init__(self, posted, amount, name='', memo='', fitid=0):
        self.type = 'OTHER'
        self.posted = posted
        self.amount = amount
        self.name = name
        self.memo = memo
        self.fitid = fitid


class OFX(object):
    def __init__(self):
        self.currency = None
        self.bank_id = None
        self.account_id = None
        self.account_type = 'CHECKING'
        self.statements = []
        self.start = None
        self.end = None

    def status_set(self, code, severity):
        return E.STATUS(
            E.CODE(str(code)),
            E.SEVERITY(severity))

    def signon_set(self):
        return E.SIGNONMSGSRSV1(
            E.SONRS(
                self.status_set(0, 'INFO'),
                E.DTSERVER(datetime.utcnow().strftime('%Y%m%d%H%M%S[+0:UTC]')),
                E.LANGUAGE('ENG')))

    def bank_acct_from(self, bank_id, account_id, account_type):
        return E.BANKACCTFROM(
            E.BANKID(bank_id),
            E.ACCTID(account_id),
            E.ACCTTYPE(account_type))

    def bank_tran_list(self, start, end, statements):
        return E.BANKTRANLIST(
            E.DTSTART(start.strftime('%Y%m%d')),
            E.DTEND(end.strftime('%Y%m%d')),
            *[self.stmt_trn(statement) for statement in statements])

    def stmt_trn(self, statement):
        if statement.memo:
            return E.STMTTRN(
                E.TRNTYPE(statement.type),
                E.DTPOSTED(statement.posted.strftime('%Y%m%d')),
                E.TRNAMT(unicode(statement.amount)),
                E.FITID(unicode(statement.fitid)),
                E.NAME(statement.name),
                E.MEMO(statement.memo))
        else:
            return E.STMTTRN(
                E.TRNTYPE(statement.type),
                E.DTPOSTED(statement.posted.strftime('%Y%m%d')),
                E.TRNAMT(unicode(statement.amount)),
                E.FITID(unicode(statement.fitid)),
                E.NAME(statement.name))

    def bank_set(self):
        return E.BANKMSGSRSV1(
            E.STMTTRNRS(
                E.TRNUID(str(time.time())),
                self.status_set(0, 'INFO'),
                E.STMTRS(
                    E.CURDEF(self.currency),
                    self.bank_acct_from(self.bank_id, self.account_id, self.account_type),
                    self.bank_tran_list(self.start, self.end, self.statements),
                    E.LEDGERBAL(
                        E.BALAMT('0'),
                        E.DTASOF('20100101'))
                    )
                )
            )

    def output(self):
        ofx = Element('OFX')
        tree = etree.ElementTree(ofx)
        # I'm going to hold this off until libofx eats XML
        #ofx.addprevious(etree.PI('OFX',
        #                         'OFXHEADER="200"'
        #                         ' VERSION="211"'
        #                         ' SECURITY="NONE"'
        #                         ' OLDFILEUID="NONE"'
        #                         ' NEWFILEUID="NONE"'))
        ofx.append(self.signon_set())
        ofx.append(self.bank_set())
        return tree
