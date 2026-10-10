#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
set -eu
cd "$(mktemp -d)"
python3 -I - <<'PY'
import importlib.metadata
from pathlib import Path
import pytrie
from pytrie import SortedStringTrie, StringTrie
assert importlib.metadata.version('PyTrie') == '0.4.0'
p = Path(pytrie.__file__).resolve()
assert p.is_relative_to(Path('/usr/lib')) or p.is_relative_to(Path('/usr/lib64'))
t = SortedStringTrie(an=0, ant=1, all=2, allot=3, alloy=4)
assert t.keys('al') == ['all', 'allot', 'alloy']
assert t.longest_prefix_item('antonym') == ('ant', 1)
assert list(t.iter_prefix_items('allotment')) == [('all', 2), ('allot', 3)]
m = StringTrie({'one': 1, 'two': 2})
m.update(three=3)
assert m.pop('one') == 1 and len(m) == 2
assert m.copy() == m
PY
