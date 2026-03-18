#!/usr/bin/env python3
"""
Copy missing submission folders from old export to new export.

Gradescope exports may exclude old submission folders when students resubmit.
Tournament system needs these folders to load eval_fn code from all submissions.

Usage:
    # Dry run (preview what would be copied)
    python copy_missing_submissions.py \
        --old-export /path/to/old/export \
        --new-export /path/to/new/export \
        --dry-run

    # Actual copy
    python copy_missing_submissions.py \
        --old-export /path/to/old/export \
        --new-export /path/to/new/export
"""

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Set, Tuple


def scan_submission_folders(export_dir: Path) -> Set[str]:
    """
    Scan export directory for submission_* folders.

    Args:
        export_dir: Path to Gradescope export directory

    Returns:
        Set of submission folder names (e.g., {'submission_391359696', ...})
    """
    submissions = set()
    for item in export_dir.glob("submission_*"):
        if item.is_dir():
            submissions.add(item.name)
    return submissions


def format_bytes(num_bytes: int) -> str:
    """Format byte count as human-readable string."""
    for unit in ("B", "KB", "MB", "GB"):
        if num_bytes < 1024.0:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} TB"


def get_folder_size(folder_path: Path) -> int:
    """Calculate total size of folder and its contents."""
    total = 0
    try:
        for entry in folder_path.rglob("*"):
            if entry.is_file():
                total += entry.stat().st_size
    except (OSError, PermissionError):
        pass
    return total


def copy_submissions(
    old_dir: Path,
    new_dir: Path,
    missing: Set[str],
    dry_run: bool,
) -> Tuple[int, int, int]:
    """
    Copy missing submission folders with error handling.

    Args:
        old_dir: Source export directory
        new_dir: Destination export directory
        missing: Set of folder names to copy
        dry_run: If True, preview without copying

    Returns:
        Tuple of (successful_count, failed_count, total_bytes)
    """
    successful = 0
    failed = 0
    total_bytes = 0

    for folder_name in sorted(missing):
        src = old_dir / folder_name
        dst = new_dir / folder_name

        try:
            folder_size = get_folder_size(src)
            size_str = format_bytes(folder_size)

            if dry_run:
                print(f"  [WOULD COPY] {folder_name} ({size_str})")
                successful += 1
                total_bytes += folder_size
            else:
                shutil.copytree(src, dst, dirs_exist_ok=False)
                print(f"  [OK] {folder_name} ({size_str})")
                successful += 1
                total_bytes += folder_size
        except FileExistsError:
            print(f"  [EXISTS] {folder_name} (already exists in new export)", file=sys.stderr)
            failed += 1
        except PermissionError:
            print(
                f"  [ERROR] {folder_name} (Permission denied)",
                file=sys.stderr,
            )
            failed += 1
        except OSError as e:
            print(
                f"  [ERROR] {folder_name} ({e.strerror})",
                file=sys.stderr,
            )
            failed += 1
        except Exception as e:
            print(
                f"  [ERROR] {folder_name} (Unexpected error: {type(e).__name__})",
                file=sys.stderr,
            )
            failed += 1

    return successful, failed, total_bytes


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Copy missing submission folders from old Gradescope export to new export.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--old-export",
        type=str,
        required=True,
        help="Path to old Gradescope export directory",
    )
    parser.add_argument(
        "--new-export",
        type=str,
        required=True,
        help="Path to new Gradescope export directory",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be copied without actually copying",
    )

    args = parser.parse_args()

    # Convert to Path objects
    old_export = Path(args.old_export)
    new_export = Path(args.new_export)

    # Validate paths exist
    if not old_export.exists():
        print(f"Error: Old export directory not found: {old_export}", file=sys.stderr)
        return 1

    if not old_export.is_dir():
        print(f"Error: Old export is not a directory: {old_export}", file=sys.stderr)
        return 1

    if not new_export.exists():
        print(f"Error: New export directory not found: {new_export}", file=sys.stderr)
        return 1

    if not new_export.is_dir():
        print(f"Error: New export is not a directory: {new_export}", file=sys.stderr)
        return 1

    # Scan both directories
    try:
        old_submissions = scan_submission_folders(old_export)
        new_submissions = scan_submission_folders(new_export)
    except Exception as e:
        print(f"Error scanning directories: {e}", file=sys.stderr)
        return 1

    # Find missing submissions
    missing = old_submissions - new_submissions

    # Print report header
    print("=" * 50)
    print("Submission Folder Sync Report")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Old Export: {old_export.resolve()}")
    print(f"New Export: {new_export.resolve()}")
    print()

    print(f"Found {len(old_submissions)} submission folder(s) in old export")
    print(f"Found {len(new_submissions)} submission folder(s) in new export")
    print(f"Missing in new export: {len(missing)} folder(s)")
    print()

    # Handle case where nothing is missing
    if not missing:
        print("No missing submissions to copy.")
        print()
        print("=" * 50)
        return 0

    # Copy submissions
    mode_label = "[DRY RUN]" if args.dry_run else "[COPYING]"
    print(f"{mode_label} Processing the following:")
    print()

    successful, failed, total_bytes = copy_submissions(
        old_export, new_export, missing, args.dry_run
    )

    # Print summary
    print()
    print("Summary:")
    print(f"  Successfully processed: {successful} folder(s) ({format_bytes(total_bytes)})")
    if failed > 0:
        print(f"  Failed: {failed} folder(s)")
    print()
    print("=" * 50)

    # Return appropriate exit code
    return 1 if failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
