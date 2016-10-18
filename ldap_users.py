#!/usr/bin/env python
# coding: utf-8
import ldap
import sys

SERVER = ""
USERCN = ""
USERPW = ""


def search_all_users(l, baseDN, searchFilter, retrieveAttributes=None):

    PAGESIZE = 1000
    searchScope = ldap.SCOPE_SUBTREE
    lc = ldap.controls.libldap.SimplePagedResultsControl(size=PAGESIZE,
                                                         cookie='')

    resultat = []
    try:
        msgid = l.search_ext(baseDN,
                             searchScope,
                             searchFilter,
                             retrieveAttributes,
                             serverctrls=[lc])
    except ldap.LDAPError as e:
        sys.exit('LDAP search failed: %s' % e)

    while True:
        try:
            rtype, rdata, rmsgid, serverctrls = l.result3(msgid)
        except ldap.LDAPError as e:
            sys.exit('Could not pull LDAP results: %s' % e)
        resultat.extend(rdata)
        pctrls = [
            c for c in serverctrls if c.controlType == ldap.controls.SimplePagedResultsControl.controlType
        ]
        if pctrls:
            cookie = lc.cookie = pctrls[0].cookie
        if cookie:
            msgid = l.search_ext(baseDN,
                                 searchScope,
                                 searchFilter,
                                 retrieveAttributes,
                                 serverctrls=[lc])
            lc.controlValue = (PAGESIZE, cookie)
        else:
            break

    return resultat


def create_file(l, filename, baseDN, searchfilter, retrieveAttributes=None):
    try:
        write_file = open(filename, 'w')
    except IOError:
        print 'Cannot open the file'
    users = search_all_users(l,
                             baseDN,
                             searchfilter,
                             retrieveAttributes)
    for user in users:
        write_file.write(user[1]['sAMAccountName'][0] + "\n")
    write_file.close()


l = ldap.initialize(SERVER)
l.set_option(ldap.OPT_REFERRALS, 0)
try:
    l.bind_s(USERCN, USERPW)
except ldap.INVALID_CREDENTIALS:
    print("Your username or password is incorrect")
    sys.exit()

#example
users = create_file(l,
                    "file_to_rite",
                    "baseDN",
                    "searchFilter",
                    attributs)
