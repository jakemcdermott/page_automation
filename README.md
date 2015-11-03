Page Automation using Pytest, Docker, and Selenium
============================================

A simple page automation project layout using pytest fixtures to invoke standalone selenium containers in docker.


Organization and Folder Structure
--------------------------------------------
- Page models go in the 'page' subpackage directory and inherit from the base Page object
- Tests go in the 'tests' subpackage directory and must be pytest compatible


Try it out
--------------------------------------------

```bash
vagrant up
vagrant ssh
cd page_automation
tox
```

Contact
--------------------------------------------
jake.mcdermott@outlook.com