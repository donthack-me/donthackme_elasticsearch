#!/usr/bin/env python2
"""TransLogReader for DontHack.Me API."""

from __future__ import print_function

import argparse
import logging
import sys
import time
import yaml

from mongoengine import connect

from donthackme_elasticsearch.models import (collection_map,
                                             TransactionLog)
from donthackme_elasticsearch.tasks import (process_object,
                                            process_trans_log)
from pymongo import CursorType


logging.basicConfig(format="%(asctime)s - %(levelname)s : %(message)s",
                    level=logging.INFO)


def config(configfile):
    """Parse Yaml Config File."""
    try:
        with open(configfile, 'r') as f:
            conf = yaml.load(f)
    except IOError:
        # msg = "Could not open config file: {0}"
        # logging.info(msg.format(configfile))
        sys.exit(1)
    else:
        return conf


class TransLogReader(object):
    """Read TransactionLogs from MongoEngine."""

    def __init__(self, conf):
        """init."""
        self.conf = config(conf)

        connect(**self.conf["mongo"])

        self.db = TransactionLog._get_db()
        self.logs = self.db.transaction_log

    def get_cursor(self, last_id=-1, await_data=True):
        """Create cursor object based on last_id."""
        spec = {'ts': {'$gt': last_id}}
        cur = self.logs.find(spec,
                             cursor_type=CursorType.TAILABLE_AWAIT,
                             oplog_replay=True)
        return cur

    def tail_log(self):
        """Main log tailing function."""
        last_id = -1
        while True:
            cur = self.get_cursor(last_id)
            for msg in cur:
                last_id = msg['ts']
                process_trans_log.delay(msg)
            time.sleep(0.1)

    def import_collection(self, collection_name):
        """Import collection en masse."""
        doc_class = collection_map[collection_name]
        cur = doc_class.objects()
        for msg in cur:
            process_object.delay(collection_name, msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", dest="config", type=str,
                        default="/etc/donthackme_elasticsearch/config.yml",
                        help="specify config location.")
    parser.add_argument("--mass-import-collection", "-m", dest="collection",
                        type=str, help="mass import a collection.")
    args = parser.parse_args()
    reader = TransLogReader(args.config)
    if args.collection:
        print("mass importing collection: {0}".format(args.collection))
        reader.import_collection(args.collection)
    else:
        reader.tail_log()
