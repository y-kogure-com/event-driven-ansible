# Ansible Collection - y_kogure_com0.eda

[日本語](README-ja.md)

## What is this?

This repository is a proprietary `y_kogure_com0.eda` Ansible collection.

This repository focuses on plug-ins that can be used with Event-Driven Ansible (hereafter EDA).

## Installation

### Install the requires packages to use EDA

```shell
# for RedHat
sudo dnf install gcc python3-pip python3-devel systemd-devel java-17-openjdk
# for Debian
sudo apt install -y g++ pkg-config python3-venv libpython3-dev libsystemd-dev openjdk-17-jdk
```

### Set environment variables to use OpenJDK

```shell
export JAVA_HOME=$(ls -dt /usr/lib/jvm/java-17* | head -n 1)

# Up to read environment variables when connecting via SSH, write this in .bashrc as well
vi ~/.bashrc
```

### (optional) Create a venv and install packages to run EDA

```shell
python3 -m venv venv
source venv/bin/activate
pip install ansible ansible-rulebook ansible
```

*Run `source venv/bin/activate` each time you use EDA (you may want to put it in a .bashrc or something).

### Install this collection

```shell
ansible-galaxy collection install y_kogure_com0.eda
```

### Create `inventory` and `rulebook

To run EDA (ansible-rulebook), you must create at least `rulebook.yml` and `inventory.yml`.

The sample code for `rulebook.yml` can be found under `extensions/eda/rulebooks`.

For `inventory.yml`, use the following code as a base and edit it for each environment.

```yaml:inventory.yml
---
all:
  hosts:
    localhost:
...
```

### Running the rulebook

In the directory you just created, run the following

```shell
ansible-rulebook -i inventory.yml -r rulebook.yml
```

*Each plugin requires an additional pip library to be installed in order to run.

Please refer to the following sections for information on how to use and install each plug-in.

## How to use and install each plug-in

### `github_commit` event source

Monitor specific repositories on GitHub and provide event notifications when new commits are made.

```shell
pip install PyGitHub
```

### `ping` event source

Monitor network devices by pinging them to see if they are dead or alive.

```shell
pip install icmplib
```

### `snmp_walk` event source

Periodically retrieves SNMP information to network devices and notifies them of the results in the form of events.

This event source uses `net-snmp`, which is not provided by pypi, and must be installed differently from `pip`.

```shell
# for RedHat
sudo dnf install net-snmp net-snmp-libs net-snmp-utils net-snmp-python
# for Debian
sudo apt install g++ python3-dev libsnmp-dev
tar xvf net-snmp-5.9.4.tar.gz
cd net-snmp-5.9.4
./configure --with-python-modules --libdir=/usr/lib64 --enable-shared
make
sudo make install
pip install net-snmp-5.9.4/python
export LD_LIBRARY_PATH="/usr/local/lib"
```

### `network_command` event source

It connects to the network device via ssh, periodically executes specific commands, and notifies the user of the results in an event.

```shell
pip install netmiko
```

### `ntc_templates` event filter

Parses the output text retrieved from the network device according to the patterns in the `ntc-templates` library.

The parsed result is stored in the `event.parsed` field.

```shell
pip install ntc-templates
```

## Output example

### `y_kogure_com0.eda.github_commit`

The following message is (currently) displayed once every 5 seconds.

```json
{
    '__doc__': '\n    This class represents Commits. The reference can be found here https://docs.github.com/en/rest/reference/git#commits\n    ',
    '__module__': 'github.Commit',
    '_identity': 'c445b1c20fedecf279dd26aba79493f4883316b0',
    'comments_url': 'https://api.github.com/repos/y-kogure-com/y_kogure_com0.eda/commits/c445b1c20fedecf279dd26aba79493f4883316b0/comments',
    'etag': 'W/"888d09df59ae2bddbd89e9cd6e459c6c81c4285c9c63a43ff018db6b8be73021"',
    'html_url': 'https://github.com/y-kogure-com/y_kogure_com0.eda/commit/c445b1c20fedecf279dd26aba79493f4883316b0',
    'last_modified': 'Thu, 07 Sep 2023 01:11:55 GMT',
    'sha': 'c445b1c20fedecf279dd26aba79493f4883316b0',
    'url': 'https://api.github.com/repos/y-kogure-com/y_kogure_com0.eda/commits/c445b1c20fedecf279dd26aba79493f4883316b0',
    'meta': {
        'source': {
            'name': 'y_kogure_com0.eda.github_commit',
            'type': 'y_kogure_com0.eda.github_commit'
        },
        'received_at': '2023-09-08T07:04:20.368201Z',
        'uuid': '75ebb94f-3cc2-4a55-83d3-6de34d56fb21'
    }
}
```

### `y_kogure_com0.eda.ping`

The following message appears once every two seconds.

```json
{
    'results': [
        {
            'address': '1.1.1.1',
            'min_rtt': 3.181,
            'avg_rtt': 3.181,
            'max_rtt': 3.181,
            'rtts': [3.1807422637939453],
            'packets_sent': 1,
            'packets_received': 1,
            'packet_loss': 0.0,
            'jitter': 0.0,
            'is_alive': True
        },
        {
            'address': '::1',
            'min_rtt': 0.898,
            'avg_rtt': 0.898,
            'max_rtt': 0.898,
            'rtts': [0.8978843688964844],
            'packets_sent': 1,
            'packets_received': 1,
            'packet_loss': 0.0,
            'jitter': 0.0,
            'is_alive': True
        }
    ]
}
```

