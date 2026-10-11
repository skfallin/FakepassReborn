"""Check the generated APT indexes against the bytes clients download."""
import bz2
import gzip
import hashlib
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent.parent
site = root / "docs"
packages = (site / "Packages").read_bytes()
assert gzip.decompress((site / "Packages.gz").read_bytes()) == packages
assert bz2.decompress((site / "Packages.bz2").read_bytes()) == packages
stanzas = packages.decode().strip().split("\n\n")
assert len(stanzas) == 1, "Only Fakepass Reborn belongs in this source"
fields = dict(line.split(": ", 1) for line in stanzas[0].splitlines() if line and not line[0].isspace())
assert fields["Package"] == "com.skfallin.fakepassreborn"
assert fields["Architecture"] == "iphoneos-arm64"
relative = Path(fields["Filename"])
assert not relative.is_absolute() and ".." not in relative.parts
package = site / relative
data = package.read_bytes()
assert int(fields["Size"]) == len(data)
assert fields["SHA256"] == hashlib.sha256(data).hexdigest()
version = subprocess.check_output(["dpkg-deb", "-f", str(package), "Version"], text=True).strip()
assert fields["Version"] == version
release = (site / "Release").read_text()
assert "Architectures: iphoneos-arm64\n" in release
for section, algorithm in (("MD5Sum", "md5"), ("SHA256", "sha256")):
    entries = release.split(f"{section}:\n", 1)[1].splitlines()[:3]
    assert len(entries) == 3
    for entry in entries:
        digest, size, name = entry.split()
        index = (site / name).read_bytes()
        assert int(size) == len(index)
        assert digest == hashlib.new(algorithm, index, usedforsecurity=False).hexdigest()
print("APT source checks passed: compression, architecture, versions and checksums")
