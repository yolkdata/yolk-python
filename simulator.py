import logging
import argparse
import json
import yolk

__name__ = 'simulator.py'
__version__ = '0.0.1'
__description__ = 'scripting simulator'


def json_hash(str):
    if str:
        return json.loads(str)

# yolk -method=<method> -yolk-write-key=<segmentWriteKey> [options]


parser = argparse.ArgumentParser(description='send a segment message')

parser.add_argument('--writeKey', help='the Yolk writeKey')
parser.add_argument('--type', help='The Yolk message type')

parser.add_argument('--userId', help='the user id to send the event as')
parser.add_argument(
    '--anonymousId', help='the anonymous user id to send the event as')
parser.add_argument(
    '--context', help='additional context for the event (JSON-encoded)')

parser.add_argument('--event', help='the event name to send with the event')
parser.add_argument(
    '--properties', help='the event properties to send (JSON-encoded)')

parser.add_argument(
    '--name', help='name of the screen or page to send with the message')

parser.add_argument(
    '--traits', help='the identify/group traits to send (JSON-encoded)')

parser.add_argument('--groupId', help='the group id')

options = parser.parse_args()


def failed(status, msg):
    raise Exception(msg)


def track():
    yolk.track(options.userId, options.event, anonymous_id=options.anonymousId,
                    properties=json_hash(options.properties), context=json_hash(options.context))

def alias():
    yolk.alias(options.userId, options.event, anonymous_id=options.anonymousId,
                    properties=json_hash(options.properties), context=json_hash(options.context))

def page():
    yolk.page(options.userId, name=options.name, anonymous_id=options.anonymousId,
                   properties=json_hash(options.properties), context=json_hash(options.context))


def screen():
    yolk.screen(options.userId, name=options.name, anonymous_id=options.anonymousId,
                     properties=json_hash(options.properties), context=json_hash(options.context))


def identify():
    yolk.identify(options.userId, anonymous_id=options.anonymousId,
                       traits=json_hash(options.traits), context=json_hash(options.context))


def group():
    yolk.group(options.userId, options.groupId, json_hash(options.traits),
                    json_hash(options.context), anonymous_id=options.anonymousId)


def unknown():
    print()


yolk.write_key = options.writeKey
yolk.on_error = failed
yolk.debug = True

log = logging.getLogger('segment')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
log.addHandler(ch)

switcher = {
    "track": track,
    "page": page,
    "screen": screen,
    "identify": identify,
    "group": group
}

func = switcher.get(options.type)
if func:
    func()
    yolk.shutdown()
else:
    print("Invalid Message Type " + options.type)
