from urllib.request import quote, unquote

from weblib.error import RequestBanned, DataNotValid

ALLOWED_HTTP_CODES = (999, 200)


def build_search_url(query):
    url_tpl = 'http://search.yahoo.com/search?p=%s&ei=UTF-8&nojs=1'
    url = url_tpl % quote(query)
    return url


def check_integrity(grab):
    if grab.doc.code == 999:
        raise RequestBanned('Ban (HTTP code %d)' % grab.doc.code)
    elif grab.doc.code != 200:
        raise HttpCodeNotValid('Non-200 HTTP code: %d' % grab.doc.code)


def check_search_result_integrity(grab):
    check_integrity(grab)
    if not grab.doc('//input[@name="p"]').exists():
        raise DataNotValid('Search query input not found')


def check_cache_integrity(grab):
    check_integrity(grab)
    if not grab.doc('//div[@class="cacheContent"]').exists():
        raise DataNotValid('Div[@class="cacheContent"] not found')


def extract_encoded_url(url):
    return unquote(url.split('/RU=')[1].split('/')[0])


def parse_search_result(grab):
    res = []
    for elem in grab.doc('//div[@id="web"]//ol/li//div[h3[@class="title"]/a]'):
        data = elem.select('h3/a/@href').text().strip()
        if '/RU=' in data:
            url = extract_encoded_url(data)
        else:
            url = data

        cache_url = None
        for node in elem.select('..//a[@href]'):
            node_url = node.attr('href')
            if '/RU=' in node_url:
                node_url = extract_encoded_url(node_url)
            if '/srpcache' in node_url:
                cache_url = node_url
                break

        res.append({
            'url': url,
            'anchor': elem.select('h3/a').text().strip(),
            'cache_url': cache_url,
        })
    return res
