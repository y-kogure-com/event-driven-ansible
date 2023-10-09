"""ping

Check that the server returns a ping request

Arguments:
---------
    hosts: Target IP addresses (list)
    timeout: Timeout seconds (default=2)
    delay: Interval seconds for next ping communication check (default=1)
"""

import asyncio
from typing import Any

from icmplib import async_multiping

async def main(queue: asyncio.Queue, args: dict[str, Any]) -> None:

    hosts = args.get('hosts')
    if not isinstance(hosts, list):
        msg = 'Missing required argument: hosts'
        raise ValueError(msg)

    timeout = args.get('timeout', 2)
    delay = args.get('delay', 1)

    while True:
        results = []
        ping_results = await async_multiping(hosts, count=1, timeout=timeout, privileged=False)

        for result in ping_results:
            r = {}
            for k in result.__dir__():
                if not k.startswith('_'):
                    r[k] = getattr(result, k)
            results.append(r)

        await queue.put({'results': results})
        await asyncio.sleep(delay)

if __name__ == "__main__":
    """MockQueue if running directly."""

    class MockQueue:
        """A fake queue."""

        async def put(self: "MockQueue", event: dict) -> None:
            """Print the event."""
            print(event)

    hosts = [
        '1.1.1.1',
        '127.0.0.1',
        '::1',
        'google.com',
        '10.10.10.10'
    ]

    asyncio.run(
        main(
            MockQueue(),
            {
                "hosts": hosts,
                "timeout": 2,
                "delay": 3
            },
        ),
    )
