"""
Tests for the .gitignore patterns introduced/updated in this PR.

Uses `git check-ignore` to verify that patterns in .gitignore match
the expected files and directories, and do NOT match files that should
be tracked.
"""

import subprocess
import os
import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def is_ignored(path: str) -> bool:
    """Return True if git considers *path* (relative to repo root) ignored."""
    result = subprocess.run(
        ["git", "check-ignore", "--quiet", path],
        cwd=REPO_ROOT,
        capture_output=True,
    )
    return result.returncode == 0


def is_not_ignored(path: str) -> bool:
    return not is_ignored(path)


# ---------------------------------------------------------------------------
# Directory patterns
# ---------------------------------------------------------------------------

class TestDirectoryPatterns:
    def test_pycache_directory_is_ignored(self):
        assert is_ignored("__pycache__/")

    def test_pycache_file_inside_directory_is_ignored(self):
        assert is_ignored("__pycache__/module.cpython-311.pyc")

    def test_egg_info_directory_is_ignored(self):
        assert is_ignored("mypackage.egg-info/")

    def test_egg_info_file_inside_is_ignored(self):
        assert is_ignored("mypackage.egg-info/PKG-INFO")

    def test_build_directory_is_ignored(self):
        assert is_ignored("build/")

    def test_dist_directory_is_ignored(self):
        assert is_ignored("dist/")

    def test_node_modules_directory_is_ignored(self):
        assert is_ignored("node_modules/")

    def test_node_modules_nested_file_is_ignored(self):
        assert is_ignored("node_modules/express/index.js")

    def test_venv_directory_is_ignored(self):
        assert is_ignored("venv/")

    def test_dot_venv_directory_is_ignored(self):
        assert is_ignored(".venv/")

    def test_coverage_directory_is_ignored(self):
        assert is_ignored("coverage/")

    def test_htmlcov_directory_is_ignored(self):
        assert is_ignored("htmlcov/")


# ---------------------------------------------------------------------------
# Compiled file patterns
# ---------------------------------------------------------------------------

class TestCompiledFilePatterns:
    def test_pyc_file_is_ignored(self):
        assert is_ignored("module.pyc")

    def test_pyo_file_is_ignored(self):
        assert is_ignored("module.pyo")

    def test_pyd_file_is_ignored(self):
        assert is_ignored("module.pyd")

    def test_so_file_is_ignored(self):
        assert is_ignored("_extension.so")

    def test_dylib_file_is_ignored(self):
        assert is_ignored("libfoo.dylib")

    def test_dll_file_is_ignored(self):
        assert is_ignored("library.dll")

    def test_exe_file_is_ignored(self):
        assert is_ignored("program.exe")

    def test_object_file_is_ignored(self):
        assert is_ignored("main.o")

    def test_obj_file_is_ignored(self):
        assert is_ignored("main.obj")

    def test_static_lib_a_is_ignored(self):
        assert is_ignored("libfoo.a")

    def test_static_lib_lib_is_ignored(self):
        assert is_ignored("foo.lib")


# ---------------------------------------------------------------------------
# Log and temporary file patterns
# ---------------------------------------------------------------------------

class TestLogAndTempPatterns:
    def test_log_file_is_ignored(self):
        assert is_ignored("app.log")

    def test_log_file_with_prefix_is_ignored(self):
        assert is_ignored("error.log")

    def test_tmp_file_is_ignored(self):
        assert is_ignored("data.tmp")

    def test_swp_file_is_ignored(self):
        assert is_ignored(".main.py.swp")

    def test_swo_file_is_ignored(self):
        assert is_ignored(".main.py.swo")


# ---------------------------------------------------------------------------
# System file patterns
# ---------------------------------------------------------------------------

class TestSystemFilePatterns:
    def test_ds_store_is_ignored(self):
        assert is_ignored(".DS_Store")

    def test_thumbs_db_is_ignored(self):
        assert is_ignored("Thumbs.db")


# ---------------------------------------------------------------------------
# Coverage patterns
# ---------------------------------------------------------------------------

class TestCoveragePatterns:
    def test_coverage_file_is_ignored(self):
        assert is_ignored(".coverage")

    def test_coverage_data_variant_is_not_ignored(self):
        # The .gitignore only contains `.coverage` (not `.coverage.*`),
        # so parallel-run data files like .coverage.1234 are NOT ignored.
        assert is_not_ignored(".coverage.1234")


# ---------------------------------------------------------------------------
# Environment file patterns
# ---------------------------------------------------------------------------

class TestEnvironmentFilePatterns:
    def test_dot_env_file_is_ignored(self):
        assert is_ignored(".env")

    def test_dot_env_local_is_ignored(self):
        assert is_ignored(".env.local")

    def test_dot_env_production_is_ignored(self):
        assert is_ignored(".env.production")

    def test_dot_env_test_is_ignored(self):
        assert is_ignored(".env.test")

    def test_env_suffix_file_is_ignored(self):
        assert is_ignored("config.env")

    def test_dot_env_star_pattern_matches_variants(self):
        assert is_ignored(".env.staging")


