# netrics-config
Netrics repository to generate and maintain configuration for Netrics FLOTO containers.

## Overview
<img width="780" alt="image" src="https://github.com/internet-equity/netrics-config/assets/2147779/df3a1b95-1107-471c-967d-dc81796c5f51">

This module turns `balena_devices_output.json` into a directory structure full of configuration files for each one of the FLOTO devices.
It takes a jinja template to serve as a base for generating the final configuration files.
TBD: plugins can be implemented to provide a logic for paramenter generation (right now, the function <b>gen_config</b> is responsible for a default configuration).

* <b>netrics-config</b> will use and write to `$HOME/.netrics-config/` in order to operate.
* No sensitive data is shared along with these configuration.
