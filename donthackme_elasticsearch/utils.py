"""Util Functions for ES Push."""
import certifi
import sys
import yaml


def _config(configfile):
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


def _prepare_es_config(self, es_config):
    """Prepare elasticsearch config entry for use in py-elasticsearch."""
    es_config["http_auth"] = (
        es_config.pop("username"),
        es_config.pop("password")
    )
    es_config["ca_certs"] = certifi.where()
    return es_config
