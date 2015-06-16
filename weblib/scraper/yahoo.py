from urllib.request import quote, unquote

from weblib.error import RequestBanned, DataNotValid, HttpCodeZero


def build_search_url(query):
    url_tpl = 'https://search.yahoo.com/search?p=%s&ei=UTF-8&nojs=1'
    url = url_tpl % quote(query)
    return url


def check_integrity(grab):
    if grab.doc.code == 999:
        raise RequestBanned('Ban (HTTP code %d)' % grab.doc.code)
    elif grab.doc.code == 0:
        raise HttpCodeZero('HTTP code ZERO')
    elif grab.doc.code != 200:
        raise HttpCodeNotValid('Non-200 HTTP code: %d' % grab.doc.code)
    elif not grab.doc('//li[@class="copyright" and '
                      'contains(text(), "Yahoo")]').exists():
        raise DataNotValid('Expected HTML element not found')


def parse_search_result(grab):
    check_integrity(grab)
    res = []
    for elem in grab.doc('//ol/li//div[@class="compTitle" and h3/a]'):
        data = elem.select('h3/a/@href').text().strip()
        if '/RU=' in data:
            url = unquote(data.split('/RU=')[1].split('/')[0])
        else:
            url = data
        res.append({
            'url': url,
            'anchor': elem.select('h3/a').text().strip(),
        })
    return res
