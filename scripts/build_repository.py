"""Publish one Fakepass Reborn build into the flat GitHub Pages APT source."""
import bz2
from datetime import datetime, timezone
from email.utils import format_datetime
import gzip
import hashlib
from pathlib import Path
import shutil
import subprocess
import sys

source = Path(sys.argv[1]).resolve()
fields = subprocess.check_output(
    ["dpkg-deb", "-f", str(source), "Package", "Version", "Architecture"], text=True)
metadata = dict(line.split(": ", 1) for line in fields.splitlines())
if metadata["Package"] != "com.skfallin.fakepassreborn" or metadata["Architecture"] != "iphoneos-arm64":
    raise SystemExit("Only the rootless Fakepass Reborn package belongs in this source")

site = Path(__file__).resolve().parent.parent / "docs"
pool = site / "pool"
pool.mkdir(parents=True, exist_ok=True)
filename = f'{metadata["Package"]}_{metadata["Version"].replace("~", ".")}_{metadata["Architecture"]}.deb'
shutil.copyfile(source, pool / filename)
packages = subprocess.check_output(["dpkg-scanpackages", "pool"], cwd=site).rstrip(b"\n") + b"\n"
(site / "Packages").write_bytes(packages)
(site / "Packages.gz").write_bytes(gzip.compress(packages, mtime=0))
(site / "Packages.bz2").write_bytes(bz2.compress(packages))
release = (
    "Origin: Fakepass Reborn\nLabel: Fakepass Reborn\nSuite: stable\nCodename: ios\n"
    "Architectures: iphoneos-arm64\nComponents: main\n"
    "Description: Experimental software lock-screen PIN for iOS 16.5.1 rootless\n"
    f"Date: {format_datetime(datetime.now(timezone.utc), usegmt=True)}\n"
)
for label, algorithm in (("MD5Sum", "md5"), ("SHA256", "sha256")):
    release += f"{label}:\n"
    for name in ("Packages", "Packages.gz", "Packages.bz2"):
        data = (site / name).read_bytes()
        digest = hashlib.new(algorithm, data, usedforsecurity=False).hexdigest()
        release += f" {digest} {len(data)} {name}\n"
(site / "Release").write_text(release)
print(f"Built Sileo source for {metadata['Version']}: {filename}")
