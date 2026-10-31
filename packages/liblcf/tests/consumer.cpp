// SPDX-License-Identifier: MIT
// Copyright (c) 2026 yinjiayi
#include <lcf/config.h>
#include <lcf/encoder.h>
#include <lcf/inireader.h>
#include <lcf/lmu/reader.h>
#include <sstream>
#include <string>
#include <iostream>
#if !LCF_SUPPORT_INI || !LCF_SUPPORT_ICU || !LCF_SUPPORT_XML
#error All default INI, ICU and XML features must be installed
#endif
int main() {
    std::stringstream ini("[Section]\nKey=42\nEnabled=yes\n");
    lcf::INIReader reader(ini);
    if (reader.ParseError() != 0 || reader.GetInteger("Section", "Key", -1) != 42 ||
        !reader.GetBoolean("Section", "Enabled", false)) return 1;
    lcf::Encoder encoder("windows-1252");
    if (!encoder.IsOk()) return 2;
    std::string text(1, char(0xe9));
    encoder.Encode(text);
    if (text != "\xc3\xa9") return 3;
    encoder.Decode(text);
    if (text != std::string(1, char(0xe9))) return 4;
    lcf::rpg::Map map;
    map.width = 2; map.height = 2; map.chipset_id = 7;
    map.lower_layer = {0,1,2,3}; map.upper_layer = {4,5,6,7};
    std::stringstream binary(std::ios::in | std::ios::out | std::ios::binary);
    if (!lcf::LMU_Reader::Save(binary, map, lcf::EngineVersion::e2k3, "UTF-8")) return 5;
    binary.seekg(0);
    auto loaded = lcf::LMU_Reader::Load(binary, "UTF-8");
    if (!loaded || loaded->width != 2 || loaded->height != 2 || loaded->chipset_id != 7 ||
        loaded->lower_layer != map.lower_layer || loaded->upper_layer != map.upper_layer) return 6;
    std::stringstream xml;
    if (!lcf::LMU_Reader::SaveXml(xml, map, lcf::EngineVersion::e2k3)) return 7;
    xml.seekg(0);
    auto from_xml = lcf::LMU_Reader::LoadXml(xml);
    if (!from_xml || from_xml->width != 2 || from_xml->height != 2 ||
        from_xml->chipset_id != 7 || from_xml->lower_layer != map.lower_layer ||
        from_xml->upper_layer != map.upper_layer) return 8;
    if (!lcf::LMU_Reader::Save("sample.lmu", map, lcf::EngineVersion::e2k3, "UTF-8")) return 9;
    std::cout << "liblcf downstream INI ICU LMU XML checks passed\n";
}
