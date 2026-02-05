#!/usr/bin/env python3
"""
Patch OpenClaw launchd plist to add SRT sandbox wrapper.

Usage:
    python3 patch-plist.py [--dry-run] [--srt-path PATH] [--srt-config PATH]

What it does:
    1. Reads ~/Library/LaunchAgents/ai.openclaw.gateway.plist
    2. Prepends SRT wrapper to ProgramArguments: srt --settings <config> --
    3. Updates PATH to include SRT's location
    4. Writes back (unless --dry-run)

The '--' separator is critical! Without it, flags in the wrapped command
(like --port) could be misinterpreted by SRT's Commander.js parser.
"""

import plistlib
import shutil
import subprocess
import sys
from pathlib import Path


def find_srt():
    """Find srt binary location."""
    # Check common locations
    candidates = [
        Path.home() / ".bun/bin/srt",
        Path("/usr/local/bin/srt"),
        Path.home() / ".local/bin/srt",
        Path.home() / ".npm-global/bin/srt",
    ]

    for path in candidates:
        if path.exists():
            return str(path)

    # Try which
    try:
        result = subprocess.run(["which", "srt"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except OSError:
        pass

    return None


def patch_plist(dry_run=False, srt_path=None, srt_config=None):
    home = Path.home()
    plist_path = home / "Library/LaunchAgents/ai.openclaw.gateway.plist"

    if not plist_path.exists():
        print(f"ERROR: Plist not found at {plist_path}")
        print("Run 'openclaw daemon install' first.")
        sys.exit(1)

    # Find SRT
    if srt_path is None:
        srt_path = find_srt()
        if srt_path is None:
            print("ERROR: Could not find srt binary.")
            print("Install with: npm install -g @anthropic-ai/sandbox-runtime")
            sys.exit(1)

    # Default config path
    if srt_config is None:
        srt_config = str(home / ".srt-settings.json")

    if not Path(srt_config).exists():
        print(f"WARNING: SRT config not found at {srt_config}")
        print("Create it first or specify with --srt-config")

    # Read plist
    with open(plist_path, "rb") as f:
        plist = plistlib.load(f)

    args = plist.get("ProgramArguments", [])

    # Check if already patched
    if args and args[0] == srt_path:
        print("Already patched with SRT wrapper.")
        return

    # Build SRT prefix with -- separator
    srt_prefix = [srt_path, "--settings", srt_config, "--"]

    # Prepend SRT wrapper
    new_args = srt_prefix + args
    plist["ProgramArguments"] = new_args

    # Update PATH to include SRT's directory
    env = plist.get("EnvironmentVariables", {})
    current_path = env.get("PATH", "/usr/bin:/bin")
    srt_dir = str(Path(srt_path).parent)

    if srt_dir not in current_path:
        env["PATH"] = f"{srt_dir}:{current_path}"
        plist["EnvironmentVariables"] = env

    # Show what we're doing
    print("Patching plist:")
    print(f"  SRT path: {srt_path}")
    print(f"  SRT config: {srt_config}")
    print("  New ProgramArguments:")
    for i, arg in enumerate(new_args):
        print(f"    [{i}] {arg}")

    if dry_run:
        print("\n[DRY RUN] No changes written.")
        return

    # Backup original
    backup_path = str(plist_path) + ".backup"
    shutil.copy(plist_path, backup_path)
    print(f"\nBackup saved to: {backup_path}")

    # Write patched plist
    with open(plist_path, "wb") as f:
        plistlib.dump(plist, f)

    print("Plist patched successfully!")
    print("\nNext steps:")
    print(f"  launchctl bootstrap gui/$(id -u) {plist_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Patch OpenClaw plist for SRT")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    parser.add_argument("--srt-path", help="Path to srt binary")
    parser.add_argument("--srt-config", help="Path to SRT config file")
    args = parser.parse_args()

    patch_plist(dry_run=args.dry_run, srt_path=args.srt_path, srt_config=args.srt_config)
