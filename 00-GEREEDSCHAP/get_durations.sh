#!/bin/bash
DIR="/home/kareltestspecial/0-boek/01-PLATFORM/public/audio/EN"
for file in "$DIR"/*.m4a; do
  duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$file")
  min=$(awk "BEGIN {print int($duration/60)}")
  sec=$(awk "BEGIN {print int($duration%60)}")
  printf "%s: %02d:%02d\n" "$(basename "$file")" "$min" "$sec"
done
