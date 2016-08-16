#!/usr/bin/env python

import argparse
import pprint
from utils import get_drive_service

def list_drive(drive_service, name=None, verbose=0):
    result = []
    page_token = None
    while True:
        param = {}
        if page_token:
            param['pageToken'] = page_token
        if name:
            param['q'] = "title = '{}'".format(name)
        files = drive_service.files().list(**param).execute()
        result.extend(files['items'])
        page_token = files.get('nextPageToken')
        if not page_token:
            break
    return(result)

def print_raw_result(result):
    print('total {}'.format(len(result)))
    for item in result:
        pprint.pprint(item)

def print_result(result, md5, parents):
    for item in result:
        if md5:
            if 'md5Checksum' in item:
                sum = item['md5Checksum']
            else:
                sum = '0'*32
            print(u'{} {}'.format(sum, item['title']).encode('utf8'))
        if parents:
            print(u'{} {}'.format(len(item['parents']), item['title']).encode('utf8'))
        if not md5 and not parents:
            print(u'{}'.format(item['title']).encode('utf8'))

if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tokenFile', action='store', required=True, help='file containing OAuth token in JSON format')
    parser.add_argument('-v', '--verbose', action='count', help='show verbose output')
    parser.add_argument('name', nargs='?', action='store', help='name to list')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-m', '--md5', action='store_true', help='show md5sums')
    group.add_argument('-p', '--parents', action='store_true', help='show parent counts')
    group.add_argument('-r', '--raw', action='store_true', help='show raw output')
    args = parser.parse_args()
    drive_service = get_drive_service(args.tokenFile, args.verbose)
    result = list_drive(drive_service, args.name, args.verbose)
    if args.raw:
        print_raw_result(result)
    else:
        print_result(result, args.md5, args.parents)
