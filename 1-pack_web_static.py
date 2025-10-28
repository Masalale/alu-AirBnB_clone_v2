#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents
of web_static folder
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        Archive path if the archive has been correctly generated,
        None otherwise
    """
    try:
        # Create versions directory if it doesn't exist
        if not os.path.exists("versions"):
            os.makedirs("versions")

        # Generate timestamp for archive name
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = "web_static_{}.tgz".format(timestamp)
        archive_path = "versions/{}".format(archive_name)

        # Create the archive
        print("Packing web_static to {}".format(archive_path))
        result = local("tar -cvzf {} web_static".format(archive_path))

        # Check if archive was created successfully
        if os.path.exists(archive_path):
            archive_size = os.path.getsize(archive_path)
            print("web_static packed: {} -> {}Bytes".format(
                archive_path, archive_size))
            return archive_path
        else:
            return None
    except Exception as e:
        print("Error: {}".format(e))
        return None
