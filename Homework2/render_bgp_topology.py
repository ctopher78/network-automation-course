
from __future__ import print_function

import sys
import json

from nornir import InitNornir
from nornir.plugins.tasks import networking
from nornir.plugins.functions.text import print_result

from jinja2 import Environment, PackageLoader, select_autoescape


def main():

    devices = InitNornir(
    core={"num_workers": 100},
    inventory={
        "plugin": "nornir.plugins.inventory.simple.SimpleInventory",
        "options": {
            "host_file": "inventory/hosts.yaml",
            "group_file": "inventory/groups.yaml"
            }
        }
    )

    results = devices.run(task=networking.napalm_get, getters=["get_bgp_neighbors_detail"])

    bgp = dict()
    for k, v in results.items():
        bgp[k] = v.result["get_bgp_neighbors_detail"]["global"]

    print(json.dumps(bgp, indent=2))
    env = Environment(
        loader=PackageLoader('bgp_topology', 'templates'),
        autoescape=select_autoescape(['html'])
    )

    template = env.get_template('js.jinja')

    rendered = template.render(netdev_bgp=bgp)

    with open("bgp_topology.html", "w+") as fh:
        fh.write(rendered)


if __name__ == "__main__":
    sys.exit(main())