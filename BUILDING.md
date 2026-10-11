# Building Fakepass Reborn

The release is a rootless `iphoneos-arm64` Debian package containing modern-ABI `arm64e` binaries. Building successfully does not establish device compatibility.

## Tested environment

- macOS, Xcode 27.0 (`27A266a`), GNU Make 4.4.1, dpkg 1.23.11 and ldid 2.1.5.
- [Theos](https://github.com/theos/theos) commit `304e0799973e8145f32e4ca2de6c747a84b758ce`, with submodules initialized.
- Patched `iPhoneOS16.5.sdk` from [theos/sdks](https://github.com/theos/sdks), commit `0222fd5413cf4b9af096f37b4621afa2688572f7`, installed in `$THEOS/sdks/iPhoneOS16.5.sdk`.
- `libSandy.h` from [opa334/libSandy](https://github.com/opa334/libSandy), commit `9c77311172485e92bf0c439391be5a9565c877e4`, installed in `$THEOS/include/libSandy.h`.
- Rootless `libsandy.dylib` from the official `com.opa334.libsandy_1.1.6-4_iphoneos-arm64.deb`, installed in `$THEOS/lib/iphone/rootless/libsandy.dylib`.

Use [Theos's installation guide](https://theos.dev/docs/installation) to set up the tools. Select a full Xcode installation using `DEVELOPER_DIR`; Command Line Tools alone are not the tested iOS compiler setup. Follow [Theos's rootless guidance](https://theos.dev/docs/rootless) when changing the build environment.

The official libSandy package is available at:

```text
https://opa334.github.io/debs/com.opa334.libsandy_1.1.6-4_iphoneos-arm64.deb
SHA256: 568c98650d8b452d68a1f893ec87f02a4f7082848b1abeec80531c4c9d484065
```

After verifying that checksum, extract the Debian archive with `dpkg-deb -x`. Its library is at `var/jb/usr/lib/libsandy.dylib`. The release does not redistribute libSandy.

## Compile and test

From this project's directory, after setting `THEOS` to your installation:

```sh
export DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer
python3 tests/check_hash.py
python3 tests/check_passcode_changes.py
python3 tests/check_removal.py
gmake clean package FINALPACKAGE=1
```

The Makefiles default to rootless packaging, arm64e, SDK 16.5 and a deployment target of 16.5. Keep the package's exact `firmware (= 16.5.1)` dependency unless testing establishes support for another version.

The package is written to `packages/com.skfallin.fakepassreborn_0.1.0~beta2_iphoneos-arm64.deb`. The hash test compiles the actual hash/salt functions and compares their output with SHA-512 reference values; it checks wrong-PIN separation, nil inputs and salt format. The passcode-change test runs the actual hook with in-memory preferences, checking that an existing PIN cannot be removed or replaced without the correct old PIN. The removal test substitutes harmless commands to verify both preference paths are cleared on removal and preserved during an upgrade. These tests do not test iOS hooks or prove lock-screen security.

## Package checks

Before publishing:

```sh
dpkg-deb --info packages/*.deb
dpkg-deb --contents packages/*.deb
shasum -a 256 packages/*.deb
git diff --check
```

Extract the package and inspect both `FakePass.dylib` and the `FakePassPrefs` executable with `file` and `otool -L`. They must be arm64e and reference the rootless dependency paths. Check that the package includes the MIT copyright file under `/var/jb/usr/share/doc/com.skfallin.fakepassreborn/`.

Only publish project source and release artifacts. Device preference files, SSH configuration, identifiers, pairing records and unredacted logs must remain local.

## Sileo source

The flat APT source is published from `docs/` on `main` using GitHub Pages at `https://skfallin.github.io/FakepassReborn/`. The source contains this package only. libSandy stays on its author's repository.

After building a new version, use the installed `dpkg-dev` tools and Python's standard library to update the indexes:

```sh
python3 scripts/build_repository.py packages/com.skfallin.fakepassreborn_0.1.0~beta2_iphoneos-arm64.deb
python3 tests/check_repository.py
```

Commit the package under `docs/pool/` and the generated `Packages`, compressed indexes and `Release` together. Upload that same `.deb` to the GitHub release and include its SHA-256 checksum. The Pages source must remain `main` / `docs`; `.nojekyll` keeps the APT files intact. This source uses HTTPS and package/index checksums; it does not include an APT signing key. Verify Sileo refreshes the source before announcing an update.
