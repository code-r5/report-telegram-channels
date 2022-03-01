import io
import os
import random
import sys
import time
import urllib
from os.path import exists
from urllib.request import urlopen
from telethon.sync import TelegramClient
from telethon import functions, types

CHANLIST_URL = 'https://github.com/fk-war-in-ukraine/report-telegram-channels/raw/master/dirty_channels.txt'

def print_help() -> None:
    print('Usage:')
    print('\tpython main.py <api_id> <api_hash>')



def get_dirty_channels() -> set:
    chan_path = os.path.join(os.path.dirname(os.path.relpath(__file__)), 'dirty_channels.txt')
    if exists(chan_path):
        with open(chan_path, 'r') as fp:
            dirty_channels = fp.readlines()
    else:
        with urlopen(CHANLIST_URL) as remote_file:
            remote_content = remote_file.read().decode('utf-8')
        with open(chan_path, 'w') as download:
            download.write(remote_content)
        dirty_channels = io.StringIO(remote_content).readlines()
    return set(dirty_channels)


def get_messages() -> list:
    with open(os.path.join(os.path.dirname(os.path.relpath(__file__)), 'messages.txt'), 'r') as fp:
        messages = fp.readlines()

    return messages


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print_help()
        exit(1)

    api_id = int(sys.argv[1])
    api_hash = sys.argv[2]

    dirty_channels = get_dirty_channels()
    messages = get_messages()

    with TelegramClient('ReportDirtyChannels', api_id, api_hash) as client:
        for dirty_channel in dirty_channels:
            dirty_channel = dirty_channel.strip()
            msg = random.choice(messages).strip()
            try:
                result = client(functions.account.ReportPeerRequest(
                    peer=client.get_entity(dirty_channel),
                    reason=types.InputReportReasonOther(),
                    message=msg
                ))
                print('{}: {} - {}'.format(dirty_channel, result, msg))
                time.sleep(random.randint(3, 15) / 10.0)
            except Exception as e:
                print('{}: error - {}'.format(dirty_channel, str(e)))
