#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "nvchecker[pypi]>=2.20",
# ]
# ///
from __future__ import annotations

import argparse
import json
import logging
import os
from pathlib import Path
import re
import subprocess
from typing import NamedTuple

# AUR package name to upstream package name.
ENTRY_TO_UPSTREAM = {
    "python-e3-core": "e3-core",
    "python-e3-testsuite": "e3-testsuite",
}


class Package(NamedTuple):
    name: str
    version: str
    revision: str | None
    gitref: str | None


def run_nvchecker(entry: str) -> list[str]:
    result = subprocess.run(  # noqa: S603
        [
            "python",
            "-m",
            "nvchecker",
            "--entry",
            ENTRY_TO_UPSTREAM.get(entry, entry),
            "--logger=json",
            "-c",
            "nvchecker.toml",
        ],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return result.stdout.splitlines()


def parse_nvchecker_output(lines: list[str]) -> list[Package]:
    nv_data = []
    for line in lines:
        data = json.loads(line)
        try:
            nv_data.append(
                Package(
                    name=ENTRY_TO_UPSTREAM.get(data["name"]) or data["name"],
                    version=data["version"],
                    revision=data.get("revision"),
                    gitref=data.get("rich_result", {}).get("gitref"),
                )
            )
        except KeyError:
            logging.warning("Skipping malformed nvchecker entry '%s': %s", data["name"], data["event"])
            raise
    return nv_data


def extract_git_url(content: str) -> str | None:
    match = re.search(r'["\'](?:[^"\']*::)?git\+([^#"\']+)', content)
    if not match:
        return None
    git_url = match.group(1)
    if "$url" in git_url:
        url_match = re.search(r'(?m)^url=["\']?([^"\'\n]+?)["\']?$', content)
        if not url_match:
            return None
        git_url = git_url.replace("${url}", url_match.group(1)).replace("$url", url_match.group(1))
    return git_url


def resolve_revision(git_url: str, gitref: str) -> str | None:
    """Resolve a ref to a commit sha, peeling annotated tags."""
    result = subprocess.run(  # noqa: S603
        ["git", "ls-remote", git_url, gitref, f"{gitref}^{{}}"],  # noqa: S607
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    refs = {}
    for line in result.stdout.splitlines():
        sha, _, ref = line.partition("\t")
        refs[ref] = sha
    return refs.get(f"{gitref}^{{}}") or refs.get(gitref)


def process_package(package: Package) -> None:
    dir_path = Path(package.name)
    pkgbuild_path = dir_path / "PKGBUILD"
    srcinfo_path = dir_path / ".SRCINFO"

    content = pkgbuild_path.read_text()
    if not content:
        msg = f"Failed to read PKGBUILD for package {package.name}"
        raise RuntimeError(msg)

    match = re.search(r"(?m)^pkgver=(.+)$", content)
    if not match:
        msg = f"pkgver not found in PKGBUILD for package {package.name}"
        raise RuntimeError(msg)

    current_version = match.group(1).strip()

    if current_version == package.version:
        return

    updated_content = re.sub(r"(?m)^pkgver=(.+)$", f"pkgver={package.version}", content)
    updated_content = re.sub(r"(?m)^pkgrel=(.+)$", "pkgrel=1", updated_content)

    if re.search(r"(?m)^_commit=", updated_content):
        # Prefer resolving the ref ourselves: nvchecker's revision is the tag
        # object id for annotated tags, not the commit it points to.
        revision = None
        if package.gitref:
            git_url = extract_git_url(updated_content)
            if git_url:
                revision = resolve_revision(git_url, package.gitref)
        revision = revision or package.revision
        if not revision:
            msg = f"Could not determine commit for {package.name} {package.version}"
            raise RuntimeError(msg)
        updated_content = re.sub(r"(?m)^_commit=(.+)$", f"_commit='{revision}'", updated_content)

    pkgbuild_path.write_text(updated_content)

    if "sums=('SKIP')" not in updated_content:
        # TODO: Hint to the user if this is uninstalled it's from the 'pacman-contrib' package.
        subprocess.run(["updpkgsums"], check=True, stdout=subprocess.DEVNULL, cwd=dir_path)

    with srcinfo_path.open(mode="w") as f:
        subprocess.run(["makepkg", "--printsrcinfo"], stdout=f, check=True, cwd=dir_path)

    print(f"Bump {package.name} from {current_version} to {package.version}")


def _directory(value: str) -> str:
    if not os.path.isdir(value):
        msg = f"'{value}' is not a valid directory path."
        raise argparse.ArgumentTypeError(msg)
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Process package version updates")
    parser.add_argument("package", type=_directory, help="The name of the package to process")
    args = parser.parse_args()

    lines = run_nvchecker(args.package)
    try:
        packages = parse_nvchecker_output(lines)
    except KeyError:
        return 1

    package = next((p for p in packages if p.name == args.package), None)

    if package:
        process_package(package)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
