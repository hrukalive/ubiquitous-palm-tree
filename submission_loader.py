"""
Submission discovery, metadata loading, and eval-function import helpers.
"""

from __future__ import annotations

import importlib
import inspect
import logging
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import yaml


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_metadata(metadata_path: str) -> Dict[str, Any]:
    """Load a single Gradescope metadata file."""
    try:
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = yaml.safe_load(f)
        return metadata if isinstance(metadata, dict) else {}
    except FileNotFoundError:
        logger.error("Metadata file not found: %s", metadata_path)
        raise
    except Exception as exc:
        logger.error("Error loading metadata from %s: %s", metadata_path, exc)
        raise


@lru_cache(maxsize=None)
def discover_export_dirs(submissions_root: str) -> Tuple[str, ...]:
    """
    Discover export directories under the submissions root.

    An export directory must contain submission_metadata.yml.
    """
    root = Path(submissions_root)
    if not root.exists():
        return ()

    export_dirs = []
    for child in sorted(root.iterdir()):
        if child.is_dir() and (child / "submission_metadata.yml").exists():
            export_dirs.append(str(child))
    return tuple(export_dirs)


@lru_cache(maxsize=None)
def load_all_metadata(submissions_root: str) -> Dict[str, Any]:
    """
    Merge metadata across all exports under submissions_root.

    Submission IDs are the stable key. The first occurrence wins, which keeps
    behavior deterministic when the same export is copied twice.
    """
    merged: Dict[str, Any] = {}
    for export_dir in discover_export_dirs(submissions_root):
        metadata_path = Path(export_dir) / "submission_metadata.yml"
        metadata = load_metadata(str(metadata_path))
        for submission_id, entry in metadata.items():
            if submission_id not in merged and isinstance(entry, dict):
                merged[submission_id] = entry
    return merged


@lru_cache(maxsize=None)
def build_submission_catalog(submissions_root: str) -> Dict[str, Dict[str, Any]]:
    """
    Build a catalog keyed by submission ID.

    Each entry includes the export directory, submission directory, and raw
    metadata needed for later leaderboard generation.
    """
    catalog: Dict[str, Dict[str, Any]] = {}
    for export_dir in discover_export_dirs(submissions_root):
        export_path = Path(export_dir)
        metadata_path = export_path / "submission_metadata.yml"
        metadata = load_metadata(str(metadata_path))
        for submission_id, entry in metadata.items():
            if submission_id in catalog or not isinstance(entry, dict):
                continue
            submission_dir = export_path / submission_id
            if not submission_dir.exists():
                continue
            catalog[submission_id] = {
                "export_dir": str(export_path),
                "submission_dir": str(submission_dir),
                "metadata": entry,
            }
    return catalog


def get_submission_directory(
    submission_id: str, submissions_root: str
) -> Optional[str]:
    entry = build_submission_catalog(submissions_root).get(submission_id)
    if not entry:
        return None
    submission_dir = entry.get("submission_dir")
    return str(submission_dir) if isinstance(submission_dir, str) else None


def get_eligible_submissions(metadata: Dict[str, Any], min_score: float) -> List[str]:
    """Filter submissions that meet the minimum score threshold."""
    eligible = []
    for submission_id, data in metadata.items():
        if isinstance(data, dict) and float(data.get(":score", 0.0)) >= min_score:
            eligible.append(submission_id)
    return sorted(eligible)


def find_breakthrough_py(submission_dir: str) -> Optional[str]:
    """Locate breakthrough.py in a submission directory."""
    submission_path = Path(submission_dir)

    direct_path = submission_path / "breakthrough.py"
    if direct_path.exists():
        return str(direct_path)

    src_path = submission_path / "src" / "breakthrough.py"
    if src_path.exists():
        return str(src_path)

    logger.warning("breakthrough.py not found in %s", submission_dir)
    return None


