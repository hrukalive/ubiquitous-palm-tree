"""
Submission Loader Module

Discovers, validates, and dynamically imports student evaluation functions
from Gradescope submissions. Handles two directory structures and normalizes
eval function signatures.
"""

import importlib
import os
import sys
import types
import inspect
import logging
from pathlib import Path
from typing import Dict, List, Optional, Callable, Tuple, Any

import yaml

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_metadata(metadata_path: str) -> Dict[str, Any]:
    """
    Load submission metadata from a YAML file.

    Args:
        metadata_path: Path to submission_metadata.yml file

    Returns:
        Dictionary with structure:
        {
            'submission_ID': {
                ':score': float,
                ':submitters': list of dicts with :name, :sid, :email
            },
            ...
        }
    """
    try:
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = yaml.safe_load(f)
        logger.info(f"Loaded metadata from {metadata_path}")
        return metadata if metadata else {}
    except FileNotFoundError:
        logger.error(f"Metadata file not found: {metadata_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading metadata from {metadata_path}: {e}")
        raise


def get_eligible_submissions(metadata: Dict[str, Any], min_score: float) -> List[str]:
    """
    Filter submissions that meet minimum score requirement.

    Args:
        metadata: Dictionary of submission metadata
        min_score: Minimum score threshold (e.g., 50.0)

    Returns:
        List of submission IDs that have score >= min_score
    """
    eligible = []
    for submission_id, data in metadata.items():
        if isinstance(data, dict) and ":score" in data:
            score = data[":score"]
            if score >= min_score:
                eligible.append(submission_id)

    logger.info(f"Found {len(eligible)} eligible submissions (score >= {min_score})")
    return sorted(eligible)


