import os

from ydk.providers import CodecServiceProvider
from ydk.services import CodecService
from ydk.services import CRUDService
from ydk.services import NetconfService, Datastore
from ydk.providers import NetconfServiceProvider
from ydk.path import Repository

# Instantiate the codec service
codec = CodecService()

# Instantiate codec providers with json and xml options
json_provider = CodecServiceProvider(type='json')
xml_provider = CodecServiceProvider(type='xml')

home = os.path.expanduser("~")
repo = Repository(os.path.join(home, "projects", "junos_yang"))
# create NETCONF provider
nc_provider = NetconfServiceProvider(
    address="10.1.2.1",
    port=22,
    username="root",
    password="Juniper",
    protocol="ssh",
    repo=repo  # see: https://community.cisco.com/t5/yang-development-kit-ydk/issue-with-retrieving-of-schema/td-p/3544980
)

if_json = r'''{
  "junos-qfx-conf-root:configuration": {
    "junos-qfx-conf-interfaces:interfaces": {
      "interface": [
        {
          "name": "ge-0/0/0",
          "description": "\"test desc\"",
          "unit": [
            {
              "name": "0",
              "family": {
                "inet": {
                  "address": [
                    {
                      "name": "10.0.0.2"
                    }
                  ]
                }
              }
            }
          ]
        }
      ]
    }
  }
}'''


# Invoke the decode method  to decode the JSON payload to a YDK python object
interface_configurations = codec.decode(json_provider, if_json)

# create NETCONF service
netconf = NetconfService()
netconf.edit_config(nc_provider, Datastore.candidate, interface_configurations)

print("exiting...")
exit()
