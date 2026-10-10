import os
from pathlib import Path
import subprocess
import tempfile

script = Path(__file__).resolve().parent.parent / "layout/DEBIAN/postrm"
with tempfile.TemporaryDirectory(prefix="fakepass-removal-") as temp:
    temp = Path(temp)
    log = temp / "calls"
    # Intercept every external command so the test cannot delete host files.
    for command in ("rm", "killall"):
        stub = temp / command
        stub.write_text('#!/bin/sh\nprintf "%s\\n" "$0" "$@" >> "$FAKEPASS_TEST_LOG"\n')
        stub.chmod(0o755)
    env = dict(os.environ, PATH=str(temp), CYDIA="", FAKEPASS_TEST_LOG=str(log))
    subprocess.run(["/bin/sh", str(script), "upgrade"], env=env, check=True)
    assert not log.exists(), "An upgrade must preserve the fake PIN"
    subprocess.run(["/bin/sh", str(script), "remove"], env=env, check=True)
    assert log.read_text().splitlines() == [
        str(temp / "rm"), "-f",
        "/var/mobile/Library/Preferences/net.cadoth.fakepass.plist",
        "/var/jb/var/mobile/Library/Preferences/net.cadoth.fakepass.plist",
        str(temp / "killall"), "-9", "cfprefsd",
    ], "Removal must clear only the two preference paths and their cache"
print("Removal and upgrade checks passed")
