# network-automation-course



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

## Console into a nx-osv
- install socat

```
brew install socat
```

- connect to console on virtual device

```
socat UNIX-CONNECT:/tmp/test STDIN
```