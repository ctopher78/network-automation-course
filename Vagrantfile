# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure("2") do |config|
  config.vm.define "server" do |server|
    server.vm.box = "centos/7"
    server.vm.provision "ansible_local" do |ansible|
        ansible.playbook = "vagrant_playbook.yml"
        ansible.install_mode = "pip"
    end
  end
  
  config.vm.define "nxos" do |nxos|
    nxos.vm.box = "nxos/7.0.3.I6.1"
    nxos.vm.boot_timeout = 600
    nxos.ssh.insert_key = false
    nxos.vm.provider "virtualbox" do |vb|
      vb.memory = "4096"
    end
  end
end
