from DateTime import DateTime


def computeAge(item):
    """ Return age of item in milliseconds. """
    created = item.created().millis()
    created = DateTime().millis() - created
    return created

def getAge(item):
    """ Return age of item in prettified format. """
    time = computeAge(item)
    time = msToPrettified(time)
    return time

def msToHumanReadable(ms):
    """
    Convert milliseconds to a string in this format:
    'yy:mo:dd:hh:mi:ss', e.g.: '16:11:11:7:42:8'.
    """
    string = ''
    ss = ms / 1000
    mi = ss / 60
    ss -= mi * 60
    hh = mi / 60
    mi -= hh * 60
    dd = hh / 24
    hh -= dd * 24
    mo = dd / 30
    dd -= mo * 30
    yy = mo / 12
    mo -= yy * 12
    chunks = [yy, mo, dd, hh, mi, ss]
    for i, chunk in enumerate(chunks):
        chunk = str(chunk)
        string += chunk
        if i != len(chunks) -1:
            string += ':'
    return string

def msToPrettified(ms, SHORTFORM=True, OMITZERO=False):
    """
    Convert milliseconds to a list of key-value-pairs,
    prepend zero for single digits:
    ['01', 'yrs', '07', 'mth', '27', 'dys',
     '23', 'hrs', '13', 'min', '04', 'sec']
    If SHORTFORM is True, only the first two biggest vals
    will be returned:
    ['01', 'yrs', '07', 'mth']
    """
    OMIT = False
    pretties = []
    units = ['yrs','mth','dys','hrs','min','sec']

    human_readables = msToHumanReadable(ms).split(':')
    for i, human_readable in enumerate(human_readables):
        if human_readable == '0' and SHORTFORM or OMITZERO: # omit zero-vals
            OMIT = True
        else: OMIT = False
        if not OMIT:
            if len(human_readable) == 1: # prepend zero if single digit
                human_readable = '0' + human_readable
            pretties.append(human_readable)
            pretties.append(units[i])
    if SHORTFORM:
        if len(pretties) > 4: # only take first two non-zero vals
            pretties = pretties[0:4]
        # Prepend pair with zero-val, if there is only one pair with a
        # non-zero-val, for better readability (same horizontal line-up
        # as the other entries in listview):
        if len(pretties) == 2:
            current_unit = pretties[1]
            previous_unit = units[units.index(current_unit) - 1]
            pretties = ['00', previous_unit] + pretties
        # Dummy val, if no time consumed:
        if len(pretties) == 0:
            pretties = ['00', 'min', '00', 'sec']
    return pretties

