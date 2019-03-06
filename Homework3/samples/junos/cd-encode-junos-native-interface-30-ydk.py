#!/usr/bin/env python
#
# Copyright 2016 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Encode configuration for model Cisco-IOS-XE-native.

usage: cd-encode-xe-native-interface-30-ydk.py [-h] [-v]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print debugging messages
"""

from argparse import ArgumentParser
from urlparse import urlparse

from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.models.junos_qfx import junos_qfx_rpc_ping as jping
from ydk.models.junos_qfx.junos_qfx_conf_root.Configuration.Interfaces import Interface 
from ydk.models.junos_qfx.junos_qfx_conf_root import Configuration
import logging


def config_native(conf):
    """Add config data to native object."""
    iface = conf.Interfaces.Interface()
    loopback.name = "xe-0/0/1"
    loopback.description = "TEST Description"

    subiface = iface
    loopback.ip.address.primary.address = "172.16.255.1"
    loopback.ip.address.primary.mask = "255.255.255.255"
    native.interface.loopback.append(loopback)


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    args = parser.parse_args()

    # log debug messages if verbose argument specified
    if args.verbose:
        logger = logging.getLogger("ydk")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                      "%(levelname)s - %(message)s"))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # create codec provider
    provider = CodecServiceProvider(type="json")

    # create codec service
    codec = CodecService()

    native = xe_native.Native()  # create object
    config_native(native)  # add object configuration

    # encode and print object
    print(codec.encode(provider, native))

    exit()
# End of script
