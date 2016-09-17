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

from dateutil.parser import parse as parse_date


logging.basicConfig(format="%(asctime)s - %(levelname)s : %(message)s",
                    level=logging.INFO)


def config(configfile):
    """Parse Yaml Config File."""
    try:
        with open(configfile, 'r') as f:
            conf = yaml.load(f)
    except IOError:
        msg = "Could not open config file: {0}"
        logging.info(msg.format(configfile))
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
        cur = self.logs.find(spec)
        return cur

    def tail_log(self):
        """Main log tailing function."""
        logging.info("Began log tailing.")
        last_id = 900000
        while True:
            cur = self.get_cursor(last_id)
            for msg in cur:
                last_id = msg['ts']
                process_trans_log.delay(msg)
            time.sleep(0.1)

    def import_collection(self, collection_name, since, until):
        """Import collection en masse."""
        doc_class = collection_map[collection_name]
        kwargs = {}

        if collection_name == "session":
            key = "start_time"
        else:
            key = "timestamp"

        if since:
            kwargs[key + "__gte"] = since
        if until:
            kwargs[key + "__lte"] = until

        cur = doc_class.objects(**kwargs)
        for msg in cur:
            process_object.delay(collection_name, msg, upload_asciinema=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", dest="config", type=str,
                        default="/etc/donthackme_elasticsearch/config.yml",
                        help="specify config location.")
    parser.add_argument("--mass-import-collection", "-m", dest="collection",
                        type=str, help="mass import a collection.")
    parser.add_argument("--since", "-s", dest="since", type=str,
                        help="starting date to import from (mass import)")
    parser.add_argument("--until", "-u", dest="until", type=str,
                        help="ending date to import from (mass import)")
    args = parser.parse_args()
    reader = TransLogReader(args.config)
    if args.collection:
        print("mass importing collection: {0}".format(args.collection))
        reader.import_collection(args.collection,
        since=args.since, until=args.until)
    else:
        reader.tail_log()
