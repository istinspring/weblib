from urllib.request import quote, unquote

from weblib.error import RequestBanned, DataNotValid

ALLOWED_HTTP_CODES = (200,)


def build_search_url(query):
    url_tpl = 'http://search.daum.net/search?&q=%s'
    url = url_tpl % quote(query)
    return url


def check_integrity(grab):
    if False:#grab.doc.code == 999:
        pass#raise RequestBanned('Ban (HTTP code %d)' % grab.doc.code)
    elif grab.doc.code != 200:
        raise HttpCodeNotValid('Non-200 HTTP code: %d' % grab.doc.code)


def check_search_result_integrity(grab):
    check_integrity(grab)
    if not grab.doc('//input[@name="q"]').exists():
        raise DataNotValid('Search query input not found')


def parse_search_result(grab):
    res = []
    for elem in grab.doc('//ul[contains(@class, "list_info")]'
                         '/li[//div[contains(@class, "wrap_tit")]]'):
        link = elem.select('.//div[contains(@class, "wrap_tit")]/a')
        res.append({
            'url': link.attr('href'),
            'anchor': link.text(),
        })
    return res

