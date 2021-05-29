Yolk's Python Tracker
==============

A Python client for Yolk based on Segment's analytics-python lib. Collect and stream data from your Python data source into your Yolk warehouse.

## 🚀 Python Setup

Install `yolk-python` using pip:
```bash
git clone https://github.com/yolkdata/yolk-python.git

pip install yolk-python
```

Or:
```bash
$ git clone https://github.com/yolkdata/yolk-python.git

$ cd yolk-python

$ sudo python3 setup.py install
```

Inside your app, you'll want to **set** `yolk.org` and `yolk.write_key` before making any analytics calls:

```python
import yolk

yolk.org = 'YOLK_ORGANIZATION_NAME'
yolk.write_key = 'YOLK_WRITE_KEY'

```

Handling Ids:
```python
yolk.ids = {
  "idName": "<id>",
  # e.g.:
  "vid": "134d33",
}
```
Setting ids will ensure your ids are sent along to Yolk with every batch.

Development/Production:
```python
yolk.env = 'production' # default: "development"
```

Optional app info:
```python
yolk.appInfo = {
    "name": "<APP NAME>",
    "ver": "<APP VERSION>",
    "release": "<APP RELEASE>",
    "type": "web", # or native, or iot.
    "lang": "e.g. django",
}
```
Setting appInfo will send along this info to Yolk with every batch.

Logging/Debugging:
```python
import logging

logging.basicConfig(filename='tracker.log', filemode='w', level=logging.DEBUG)
```

## Django Setup
To add yolk to Django, you need to include the initialization code in the ready() method of a custom AppConfig object for one of the apps in your project. This method is responsible for performing initialization tasks for your project.

myapp/apps.py file:
```bash
from django.apps import AppConfig
import yolk

class MyAppConfig(AppConfig):

    def ready(self):
        yolk.org = 'YOUR_YOLK_USERNAME'
        yolk.write_key = 'YOUR_WRITE_KEY'
```

myapp/__init__.py file:
```bash
default_app_config = 'myapp.apps.MyAppConfig'
```

Be sure to review Python Setup section for more settings.

## Sending your first event, wohoo!

```python
yolk.track({
    "name": "test event",
    "properties": {
        "page_type": "home",
    },
    "created": datetime.utcnow().replace(tzinfo=tzutc()).isoformat(),   
})
```

## Aliasing people
An alias creates a connection between one identifier and another for an individual. For example tying a visitor id to a user id, or tying an email address to a visitor id.

```python
yolk.alias({
    "properties":{
        "idName": "123",
    },
    "created": datetime.utcnow().replace(tzinfo=tzutc()).isoformat(),
})
```
This will send an alias record tying "idName" to any ids set in `yolk.ids`.


## Stuck?
Let us know on slack and check out Segment's analytics-python Documentation: [https://segment.com/libraries/python](https://segment.com/libraries/python).


## License

```
WWWWWW||WWWWWW
 W W W||W W W
      ||
    ( OO )__________
     /  |           \
    /o o|    MIT     \
    \___/||_||__||_|| *
         || ||  || ||
        _||_|| _||_||
       (__|__|(__|__|
```

(The MIT License)

Copyright (c) 2013 Segment Inc. <friends@segment.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
