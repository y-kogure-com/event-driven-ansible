# Ansible Collection - y_kogure_com0.eda

[English](README.md)

## これはなに？

自作Ansibleコレクションの `y_kogure_com0.eda` です。

Event-Driven Ansible(以下EDA)で使えるプラグインを中心にまとめています。

## 導入方法

### EDAを利用するために必要なパッケージをインストールする

```shell
# RedHat系の場合
sudo dnf install gcc python3-pip python3-devel systemd-devel java-17-openjdk
# Debian系の場合
sudo apt install -y g++ pkg-config python3-venv libpython3-dev libsystemd-dev openjdk-17-jdk
```

### OpenJDKを利用するための環境変数を設定する

```shell
export JAVA_HOME=$(ls -dt /usr/lib/jvm/java-17* | head -n 1)

# SSH接続時に環境変数を読み込むために↑これを.bashrcにも書く
vi ~/.bashrc
```

### (optional) venvを作成し、EDAを実行するためのパッケージをインストールする

```shell
python3 -m venv venv
source venv/bin/activate
pip install ansible ansible-rulebook ansible
```

※ `source venv/bin/activate` はEDAを利用する際は都度実行してください(.bashrcあたりに書いておいてもいいかも)

### このプラグインをインストールする

```shell
ansible-galaxy collection install y_kogure_com0.eda
```

### `inventory` と `rulebook` の作成

EDA(ansible-rulebook)を実行するためには最低限 `rulebook.yml` と `inventory.yml` を用意する必要があります。

`rulebook.yml` のサンプルコードは `extensions/eda/rulebooks` 配下にあります。

`inventory.yml` については以下のコードをベースにして各環境用に編集してください。

```yaml:inventory.yml
---
all:
  hosts:
    localhost:
...
```

### rulebook実行

先ほど作成したディレクトリ内で、以下のように実行します。

```shell
ansible-rulebook -i inventory.yml -r rulebook.yml
```

※各プラグインを実行するためには、それぞれ追加でインストールするpipライブラリが必要となります。

各プラグインの利用方法・インストール方法については、次の項を参照してください。

## 各プラグインの利用方法・導入方法

利用するプラグインによって追加でインストールするパッケージが異なります。

### `github_commit` イベントソース

GitHubの特定リポジトリを監視し、新規コミットがあったらイベント通知を行います。

```shell
pip install PyGitHub
```

### `ping` イベントソース

ネットワークデバイスをpingにて死活監視します。

```shell
pip install icmplib
```

### `snmp_walk` イベントソース

ネットワークデバイスにSNMP情報を定期取得し、結果をイベント通知します。

このイベントソースは、pypiで提供されていない `net-snmp` を利用しているため、 `pip` とは異なる方法でインストールする必要があります

```shell
# RedHat系の場合
sudo dnf install net-snmp net-snmp-libs net-snmp-utils net-snmp-python
# Debian系の場合
sudo apt install g++ python3-dev libsnmp-dev
tar xvf net-snmp-5.9.4.tar.gz
cd net-snmp-5.9.4
./configure --with-python-modules --libdir=/usr/lib64 --enable-shared
make
sudo make install
pip install net-snmp-5.9.4/python
export LD_LIBRARY_PATH="/usr/local/lib"
```


### `network_command` イベントソース

ネットワークデバイスにssh接続し、定期的に特定のコマンドを実行し、結果をイベント通知します。

```shell
pip install netmiko
```

### `ntc_templates` イベントフィルタ

ネットワークデバイスから取得した出力テキストを `ntc-templates` ライブラリのパターンに沿って解析します。

解析結果は `event.parsed` フィールドに格納されます。

```shell
pip install ntc-templates
```

## 出力例

### `y_kogure_com0.eda.github_commit`

以下のようなメッセージが(現状)5秒に1回表示されます。

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

以下のようなメッセージが2秒に1回表示されます。

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

以下のようなメッセージが5秒に1回表示されます。

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

以下のようなメッセージが5秒に1回表示されます。

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