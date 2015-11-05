Headless Browser Automation in Parallel using Pytest, Docker, and Selenium
============================================
[![Build Status](https://img.shields.io/travis/jakemcdermott/page_automation.svg)](https://travis-ci.org/jakemcdermott/page_automation)

A page automation project layout using pytest fixtures to invoke multiple selenium containers in parallel.

Organization and Folder Structure
--------------------------------------------
Page models go in the 'page' subpackage directory and inherit from the base Page object.  
Tests go in the 'tests' subpackage directory and must be pytest compatible.


Requires
--------------------------------------------
- docker
- python
- tox

Try it
--------------------------------------------

```bash
cd page_automation
make tests
```

Contact
--------------------------------------------
jake.mcdermott@outlook.com
