# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.ssh.insert_key = false

  # set our network type to private - machines will be accessible only through 
  # ssh and mapped ports. 
  config.vm.network "private_network", type: "dhcp"

  # https://github.com/Varying-Vagrant-Vagrants/VVV/issues/517
  config.vm.provision "fix-no-tty", type: "shell" do |s|
      s.privileged = false
      s.inline = "sudo sed -i '/tty/!s/mesg n/tty -s \\&\\& mesg n/' /root/.profile"
  end

  config.vm.define "automation" do |automation|
    automation.vm.hostname = "qa-automation"

    # https://github.com/mitchellh/vagrant/issues/5697
    #config.vm.provision :shell, inline: "sudo apt-get update"

    config.vm.provision :shell, inline: "sudo apt-get install -y python-dev"
    config.vm.provision :shell, inline: "sudo apt-get install -y python-setuptools"
    config.vm.provision :shell, inline: "easy_install pip"
    config.vm.provision :shell, inline: "pip install tox"

    automation.vm.provision "docker" do |d|
      d.pull_images "selenium/standalone-chrome"
      d.pull_images "selenium/standalone-firefox"
    end

  end
end
