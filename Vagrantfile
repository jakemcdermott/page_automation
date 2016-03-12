# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.ssh.insert_key = false

  # Set our network type to private - machines will be accessible only through 
  # ssh and mapped ports. 
  config.vm.network "private_network", type: "dhcp"

  # Use all cpus and a quarter of the available system memory (Linux / OSX)
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

  # https://github.com/mitchellh/vagrant/issues/1673
  config.vm.provision "fix-no-tty", type: "shell" do |s|
      s.privileged = false
      s.inline = "sudo sed -i '/tty/!s/mesg n/tty -s \\&\\& mesg n/' /root/.profile"
  end

  config.vm.define "qe_automation" do |qe_automation|
    qe_automation.vm.hostname = "qe-automation"

    packages = [
      "python-dev", "python-pip", "python-tk",
      "libtiff5-dev", "libjpeg8-dev", "zlib1g-dev",
      "libfreetype6-dev", "liblcms2-dev",
      "libwebp-dev", "tcl8.6-dev", "tk8.6-dev"
    ]

    qe_automation.vm.provision :shell, inline: "sudo apt-get update"

    packages.each do |pkg|
      qe_automation.vm.provision :shell, inline: "sudo apt-get install -y #{pkg}"
    end
                                                                     
    qe_automation.vm.provision :shell, inline: "pip install tox"

    # install docker and pull standalone selenium containers from Dockerhub
    qe_automation.vm.provision "docker" do |d|
      d.pull_images "selenium/standalone-chrome"
      d.pull_images "selenium/standalone-firefox"
    end

    qe_automation.vm.synced_folder ".", "/home/vagrant/page_automation"

  end
end
