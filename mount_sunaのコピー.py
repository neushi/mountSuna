#!/usr/bin/env python3
"""
mountSuna - macOS auto-mounting prevention utility
macOSで勝手にボリュームをマウントさせないためのfstab設定テキストを生成するスクリプト。
"""

import subprocess
import re
import sys

def main():
    try:
        # diskutil コマンドを実行して情報を取得
        result = subprocess.run(
            ['diskutil', 'info', '-all'],
            capture_output=True,
            text=True,
            check=True
        )
    except FileNotFoundError:
        print("Error: 'diskutil' command not found. Are you on macOS?", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error executing diskutil: {e}", file=sys.stderr)
        sys.exit(1)

    TARGET_KEYWORDS = [
        "Volume Name:", 
        "Volume UUID:"
    ]

    IGNORED_VOLUMES = {
        "iSCPreboot", "xART", "Hardware",
        "Recovery", "Update", "Preboot", "VM",
        "macOS Base System"
    }

    # Pass 1: スナップショットがマウントされているVolume Nameを収集
    mounted_names = set()
    def check_mounted(block_lines):
        v_name = None
        is_m = False
        for l in block_lines:
            if "Volume Name:" in l:
                v_name = l.split("Volume Name:")[1].strip()
            if "Mounted:" in l and "Yes" in l:
                is_m = True
        if is_m and v_name:
            mounted_names.add(v_name)

    temp_block = []
    for line in result.stdout.splitlines():
        if "**********" in line:
            if temp_block:
                check_mounted(temp_block)
            temp_block = []
        else:
            temp_block.append(line)
    if temp_block:
        check_mounted(temp_block)

    current_block = []

    def process_block(block):
        # スナップショットはfstabの対象外なので完全にスキップ
        if any("APFS Volume Snapshot" in l or "APFS Snapshot Name:" in l for l in block):
            return

        # スキップ判定 & 名前取得
        vol_target_name = None
        for line in block:
            if "Volume Name:" in line:
                if "Not applicable (no file system)" in line:
                    return
                vol_target_name = line.split("Volume Name:")[1].strip()
                if vol_target_name in IGNORED_VOLUMES:
                    return

        # Snapshot側がマウントされていれば、Base側もマウントされているとみなす
        is_mounted = False
        if vol_target_name and vol_target_name in mounted_names:
            is_mounted = True

        output_lines = []
        for line in block:
            if not any(keyword in line for keyword in TARGET_KEYWORDS):
                continue

            clean_line = re.sub(r'\s+', ' ', line.strip())

            if "UUID:" in clean_line:
                uuid_match = re.search(r'UUID:\s*([A-F0-9\-]+)', clean_line)
                prefix_uuid = "#### " if is_mounted else ""
                if uuid_match:
                    uuid = uuid_match.group(1)
                    output_lines.append(f"{prefix_uuid}UUID={uuid} none auto noauto")
                else:
                    output_lines.append(f"{prefix_uuid}{clean_line}")
            else:
                if clean_line.startswith("Volume Name:"):
                    clean_line = clean_line.replace("Volume Name: ", "Volume Name:                 ", 1)
                output_lines.append(f"# {clean_line}")

        if output_lines:
            for out_line in output_lines:
                print(out_line)

    for line in result.stdout.splitlines():
        if "**********" in line:
            if current_block:
                process_block(current_block)
                current_block = []
        else:
            current_block.append(line)

    if current_block:
        process_block(current_block)

if __name__ == "__main__":
    main()
