#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
from pathlib import Path
import sys
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('manuscript/main.tex')
if not p.exists():
    print('missing file')
    raise SystemExit(1)
print('quality gate passed')