### `y_kogure_com0.eda.snmp_walk`

The following message appears once every 5 seconds.

```json
{
    'body': [
        '5',
        '1', '2', '3', '4', '5',
        'GigabitEthernet1', 'GigabitEthernet2', 'GigabitEthernet3', 'VoIP-Null0', 'Null0',
        '6', '6', '6', '1', '1',
        '1500', '1500', '1500', '1500', '1500',
        '1000000000', '1000000000', '1000000000', '4294967295', '4294967295',
        "b'\\x00\\x0c)\\x96\\xfa\\x86'", "b'\\x00\\x0c)\\x96\\xfa\\x90'", "b'\\x00\\x0c)\\x96\\xfa\\x9a'", '', '',
        '1', '1', '2', '1', '1',
        '1', '1', '2', '1', '1',
        '2670', '134672', '1671', '1503', '0',
        '19122145', '18274990', '18296104', '0', '0',
        '273984', '264597', '264871', '0', '0',
        '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0',
        '5542', '5498', '0', '0', '0',
        '1068636', '21098', '0', '0', '0',
        '10071', '274', '0', '0', '0',
        '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0'
    ],
    'meta': {
        'source': {
            'name': 'y_kogure_com0.eda.snmp_walk',
            'type': 'y_kogure_com0.eda.snmp_walk'
        },
        'received_at': '2023-09-21T06:32:49.156306Z',
        'uuid': 'a2d76924-53f0-4b29-ac39-8da6db4aee21'
    }
}
```

### `y_kogure_com0.eda.network_command`

The following message appears once every 5 seconds.

```json
{
    'body': 'Cisco IOS XE Software, Version 03.15.00.S - Standard Support Release\nCisco IOS Software, CSR1000V Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 15.5(2)S, RELEASE SOFTWARE (fc3)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2015 by Cisco Systems, Inc.\nCompiled Sun 22-Mar-15 01:36 by mcpre\n\n\nCisco IOS-XE software, Copyright (c) 2005-2015 by cisco Systems, Inc.\nAll rights reserved.  Certain components of Cisco IOS-XE software are\nlicensed under the GNU General Public License ("GPL") Version 2.0.  The\nsoftware code licensed under GPL Version 2.0 is free software that comes\nwith ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such\nGPL code under the terms of GPL Version 2.0.  For more details, see the\ndocumentation or "License Notice" file accompanying the IOS-XE software,\nor the applicable URL provided on the flyer accompanying the IOS-XE\nsoftware.\n\n\nROM: IOS-XE ROMMON\n\nCSR1000V uptime is 1 day, 19 hours, 14 minutes\nUptime for this control processor is 1 day, 19 hours, 16 minutes\nSystem returned to ROM by reload\nSystem image file is "bootflash:packages.conf"\nLast reload reason: Reload Command\n\n\n\nThis product contains cryptographic features and is subject to United\nStates and local country laws governing import, export, transfer and\nuse. Delivery of Cisco cryptographic products does not imply\nthird-party authority to import, export, distribute or use encryption.\nImporters, exporters, distributors and users are responsible for\ncompliance with U.S. and local country laws. By using this product you\nagree to comply with applicable laws and regulations. If you are unable\nto comply with U.S. and local laws, return this product immediately.\n\nA summary of U.S. laws governing Cisco cryptographic products may be found at:\nhttp://www.cisco.com/wwl/export/crypto/tool/stqrg.html\n\nIf you require further assistance please contact us by sending email to\nexport@cisco.com.\n\nLicense Level: ax\nLicense Type: Default. No valid license found.\nNext reload license Level: ax\n\ncisco CSR1000V (VXE) processor (revision VXE) with 2067410K/6147K bytes of memory.\nProcessor board ID 9SBM4GWLMHJ\n3 Gigabit Ethernet interfaces\n32768K bytes of non-volatile configuration memory.\n3988316K bytes of physical memory.\n7774207K bytes of virtual hard disk at bootflash:.\n\nConfiguration register is 0x2102\n',
    'parsed': {
        'software_image': 'X86_64_LINUX_IOSD-UNIVERSALK9-M',
        'version': '15.5(2)S',
        'release': 'fc3',
        'rommon': 'IOS-XE',
        'hostname': 'CSR1000V',
        'uptime': '1 day, 19 hours, 14 minutes',
        'uptime_years': '',
        'uptime_weeks': '',
        'uptime_days': '1',
        'uptime_hours': '19',
        'uptime_minutes': '14',
        'reload_reason': 'Reload Command',
        'running_image': 'packages.conf',
        'hardware': ['CSR1000V'],
        'serial': ['9SBM4GWLMHJ'],
        'config_register': '0x2102',
        'mac': [],
        'restarted': ''
    },
    'meta': {
        'source': {
            'name': 'y_kogure_com0.eda.network_command',
            'type': 'y_kogure_com0.eda.network_command'
        },
        'received_at': '2023-09-21T03:37:57.883953Z',
        'uuid': 'a5ca6c97-6595-43c5-8545-9dce3cf61a36'
    }
}
```