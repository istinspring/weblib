from urllib.request import quote, unquote

from weblib.error import RequestBanned, DataNotValid

ALLOWED_HTTP_CODES = (200,)


def build_search_url(query):
    url_tpl = 'http://m.search.rambler.ru/search?query=%s'
    url = url_tpl % quote(query)
    return url


def check_integrity(grab):
    if False:#grab.doc.code == 999:
        pass#raise RequestBanned('Ban (HTTP code %d)' % grab.doc.code)
    elif grab.doc.code != 200:
        raise HttpCodeNotValid('Non-200 HTTP code: %d' % grab.doc.code)


def check_search_result_integrity(grab):
    check_integrity(grab)
    if not grab.doc('//input[@name="query"]').exists():
        raise DataNotValid('Search query input not found')


def parse_search_result(grab):
    res = []
    for elem in grab.doc('//div[@class="b-serp-item" and article/h2/a]'):
        link = elem.select('article/h2/a')
        res.append({
            'url': link.attr('href'),
            'anchor': link.text(),
        })
    return res
