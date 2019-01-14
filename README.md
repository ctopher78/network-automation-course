# network-automation-course

This is my [Building Automated Networks](https://my.ipspace.net/bin/list?id=NetAutSol) project repo.

The base network diagram is pretty simple.  Mainly because I only have enough memory in my laptop to handle a couple of Vagrant boxes at once.

![Base Network Diagram](images/base_%20network_diagram.png)

## Vagrant Boxes

**1. CentOS|7**
This device runs all the services needed to test my automation solutions.

I'm using Vagrants `ansible_local` provisioner to bring the management server into a state where it can assist with ZTP of network devices.



Added Software:
- Ansible 2.7.5
- Go 1.11.4

Services Running:
- DHCP
- TFTP
- Rsyslog listener
- Custom Golang DHCP snooping service 

**2. Cisco NXOSv [nxosv-final.7.0.3.I6.1.box]**(https://software.cisco.com/download/home/286312239/type/282088129/release/7.0%25283%2529I6%25281%2529)
- Initial config is added using POAP.  I realize that there are easier ways to configure the NXOSv, but I wanted a POAP test-ground.
