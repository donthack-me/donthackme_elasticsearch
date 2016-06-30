#!/usr/bin/env python2
"""TransLogReader for DontHack.Me API."""

from __future__ import print_function

import argparse
import certifi
import logging
import netaddr
import sys
import socket
import time
import yaml


from mongoengine import connect
from elasticsearch import Elasticsearch

from donthackme_elasticsearch.indexes import donthackme_mappings
from donthackme_elasticsearch.models import (collection_map,
                                             TransactionLog,
                                             IpLocation)


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


def geoip(ip_address):
    """Geolocate IP."""
    ip_address = int(netaddr.IPAddress(ip_address))
    location = IpLocation.objects.get(
        ip_from__lte=ip_address,
        ip_to__gt=ip_address
    )
    return location


class TransLogReader(object):
    """Read TransactionLogs from MongoEngine."""

    def __init__(self, conf):
        """init."""
        self.conf = config(conf)

        connect(**self.conf["mongo"])

        self.db = TransactionLog._get_db()
        self.logs = self.db.transaction_log

        es_config = self.prepare_es_config(self.conf["elasticsearch"])
        self.es = Elasticsearch(**es_config)

        self.index = self.conf["index"]
        if not self.es.indices.exists(self.index):
            self.es.indices.create(
                index=self.index,
                body=donthackme_mappings
            )

    def _ensure_ip(self, address):
        try:
            socket.inet_aton(address)
            return address
        except:
            return socket.gethostbyname(address)

    def prepare_es_config(self, es_config):
        """Prepare elasticsearch config entry for use in py-elasticsearch."""
        es_config["http_auth"] = (
            es_config.pop("username"),
            es_config.pop("password")
        )
        es_config["ca_certs"] = certifi.where()
        return es_config

    def process_trans_log(self, log):
        """Process a TransactionLog object."""
        doc_class = collection_map[log["collection"]]
        item = doc_class.objects.get(id=log["doc_id"]).to_dict()
        print(item)
        if log["collection"] == "sensor":
            location = geoip(item["ip"])
            item["country"] = location.country_name
            item["region"] = location.region_name
            item["city"] = location.city_name
            item["location"] = {
                "lat": location.lat,
                "lon": location.lon
            }
        if log["collection"] == "session":
            item["timestamp"] = item["start_time"]
            location = geoip(item["source_ip"])
            item["country"] = location.country_name
            item["region"] = location.region_name
            item["city"] = location.city_name
            item["location"] = {
                "lat": location.lat,
                "lon": location.lon
            }
        print(item)
        for key in ["source_ip", "dest_ip"]:
            if key in item:
                item[key] = self._ensure_ip(item[key])
        self.es.index(
            index=self.index,
            doc_type=log["collection"],
            id=str(log["doc_id"]),
            body=item
        )

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
                print(msg)
                self.process_trans_log(msg)
            time.sleep(0.1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", dest="config", type=str,
                        default="/etc/donthackme_elasticsearch/config.yml",
                        help="specify config location.")
    args = parser.parse_args()
    reader = TransLogReader(args.config)
    reader.tail_log()
