"""ntc_templates

Parses log messages using ntc-templates.

requirements: ntc-templates package

```
pip install ntc-templates
```

Arguments:
---------
    * message = Command output for network devices (Specify variables in Jinja2 format)
    * platform = Specifies ntc-templates platform
    * command = Specifies ntc-templates command
"""

from ntc_templates.parse import parse_output
from jinja2 import Template

def main(event: dict, message: str, platform: str, command: str) -> dict:

    tmpl = Template(message)
    rendered = tmpl.render(event = event)

    parsed = parse_output(platform=platform, command=command, data=rendered)
    event['parsed'] = parsed[0]

    return event
