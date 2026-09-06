#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- SFML SFML-devel

for module in all system window graphics audio network; do
  test "$(pkg-config --modversion "sfml-$module")" = "2.6.2"
done

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/CMakeLists.txt" <<'EOF'
cmake_minimum_required(VERSION 3.16)
project(sfml_smoke LANGUAGES CXX)
find_package(SFML 2.6 COMPONENTS graphics audio network REQUIRED)
add_executable(sfml-smoke smoke.cpp)
target_compile_features(sfml-smoke PRIVATE cxx_std_17)
target_link_libraries(sfml-smoke PRIVATE sfml-graphics sfml-audio sfml-network)
EOF

cat >"$smoke_dir/smoke.cpp" <<'EOF'
#include <SFML/Audio.hpp>
#include <SFML/Graphics.hpp>
#include <SFML/Network.hpp>
#include <SFML/System.hpp>

#include <array>
#include <string>

int main(int argc, char** argv)
{
    if (argc != 3 || SFML_VERSION_MAJOR != 2 || SFML_VERSION_MINOR != 6 || SFML_VERSION_PATCH != 2)
        return 1;

    sf::Clock clock;
    (void)clock.getElapsedTime();

    sf::Image image;
    image.create(2, 2, sf::Color(12, 34, 56, 255));
    if (image.getPixel(1, 1) != sf::Color(12, 34, 56, 255) || !image.saveToFile(argv[1]))
        return 2;
    sf::Image reloadedImage;
    if (!reloadedImage.loadFromFile(argv[1]) || reloadedImage.getSize() != sf::Vector2u(2, 2))
        return 3;

    const std::array<sf::Int16, 8> samples{{0, 1200, -1200, 600, -600, 0, 300, -300}};
    sf::SoundBuffer sound;
    if (!sound.loadFromSamples(samples.data(), samples.size(), 1, 8000) || !sound.saveToFile(argv[2]))
        return 4;
    sf::SoundBuffer reloadedSound;
    if (!reloadedSound.loadFromFile(argv[2]) || reloadedSound.getSampleCount() != samples.size())
        return 5;

    sf::Packet packet;
    packet << sf::Uint32(0x12345678) << std::string("sfml-2.6.2");
    sf::Uint32 value = 0;
    std::string text;
    packet >> value >> text;
    return packet && value == 0x12345678 && text == "sfml-2.6.2" ? 0 : 6;
}
EOF

cmake -S "$smoke_dir" -B "$smoke_dir/build" -DCMAKE_BUILD_TYPE=Release
cmake --build "$smoke_dir/build" --parallel
"$smoke_dir/build/sfml-smoke" "$smoke_dir/image.png" "$smoke_dir/sound.wav"
