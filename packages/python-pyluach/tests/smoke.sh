#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-pyluach
python3 - <<'PY'
from importlib.metadata import version
from pyluach import dates, hebrewcal, parshios
import pyluach

assert version('pyluach') == '2.3.0'
assert pyluach.__version__ == '2.3.0'
# Fixed examples from the official README; no clock/randomness dependency.
greg = dates.GregorianDate(1986, 3, 21)
heb = dates.HebrewDate(5746, 13, 10)
assert greg == heb
assert greg.to_heb() == heb
assert heb.to_greg() == greg
assert dates.HebrewDate(5782, 7, 1).holiday() == 'Rosh Hashana'
assert hebrewcal.Month(5781, 10).month_name() == 'Teves'
assert parshios.getparsha_string(dates.GregorianDate(2021, 3, 10)) == 'Vayakhel, Pekudei'
PY
