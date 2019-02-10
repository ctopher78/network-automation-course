# Junos Topology Discovery & Visualization Lab

## Summary

The Vagrantfile for this lab has been lifted directly from [Juniper vqfx10k-vagrant repo](https://github.com/Juniper/vqfx10k-vagrant).  I've made slight modifications to the topology, such as removing the hosts, to keep the memory consumption down.  The boxes are provisioned using an Ansible playbook provided by Juniper.  My goal with this lab it to practice network discovery and using that info to generate a logical BGP topology visualization.

One really nice thing about the Juniper vagrant boxes is that they are available on the (Vagrant Cloud site)[https://app.vagrantup.com/juniper/boxes/vqfx10k-re], which means you don't need to sign into a Juniper account, download the vagrant box, manually add that box to vagrant -- which are things you need to do with Cisco NXOS v9k and Arista vEOS.  I appreciate Juniper's openness here.  

That being said...the [Juniper vqfx10k-vagrant repo](https://github.com/Juniper/vqfx10k-vagrant) appears to be unmaintained, and I ran into the following issue while trying to bring the boxes up:
- The vqfx10k images are 32-bit, which are no longer supported in VirtualBox 6.  I ran across this issue -- and fought for hours trying to understand why I couldn't ssh into any switches.  The eventual fix was to downgrade to VirtualBox 5.2.  There has been an issue opened on this already, and I submitted a PR to update the docs, but neither of those contributions have been acknowledged.

Another issue I hit, which was an Ansible issue:
-  The Juniper.junos role was failing to import a module (`plugins.action.normal`).  A good description of the problem can be seen [here](https://github.com/Juniper/ansible-junos-stdlib/issues/412).  It turns out that Ansible 2+ runs into issues when you are using python installed somewhere other than `/usr/bin/python`.  In my case, I was using a virtualenv.  I responded the the orignal issue with a workaround I dug up from another Ansible issue.

# Running this lab

FILL ME OUT

### Original Juniper Docs (with a few details added that the docs were missing)

This Vagrantfile will create an IP Fabric composed of 2 spine and 3 leaf devices with 1 server attached to each leaf.
Overall it will spawn 5 instances of VQFX (light) and 3 Ubuntu servers.

The configuration of the Junos devices can be done using Ansible.
# Requirement
### Resources
 - RAM : 7G
 - CPU : 2 Core (shared)

### Tools
 - Ansible for provisioning (except for windows)
 - Junos module for Ansible

 #### Juniper.junos Module install
 ansible-galaxy install Juniper.junos

 #### PyEZ install (Python3 with pipenv)
 pipenv install junos-eznc

# Topology

Spine / Leaf topology with
- 2 spine
- 3 leaf
- 3 servers

# Provisioning / Configuration

Ansible is used to preconfigured all VQFX with an IP address on their interfaces
Both servers are preconfigured with an IP address and a route to their respective vQFX

If you don't have ansible or if ansible is not working you can start the topology without Ansible
```
vagrant up --no-provision
```

Later it's possible deploy all configuration
```
vagrant provision
```

Once the topology has been provisioned at least once, Vagrant will create a topology file corresponding to your topology.
The project is configured to automatically use this file, it's possible to call any playbook manually.  
```
ansible-playbook pb.conf.all.commit.yaml
```
