// SPDX-License-Identifier: MIT
// Copyright (c) 2026 yinjiayi
#include <bioparser/fasta_parser.hpp>
#include <cstdint>
#include <string>
#include <stdexcept>
struct Sequence {
  std::string name, data;
  Sequence(const char* n, std::uint32_t nl, const char* d, std::uint32_t dl)
      : name(n, nl), data(d, dl) {}
};
int main(int argc, char** argv) {
  if (argc != 3) return 1;
  for (int i = 1; i < argc; ++i) {
    auto parser = bioparser::Parser<Sequence>::Create<bioparser::FastaParser>(argv[i]);
    for (int round = 0; round != 2; ++round) {
      auto records = parser->Parse(static_cast<std::uint64_t>(-1));
      std::size_t names = 0, bases = 0;
      for (const auto& r : records) { names += r->name.size(); bases += r->data.size(); }
      if (records.size() != 14 || names != 65 || bases != 109117) return 2;
      parser->Reset();
    }
  }
  return 0;
}
