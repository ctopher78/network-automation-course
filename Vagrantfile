# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"
end

Vagrant.configure("2") do |config|
  # Run Ansible from the Vagrant VM
  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "vagrant_playbook.yml"
    ansible.install_mode = "pip"
  end
end