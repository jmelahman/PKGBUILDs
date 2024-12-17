#!/usr/bin/env python3
from datetime import datetime
import json
import re
import subprocess
from pathlib import Path
from typing import NamedTuple

class Package(NamedTuple):
    name: str
    version: str

def run_nvchecker() -> list[str]:
    result = subprocess.check_output(
        ["nvchecker", "--logger=json", "-c", "nvchecker.toml"],
        text=True,
    )
    return result.splitlines()

def parse_nvchecker_output(lines: list[str]) -> list[Package]:
    nv_data = []
    for line in lines:
        data = json.loads(line)
        nv_data.append(Package(name=data["name"], version=(data["version"])))
    return nv_data

def process_package(package: Package) -> None:
    latest_version = package.version.lstrip("v")

    dir_path = Path(package.name)
    pkgbuild_path = dir_path / "PKGBUILD"

    content = pkgbuild_path.read_text()
    if not content:
        raise RuntimeError(f"Failed to read PKGBUILD for package {package.name}")

    match = re.search(r"(?m)^pkgver=(.+)$", content)
    if not match:
        raise RuntimeError(f"pkgver not found in PKGBUILD for package {package.name}")

    current_version = match.group(1).strip()

    if current_version == latest_version:
        return

    updated_content = re.sub(r"(?m)^pkgver=(.+)$", f"pkgver={latest_version}", content)
    pkgbuild_path.write_text(updated_content)
    subprocess.run(["updpkgsums"], check=True, capture_output=True, cwd=dir_path)

    print(f"Bump {package.name} from v{current_version} to {package.version}")

def main():
    lines = run_nvchecker()
    packages = parse_nvchecker_output(lines)

    for package in packages:
        process_package(package)

if __name__ == "__main__":
    main()
