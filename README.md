Headless Cross-Browser Automation using Pytest, Docker, and Selenium
============================================
[![Build Status](https://img.shields.io/travis/jakemcdermott/page_automation.svg)](https://travis-ci.org/jakemcdermott/page_automation)

This is a proof of concept for using [pytest-xdist](https://pypi.python.org/pypi/pytest-xdist) and [docker-selenium](https://github.com/SeleniumHQ/docker-selenium) to instantiate containerized selenium fixtures in parallel for high-throughput multi-browser compatibility testing.

Requires
--------------------------------------------
- docker
- python
- tox

Testing with Travis-CI
--------------------------------------------
Take a look at [.travis.yml](https://github.com/jakemcdermott/page_automation/blob/master/.travis.yml) to see an example test configuration. 

Try it Locally (Requires [Vagrant](https://www.vagrantup.com/))
--------------------------------------------

```bash
vagrant up
vagrant ssh
cd page_automation
make tests
```
