import MultiPManager.distProc as man


def saltedHash(psw):
    import hashlib
    import binascii
    print("Hashing {}".format(psw))
    dk = hashlib.pbkdf2_hmac('sha256', psw, 'salt', 100000)
    return binascii.hexlify(dk)


def GetWords(N):
    import urllib2
    word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
    response = urllib2.urlopen(word_site)
    txt = response.read()
    WORDS = txt.splitlines()
    return WORDS[0:N]


man.tlon_parallelize(saltedHash, GetWords(132))