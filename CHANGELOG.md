# Changelog

## Dopamine Test build 4 — 2026-10-16

Companion app release tagged `dopamine-test-build4`, based on pwnerblu/Dopamine `3.0.9-fix` at `01a1d49b59b81c7ae48cba08759abcaabd2d947a`. The Fakepass Reborn Debian package remains `0.1.0~beta2`.

- Restore and verify Dopamine's platform permission before changing jailbreak visibility, including after relaunch without systemhook.
- Run mount/protection helpers after the app's temporary credentials have been restored; check command results, mount state and the `/var/jb` link.
- Offer Retry restore on error and respring after a successful Show operation to reload tweaks.
- Publish the tested TIPA, source patch, regression test, upstream license and checksums; add English and Italian TrollStore installation instructions.
- Three consecutive Hide/Show cycles passed on one XS Max / iOS 16.5.1 development device using the corrected private FakePass prototype. Wrong PIN rejected, current PIN accepted, preferences preserved and no full reboot confirmed. The public rebranded package, other configurations and long-term stability were not newly device-tested.

The software PIN remains inactive while the jailbreak is hidden or injection is disabled.

## 0.1.0-beta.2 — 2026-10-11

- Require the correct old PIN for every change to an existing fake PIN, including removal. Previously a missing or empty old PIN bypassed validation.
- Add a regression test covering PIN creation, unauthenticated removal/replacement, and authenticated change/removal. An upgrade of the private prototype preserved the existing PIN across its installation and respring on the development device on 2026-10-11; the rebranded package and persistence overnight have not been device-tested.
- Add a Sileo package source hosted on GitHub Pages, with package indexes and checksums.

This change prevents unauthenticated PIN changes; it does not fix jailbreak/tweak-injection failures. The precise cause of the earlier overnight PIN loss was not confirmed.

## 0.1.0-beta.1 — 2026-10-10

First public experimental release of the rootless arm64e adaptation of FakePass 0.1.5.

- Modern arm64e build for the tested XS Max / iOS 16.5.1 configuration.
- Fakepass Reborn branding, installation/recovery instructions and explicit compatibility limits.
- Removed sensitive logging, device-erasure code and permanent software lockout.
- Initialization checks and fake grace-period handling.
- Rootless removal cleanup and packaged MIT license.
- Local PIN hashing test.

Basic six-digit PIN behavior and persistence across respring were confirmed on the development prototype on one device. The renamed release package was rebuilt and checked locally; it has not been installed on a device. Face ID, native passcode security and Apple Pay are not provided.
