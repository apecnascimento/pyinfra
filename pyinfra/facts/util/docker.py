import json
import re


def convert_key(key):
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    ignored_keys = ["ID", "IPv6", "IPv4"]

    if key in ignored_keys:
        return key.lower()

    return pattern.sub("_", key).lower()


def convert_dict(docker_object):
    return {convert_key(key): docker_object[key] for key in docker_object}


def parse_response(output):
    return [convert_dict(json.loads(o)) for o in output]
