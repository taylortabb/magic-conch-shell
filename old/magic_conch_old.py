#!/usr/bin/env python

# Taylor Tabb. January 2018.

from __future__ import print_function

import logging
import platform
import subprocess
import sys

import argparse
import json
import os.path
import pathlib2 as pathlibz

from playsound import playsound

import google.oauth2.credentials

from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file
from google.assistant.library.device_helpers import register_device

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


WARNING_NOT_REGISTERED = """
    This device is not registered. This means you will not be able to use
    Device Actions or see your device in Assistant Settings. In order to
    register this device follow instructions at:

    https://developers.google.com/assistant/sdk/guides/library/python/embed/register-device
"""


# def process_event(event):
#     """Pretty prints events.

#     Prints all events that occur with two spaces between each new
#     conversation and a single space between turns of a conversation.

#     Args:
#         event(event.Event): The current event to process.
#     """
#     if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
#         print()

#     print(event)

#     if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
#             event.args and not event.args['with_follow_on_turn']):
#         print()
#     if event.type == EventType.ON_DEVICE_ACTION:
#         for command, params in event.actions:
#             print('Do command', command, 'with params', str(params))

###me
def married():
    playsound('/conch-recordings/maybe_some_day.wav')

def process_event(assistant, event):
    if event.type == EventType.ON_START_FINISHED:
        print('ready')
        if sys.stdout.isatty():
            print('Say "OK, Google" then speak, or press Ctrl+C to quit...')

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        print('listening')

    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('You said:', event.args['text'])
        text = event.args['text'].lower()
        if text == 'Will I ever get married':
            assistant.stop_conversation()
            married()
        
    elif event.type == EventType.ON_END_OF_UTTERANCE:
        print('thinking')

    elif event.type == EventType.ON_CONVERSATION_TURN_FINISHED:
        print('ready')

    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)

### end me

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--device-model-id', '--device_model_id', type=str,
                        metavar='DEVICE_MODEL_ID', required=False,
                        help='the device model ID registered with Google')
    parser.add_argument('--project-id', '--project_id', type=str,
                        metavar='PROJECT_ID', required=False,
                        help='the project ID used to register this device')
    parser.add_argument('--nickname', type=str,
                        metavar='NICKNAME', required=False,
                        help='the nickname used to register this device')
    parser.add_argument('--device-config', type=str,
                        metavar='DEVICE_CONFIG_FILE',
                        default=os.path.join(
                            os.path.expanduser('~/.config'),
                            'googlesamples-assistant',
                            'device_config_library.json'
                        ),
                        help='path to store and read device configuration')
    parser.add_argument('--credentials', type=existing_file,
                        metavar='OAUTH2_CREDENTIALS_FILE',
                        default=os.path.join(
                            os.path.expanduser('~/.config'),
                            'google-oauthlib-tool',
                            'credentials.json'
                        ),
                        help='path to store and read OAuth2 credentials')
    parser.add_argument('--query', type=str,
                        metavar='QUERY',
                        help='query to send as soon as the Assistant starts')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + Assistant.__version_str__())

    args = parser.parse_args()
    with open(args.credentials, 'r') as f:
        credentials = google.oauth2.credentials.Credentials(token=None,
                                                            **json.load(f))

    device_model_id = 'magic-conch-shell-pi'
    last_device_id = '50196C5AD73A2994B2FB137E893F4181'
    
    try:
        with open(args.device_config) as f:
            device_config = json.load(f)
            device_model_id = device_config['model_id']
            last_device_id = device_config.get('last_device_id', None)
    except FileNotFoundError:
        pass

    if not args.device_model_id and not device_model_id:
        raise Exception('Missing --device-model-id option')

    # Re-register if "device_model_id" is given by the user and it differs
    # from what we previously registered with.
    should_register = (
        args.device_model_id and args.device_model_id != device_model_id)

    device_model_id = args.device_model_id or device_model_id

    with Assistant(credentials, device_model_id) as assistant:
        events = assistant.start()

        device_id = assistant.device_id
        print('device_model_id:', device_model_id)
        print('device_id:', device_id + '\n')

        # Re-register if "device_id" is different from the last "device_id":
        if should_register or (device_id != last_device_id):
            if args.project_id:
                register_device(args.project_id, credentials,
                                device_model_id, device_id, args.nickname)
                pathlib.Path(os.path.dirname(args.device_config)).mkdir(
                    exist_ok=True)
                with open(args.device_config, 'w') as f:
                    json.dump({
                        'last_device_id': device_id,
                        'model_id': device_model_id,
                    }, f)
            else:
                print(WARNING_NOT_REGISTERED)

        for event in events:
            if event.type == EventType.ON_START_FINISHED and args.query:
                assistant.send_text_query(args.query)

            process_event(assistant, event)


if __name__ == '__main__':
    main()

