#!/bin/bash
set -euo pipefail
cd /tmp
python3 -I - <<'PY'
from datetime import timedelta
from importlib.metadata import version
from pathlib import Path
import durationpy

assert version('durationpy') == '0.11'
assert Path(durationpy.__file__).is_absolute()
assert 'site-packages' in Path(durationpy.__file__).parts
mixed = timedelta(hours=4, minutes=3, seconds=2, milliseconds=1)
assert durationpy.from_str('4h3m2s1ms') == mixed
assert durationpy.from_str(durationpy.to_str(mixed)) == mixed
assert durationpy.from_str('-2m3.4s') == -timedelta(minutes=2, seconds=3.4)
assert durationpy.from_str('1us') == timedelta(microseconds=1)
assert durationpy.from_str('1ns') == timedelta(0)
assert durationpy.to_str(timedelta(0)) == '0'
extended = timedelta(days=367, hours=3)
assert durationpy.from_str(durationpy.to_str(extended, extended=True)) == extended
for invalid in ('', '3', 'X3h', '999999999999999999999999999y'):
    try:
        durationpy.from_str(invalid)
    except durationpy.DurationError as error:
        assert invalid in str(error)
    else:
        raise AssertionError(f'invalid duration accepted: {invalid!r}')
print('installed durationpy 0.11 parse/format/sign/precision/error smoke passed')
PY
