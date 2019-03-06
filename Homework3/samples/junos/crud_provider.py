#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import yaml

from ydk.types import Empty
from ydk.types import Filter

from ydk.path import Repository

from ydk.services import CRUDService
from ydk.services import CodecService
from ydk.services import ExecutorService

from ydk.providers import CodecServiceProvider
from ydk.providers import NetconfServiceProvider

from ydk.models.junos_qfx.junos_qfx_conf_root import Configuration


def config_ifaces(ifaces_obj, edges):
    for edge in edges:
        iface = Configuration.Interfaces.Interface()
        iface.name = edge["interface"]
        iface.description = edge["desc"]

        unit = Configuration.Interfaces.Interface.Unit()
        unit.name = "0"

        family = Configuration.Interfaces.Interface.Unit.Family()

        inet = Configuration.Interfaces.Interface.Unit.Family.Inet()

        family_inet_addr = Configuration.Interfaces.Interface.Unit.Family.Inet.Address()
        family_inet_addr.name = edge["local_ip"] + "/30"

        inet.address.append(family_inet_addr)

        family.inet = inet

        unit.family = family

        iface.unit.append(unit)
        ifaces_obj.interface.append(iface)


def config_bgp(bgp, edges):
    bgp_group = bgp.Group()
    bgp_group.name = "underlay"

    for edge in edges:
        print("adding neighbor '{}', peer asn '{}'".format(edge["peer_ip"], edge["asn"]))

        neighbor = bgp_group.Neighbor()
        neighbor.name = edge["peer_ip"]
        neighbor.peer_as = str(edge["asn"])

        bgp_group.neighbor.append(neighbor)

    bgp.group.append(bgp_group)


def get_netconf_provider(device_ip):
    home = os.path.expanduser("~")
    repo = Repository(os.path.join(home, "projects", "junos_yang"))
    
    nc_provider = NetconfServiceProvider(
        address=device_ip,
        port=22,
        username="root",
        password="Juniper",
        protocol="ssh",
        repo=repo  # see: https://community.cisco.com/t5/yang-development-kit-ydk/issue-with-retrieving-of-schema/td-p/3544980
    )

    return nc_provider


def config_edges(model):
    for node, attrs in model["nodes"].items():
        print("Configuring edges for: ", node)
        print("setting up netconf provider for: '{}'".format(attrs["mgt_ip"]))
        nc_provider = get_netconf_provider(attrs["mgt_ip"])

        # create CRUD service
        crud = CRUDService()

        ifaces_obj = Configuration.Interfaces()
        config_ifaces(ifaces_obj, attrs["edges"])  # add object configuration

        bgp_obj = Configuration.Protocols.Bgp()
        config_bgp(bgp_obj, attrs["edges"])

        # NOTE: The filter didn't work for me as I expected it to 
        # investigate this option further.
        # create_filter = Filter(ifaces_obj, bgp_obj)

        # create configuration on NETCONF device
        crud.create(nc_provider, ifaces_obj)
        crud.create(nc_provider, bgp_obj)


def main():

    with open("node_edges.yaml", "r") as fh:
        model = yaml.load(fh.read())

    config_edges(model)
 
    print("done!")


if __name__ == "__main__":
    sys.exit(main())