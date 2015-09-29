from six.moves.urllib.parse import quote

from weblib.error import RequestBanned, DataNotValid

ALLOWED_HTTP_CODES = (200,)


def build_search_url(query):
    url_tpl = 'https://www.ixquick.com/do/search?q=%s'
    url = url_tpl % quote(query)
    return url


def check_search_result_integrity(grab):
    if ('your Internet connection has been prevented from accessing it' in
            grab.doc.unicode_body()):
        raise RequestBanned('Found ban message')
    if grab.doc('//form[@id="captcha_form"]').exists():
        raise RequestBanned('Found captcha form')
    if grab.doc.code != 200:
        raise DataNotValid('Non-200 HTTP code: %d' % grab.doc.code)
    elif not grab.doc('//base[contains(@href, "ixquick.com")]').exists():
        grab.doc.save('/tmp/x.html')
        import pdb; pdb.set_trace()
        raise DataNotValid('Expected HTML element not found')


def parse_search_result(grab):
    res = []
    for elem in grab.doc('//ol[contains(@class, "web_regular_results")]'
                         '/li/div[1]'):
        link = elem.select('h3/a').one()
        res.append({
            'url': link.attr('href'),
            'anchor': link.text(),
        })
    return res