# ---------------------------------------------------------------------------
# Python-specific patterns
# ---------------------------------------------------------------------------

class TestPythonSpecificPatterns:
    def test_pyc_via_py_cod_pattern(self):
        # *.py[cod] matches .pyc, .pyo, .pyd
        assert is_ignored("compiled.pyc")

    def test_pyo_via_py_cod_pattern(self):
        assert is_ignored("compiled.pyo")

    def test_pyd_via_py_cod_pattern(self):
        assert is_ignored("extension.pyd")

    def test_py_class_file_is_ignored(self):
        assert is_ignored("MyClass$py.class")

    def test_eggs_directory_is_ignored(self):
        assert is_ignored(".eggs/")

    def test_pip_log_is_ignored(self):
        assert is_ignored("pip-log.txt")

    def test_pip_delete_dir_is_ignored(self):
        assert is_ignored("pip-delete-this-directory.txt")


# ---------------------------------------------------------------------------
# Compressed file patterns
# ---------------------------------------------------------------------------

class TestCompressedFilePatterns:
    def test_zip_is_ignored(self):
        assert is_ignored("archive.zip")

    def test_gz_is_ignored(self):
        assert is_ignored("archive.gz")

    def test_tar_is_ignored(self):
        assert is_ignored("archive.tar")

    def test_tgz_is_ignored(self):
        assert is_ignored("archive.tgz")

    def test_bz2_is_ignored(self):
        assert is_ignored("archive.bz2")

    def test_xz_is_ignored(self):
        assert is_ignored("archive.xz")

    def test_7z_is_ignored(self):
        assert is_ignored("archive.7z")

    def test_rar_is_ignored(self):
        assert is_ignored("archive.rar")

    def test_zst_is_ignored(self):
        assert is_ignored("archive.zst")

    def test_lz4_is_ignored(self):
        assert is_ignored("archive.lz4")

    def test_rpm_is_ignored(self):
        assert is_ignored("package.rpm")

    def test_deb_is_ignored(self):
        assert is_ignored("package.deb")

    def test_tar_gz_is_ignored(self):
        assert is_ignored("archive.tar.gz")

    def test_tar_bz2_is_ignored(self):
        assert is_ignored("archive.tar.bz2")

    def test_tar_xz_is_ignored(self):
        assert is_ignored("archive.tar.xz")

    def test_tar_zst_is_ignored(self):
        assert is_ignored("archive.tar.zst")


# ---------------------------------------------------------------------------
# Markdown code fence boundaries (PR-specific regression tests)
#
# The .gitignore in this PR is wrapped in markdown code fences (``` at line 1
# and line 79). Git interprets these as literal patterns, meaning any file
# or directory literally named ``` would be ignored.
# ---------------------------------------------------------------------------

class TestMarkdownCodeFenceBoundaries:
    def test_backtick_fence_pattern_is_present(self):
        """The .gitignore file starts and ends with ``` which git treats as
        a literal pattern entry.  Verify git recognises a path named ` `` ` as
        ignored (regression guard for the fence wrapping introduced in this PR).
        """
        assert is_ignored("```")

    def test_gitignore_first_line_is_code_fence(self):
        """Structural check: first non-empty byte sequence in .gitignore is ```."""
        gitignore_path = os.path.join(REPO_ROOT, ".gitignore")
        with open(gitignore_path, "r") as fh:
            first_line = fh.readline().rstrip("\n")
        assert first_line == "```"

    def test_gitignore_last_line_is_code_fence(self):
        """Structural check: last line in .gitignore is ```."""
        gitignore_path = os.path.join(REPO_ROOT, ".gitignore")
        with open(gitignore_path, "r") as fh:
            lines = fh.readlines()
        last_line = lines[-1].rstrip("\n")
        assert last_line == "```"


# ---------------------------------------------------------------------------
# Negative tests — files that SHOULD be tracked
# ---------------------------------------------------------------------------

class TestNegativePatterns:
    def test_python_source_file_is_not_ignored(self):
        assert is_not_ignored("main.py")

    def test_python_test_file_is_not_ignored(self):
        assert is_not_ignored("tests/test_main.py")

    def test_plain_text_file_is_not_ignored(self):
        assert is_not_ignored("notes.txt")

    def test_readme_is_not_ignored(self):
        assert is_not_ignored("README.md")

    def test_requirements_file_is_not_ignored(self):
        assert is_not_ignored("requirements.txt")

    def test_setup_py_is_not_ignored(self):
        assert is_not_ignored("setup.py")

    def test_json_file_is_not_ignored(self):
        assert is_not_ignored("config.json")

    def test_yaml_file_is_not_ignored(self):
        assert is_not_ignored("config.yaml")

    def test_src_directory_python_file_is_not_ignored(self):
        assert is_not_ignored("src/app.py")