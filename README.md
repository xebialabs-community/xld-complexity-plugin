# Preface #

[![License MIT][license-image]][license-url]

[license-image]: https://img.shields.io/badge/license-MIT-yellow.svg
[license-url]: https://opensource.org/licenses/MIT



This document describes the functionality provided by the xld-complexity-plugin.

See the **XL Deploy Reference Manual** for background information on XL Deploy and deployment concepts.

# Overview #

The xld-complexity-plugin is a XL Deploy plugin that adds capability count CIs to calculate your complexity score
of your XL Deploy instance.

# CI-Counter Script #

This script can be ran on any machine that can reach the digital.ai Deploy url instance and has python on the machine.

It uses the rest api of digital.ai Deploy to count your CIs and applications and prints out a table of the results

to use this script you will simply have to use

`python ci-counter.py`

this will provide you with a prompt to enter the deploy instance url and credentials.

```
Enter your URL : http://localhost:4516
Enter your username : user1
password:
```
After your provide this it will output a table of your complexity number