def build_student_submission_map(metadata: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Build mapping from student_id -> [submission_ids] from metadata.
    
    Args:
        metadata: Dictionary from load_metadata()
        
    Returns:
        Dict mapping student_id (`:sid`) to list of submission IDs
        
    Example:
        {"901026365": ["submission_390957350"]}
    """
    sid_map = {}  # student_id -> [submission_id, ...]
    for sub_id, data in metadata.items():
        if not isinstance(data, dict):
            continue
        submitters = data.get(":submitters", [])
        if submitters:
            student_id = submitters[0].get(":sid", "")
            if student_id:
                sid_map.setdefault(student_id, []).append(sub_id)
    return sid_map


def build_submission_to_student_map(metadata: Dict[str, Any]) -> Dict[str, str]:
    """
    Build reverse mapping from submission_id -> student_id.
    
    Args:
        metadata: Dictionary from load_metadata()
        
    Returns:
        Dict mapping submission_id to student_id (`:sid`)
        
    Example:
        {"submission_390957350": "901026365"}
    """
    return {
        sub_id: data.get(":submitters", [{}])[0].get(":sid", "")
        for sub_id, data in metadata.items()
        if isinstance(data, dict) and data.get(":submitters")
    }


def find_breakthrough_py(submission_dir: str) -> Optional[str]:
    """
    Locate breakthrough.py in submission directory.

    Handles two directory structures:
    - Type A: submission_XXX/breakthrough.py (direct)
    - Type B: submission_XXX/src/breakthrough.py (in src subdir)

    Args:
        submission_dir: Path to submission directory

    Returns:
        Full path to breakthrough.py or None if not found
    """
    submission_path = Path(submission_dir)

    # Try Type A (direct)
    direct_path = submission_path / "breakthrough.py"
    if direct_path.exists():
        return str(direct_path)

    # Try Type B (in src subdirectory)
    src_path = submission_path / "src" / "breakthrough.py"
    if src_path.exists():
        return str(src_path)

    logger.warning(f"breakthrough.py not found in {submission_dir}")
    return None


def load_eval_fn(submission_id: str, submissions_dir: str) -> Optional[Callable]:
    """
    Dynamically load evaluation function from a student submission.

    Steps:
    1. Find breakthrough.py (Type A or Type B structure)
    2. Set up isolated environment with mock games module
    3. Execute the code
    4. Extract eval function (tries common names)
    5. Normalize signature to (state, player) -> float
    6. Clean up sys.path and sys.modules

    Args:
        submission_id: Submission ID (e.g., 'submission_391569593')
        submissions_dir: Path to submissions directory

    Returns:
        Normalized callable (state, player) -> float, or None on failure
    """
    submission_path = os.path.join(submissions_dir, submission_id)

    # Find breakthrough.py
    breakthrough_file = find_breakthrough_py(submission_path)
    if not breakthrough_file:
        logger.error(f"{submission_id}: breakthrough.py not found")
        return None

    # Determine directory to add to sys.path for imports
    submission_root = os.path.dirname(breakthrough_file)

    # Save original state
    original_path = sys.path.copy()
    original_modules = set(sys.modules.keys())
    # [DEBUG] Log games* modules before defensive cleanup
    games_before = [k for k in sys.modules if k == "games" or k.startswith("games.")]
    if games_before:
        logger.debug(f"{submission_id}: [BEFORE CLEANUP] Found stale games* modules: {games_before}")
    # Defensive cleanup: remove any residual 'games' mock from previous load
    # This ensures a clean slate even if a previous call's cleanup was incomplete
    stale_games = [key for key in sys.modules if key == "games" or key.startswith("games.")]
    for mod_name in stale_games:
        sys.modules.pop(mod_name, None)
    importlib.invalidate_caches()

    try:
        # Set up isolated environment
        sys.path.insert(0, submission_root)

        # Import real games module (contains Game class)
        import games
        sys.modules["games"] = games

        # Read and execute the breakthrough.py code
        with open(breakthrough_file, "r", encoding="utf-8") as f:
            code = f.read()

        # Create namespace for execution
        namespace = {}

        # Execute the code
        exec(code, namespace)
        # [DEBUG] Log games* modules after exec()
        games_after_exec = [k for k in sys.modules if k == "games" or k.startswith("games.")]
        logger.debug(f"{submission_id}: [AFTER EXEC] games* modules present: {games_after_exec}")

        # Try to find eval function (common naming patterns)
        eval_fn_names = [
            "competition_eval_fn",
            "ag_eval_fn",
            "eval_fn",
            "evaluator",
            "evaluator_1",
            "evaluator_2",
            "evaluator_3",
            "evaluator_4",
        ]

        raw_fn = None
        for fn_name in eval_fn_names:
            if fn_name in namespace:
                raw_fn = namespace[fn_name]
                if callable(raw_fn):
                    logger.info(f"{submission_id}: Found eval function '{fn_name}'")
                    break

        if raw_fn is None:
            logger.error(f"{submission_id}: No eval function found")
            return None

        # Normalize function signature
        sig = inspect.signature(raw_fn)
        params = list(sig.parameters.values())
        num_params = len(params)

        if num_params == 1:
            # Single param: wrap to accept both state and player
            logger.info(f"{submission_id}: Wrapping 1-param signature")
            normalized = lambda state, player, _fn=raw_fn: _fn(state)
        elif num_params >= 2:
            # Two or more params: use as-is
            logger.info(f"{submission_id}: Using {num_params}-param signature as-is")
            normalized = raw_fn
        else:
            logger.error(f"{submission_id}: Invalid signature (0 params)")
            return None

        logger.info(f"{submission_id}: Successfully loaded eval function")
        return normalized


    except Exception as e:
        import traceback
        logger.error(f"{submission_id}: Error loading eval function: {e}")
        logger.error(f"{submission_id}: Traceback:\n{traceback.format_exc()}")
        return None

    finally:
        # Clean up sys.path first (order matters - prevents re-imports during cleanup)
        sys.path = original_path
        # Explicitly remove 'games' mock and all submodules (e.g., games.board)
        # This must happen before the general cleanup to ensure complete removal
        games_modules = [key for key in sys.modules if key == "games" or key.startswith("games.")]
        for mod_name in games_modules:
            sys.modules.pop(mod_name, None)

        # Clean up ALL modules added or modified during execution
        # Strategy: Remove everything not in the original snapshot
        current_keys = list(sys.modules.keys())  # Snapshot before iteration
        for mod_name in current_keys:
            if mod_name not in original_modules:
                sys.modules.pop(mod_name, None)

        # Invalidate import caches to prevent stale references
        importlib.invalidate_caches()
        # [DEBUG] Log games* modules after cleanup (should be empty)
        games_after_cleanup = [k for k in sys.modules if k == "games" or k.startswith("games.")]
        if games_after_cleanup:
            logger.warning(f"{submission_id}: [AFTER CLEANUP] Cleanup incomplete! Residual modules: {games_after_cleanup}")
        else:
            logger.debug(f"{submission_id}: [AFTER CLEANUP] All games* modules removed successfully")


def load_all_eligible(
    submissions_dir: str, metadata_path: str, min_score: float = 50.0
) -> Dict[str, Tuple[str, Optional[Callable]]]:
    """
    Load all eligible submissions' eval functions.

    Args:
        submissions_dir: Path to submissions directory
        metadata_path: Path to submission metadata YAML
        min_score: Minimum score threshold

    Returns:
        Dictionary mapping submission_id to (student_name, eval_fn) tuples
        where eval_fn may be None if loading failed
    """
    # Load metadata
    metadata = load_metadata(metadata_path)

    # Get eligible submissions
    eligible_ids = get_eligible_submissions(metadata, min_score)
    logger.info(f"Loading {len(eligible_ids)} eligible submissions...")

    result = {}
    for submission_id in eligible_ids:
        # Extract student name from metadata
        submission_data = metadata.get(submission_id, {})
        submitters = submission_data.get(":submitters", [])
        student_name = (
            submitters[0].get(":name", "Unknown") if submitters else "Unknown"
        )

        # Load eval function
        eval_fn = load_eval_fn(submission_id, submissions_dir)

        result[submission_id] = (student_name, eval_fn)

        status = "OK" if eval_fn else "FAIL"
        logger.info(f"{status} {submission_id}: {student_name}")

    loaded_count = sum(1 for _, fn in result.values() if fn is not None)
    logger.info(
        f"Successfully loaded {loaded_count}/{len(eligible_ids)} eval functions"
    )

    return result


def build_history_trace_map(metadata: Dict[str, Any]) -> Dict[str, str]:
    """
    Build mapping from old submission numeric IDs to latest submission IDs.
    
    Traces retired submissions through the :history field to find their
    latest submission, enabling retired submissions to display the current
    name and profile of the latest submission in the lineage.
    
    Args:
        metadata: Dictionary from load_metadata()
        
    Returns:
        Dict mapping numeric_id (str) to submission_id
        Example: {'392447693': 'submission_392592649'}
    """
    trace_map = {}
    for current_sub_id, entry in metadata.items():
        if not isinstance(entry, dict):
            continue
        history = entry.get(':history', [])
        for hist_entry in history:
            if isinstance(hist_entry, dict):
                old_id = hist_entry.get(':id')
                if old_id:
                    trace_map[str(old_id)] = current_sub_id
    return trace_map


def load_profile_name(submission_dir: str) -> Optional[str]:
    """
    Load custom display name from profile.txt in a submission directory.
    
    Handles two directory structures:
    - Type A: submission_XXX/profile.txt (direct)
    - Type B: submission_XXX/src/profile.txt (in src subdir)
    
    Args:
        submission_dir: Path to submission directory
        
    Returns:
        Display name string (max 30 chars) or None if missing/empty
    """
    submission_path = Path(submission_dir)
    
    # Try Type A (direct)
    profile_path = submission_path / "profile.txt"
    if not profile_path.exists():
        # Try Type B (in src subdirectory)
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
    # For testing
    from tournament_config import SUBMISSIONS_DIR, METADATA_FILE, MIN_SCORE

    print("Testing submission_loader.py...")

    # Test load_metadata
    print("\n1. Testing load_metadata...")
    metadata = load_metadata(METADATA_FILE)
    print(f"   Loaded {len(metadata)} submissions")

    # Test get_eligible_submissions
    print("\n2. Testing get_eligible_submissions...")
    eligible = get_eligible_submissions(metadata, MIN_SCORE)
    print(f"   Found {len(eligible)} eligible submissions")

    # Test find_breakthrough_py
    print("\n3. Testing find_breakthrough_py...")
    for submission_id in eligible[:2]:
        sub_dir = os.path.join(SUBMISSIONS_DIR, submission_id)
        bt_path = find_breakthrough_py(sub_dir)
        print(f"   {submission_id}: {bt_path}")

    # Test load_eval_fn for a couple submissions
    print("\n4. Testing load_eval_fn...")
    for submission_id in eligible[:2]:
        fn = load_eval_fn(submission_id, SUBMISSIONS_DIR)
        print(f"   {submission_id}: {'OK' if fn else 'FAIL'}")

    # Test load_all_eligible
    print("\n5. Testing load_all_eligible...")
    all_fns = load_all_eligible(SUBMISSIONS_DIR, METADATA_FILE, MIN_SCORE)
    print(f"   Loaded {len(all_fns)} submissions total")

    print("\nAll tests completed!")