def load_eval_fn(submission_id: str, submissions_root: str) -> Optional[Callable]:
    """
    Dynamically load a student evaluation function by submission ID.
    """
    submission_dir = get_submission_directory(submission_id, submissions_root)
    if not submission_dir:
        logger.error("%s: submission directory not found", submission_id)
        return None

    breakthrough_file = find_breakthrough_py(submission_dir)
    if not breakthrough_file:
        logger.error("%s: breakthrough.py not found", submission_id)
        return None

    breakthrough_path = Path(breakthrough_file)
    source_dir = breakthrough_path.parent
    import_root = source_dir.parent if source_dir.name == "src" else source_dir
    original_path = sys.path.copy()
    original_modules = set(sys.modules.keys())

    stale_games = [key for key in sys.modules if key == "games" or key.startswith("games.")]
    for mod_name in stale_games:
        sys.modules.pop(mod_name, None)
    importlib.invalidate_caches()

    try:
        sys.path.insert(0, str(import_root))
        if source_dir != import_root:
            sys.path.insert(0, str(source_dir))

        try:
            import distutils.command.install as distutils_install

            if not hasattr(distutils_install, "value"):
                distutils_install.value = None
        except Exception:
            pass

        import games

        sys.modules["games"] = games

        with breakthrough_path.open("r", encoding="utf-8") as f:
            code = f.read()

        namespace: Dict[str, Any] = {}
        exec(code, namespace)

        eval_fn_names = [
            "competition_eval_fn"
        ]

        raw_fn = None
        for fn_name in eval_fn_names:
            candidate = namespace.get(fn_name)
            if callable(candidate):
                raw_fn = candidate
                logger.info("%s: Found eval function '%s'", submission_id, fn_name)
                break

        if raw_fn is None:
            logger.error("%s: No eval function found", submission_id)
            return None

        sig = inspect.signature(raw_fn)
        params = list(sig.parameters.values())

        if len(params) == 1:
            logger.info("%s: Wrapping 1-param signature", submission_id)
            return lambda state, player, _fn=raw_fn: _fn(state)

        if len(params) >= 2:
            logger.info("%s: Using %s-param signature as-is", submission_id, len(params))
            return raw_fn

        logger.error("%s: Invalid signature (0 params)", submission_id)
        return None

    except Exception as exc:
        import traceback

        logger.error("%s: Error loading eval function: %s", submission_id, exc)
        logger.error("%s: Traceback:\n%s", submission_id, traceback.format_exc())
        return None

    finally:
        sys.path = original_path
        games_modules = [key for key in sys.modules if key == "games" or key.startswith("games.")]
        for mod_name in games_modules:
            sys.modules.pop(mod_name, None)

        current_keys = list(sys.modules.keys())
        for mod_name in current_keys:
            if mod_name not in original_modules:
                sys.modules.pop(mod_name, None)

        importlib.invalidate_caches()


def load_profile_name(submission_dir: str) -> Optional[str]:
    """Load a custom display name from profile.txt if present."""
    submission_path = Path(submission_dir)

    profile_path = submission_path / "profile.txt"
    if not profile_path.exists():
        profile_path = submission_path / "src" / "profile.txt"

    if not profile_path.exists():
        return None

    try:
        with open(profile_path, "r", encoding="utf-8") as f:
            line = f.readline().strip()
        if not line:
            return None
        return line[:30]
    except Exception:
        return None


if __name__ == "__main__":
    from tournament_config import MIN_SCORE, SUBMISSIONS_DIR

    print("Testing submission_loader.py...")

    catalog = build_submission_catalog(SUBMISSIONS_DIR)
    print(f"Discovered {len(discover_export_dirs(SUBMISSIONS_DIR))} export directories")
    print(f"Catalogued {len(catalog)} submissions")

    metadata = load_all_metadata(SUBMISSIONS_DIR)
    eligible = get_eligible_submissions(metadata, MIN_SCORE)
    print(f"Found {len(eligible)} eligible submissions")

    for submission_id in eligible[:2]:
        fn = load_eval_fn(submission_id, SUBMISSIONS_DIR)
        print(f"{submission_id}: {'OK' if fn else 'FAIL'}")
