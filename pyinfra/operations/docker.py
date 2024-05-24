"""
Manager Docker Containers, Volumes and Networks
"""
from pyinfra import host
from pyinfra.api import operation
from pyinfra.facts.docker import DockerContainer, DockerVolume

from .util.docker import handle_docker


@operation()
def container(
    container,
    image="",
    ports=[],
    networks=[],
    volumes=[],
    env_vars=[],
    pull_always=False,
    present=True,
    force=False,
    start=True,
):
    """
    Manage Docker containers
    + container: name to identify the container
    + image: container image and tag ex: nginx:alpine
    + networks: network list to attach on container
    + ports: port list to expose
    + volumes: volume list to map on container
    + env_vars: environment varible list to inject on container
    + pull_always: force image pull
    + force: remove a contaner with same name and create a new one
    + present: whether the container should be up and running
    + start: start or stop the container

    **Examples:**

    . code:: python

        # Run a container
        docker.container(
            name="Deploy Nginx container",
            container="nginx",
            image="nginx:alpine",
            ports=["80:80"],
            present=True,
            detach=True,
            force=True,
            networks=["proxy", "services"],
            volumes=["nginx_data:/usr/share/nginx/html"],
            pull_always=True,
        )

        # Stop a container
        docker.container(
            name="Stop Nginx container",
            container="nginx",
            start=False,`
        )

        # Start a container
        docker.container(
            name="Start Nginx container",
            container="nginx",
            start=True,
        )
    """

    existent_container = next(iter(host.get_fact(DockerContainer, object_id=container)), None)

    if force:
        if existent_container:
            yield handle_docker(
                resource="container",
                command="remove",
                container=container,
            )

    if present:
        if not existent_container or force:
            yield handle_docker(
                resource="container",
                command="create",
                container=container,
                image=image,
                ports=ports,
                networks=networks,
                volumes=volumes,
                env_vars=env_vars,
                pull_always=pull_always,
                present=present,
                force=force,
                start=start,
            )

    if existent_container and start:
        if existent_container["State"]["Status="] != "running":
            yield handle_docker(
                resource="container",
                command="start",
                container=container,
            )

    if existent_container and not start:
        if existent_container["State"]["Status"] == "running":
            yield handle_docker(
                resource="container",
                command="stop",
                container=container,
            )

    if existent_container and not present:
        yield handle_docker(
            resource="container",
            command="remove",
            container=container,
        )


@operation()
def image(image, present=True):
    """
    Manage Docker images
    + image: Image and tag ex: nginx:alpine
    + present: whether the Docker image should be exist

    **Examples:**

    . code:: python

        # Pull a Docker image
        docker.image(
            name="Pull nginx image",
            image="nginx:alpine",
            present=True,
        )

        # Remove a Docker image
        docker.image(
            name="Remove nginx image",
            image:"nginx:image",
            present=False,
        )
    """

    if present:
        yield handle_docker(
            resource="image",
            command="pull",
            image=image,
        )

    else:
        yield handle_docker(
            resource="image",
            command="remove",
            image=image,
        )


@operation()
def volume(volume, driver="", labels=[], present=True):
    """
    Manage Docker volumes
    + volume_name: Image name
    + driver: Docker volume storage driver
    + labels: Label list to attach in the volume
    + present: whether the Docker volume should exist

    **Examples:**

    . code:: python

        # Create a Docker volume
        docker.volume(
            name="Create nginx volume",
            volume_name="nginx_data",
            present=True
        )
    """

    existent_volume = next(iter(host.get_fact(DockerVolume, object_id=volume)), None)

    if present:

        if existent_volume:
            host.noop("Volume alredy exist!")
            return

        yield handle_docker(
            resource="volume",
            command="create",
            volume=volume,
            driver=driver,
            labels=labels,
            present=present,
        )

    else:
        if existent_volume is None:
            host.noop("There is no {0} volume!".format(volume))
            return

        yield handle_docker(
            resource="volume",
            command="remove",
            volume=volume,
        )
