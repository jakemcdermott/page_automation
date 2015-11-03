# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/vivid64"

  config.ssh.insert_key = false

  # set our network type to private - machines will be accessible only through 
  # ssh and mapped ports. 
  config.vm.network "private_network", type: "dhcp"

  config.vm.define "qa_automation" do |qa_automation|
    qa_automation.vm.hostname = "qa-automation"

    qa_automation.vm.provision :shell, inline: "sudo apt-get update"
    qa_automation.vm.provision :shell, inline: "sudo apt-get install -y python-pip"

    qa_automation.vm.provision :shell, inline: "sudo apt-get install -y libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk"


    qa_automation.vm.provision :shell, inline: "pip install tox"

    qa_automation.vm.provision "docker" do |d|
      d.pull_images "selenium/standalone-chrome"
      d.pull_images "selenium/standalone-firefox"
    end

  end
end
