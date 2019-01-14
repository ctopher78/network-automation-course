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

**2. Cisco NXOSv [nxosv-final.7.0.3.I6.1.box](https://software.cisco.com/download/home/286312239/type/282088129/release/7.0%25283%2529I6%25281%2529)**
- Initial config is added using POAP.  I realize that there are easier ways to configure the NXOSv, but I wanted a POAP test-ground.
- v9k's don't have static serial numbers, so I created a Go program that runs in the background and renames the `spine1` config file automatically.  This program snoops DHCP request packets to determine the current serial number associated to the active v9k Vagrant Box.

# Running this lab

### Bring the lab up
```
vagrant up
```

### Access management server
```
vagrant ssh mgt_server
```

### Access virtual Cisco 9k

Once the 9k is up, you can use ssh:
```
vagran ssh spine1

password: Admin1234!
```

**If you want to watch the device boot up, you can console in as well:**

- install socat

```
brew install socat
```

- connect to console on virtual device

```
socat UNIX-CONNECT:/tmp/test STDIN
```
