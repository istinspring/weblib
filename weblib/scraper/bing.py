from urllib.request import quote, unquote

from weblib.error import RequestBanned, DataNotValid, HttpCodeZero

ALLOWED_HTTP_CODES = (999, 200)


def build_search_url(query, cc='us'):
    url_tpl = 'http://www.bing.com/search?q=%s&cc=%s'
    url = url_tpl % (quote(query), cc)
    return url


def check_integrity(grab):
    #if grab.doc.code == 999:
    #    raise RequestBanned('Ban (HTTP code %d)' % grab.doc.code)
    if grab.doc.code != 200:
        raise HttpCodeNotValid('Non-200 HTTP code: %d' % grab.doc.code)


def check_search_result_integrity(grab):
    check_integrity(grab)
    if not grab.doc('//input[@name="q"]').exists():
        raise DataNotValid('Search query input not found')


def check_cache_integrity(grab):
    check_integrity(grab)
    if not grab.doc('//div[@class="b_vPanel"]').exists():
        raise DataNotValid('Div[@class="b_vPanel"] not found')


def parse_search_result(grab):
    res = []
    for elem in grab.doc('//ol[@id="b_results"]/li[contains(@class, "b_algo")'
                         ' and .//h2/a]'):
        link = elem.select('.//h2/a')
        try:
            b_attr = elem.select('.//div[@class="b_attribution"]/@u')\
                         .text(default=None)
            if b_attr:
                x, y, attr_d, attr_w = b_attr.split('|')
                cache_url = 'http://cc.bingj.com/cache.aspx?q=zzz&d=%s&w=%s' % (
                    attr_d, attr_w)
            else:
                cache_url = None
        except Exception as ex:
            logging.error(exc_info=ex)
            import pdb; pdb.set_trace()
        res.append({
            'url': link.attr('href'),
            'anchor': link.text(),
            'cache_url': cache_url,
        })
    return res
