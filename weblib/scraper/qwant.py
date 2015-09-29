from six.moves.urllib.parse import quote

from weblib.error import RequestBanned, DataNotValid

ALLOWED_HTTP_CODES = (200,)


def build_search_url(query):
    url_tpl = ('https://api.qwant.com/api/search/web'
               '?count=10&f=safesearch%%3A1&locale=en_US&q=%s')
    url = url_tpl % quote(query)
    return url


def check_search_result_integrity(grab):
    if grab.doc.code != 200:
        raise DataNotValid('Non-200 HTTP code: %d' % grab.doc.code)
    elif not b'"status":"success"' in grab.doc.body:
        #grab.doc.save('/tmp/x.html')
        #print('not success')
        #import pdb; pdb.set_trace()
        raise DataNotValid('JSON success status not found')


def parse_search_result(grab):
    res = []
    for elem in grab.doc.json['data']['result']['items']:
        res.append({
            'url': elem['url'],
            'anchor': elem['title'],
        })
    return res

