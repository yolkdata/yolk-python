import json
from datetime import date, datetime
from io import BytesIO
from gzip import GzipFile
import logging
from dateutil.tz import tzutc
from requests.auth import HTTPBasicAuth
from requests import sessions

from yolk.version import VERSION
from yolk.utils import remove_trailing_slash

_session = sessions.Session()


def post(org, write_key, env, ids, appInfo, gzip, timeout=15, proxies=None, **kwargs):
    """Post the `kwargs` to the API"""
    log = logging.getLogger('yolk')
    batch = kwargs["batch"]

    meta = {
        "tracker": {
            "name" : "yolk-python",
            "vendor": "yolk",
            "lang": "python",
            "origin": "client",
            "platform": "web",
            "method": "xhr",
            "ver": VERSION
        },
        "ids": ids,
        "schemas": [{
            "name": "yolk-core",
            "ver": "0.0.1"
        }],
        "app": {
            "name": appInfo['name'] or None,
            "ver": appInfo['ver'] or None,
            "release": appInfo['release'] or None,
            "type": appInfo['type'] or None,
            "lang": appInfo['lang'] or None,
            "env": env or "development",
        },
        "apiKey": write_key,
        "sent": datetime.utcnow().replace(tzinfo=tzutc()).isoformat()
    }

    data = []
    for msg in batch:
        data.append(msg["data"])

    wrapper = {
        "meta": meta,
        "data": data
    }

    url = remove_trailing_slash('https://' + org + '.yolk-api.com/track')

    body = json.dumps(wrapper, cls=DatetimeSerializer)

    log.debug('making request : %s', body)
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'yolk-python-tracker/' + VERSION
    }

    # yolk todo: support gzip in collector
    gzip = False
    if gzip:
        log.debug('making request using gzip')
        headers['Content-Encoding'] = 'gzip'
        buf = BytesIO()
        with GzipFile(fileobj=buf, mode='w') as gz:
            # 'data' was produced by json.dumps(),
            # whose default encoding is utf-8.
            gz.write(body.encode('utf-8'))
        body = buf.getvalue()
    
    kwargs = {
        "data": body,
        "auth": None,
        "headers": headers,
        "timeout": 15,
    }

    if proxies:
        kwargs['proxies'] = proxies

    res = _session.post(url, data=body, auth=None,
                        headers=headers, timeout=timeout)

    if res.status_code == 200:
        log.debug('data uploaded successfully')
        return res

    try:
        payload = res.json()
        log.debug('received response: %s', payload)
        raise APIError(res.status_code, payload['code'], payload['message'])
    except ValueError:
        raise APIError(res.status_code, 'unknown', res.text)


class APIError(Exception):

    def __init__(self, status, code, message):
        self.message = message
        self.status = status
        self.code = code

    def __str__(self):
        msg = "[Yolk] {0}: {1} ({2})"
        return msg.format(self.code, self.message, self.status)


class DatetimeSerializer(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)
