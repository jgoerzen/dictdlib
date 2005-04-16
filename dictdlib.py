b64_list = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def b64_encode(val):
    """Takes as input an integer val and returns a string of it encoded
    with the base64 algorithm used by dict indexes."""
    startfound = 0
    retval = ""
    for i in range(5, -1, -1):
        thispart = (val >> (6 * i)) & ((2 ** 6) - 1)
        if (not startfound) and (not thispart):
            # Both zero -- keep going.
            continue
        startfound = 1
        retval += b64_list[thispart]
    if len(retval):
        return retval
    else:
        return b64_list[0]
    
def b64_decode(string):
    """Takes as input a string and returns an integer value of it decoded
    with the base64 algorithm used by dict indexes."""
    if not len(string):
        return 0
    retval = 0
    shiftval = 0
    for i in range(len(string) - 1, -1, -1):
        val = b64_list.index(string[i])
        retval = retval | (val << shiftval)
        shiftval += 6
    return retval

class DictWriter:
    
