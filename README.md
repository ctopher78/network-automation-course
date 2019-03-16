# Network Automation Lab

This is my [Building Automated Networks](https://my.ipspace.net/bin/list?id=NetAutSol) project repo.

It contains my completed (and let's be honest -- some incomplete) assignments for the the course.


### Homework1
#### Cisco NXOS ZTP lab.

This lab contains on NXOS switch and a host that provides the necessary services to test Cisco ZTP (i.e POAP).


### Homework2
#### Juniper BGP Topology Discovery and Visualization

This lab contains a simple Juniper fabric topology consiting of 2 spine switches and 3 leaf switches (all vQFX).

The automation for this assignment uses NAPALM and Nornir to read the networks current BGP state and generates an HTML/JS DOT page representing the BPG connections between all the devices and thier status.

### Homework3
#### The End (of templates) Is Near!!

This assignment is a WIP...  My goal here was to gain a better understanding of YANG, Netconf, and the tools I could use to 100% programmatically interact with network devices over Netconf (no templates/CLI interaction).  I'm using a very simple data model and [YDK](https://github.com/CiscoDevNet/ydk-py).  I had to manually add Junos models to YDK, but after doing so, it works as expected.

