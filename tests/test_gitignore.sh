#!/usr/bin/env bash
# Tests for .gitignore patterns modified in this PR.
# Uses `git check-ignore` to verify each pattern produces the expected result.
# Exit 0 = all tests passed; non-zero = at least one failure.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0
FAIL=0

# Colours (disabled when not a tty)
if [ -t 1 ]; then
    GREEN='\033[0;32m'; RED='\033[0;31m'; RESET='\033[0m'
else
    GREEN=''; RED=''; RESET=''
fi

pass() { echo -e "${GREEN}PASS${RESET} $1"; PASS=$((PASS+1)); }
fail() { echo -e "${RED}FAIL${RESET} $1"; FAIL=$((FAIL+1)); }

# Assert a path IS ignored by .gitignore
assert_ignored() {
    local path="$1"
    local desc="$2"
    if git -C "$REPO_ROOT" check-ignore -q "$REPO_ROOT/$path" 2>/dev/null; then
        pass "$desc ('$path' is ignored)"
    else
        fail "$desc ('$path' should be ignored but is NOT)"
    fi
}

# Assert a path is NOT ignored by .gitignore
assert_not_ignored() {
    local path="$1"
    local desc="$2"
    if git -C "$REPO_ROOT" check-ignore -q "$REPO_ROOT/$path" 2>/dev/null; then
        fail "$desc ('$path' should NOT be ignored but IS)"
    else
        pass "$desc ('$path' is not ignored)"
    fi
}

# ---------------------------------------------------------------------------
# Patterns ADDED or NEWLY present in this PR
# ---------------------------------------------------------------------------

# *.out — new compiled-artifact pattern
assert_ignored "program.out"           "*.out — output binary ignored"
assert_ignored "deep/dir/run.out"      "*.out — nested output binary ignored"

# target/ — build output (Rust/Maven etc.)
assert_ignored "target/"               "target/ directory ignored"
assert_ignored "target/release"        "file inside target/ ignored"

# .gradle/ — Gradle cache
assert_ignored ".gradle/"              ".gradle/ directory ignored"
assert_ignored ".gradle/caches"        "file inside .gradle/ ignored"

# .mypy_cache/ — mypy type-checker cache
assert_ignored ".mypy_cache/"          ".mypy_cache/ directory ignored"
assert_ignored ".mypy_cache/3.11"      "file inside .mypy_cache/ ignored"

# .pytest_cache/ — pytest cache
assert_ignored ".pytest_cache/"        ".pytest_cache/ directory ignored"
assert_ignored ".pytest_cache/v"       "file inside .pytest_cache/ ignored"

# .env.local — explicit local env file (new entry)
assert_ignored ".env.local"            ".env.local ignored"

# *.env.* — wildcard env variants (e.g. .env.production, app.env.test)
assert_ignored ".env.production"       "*.env.* — .env.production ignored"
assert_ignored "app.env.staging"       "*.env.* — app.env.staging ignored"
assert_ignored "config.env.local"      "*.env.* — config.env.local ignored"

# htmlcov/ — HTML coverage report directory (moved from old section)
assert_ignored "htmlcov/"              "htmlcov/ directory ignored"
assert_ignored "htmlcov/index.html"    "file inside htmlcov/ ignored"

# .coverage — coverage data file (reorganized; must still be ignored)
assert_ignored ".coverage"             ".coverage data file still ignored"

# coverage/ — coverage directory (must still be ignored after reorganisation)
assert_ignored "coverage/"             "coverage/ directory still ignored"
assert_ignored "coverage/lcov.info"    "file inside coverage/ still ignored"

# ---------------------------------------------------------------------------
# Core compiled-artifact patterns that remain (regression guard)
# ---------------------------------------------------------------------------

assert_ignored "module.pyc"            "*.pyc still ignored"
assert_ignored "__pycache__/"          "__pycache__/ still ignored"
assert_ignored "native.o"             "*.o still ignored"
assert_ignored "native.obj"           "*.obj still ignored"
assert_ignored "lib.a"                "*.a still ignored"
assert_ignored "app.exe"              "*.exe still ignored"
assert_ignored "lib.dll"              "*.dll still ignored"
assert_ignored "lib.so"               "*.so still ignored"

# ---------------------------------------------------------------------------
# Patterns REMOVED in this PR — must NOT be matched by the old specific rule
# (they may still be caught by broader globs; we check the specific removed
#  patterns are absent when those broader globs would not catch them)
# ---------------------------------------------------------------------------

# *.pyo / *.pyd — removed; no remaining glob covers plain .pyo/.pyd files
assert_not_ignored "module.pyo"        "*.pyo — rule removed, not ignored"
assert_not_ignored "module.pyd"        "*.pyd — rule removed, not ignored"

# *.dylib — removed (macOS dynamic lib); no remaining glob covers it
assert_not_ignored "lib.dylib"         "*.dylib — rule removed, not ignored"

# *.lib — removed (Windows import lib); no remaining glob covers it
assert_not_ignored "import.lib"        "*.lib — rule removed, not ignored"

# .eggs/ — Python eggs directory removed
assert_not_ignored ".eggs/"            ".eggs/ — rule removed, not ignored"
assert_not_ignored ".eggs/mypkg"       "file inside .eggs/ — rule removed, not ignored"

# pip-log.txt — removed
assert_not_ignored "pip-log.txt"       "pip-log.txt — rule removed, not ignored"

# pip-delete-this-directory.txt — removed
assert_not_ignored "pip-delete-this-directory.txt" \
    "pip-delete-this-directory.txt — rule removed, not ignored"

# ---------------------------------------------------------------------------
# Boundary / regression cases
# ---------------------------------------------------------------------------

# .env is still explicitly listed
assert_ignored ".env"                  ".env still ignored (explicit entry)"

# .env.local boundary: a file named exactly ".envlocal" (no dot) should NOT match *.env.*
assert_not_ignored "envlocal"          "bare 'envlocal' not ignored by *.env.*"

# *.out should not match a directory named "output" (no .out extension)
assert_not_ignored "output/"           "'output/' dir not caught by *.out"

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

echo ""
echo "Results: ${PASS} passed, ${FAIL} failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1