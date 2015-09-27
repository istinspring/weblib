from six.moves.urllib.parse import quote

from weblib.error import RequestBanned, DataNotValid

ALLOWED_HTTP_CODES = (403, 200)


def build_search_url(query):
    url_tpl = 'https://duckduckgo.com/html?q=%s'
    url = url_tpl % quote(query)
    return url


def check_search_result_integrity(grab):
    if grab.doc.code == 403:
        raise RequestBanned('Ban (HTTP code %d)' % grab.doc.code)
    elif grab.doc.code != 200:
        raise DataNotValid('Non-200 HTTP code: %d' % grab.doc.code)
    elif not grab.doc('//link[contains(@href, "opensearch") and '
                      'contains(@title, "DuckDuckGo")]').exists():
        raise DataNotValid('Expected HTML element not found')


def parse_search_result(grab):
    res = []
    for elem in grab.doc('//div[@id="links"]'
                         '/div/div[contains(@class, "links_main") and'
                         ' a[@class="large"]]'):
        link = elem.select('a[@class="large"]').one()
        res.append({
            'url': link.attr('href'),
            'anchor': link.text(),
        })
    return res
