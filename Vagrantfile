# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/vivid64"

  config.ssh.insert_key = false

  # set our network type to private - machines will be accessible only through 
  # ssh and mapped ports. 
  config.vm.network "private_network", type: "dhcp"

  config.vm.provider "virtualbox" do |v|
    if RbConfig::CONFIG['host_os'] =~ /linux/
      cpu = `nproc`.to_i
      ram = `grep MemTotal /proc/meminfo | awk '{ print $2 }'`.to_i / (1024 * 4)
    elsif RbConfig::CONFIG['host_os'] =~ /darwin/
      cpu = `sysctl -n hw.ncpu`.to_i
      ram = `sysctl -n hw.memsize`.to_i / (1024 ** 2 * 4)
    else
      cpu = 2
      ram = 1024
    end
    v.customize ["modifyvm", :id, "--memory", ram]
    v.customize ["modifyvm", :id, "--cpus", cpu]
  end

  config.vm.define "qa_automation" do |qa_automation|
    qa_automation.vm.hostname = "qa-automation"

    qa_automation.vm.provision :shell, inline: "sudo apt-get update"
    qa_automation.vm.provision :shell, inline: "sudo apt-get install -y python-dev python-pip"
    qa_automation.vm.provision :shell, inline: "sudo apt-get install -y libtiff5-dev libjpeg8-dev zlib1g-dev "\
                                               "libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev "\
                                               "python-tk"
                                               
    qa_automation.vm.provision :shell, inline: "pip install tox"

    qa_automation.vm.provision "docker" do |d|
      d.pull_images "selenium/standalone-chrome"
      d.pull_images "selenium/standalone-firefox"
    end

    qa_automation.vm.synced_folder ".", "/home/vagrant/page_automation"

  end
end
