import hashlib, struct, random



def computeHash(ver, prev_block, mrkl_root, time_, bits, nonce):    
    # https://en.bitcoin.it/wiki/Difficulty
    exp = bits >> 24
    mant = bits & 0xffffff
    target_hexstr = '%064x' % (mant * (1<<(8*(exp - 3))))
    target_str = target_hexstr.decode('hex')
    
    header = ( struct.pack("<L", ver) + prev_block.decode('hex')[::-1] +
          mrkl_root.decode('hex')[::-1] + struct.pack("<LLL", time_, bits, nonce))
    hash = hashlib.sha256(hashlib.sha256(header).digest()).digest()

    successful = hash[::-1] < target_str
    return hash[::-1].encode('hex'), successful



    
def testOriginalCode():
    ver = 2
    prev_block = "000000000000000117c80378b8da0e33559b5997f2ad55e2f7d18ec1975b9717"
    mrkl_root = "871714dcbae6c8193a2bb9b2a69fe1c0440399f38d94b3a0f1b447275a29978a"
    time_ = 0x53058b35 # 2014-02-20 04:57:25
    bits = 0x19015f53
    nonce = 0

    print nonce, computeHash(ver, prev_block, mrkl_root, time_, bits, nonce)


def testBlock620954():
    ver = 0x3fff0000
    prev_block = "0000000000000000000140ac4688aea45aacbe7caf6aaca46f16acd93e1064c3"
    mrkl_root = "422458fced12693312058f6ee4ada19f6df8b29d8cac425c12f4722e0dc4aafd"
    time_ = 0x5E664C76
    bits = 0x17110119
    nonce = 538463288

    print nonce, computeHash(ver, prev_block, mrkl_root, time_, bits, nonce)

    for nonce in range(5):
        print nonce, computeHash(ver, prev_block, mrkl_root, time_, bits, nonce)


def testBlock620123():
    ver = 0x20002000
    prev_block = "00000000000000000006e6934a1846d5176604ffa5ed675c97b669a8c5a56631"
    mrkl_root = "d0c89c4695e16b5c37bc3a7fd5a633587c000c94814bd24c2db1146f1a20a146"
    time_ = 0x5E5F6802
    bits = 0x17122cbc
    nonce = 0x2e724fba

    print nonce, computeHash(ver, prev_block, mrkl_root, time_, bits, nonce)


def solveFirst():
    print '\n'
    print "Showing results for the first query..."

    ver = 0x20400000
    prev_block = "00000000000000000006a4a234288a44e715275f1775b77b2fddb6c02eb6b72f"
    mrkl_root = "2dc60c563da5368e0668b81bc4d8dd369639a1134f68e425a9a74e428801e5b8"
    time_ = 0x5DB8AB5E
    bits = 0x17148EDF
    
    lo = 3000000000
    hi = 3100000000

    for nonce in range(lo, lo + 5):
        print nonce, computeHash(ver, prev_block, mrkl_root, time_, bits, nonce)

    for nonce in range(lo, hi):
        result = computeHash(ver, prev_block, mrkl_root, time_, bits, nonce)
        if result[1]:
            print nonce, result
            return
        
    print "Can't find nonce in range [%i, %i)" % (lo, hi)


def solveSecond():
    print '\n'
    print "Showing results for the second query..."

    ver = 0x20400000
    prev_block = "00000000000000000006a4a234288a44e715275f1775b77b2fddb6c02eb6b72f"
    mrkl_root = "2dc60c563da5368e0668b81bc4d8dd369639a1134f68e425a9a74e428801e5b8"
    time_ = 0x5DB8AB5E
    bits = 0x17148EDF
    
    nonce1 = 3060331852
    num_tries = 100100100

    random.seed(0xCAFEF00D)
    lo = random.randint(nonce1 + 1, (1<<32) - num_tries - 10)
    hi = lo + num_tries
    print "random number = %i" % lo
    print "trying numbers in [%i, %i)" % (lo, hi)

    for nonce in range(lo, hi):
        result = computeHash(ver, prev_block, mrkl_root, time_, bits, nonce)
        if result[1]:
            print nonce, result
            return
        
    print "Can't find nonce in range [%i, %i)" % (lo, hi)


# testOriginalCode()
# testBlock620954()
# testBlock620123()

# solveFirst()
solveSecond()

