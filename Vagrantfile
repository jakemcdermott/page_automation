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

  config.vm.define "qa_automation" do |qa_automation|
    qa_automation.vm.hostname = "qa-automation"

    #qa_automation.vm.provision :shell, inline: "sudo apt-get update"

    qa_automation.vm.provision :shell, inline: "sudo apt-get install -y python-dev"
    qa_automation.vm.provision :shell, inline: "sudo apt-get install -y python-setuptools"
    qa_automation.vm.provision :shell, inline: "sudo apt-get install -y libffi-dev"
    qa_automation.vm.provision :shell, inline: "sudo apt-get install -y libssl-dev"

    qa_automation.vm.provision :shell, inline: "sudo apt-get install -y libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk"



    qa_automation.vm.provision :shell, inline: "easy_install pip"

    #qa_automation.vm.provision :shell, inline: "pip install pyopenssl"
    qa_automation.vm.provision :shell, inline: "pip install tox"

    #qa_automation.vm.provision "docker" do |d|
      #d.pull_images "selenium/standalone-chrome"
      #d.pull_images "selenium/standalone-firefox"
    #end

  end
end
