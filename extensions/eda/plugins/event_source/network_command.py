"""snmp_walk

SSH into the network device and execute the command periodically.

Arguments:
---------
    host: target host address.
    port: target host SSH port. (default: 22)
    device_type: device_type
    username: login username
    password: login password
    key_file: SSH Key file path
    command: execute command
    delay: delay seconds. (default: 5)
"""

import asyncio
from typing import Any

from netmiko import ConnectHandler

async def main(queue: asyncio.Queue, args: dict[str, Any]) -> None:

    params = {
        'host': args.get('host'),
        'port': args.get('port', 22),
        'device_type': args.get('device_type'),
        'username': args.get('username'),
        'password': args.get('password'),
        'key_file': args.get('key_file'),
        'disable_sha2_fix': True
    }

    command = args.get('command')
    delay = args.get('delay', 5)

    try:
        ssh = ConnectHandler(**params)
    except:
        raise

    while True:
        try:
            result = ssh.send_command(command)
            await queue.put({'body': result})
        except:
            raise
        await asyncio.sleep(delay)

if __name__ == "__main__":
    """MockQueue if running directly."""

    class MockQueue:
        """A fake queue."""

        async def put(self: "MockQueue", event: dict) -> None:
            """Print the event."""
            print(event)

    asyncio.run(
        main(
            MockQueue(),
            {
                'host': '192.168.125.113',
                'port': '22',
                'device_type': 'cisco_ios',
                'username': 'y-kogure',
                'key_file': '~/.ssh/id_rsa',
                'command': 'show version'
            },
        ),
    )
