"""Index String for elasticsearch."""
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

donthackme_mappings = {
    "mappings": {
        "sensor": {
            "properties": {
                "timestamp": {"type": "date"},
                "name": {
                    "type": "string",
                    "fields": {
                        "raw": {"type": "string", "index": "not_analyzed"}
                    }
                },
                "ip": {"type": "ip"},
                "country": {
                    "type": "string",
                    "fields": {
                        "raw": {"type": "string", "index": "not_analyzed"}
                    }
                },
                "region": {
                    "type": "string",
                    "fields": {
                        "raw": {"type": "string", "index": "not_analyzed"}
                    }
                },
                "city": {
                    "type": "string",
                    "fields": {
                        "raw": {"type": "string", "index": "not_analyzed"}
                    }
                },
                "location": {"type": "geo_point"}
            }
        },
        "command": {
            "properties": {
                "timestamp": {"type": "date"},
                "sensor_name": {
                    "type": "string",
                    "fields": {
                        "raw": {"type": "string", "index": "not_analyzed"}
                    }
                },
                "sensor_ip": {"type": "ip"},
                "command": {
                    "type": "string",
                    "fields": {
                        "raw": {"type": "string", "index": "not_analyzed"}
                    }
                },
                "success": {"type": "boolean"}
            }
        },
        "credentials": {
            "properties": {
                "timestamp": {"type": "date"},
                "sensor_name": {
                    "type": "string",
                    "fields": {
                        "raw": {"type": "string", "index": "not_analyzed"}
                    }
                },
                "sensor_ip": {"type": "ip"},
                "username": {
                    "type": "string",
                    "fields": {
                        "raw": {"type": "string", "index": "not_analyzed"}
                    }
                },
                "password": {
                    "type": "string",
                    "fields": {
                        "raw": {"type": "string", "index": "not_analyzed"}
                    }
                },
                "success": {"type": "boolean"},
            }
        },
        "fingerprint": {
            "properties": {
                "timestamp": {"type": "date"},
                "sensor_name": {
                    "type": "string",
                    "fields": {
                        "raw": {"type": "string", "index": "not_analyzed"}
                    }
                },
                "sensor_ip": {"type": "ip"},
                "username": {
                    "type": "string",
                    "fields": {
                        "raw": {"type": "string", "index": "not_analyzed"}
                    }
                },
                "fingerprint": {
                    "type": "string",
                    "fields": {
                        "raw": {"type": "string", "index": "not_analyzed"}
                    }
                }
            }
        },
        "download": {
            "properties": {
                "timestamp": {"type": "date"},
                "sensor_name": {
                    "type": "string",
                    "fields": {
                        "raw": {"type": "string", "index": "not_analyzed"}
                    }
                },
                "sensor_ip": {"type": "ip"},
                "realm": {
                    "type": "string",
                    "fields": {
                        "raw": {"type": "string", "index": "not_analyzed"}
                    }
                },
                "shasum": {
                    "type": "string",
                    "fields": {
                        "raw": {"type": "string", "index": "not_analyzed"}
                    }
                },
                "url": {
                    "type": "string",
                    "fields": {
                        "raw": {"type": "string", "index": "not_analyzed"}
                    }
                },
                "outfile": {
                    "type": "string",
                    "index": "not_analyzed"
                }
            }
        },
        "tcp_connection": {
            "properties": {
                "timestamp": {"type": "date"},
                "sensor_name": {
                    "type": "string",
                    "fields": {
                        "raw": {"type": "string", "index": "not_analyzed"}
                    }
                },
                "sensor_ip": {"type": "ip"},
                "dest_ip": {"type": "ip"},
                "dest_port": {"type": "integer"}
            }
        },
        "session": {
            "properties": {
                "timestamp": {"type": "date"},
                "start_time": {"type": "date"},
                "end_time": {"type": "date"},
                "sensor_name": {
                    "type": "string",
                    "fields": {
                        "raw": {"type": "string", "index": "not_analyzed"}
                    }
                },
                "sensor_ip": {"type": "ip"},
                "source_ip": {"type": "ip"},
                "src_country": {
                    "type": "string",
                    "fields": {
                        "raw": {"type": "string", "index": "not_analyzed"}
                    }
                },
                "src_region": {
                    "type": "string",
                    "fields": {
                        "raw": {"type": "string", "index": "not_analyzed"}
                    }
                },
                "src_city": {
                    "type": "string",
                    "fields": {
                        "raw": {"type": "string", "index": "not_analyzed"}
                    }
                },
                "src_location": {"type": "geo_point"},
                "ttylog": {
                    "type": "nested",
                    "properties": {
                        "size": {"type": "integer"},
                        "log_location": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "asciicast": {
                            "type": "dynamic"
                        },
                        "asciinema_url": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "log_binary": {
                            "type": "binary"
                        }
                    }
                },
                "ttysize": {
                    "type": "nested",
                    "properties": {
                        "width": {"type": "integer"},
                        "height": {"type": "integer"}
                    }
                },
                "ssh_version": {
                    "type": "string",
                    "fields": {
                        "raw": {"type": "string", "index": "not_analyzed"}
                    }
                }
            }
        }
    }
}
