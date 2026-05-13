#!/bin/bash
NLM="/home/kareltestspecial/0-boek/00-GEREEDSCHAP/nlm_venv/bin/python3 -m notebooklm_tools.cli.main"
OUT_DIR="/home/kareltestspecial/0-boek/01-PLATFORM/public/audio/EN"
NID="7ab2c68e-4543-44c8-bad1-e27caf7cbddc"

mkdir -p "$OUT_DIR"

$NLM download audio --id 517bdec2-7d50-4071-aa78-c47248c3ce1c --output "$OUT_DIR/Upgrading_humanity_to_a_Sovereign_Reality.m4a" $NID
$NLM download audio --id 09a58fb0-9f0d-4276-95dd-3da9d4ab1c8f --output "$OUT_DIR/Patching_the_Human_Legacy_Kernel.m4a" $NID
$NLM download audio --id ffa59408-dc57-4d0e-872f-fc37395d0b03 --output "$OUT_DIR/Patching_the_software_bugs_of_humanity.m4a" $NID
$NLM download audio --id 73959c59-3bec-4ffb-a500-180f880925b9 --output "$OUT_DIR/Human_suffering_is_a_technical_bug.m4a" $NID
$NLM download audio --id 088e70ef-52ad-4cc8-8ae6-c8ef2f0dd5bc --output "$OUT_DIR/Debugging_the_legacy_kernel_of_humanity.m4a" $NID
$NLM download audio --id 6874944b-8867-4062-89d7-7f220843a58a --output "$OUT_DIR/A_software_patch_for_humanity.m4a" $NID
