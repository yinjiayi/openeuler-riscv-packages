# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
import sys
import xml.etree.ElementTree as ET
root = ET.parse(sys.argv[1]).getroot()
cases = root.findall("./testsuite/testcase")
assert root.tag == "testsuites" and root.attrib["tests"] == "35"
assert len(cases) == 35 and len({(x.attrib["classname"], x.attrib["name"]) for x in cases}) == 35
assert all(int(root.attrib.get(k, "0")) == 0 for k in ("failures", "errors", "disabled", "skipped"))
assert all(x.attrib.get("status") == "run" and x.attrib.get("result") == "completed" for x in cases)
assert all(x.find("failure") is None and x.find("skipped") is None for x in cases)
print("All 35 original Bioparser cases completed without failures or skips")
