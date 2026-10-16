# Dopamine Test build 4

Experimental companion app for Fakepass Reborn's tested **XS Max / iOS 16.5.1 / pwnerblu Dopamine 3.0.9-fix** configuration. It repairs the Hide/Show sequence so tweak injection can return after a respring. It does not provide a PIN while the jailbreak is hidden.

[Release and downloads](https://github.com/skfallin/FakepassReborn/releases/tag/dopamine-test-build4) · [Installation: English and Italian](https://github.com/skfallin/FakepassReborn/blob/main/README.md)

## Source and changes

- Base repository: [pwnerblu/Dopamine](https://github.com/pwnerblu/Dopamine), tag `3.0.9-fix`.
- Base commit: [`01a1d49b59b81c7ae48cba08759abcaabd2d947a`](https://github.com/pwnerblu/Dopamine/commit/01a1d49b59b81c7ae48cba08759abcaabd2d947a).
- [Source patch and regression test](Dopamine-HideRestore-test4.patch).
- Original [MIT license](LICENSE.md), copyright Lars Fröder / opa334; this is an unofficial modification, not an endorsed Dopamine release.

The patch changes `DOEnvironmentManager.m` and `.h`, `DOSettingsController.m`, and `main.m`, and adds `tests/check_hide_restore.py` to the upstream tree.

Before changing visibility, it checks `CS_PLATFORM_BINARY`. If needed, it calls the existing `jbclient_process_checkin` and checks the flag again. The unmodified jailbreak service recognizes Dopamine and grants that permission. Failure stops the operation before unregistering apps or unmounting injection.

Mount/protection commands run outside the outer temporary root/sandbox blocks, respecting jbctl's wait handshake. The method checks command failures, link changes and mount state. The 3.0.9 binary's void enable/disable RPC handler echoes its input flag, so a positive enable result is accepted. Show can retry a partial restore with an already-visible `/var/jb`; the UI offers **Retry restore** on error and resprings after success.

## Apply and test the patch

Save the patch from this directory, clone the base, and apply it from that exact revision:

```sh
git clone --branch 3.0.9-fix https://github.com/pwnerblu/Dopamine.git Dopamine-HideRestore
cd Dopamine-HideRestore
git checkout --detach 01a1d49b59b81c7ae48cba08759abcaabd2d947a
git apply --check /path/to/Dopamine-HideRestore-test4.patch
git apply /path/to/Dopamine-HideRestore-test4.patch
DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer python3 tests/check_hide_restore.py
git diff --check
```

The test extracts and compiles the actual Objective-C method on macOS, with mocked device operations. It covers repeated relaunches without platform permission, unsuccessful check-in, mount/link/permission errors and retrying a partial restore. The new repeated-cycle case fails against the previous build 3 method and passes with build 4. It does not simulate the kernel or certify device security.

## Binary provenance

The published TIPA is the same file installed and tested on the development phone:

```text
fa2158df0eaa877a532086db15f518c26e760357c1578fe0fbf1093702667d3f  Dopamine-HideRestore-test4.tipa
```

The app was compiled with Xcode 27 / iOS SDK 27 and deployment target iOS 15. Pre-existing SDK compatibility errors in weightBufs were avoided by linking the original release frameworks through a local Xcode project. The original full-fork build with that SDK was not verified to succeed; byte-for-byte reproducible builds are not claimed.

Frameworks, runtime libraries, package/bootstrap resources, basebin and trustcache were preserved byte for byte from [the original 3.0.9-fix release](https://github.com/pwnerblu/Dopamine/releases/tag/3.0.9-fix). Its original `Dopamine.tipa` SHA-256 is `fed68f89f7b5d7195486d06e6a7d86e28f09c666d956e5826d135abc9a1e2e01`. Bundled licenses were retained.

Packaging sets the display name to **Dopamine Test** and `CFBundleVersion` to **4**; the identifier stays `com.opa334.Dopamine`, and the environment version stays **3.0.9**. The executable was stripped of debug information, signed ad hoc, and passed `codesign --verify --deep --strict` before TrollStore installation. Entitlements match the original fork, including `com.apple.private.security.no-sandbox = false`. TrollStore applies its own installation/signing step.

The release's `SHA256SUMS` covers the TIPA, source patch and license. On macOS, check downloads in one directory with `shasum -a 256 -c SHA256SUMS`.

## Validation and limits

On **16 October 2026**, the user confirmed three consecutive Hide/Show cycles, reopening Dopamine after each respring: FakePass returned in Settings, one wrong PIN was rejected and the current PIN unlocked. The phone used the corrected private FakePass prototype; the public rebranded package was not newly installed for this test.

The final Mac check confirmed `/var/jb`, the injection mount, unchanged native/rootless FakePass preferences and the same launchd start time as before the test. No complete device reboot was needed. PIN/hash/salt values, identifiers, SSH settings and device logs are not distributed.

Other devices, firmware, jailbreak versions and long-term stability have not been validated. Hidden jailbreak, Safe Mode or disabled injection bypasses the software lock. This app does not restore the native iOS passcode, Face ID or Apple Pay.

The Fakepass Reborn Debian package and Sileo indexes remain at **0.1.0~beta2**. Install this companion with TrollStore using the main README; it is not a Sileo package.
