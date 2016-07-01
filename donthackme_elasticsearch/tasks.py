"""Celery Tasks for distributed ES Push."""

import os
import netaddr
import socket

from celery import Celery
from datetime import datetime
from elasticsearch import Elasticsearch
from mongoengine import connect

from donthackme_elasticsearch.utils import (_config,
                                            _prepare_es_config)

from donthackme_elasticsearch.indexes import donthackme_mappings
from donthackme_elasticsearch.models import (collection_map,
                                             IpLocation)

try:
    configfile = os.environ["ESPUSH_CELERY_CONFIG"]
except KeyError:
    print("Please set config file location in env:ESPUSH_CELERY_CONFIG")


conf = _config(configfile)

connect(**conf["mongo"])

es_config = _prepare_es_config(conf["elasticsearch"])
es = Elasticsearch(**es_config)

if not es.indices.exists(conf["index"]):
    es.indices.create(
        index=conf["index"],
        body=donthackme_mappings
    )

app = Celery("tasks", broker=conf["celery"]["broker"])


def _geoip(ip_address):
    """Geolocate IP."""
    ip_address = int(netaddr.IPAddress(ip_address))
    location = IpLocation.objects.get(
        ip_from__lte=ip_address,
        ip_to__gt=ip_address
    )

    return location


def _ensure_ip(address):
    try:
        socket.inet_aton(address)
        return address
    except:
        return socket.gethostbyname(address)


@app.task
def process_trans_log(log):
    """Process a TransactionLog object."""
    doc_class = collection_map[log["collection"]]
    obj = doc_class.objects.get(id=log["doc_id"])
    process_object(log["collection"], obj)


@app.task
def process_object(es_object, index_name, collection_name, obj):
    """Process a MongoEngine object."""
    item = obj.to_dict()
    item["doc_id"] = str(obj.id)
    if collection_name == "sensor":
        location = _geoip(item["ip"])
        item["country"] = location.country_name
        item["region"] = location.region_name
        item["city"] = location.city_name
        item["location"] = {
            "lat": location.lat,
            "lon": location.lon
        }
    if collection_name == "session":
        item["timestamp"] = item["start_time"]
        location = _geoip(item["source_ip"])
        item["country"] = location.country_name
        item["region"] = location.region_name
        item["city"] = location.city_name
        item["location"] = {
            "lat": location.lat,
            "lon": location.lon
        }
    print("{0}:  {1}  -  {2}".format(
        str(datetime.utcnow()),
        collection_name,
        item["doc_id"]
    ))
    for key in ["source_ip", "dest_ip"]:
        if key in item:
            item[key] = _ensure_ip(item[key])
    es.index(
        index=index_name,
        doc_type=collection_name,
        id=item["doc_id"],
        body=item
    )
