# network-automation-course

![Base Network Diagram](images/base_%20network_diagram.png)


# resources

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

## NX-OSv POAP
- While running the POAP scripts, the bios upgrade check fails on v9k because the bios version can't be parsed from the `show ver` (the value is empty).
  I had to add some code to to the paop script to account for this difference in the v9k `show ver`.
- NXOSv devies do *not* have static serial numbers.  Each time you destroy/rebuild the box the v9k will have a new serial number. 
  If you want to use serial number poap'ing method, which I did, you need to update the device config file name after the v9k has
  initialized.  I created a program to do this, with the uncleaver name of `ConfigRenamer`.  This program is always running in 
  the background and is looking for DHCP request packets.  If it sees a DHCP request packet from an v9k, it will rename the 
  config file in /var/lib/tftpboot/cfg.<serial_number> to a name that includes the correct serial number.
- 
