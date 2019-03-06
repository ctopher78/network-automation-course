

from ydk.providers import CodecServiceProvider
from ydk.services import CodecService

# Instantiate the codec service
codec = CodecService()

# Instantiate codec providers with json and xml options
json_provider = CodecServiceProvider(type='json')
xml_provider = CodecServiceProvider(type='xml')

if_xmls = '''<configuration xmlns="http://yang.juniper.net/junos-qfx/conf/root" xmlns:jc-interfaces="http://yang.juniper.net/junos-qfx/conf/interfaces">
        <jc-interfaces:interfaces>
          <jc-interfaces:interface>
            <jc-interfaces:name>ge-0/0/0</jc-interfaces:name>
            <jc-interfaces:description>"test desc"</jc-interfaces:description>
            <jc-interfaces:unit>
              <jc-interfaces:name>0</jc-interfaces:name>
              <jc-interfaces:family>
                <jc-interfaces:inet>
                  <jc-interfaces:address>
                    <jc-interfaces:name xc:operation="create">10.0.0.1</jc-interfaces:name>
                  </jc-interfaces:address>
                </jc-interfaces:inet>
              </jc-interfaces:family>
            </jc-interfaces:unit>
          </jc-interfaces:interface>
        </jc-interfaces:interfaces>
      </configuration>'''

if_json2 = r'''{
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
                      "name": "10.0.0.1"
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

# Declare the JSON configuration
if_json = ''' {
  "Cisco-IOS-XR-ifmgr-cfg:interface-configurations": {
    "interface-configuration": [
      {
        "active": "act",
        "interface-name": "Loopback0",
        "description": "PRIMARY ROUTER LOOPBACK",
        "Cisco-IOS-XR-ipv4-io-cfg:ipv4-network": {
          "addresses": {
            "primary": {
              "address": "172.16.255.1",
              "netmask": "255.255.255.255"
            }
          }
        }
      }
    ]
  }
}'''

# Invoke the decode method  to decode the JSON payload to a YDK python object
interface_configurations = codec.decode(json_provider, if_json)

interface_configurations2 = codec.decode(json_provider, if_json2)

interface_configurationsx = codec.decode(xml_provider, if_xmls)

# Invoke the encode method to encode the YDK python object to an XML string
if_xml = codec.encode(xml_provider, interface_configurations)

if_xml2 = codec.encode(xml_provider, interface_configurations2)

if_jsons = codec.encode(json_provider, interface_configurationsx)
print(if_xml)

print("#"*15)

print(if_xml2)

print("#"*15)

print(if_jsons)