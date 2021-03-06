# -*- coding: utf-8 -*-

# CURRENTLY BROKEN (Google keeps changing :( )

__module_author__ = 'Ward Muylaert'
__module_name__ = 'GCalc'
__module_version__ = '0.2'
__module_description__ = 'Google Calculator'

import xchat
from urllib import URLopener
import re

class MyURL(URLopener):
    version = 'Mozilla/5.0 (X11; Linux x86_64; rv:9.0.1) Gecko/20100101 Firefox/9.0.1'

def gcalc(word, word_eol, userdata):
    baseurl = 'http://www.google.com/search?q=%s'
    query = word_eol[1]
    debug = False
    if word[1] == '--debug':
        debug = True
        query = word_eol[2]

    # TODO: Fix freeze while loading.
    opener = MyURL()
    content = opener.open(baseurl % query).read()

    if debug:
        for i in range(len(content)/1000):
            print content[i*1000:(i+1)*1000]
        return xchat.EAT_ALL

    lindex = content.find('<h2 class=r style="font-size:138%">')
    if lindex == -1:
        xchat.prnt('Nothing found. If this seems wrong, please debug.')
        return xchat.EAT_ALL
    lindex = lindex + len('<h2 class=r style="font-size:138%"><b>')
    rindex = content.find('</b></h2>', lindex)
    result = content[lindex:rindex]
    result = " ".join(result.split())
    result = result.replace('&nbsp;', ' ')
    result = result.replace('&#215;', '×')
    result = re.sub(r'<sup>(\d+)<\/sup>&#8260;<sub>(\d+)</sub>',
            r' \1⁄\2',
            result)
    result = result.replace('<sup>', '^')
    result = result.replace('</sup>', '')
    result = result.replace('<font size=-2> </font>', ',')
    xchat.prnt("Google Calculator: %s" % result)
    return xchat.EAT_ALL

xchat.hook_command('gcalc', gcalc)

xchat.prnt('Loaded %s v%s by %s.'
        % (__module_name__, __module_version__, __module_author__))
