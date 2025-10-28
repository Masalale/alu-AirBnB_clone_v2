#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from web_static
"""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Generates a .tgz archive from web_static folder"""
    if not os.path.isdir("versions"):
        os.makedirs("versions")
    now = datetime.now()
    archive_name = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)
    result = local("tar -cvzf {} web_static".format(archive_name))
    if result.succeeded:
        return archive_name
    else:
        return None
