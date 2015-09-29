from urllib.request import quote, unquote
import re

from weblib.error import RequestBanned, DataNotValid, HttpCodeZero

ALLOWED_HTTP_CODES = (200,)


def build_search_url(query, lr=84):
    # https://search.yaca.yandex.ru/geo.c2n
    # 84 - USA
    # 111 - europe
    # 166 - xUSSR
    # 318 - universal
    # 225 - russia
    url_tpl = 'http://yandex.ru/search/?text=%s&lr=%d'
    url = url_tpl % (quote(query), lr)
    return url


def check_integrity(grab):
    #if grab.doc.code == -1: # FIX
    #    raise RequestBanned('Ban (HTTP code %d)' % grab.doc.code)
    if grab.doc.select('//img[contains(@src, "/captchaimg?")]').exists():
        raise RequestBanned('Ban (captcha)')
    elif grab.doc.code != 200:
        #grab.doc.save('/tmp/x.html')
        #print('NOT 200 CODE')
        #import pdb; pdb.set_trace()
        raise DataNotValid('Non-200 HTTP code: %d' % grab.doc.code)


def check_search_result_integrity(grab):
    check_integrity(grab)
    if not grab.doc('//input[@name="text"]').exists():
        raise DataNotValid('Expected HTML element not found')


def check_cache_integrity(grab):
    check_integrity(grab)
    if not grab.doc('//script[contains(@src,'
                    '"yandex.st/hilitedaemon-js")]').exists():
        raise DataNotValid('Expected yandex.st script not found')


def parse_search_result(grab):
    res = []
    for elem in grab.doc('//h2[@class="serp-item__title"]'):
        res.append({
            'url': elem.select('a/@href').text(),
            'anchor': elem.select('a').text(),
            'cache_url': elem.select(
                '..//a[contains(@href, "hghltd.yandex.net")]'
                '/@href').text(default=None),
        })
    return res
