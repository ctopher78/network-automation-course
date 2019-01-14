# network-automation-course

This is my [Building Automated Networks](https://my.ipspace.net/bin/list?id=NetAutSol) project repo.

The base network diagram is pretty simple.  Mainly because I only have enough memory in my laptop to handle a couple of Vagrant boxes at once.

![Base Network Diagram](images/base_%20network_diagram.png)

## Vagrant Boxes

**1. CentOS|7**
This device runs all the services needed to test my automation solutions.

Added Software:
- Ansible 2.7.5
- Go 1.11.4

Services Running:
- DHCP
- TFTP
- Rsyslog listener
- Custom Golang DHCP snooping service 

**2. Cisco NXOSv [nxosv-final.7.0.3.I6.1.box]**(https://software.cisco.com/download/home/286312239/type/282088129/release/7.0%25283%2529I6%25281%2529)
- not much else to say...

# resources

These are some resources I found helpful while setting up this lab.

## virtual device resources
[Virtual NX-OS 9/3K Config Guide](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/7-x/nx-osv/configuration/guide/b_NX-OSv_9000/b_NX-OSv_chapter_01.html#id_45079)

## vagrantfile resources
[github/ipspace example vagrant topologies](https://github.com/ipspace/NetOpsWorkshop/tree/master/topologies)

[github.com/dravetech example vagrantfile](https://github.com/dravetech/network-tutorials/tree/master/labs/lab1)

## vagrant networking
[vagrant vitrualbox networking](https://www.vagrantup.com/docs/virtualbox/networking.html)

## vagrant provisioning
[vagrant ansible_local provisioning](https://www.vagrantup.com/docs/provisioning/ansible_local.html)


# Tips & Tricks

## Console into a v9k
- install socat

```
brew install socat
```

- connect to console on virtual device

```
socat UNIX-CONNECT:/tmp/test STDIN
```

## Run vagrant_provisioning playbook on CentOS box
```
ansible-playbook -i 127.0.0.1, vagrant_provisioning.yml
```

## NX-OSv POAP

I ran into a host of odd issues related to Cisco POAP and the virtual NXOS software.  I documented some of the below:

- While running the POAP scripts, the bios upgrade check fails on v9k because the bios version can't be parsed from the `show ver` (the value is empty).
  I had to add some code to to the paop script to account for this difference in the v9k `show ver`.
- NXOSv devies do *not* have static serial numbers.  Each time you destroy/rebuild the box the v9k will have a new serial number. 
  If you want to use serial number poap'ing method, which I did, you need to update the device config file name after the v9k has
  initialized.  I created a program to do this, with the uncleaver name of `ConfigRenamer`.  This program is always running in 
  the background and is looking for DHCP request packets.  If it sees a DHCP request packet from an v9k, it will rename the 
  config file in /var/lib/tftpboot/cfg.<serial_number> to a name that includes the correct serial number.
