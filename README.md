# netrics-config
Netrics repository to generate and maintain configuration for Netrics FLOTO containers.

## Overview
<img width="780" alt="image" src="https://github.com/internet-equity/netrics-config/assets/2147779/df3a1b95-1107-471c-967d-dc81796c5f51">

This module turns `balena_devices_output.json` into a directory structure full of configuration files for each one of the FLOTO devices.
It takes a jinja template to serve as a base for generating the final configuration files.
TBD: plugins can be implemented to provide a logic for paramenter generation (right now, the function <b>gen_config</b> is responsible for a default configuration).

* <b>netrics-config</b> can be operated through the scripts available in the `scripts` folder, mainly through `manage.py`
* <b>netrics-config</b> will use and write to `$HOME/.netrics-config/` in order to operate.
* No sensitive data is shared along with these configuration.


## Steps to operate an existing data
1. Establish the AWS bucket credentials through AWS configure;
2. Make sure you have write permissions and puclic read permissions to the bucket;
3. Copy `database.yaml` and `data/s3` from either <b>netrics-config-data-v1</b> or <b>netrics-config-data-v2</b> private repos;
4. Any changes to `database.yaml` and/or `data/s3` should be ideally updated on the private data repos
5. From `scripts` run `manage.py -i balena_devices_output.json` to generate new data on local `data/s3`
6. Run `sync.sh` to update to the cloud.

## Steps to bootstrap a new bucket
TBD
