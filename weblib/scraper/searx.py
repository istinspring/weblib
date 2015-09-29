from six.moves.urllib.parse import quote

from weblib.error import RequestBanned, DataNotValid

ALLOWED_HTTP_CODES = (200,)


def build_search_url(query):
    url_tpl = 'https://www.searx.me/?q=%s&categories=general'
    url = url_tpl % quote(query)
    return url


def check_search_result_integrity(grab):
    #if grab.doc.code == 403:
    #    raise RequestBanned('Ban (HTTP code %d)' % grab.doc.code)
    if grab.doc.code != 200:
        raise DataNotValid('Non-200 HTTP code: %d' % grab.doc.code)
    elif not grab.doc('//meta[@name="generator" and'
                      ' contains(@content, "searx/")]').exists():
        raise DataNotValid('Expected HTML element not found')


def parse_search_result(grab):
    res = []
    for elem in grab.doc('//div[@id="main_results"]'
                         '/div[contains(@class, "result")]'):
        link = elem.select('h4/a').one()
        res.append({
            'url': link.attr('href'),
            'anchor': link.text(),
        })
    return res
