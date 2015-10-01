from urllib.request import quote, unquote

from weblib.error import RequestBanned, DataNotValid

ALLOWED_HTTP_CODES = (200,)


def build_search_url(query):
    url_tpl = 'http://search.goo.ne.jp/web.jsp?MT=%s'
    url = url_tpl % quote(query)
    return url


def check_integrity(grab):
    if False:#grab.doc.code == 999:
        pass#raise RequestBanned('Ban (HTTP code %d)' % grab.doc.code)
    elif grab.doc.code != 200:
        raise HttpCodeNotValid('Non-200 HTTP code: %d' % grab.doc.code)


def check_search_result_integrity(grab):
    check_integrity(grab)
    if not grab.doc('//input[@name="MT"]').exists():
        raise DataNotValid('Search query input not found')


def parse_search_result(grab):
    res = []
    for elem in grab.doc('//div[@class="result"'
                         ' and p[contains(@class, "title")]/a]'):
        link = elem.select('p[contains(@class, "title")]/a')
        res.append({
            'url': link.attr('href'),
            'anchor': link.text(),
        })
    return res

