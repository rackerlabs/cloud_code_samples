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
import logging
import argparse


# Logging
#logging.basicConfig(level=logging.INFO)

# Setup pyrax creds and objects
pyrax.set_credential_file(".rackspace_cloud_credentials")
dns = pyrax.cloud_dns

# Handle arguments
parser = argparse.ArgumentParser()
parser.add_argument('FQDN', type=str,
                    help="The name of the new A record.")
parser.add_argument('IP', type=str,
                    help="The IP address for this new record.")
parser.add_argument('-z', '--zone', type=str,
                    help="Specify the zone where the record is to be added.")

args = parser.parse_args()

# Handle the zone
if args.zone:
    zone = args.zone
else:
    # Give the (hopefully) root domain of the FQDN.
    zone = '.'.join(args.FQDN.split('.')[-2:])

# Build the a record dictionary
a_record = {"type": "A",
            "name": args.FQDN,
            "data": args.IP,
            "ttl": 300}

# Check for the domain
try:
    dom = dns.find(name=zone)
except pyrax.exceptions.NotFound:
    logging.error("Domain %s was not found. Specify your zone using -z.", zone)
else:
    records = dom.add_records(a_record)
    print records
