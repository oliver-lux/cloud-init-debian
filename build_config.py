#!/usr/bin/env python3
import sys, re
from pathlib import Path
from shutil import copy

IN, OUT, SEC, SEC_EX = 'cloud-config.yaml', '.private/cloud-config-ready.yaml', '.private/credentials.yaml', 'credentials.yaml.example'

# Auto-copy credentials example if needed
if not Path(SEC).exists():
    if not Path(SEC_EX).exists():
        sys.exit(f"Error: {SEC_EX} not found! Cannot create {SEC}")
    Path(SEC).parent.mkdir(exist_ok=True)
    copy(SEC_EX, SEC)
    print(f"✓ Created {SEC} from {SEC_EX}")
    sys.exit(f"⚠ Please edit {SEC} and add your secrets, then run again.")

# Check template exists
if not Path(IN).exists():
    sys.exit(f"Error: {IN} not found!")

secrets = {}
for line in Path(SEC).read_text().splitlines():
    if m := re.match(r'^(\w+):\s*["\']?([^"\']+)["\']?$', line.strip()):
        secrets[m[1]] = m[2]

content = Path(IN).read_text()

for name in set(re.findall(r'\{\{([A-Z_]+)\}\}', content)):
    key = name.lower()
    if key not in secrets:
        sys.exit(f"Error: Missing '{key}'")
    content = content.replace(f'{{{{{name}}}}}', secrets[key])

Path(OUT).parent.mkdir(exist_ok=True)
Path(OUT).write_text(content)
print(f"✓ {OUT}")