# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure("2") do |config|
  config.vm.define "mgt_server" do |server|
    server.vm.box = "bento/centos-7"
    server.vm.provision "ansible_local" do |ansible|
        ansible.playbook = "vagrant_playbook.yml"
        ansible.install_mode = "pip"
    server.vm.network "private_network", ip: "192.168.1.1", virtualbox__intnet: "mgt1-spn1"
    end
  end
  
  config.vm.define "spine1" do |spine1|
    spine1.vm.box = "nxos/7.0.3.I6.1"
    spine1.ssh.insert_key = false
    spine1.vm.provider "virtualbox" do |vb|
      vb.memory = "4096"
    spine1.vm.network "private_network", ip: "192.168.1.2", virtualbox__intnet: "mgt1-spn1"
    end
  end
end
