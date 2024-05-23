from pyinfra.api import OperationError


def _create_container(**kwargs):
    command = []

    if kwargs["image"] == "":
        raise OperationError("missing 1 required argument: 'image'")

    command.append("docker container create --name {0}".format(kwargs["container"]))

    for network in kwargs["networks"]:
        command.append("--network {0}".format(network))

    for port in kwargs["ports"]:
        command.append("-p {0}".format(port))

    for volume in kwargs["volumes"]:
        command.append("-v {0}".format(volume))

    for env_var in kwargs["env_vars"]:
        command.append("-e {0}".format(env_var))

    if kwargs["pull_always"]:
        command.append("--pull always")

    command.append(kwargs["image"])

    if kwargs["start"]:
        command.append("; {0}".format(_start_container(container=kwargs["container"])))

    return " ".join(command)


def _remove_container(**kwargs):
    return "docker container rm -f {0}".format(kwargs["container"])


def _start_container(**kwargs):
    return "docker container start {0}".format(kwargs["container"])


def _stop_container(**kwargs):
    return "docker container stop {0}".format(kwargs["container"])


def _pull_image(**kwargs):
    return "docker image pull {0}".format(kwargs["image"])


def _remove_image(**kwargs):
    return "docker image rm {0}".format(kwargs["image"])


def _create_volume(**kwargs):
    command = []
    command.append("docker volume create {0}".format(kwargs["volume"]))

    if kwargs["driver"] != "":
        command.append("-d {0}".format(kwargs["driver"]))

    for label in kwargs["labels"]:
        command.append("--label {0}".format(kwargs[label]))

    return " ".join(command)


def _remove_volume(**kwargs):
    return "docker image rm {0}".format(kwargs["volume"])


def _create_network(**kwargs):
    command = []
    command.append("docker network create {0}".format(kwargs["network"]))
    if kwargs["driver"] != "":
        command.append("-d {0}".format(kwargs["driver"]))

    if kwargs["gateway"] != "":
        command.append("--gateway {0}".format(kwargs["gateway"]))

    if kwargs["ip_range"] != "":
        command.append("--ip-range {0}".format(kwargs["ip_range"]))

    if kwargs["ipam_driver"] != "":
        command.append("--ipam-driver {0}".format(kwargs["ipam_driver"]))

    if kwargs["subnet"] != "":
        command.append("--subnet {0}".format(kwargs["subnet"]))

    if kwargs["scope"] != "":
        command.append("--scope {0}".format(kwargs["scope"]))

    if kwargs["ingress"]:
        command.append("--ingress")

    if kwargs["attachable"]:
        command.append("--attachable")

    for opt in kwargs["opts"]:
        command.append("--opt {0}".format(opt))

    for opt in kwargs["ipam_opts"]:
        command.append("--ipam-opt {0}".format(opt))

    for label in kwargs["labels"]:
        command.append("--label {0}".format(label))


def _remove_network(**kwargs):
    return "docker network rm {0}".format(kwargs["network"])


def handle_docker(resource, command, **kwargs):
    container_commands = {
        "create": _create_container,
        "remove": _remove_container,
        "start": _start_container,
        "stop": _stop_container,
    }

    image_commands = {
        "pull": _pull_image,
        "remove": _remove_image,
    }

    volume_commands = {
        "create": _create_volume,
        "remove": _remove_volume,
    }

    network_commands = {
        "create": _create_network,
        "remove": _remove_network,
    }

    docker_commands = {
        "container": container_commands,
        "image": image_commands,
        "volume": volume_commands,
        "network": network_commands,
    }

    return docker_commands[resource][command](**kwargs)
