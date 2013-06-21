#!/usr/bin/python
# -*- coding: utf-8 -*-
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import pyrax
import time
import logging


# Servers to build
server_names = ['web1', 'web2', 'web3']
delete = False

# Logging
#logging.basicConfig(level=logging.INFO)
logging.warn("Change logging level to INFO for more details.")

# Setup pyrax creds and objects
pyrax.set_credential_file(".rackspace_cloud_credentials")
cs = pyrax.cloudservers
imgs = cs.images.list()
flvs = cs.flavors.list()

# Select Ubuntu and 512MB
ubu_image = [img for img in cs.images.list()
             if "Ubuntu 12.04" in img.name][0]
flavor_512 = [flavor for flavor in cs.flavors.list()
              if flavor.ram == 512][0]

servers = []
output = []

for name in server_names:
    network = 0

    # Create server and print attributes
    server = cs.servers.create(name, ubu_image.id, flavor_512.id)
    servers.append(server)
    output.append("=" * 30)
    output.append("Name: " + str(server.name))
    output.append("ID: " + str(server.id))
    output.append("Status: " + str(server.status))
    output.append("Admin Password: " + str(server.adminPass))

    # Check for network configuration
    logging.warn("Waiting for network. This can take a while. Be patient.")
    while "public" not in server.networks:
        server = cs.servers.get(server.id)
        time.sleep(10)
    else:
        output.append("Network: " + str(server.networks))

# Delete servers
if delete is True:
    for server in servers:
        logging.warn("Deleting %s", server.id)
        server.delete()

for message in output:
    print message
