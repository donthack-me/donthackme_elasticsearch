"""Index String for elasticsearch."""
donthackme_mappings = {
  "mappings": {
    "sensor": {
      "properties": {
        "timestamp":    { "type": "date"      },
        "name":         { "type": "string"    },
        "ip":           { "type": "ip"        },
        "country":      { "type": "string"    },
        "region":       { "type": "string"    },
        "city":         { "type": "string"    },
        "location":     { "type": "geo_point" }
      }
    },
    "command": {
      "properties": {
        "timestamp":    { "type": "date"      },
        "sensor_name":  { "type": "string"    },
        "sensor_ip":    { "type": "ip"        },
        "command":		{ "type": "string"    },
        "success":      { "type": "boolean"   }
      }
    },
    "credentials": {
      "properties": {
        "timestamp":    { "type": "date"      },
        "sensor_name":  { "type": "string"    },
        "sensor_ip":    { "type": "ip"        },
        "username":     { "type": "string"    },
        "password":     { "type": "string"    },
        "success":      { "type": "boolean"   },
      }
    },
    "fingerprint": {
      "properties": {
        "timestamp":    { "type": "date"      },
        "sensor_name":  { "type": "string"    },
        "sensor_ip":    { "type": "ip"        },
        "username":     { "type": "string"    },
        "fingerprint":  { "type": "string"    }
      }
    },
    "download": {
      "properties": {
        "timestamp":    { "type": "date"      },
        "sensor_name":  { "type": "string"    },
        "sensor_ip":    { "type": "ip"        },
        "realm":        { "type": "string"    },
        "shasum":       {
          "type": "string",
          "index": "not_analyzed"
        },
        "url":          { "type": "string"    },
        "outfile":      {
          "type": "string",
          "index": "not_analyzed"
        }
      }
    },
    "tcp_connection": {
      "properties": {
        "timestamp":    { "type": "date"      },
        "sensor_name":  { "type": "string"    },
        "sensor_ip":    { "type": "ip"        },
        "dest_ip":		{ "type": "ip"        },
        "dest_port":    { "type": "integer"   }
      }
    },
    "session": {
      "properties": {
        "timestamp":    { "type": "date"      },
        "start_time":   { "type": "date"      },
        "end_time":     { "type": "date"      },
        "sensor_name":  { "type": "string"    },
        "sensor_ip":    { "type": "ip"        },
        "source_ip":    { "type": "ip"        },
        "src_country":  { "type": "string"    },
        "src_region":   { "type": "string"    },
        "src_city":         { "type": "string"    },
        "src_location": { "type": "geo_point" },
        "ttylog":       {
          "type": "nested",
          "properties": {
            "size":         { "type": "integer" },
            "log_location": {
              "type": "string",
              "index": "not_analyzed"
            },
            "log_binary":   {
              "type": "binary",
              "index": "not_analyzed"
            }
          }
        },
        "ttysize": {
          "type": "nested",
          "properties": {
            "width":        { "type": "integer" },
            "height":       { "type": "integer" }
          }
        },
        "ssh_version":  { "type": "string"    },
      }
    }
  }
}
