"""snmp_walk

Polling for snmpwalk information.

Arguments:
---------
    host: target host address.
    port: target host SNMP port. (default: 161)
    community: SNMP community. (default: public)
    mib: SNMP object name.
    version: SNMP version. (default: 2)
    delay: delay seconds. (default: 5)
"""

import asyncio
from typing import Any

import netsnmp

async def main(queue: asyncio.Queue, args: dict[str, Any]) -> None:

    host = args.get('host')
    port = args.get('port', 161)
    community = args.get('community', 'public')
    version = args.get('version', 2)
    mib = args.get('mib')
    delay = args.get('delay', 5)

    sess = netsnmp.Session(
        Version = version,
        Community = community,
        DestHost = f'{host}:{port}'
    )

    while True:
        varlist = netsnmp.VarList(netsnmp.Varbind(mib))
        try:
            result = sess.walk(varlist)
            await queue.put({'body': [ str(v) for v in result ]})
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
                'port': 161,
                'community': 'public',
                'version': 2,
                'mib': 'interfaces',
                'delay': 5
            },
        ),
    )
