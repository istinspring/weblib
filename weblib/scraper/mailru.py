from urllib.request import quote, unquote
import re

from weblib.error import RequestBanned, DataNotValid, HttpCodeZero

ALLOWED_HTTP_CODES = (200,)


def build_search_url(query, site=None):
    url_tpl = 'http://go.mail.ru/search?q=%s'
    if site:
        url_tpl += '&site=%s' % quote(site)
    url = url_tpl % quote(query)
    return url


def build_ajax_search_url(query, site=None):
    url_tpl = 'http://go.mail.ru/api/v1/web_search?q=%s'
    if site:
        url_tpl += '&site=%s' % quote(site)
    url = url_tpl % quote(query)
    return url


def check_integrity(grab):
    #if grab.doc.code == -1: # FIX
    #    raise RequestBanned('Ban (HTTP code %d)' % grab.doc.code)
    if False:#grab.doc.select('//img[contains(@src, "/captchaimg?")]').exists():
        raise RequestBanned('Ban (captcha)')
    elif grab.doc.code != 200:
        raise DataNotValid('Non-200 HTTP code: %d' % grab.doc.code)


def check_ajax_search_result_integrity(grab):
    #if grab.doc.code == -1: # FIX
    #    raise RequestBanned('Ban (HTTP code %d)' % grab.doc.code)
    if grab.doc.code != 200:
        raise DataNotValid('Non-200 HTTP code: %d' % grab.doc.code)
    else:
        try:
            info = grab.doc.json
        except (TypeError, ValueError) as ex:
            raise DataNotValid('Not valid JSON')
        if not info.get('body', {}).get('serp'):
            raise DataNotValid('body->serp key not found')
        elif info['body']['antirobot']['blocked']:
            raise RequestBanned('Ban!')


def parse_search_result(grab):
    res = []
    for elem in grab.doc('//li[@class="result__li"]'):
        link = elem.select('//h3/a')
        res.append({
            'url': link.attr('href'),
            'anchor': link.text(),
        })
    return res


def parse_ajax_search_result(grab):
    res = []
    for elem in grab.doc.json['body']['serp']['results']:
        if 'url' in elem:
            url = elem['url']
        elif 'orig_url' in elem:
            url = elem['orig_url']
        else:
            pass
        if url and 'title' in elem:
            res.append({
                'url': url,
                'anchor': elem['title'],
            })
    return res
