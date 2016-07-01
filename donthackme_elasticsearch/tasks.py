"""Celery Tasks for distributed ES Push."""
# Copyright 2016 Russell Troxel
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

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
    location = IpLocation.objects(
        ip_from__lte=ip_address,
        ip_to__gt=ip_address
    ).first()

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
def process_object(collection_name, obj):
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
        item["src_country"] = location.country_name
        item["src_region"] = location.region_name
        item["src_city"] = location.city_name
        item["src_location"] = {
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
        index=conf["index"],
        doc_type=collection_name,
        id=item["doc_id"],
        body=item
    )
