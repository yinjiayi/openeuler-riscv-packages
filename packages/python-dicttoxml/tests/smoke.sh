#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-dicttoxml
python3 - <<'PY'
from importlib.metadata import version
import xml.etree.ElementTree as ET
import dicttoxml

assert version('dicttoxml') == dicttoxml.__version__ == '1.7.16'
obj = {'mylist': ['foo', 'bar', 'baz'], 'mydict': {'foo': 'bar', 'baz': 1}, 'ok': True}
root = ET.fromstring(dicttoxml.dicttoxml(obj))
assert root.tag == 'root'
assert [x.text for x in root.findall('mylist/item')] == ['foo', 'bar', 'baz']
assert root.find('mydict/baz').text == '1'
assert root.find('ok').text == 'true'
assert root.find('ok').get('type') == 'bool'
root = ET.fromstring(dicttoxml.dicttoxml({'message': '<&>]]>'}, cdata=True, custom_root='example'))
assert root.tag == 'example' and root.find('message').text == '<&>]]>'
assert 'type=' not in dicttoxml.dicttoxml(obj, attr_type=False).decode()
assert isinstance(dicttoxml.dicttoxml(obj, return_bytes=False), str)
PY
