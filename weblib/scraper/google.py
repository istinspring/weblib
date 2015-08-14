from random import choice
from urllib.request import quote

from weblib.scraper.google_host import GOOGLE_HOST_LIST
from weblib.error import DataNotValid, RequestBanned, NextPageNotFound

__all__ = ['build_search_url', 'check_integrity',
           'parse_search_result', 'parse_next_page',
           'ALLOWED_HTTP_CODES']

ALLOWED_HTTP_CODES = (403, 503, 200)


def build_search_url(query, host=None, country='us'):
    if host is None:
        host = choice(GOOGLE_HOST_LIST)
    url_tpl = 'https://www.%s/search?q=%s&gl=%s'
    return url_tpl % (host, quote(query), country)


def check_integrity(grab):
    if grab.doc.code in (503, 403) or grab.doc('//input[@name="captcha"]').exists():
        raise RequestBanned('Captcha found')


def check_search_result_integrity(grab):
    check_integrity(grab)
    if not grab.doc('//div[@id="res"]').exists():
        raise DataNotValid('Content of response has unexpected format.')


def check_cache_integrity(grab):
    check_integrity(grab)
    if grab.doc.code == 404:
        pass
    elif not grab.doc('//div[@id="google-cache-hdr"]').exists():
        raise DataNotValid('Google Cache Header not found')


def parse_search_result(grab):
    res = []
    for elem in grab.doc('//h3[following-sibling::div[@class="s"]]'):
        res.append({
            'url': elem.select('a/@href').text().strip(),
            'anchor': elem.select('a').text().strip(),
            #snippet = elem.select('./following-sibling::div[@class="s"]')
        })
    return res


def parse_next_page(grab):
    """
    Returns tuple (next_page_number, next_page_url)
    """
    elem = grab.doc('//div[@id="navcnt"]')
    cur_page = int(elem.select('.//td[@class="cur"]').text())
    pages = {}
    for sub_elem in elem.select('.//td/a[@class="fl"]'):
        number = int(sub_elem.text())
        pages[number] = sub_elem.attr('href')
    next_page = cur_page + 1
    if next_page in pages:
        return next_page, pages[next_page]
    else:
        raise NextPageNotFound
