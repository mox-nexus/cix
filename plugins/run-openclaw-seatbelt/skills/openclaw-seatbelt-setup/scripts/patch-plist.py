#!/usr/bin/env python3
"""
Patch OpenClaw launchd plist to add Seatbelt sandbox wrapper.

Usage:
    python3 patch-plist.py [--dry-run] [--json] [--profile PATH]

What it does:
    1. Reads ~/Library/LaunchAgents/ai.openclaw.gateway.plist
    2. Prepends sandbox-exec -f <profile> to ProgramArguments
    3. Updates Comment to reflect Seatbelt sandboxing
    4. Writes back (unless --dry-run)

Exit codes:
    0 - Success (or already patched)
    1 - Plist not found
    2 - Seatbelt profile not found
"""

import json
import plistlib
import shutil
import sys
from pathlib import Path

SANDBOX_EXEC = "/usr/bin/sandbox-exec"
DEFAULT_PROFILE = Path.home() / ".openclaw" / "sandbox.sb"


def patch_plist(dry_run=False, profile_path=None, json_output=False):
    """Patch the plist file. Returns result dict for JSON output."""
    result = {"success": False, "action": None, "error": None}
    home = Path.home()
    plist_path = home / "Library/LaunchAgents/ai.openclaw.gateway.plist"

    if not plist_path.exists():
        result["error"] = f"Plist not found at {plist_path}"
        if json_output:
            print(json.dumps(result))
        else:
            print(f"ERROR: {result['error']}")
            print("Run 'openclaw daemon install' first.")
        sys.exit(1)

    # Resolve profile path
    profile = Path(profile_path) if profile_path else DEFAULT_PROFILE
    if not profile.exists():
        result["error"] = f"Seatbelt profile not found at {profile}"
        if json_output:
            print(json.dumps(result))
        else:
            print(f"ERROR: {result['error']}")
            print("Copy the template: cp assets/sandbox.sb ~/.openclaw/sandbox.sb")
        sys.exit(2)

    # Read plist
    with open(plist_path, "rb") as f:
        plist = plistlib.load(f)

    args = plist.get("ProgramArguments", [])

    # Check if already patched with sandbox-exec
    if args and args[0] == SANDBOX_EXEC:
        result["success"] = True
        result["action"] = "already_patched"
        result["profile"] = str(profile)
        if json_output:
            print(json.dumps(result))
        else:
            print(f"Already patched with sandbox-exec (profile: {profile}).")
        return

    # Strip any existing SRT wrapper (srt --settings ... --)
    if args and "srt" in args[0]:
        # Find the -- separator and take everything after it
        try:
            sep_idx = args.index("--")
            args = args[sep_idx + 1 :]
        except ValueError:
            pass  # No separator, leave as-is

    # Build sandbox-exec prefix
    sb_prefix = [SANDBOX_EXEC, "-f", str(profile)]

    # Prepend sandbox-exec wrapper
    new_args = sb_prefix + args
    plist["ProgramArguments"] = new_args

    # Update comment
    version = plist.get("EnvironmentVariables", {}).get("OPENCLAW_SERVICE_VERSION", "unknown")
    plist["Comment"] = (
        f"OpenClaw Gateway (v{version}) - "
        "Seatbelt sandbox (filesystem only, network open pending openclaw/openclaw#13567)"
    )

    # Show what we're doing
    if not json_output:
        print("Patching plist for Seatbelt sandbox:")
        print(f"  Profile: {profile}")
        print("  New ProgramArguments:")
        for i, arg in enumerate(new_args):
            print(f"    [{i}] {arg}")

    if dry_run:
        result["success"] = True
        result["action"] = "dry_run"
        result["profile"] = str(profile)
        result["new_args"] = new_args
        if json_output:
            print(json.dumps(result))
        else:
            print("\n[DRY RUN] No changes written.")
        return

    # Backup original
    backup_path = str(plist_path) + ".backup"
    shutil.copy(plist_path, backup_path)

    # Write patched plist
    with open(plist_path, "wb") as f:
        plistlib.dump(plist, f)

    result["success"] = True
    result["action"] = "patched"
    result["profile"] = str(profile)
    result["backup_path"] = backup_path
    result["plist_path"] = str(plist_path)

    if json_output:
        print(json.dumps(result))
    else:
        print(f"\nBackup saved to: {backup_path}")
        print("Plist patched successfully!")
        print("\nNext steps:")
        print(f"  launchctl bootstrap gui/$(id -u) {plist_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Patch OpenClaw plist for Seatbelt sandbox")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    parser.add_argument("--json", action="store_true", help="Output JSON for scripting")
    parser.add_argument("--profile", help=f"Path to Seatbelt profile (default: {DEFAULT_PROFILE})")
    args = parser.parse_args()

    patch_plist(
        dry_run=args.dry_run,
        profile_path=args.profile,
        json_output=args.json,
    )
