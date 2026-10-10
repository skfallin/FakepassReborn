# Changelog

## 0.1.0-beta.1 — 2026-10-10

First public experimental release of the rootless arm64e adaptation of FakePass 0.1.5.

- Modern arm64e build for the tested XS Max / iOS 16.5.1 configuration.
- Fakepass Reborn branding, installation/recovery instructions and explicit compatibility limits.
- Removed sensitive logging, device-erasure code and permanent software lockout.
- Initialization checks and fake grace-period handling.
- Rootless removal cleanup and packaged MIT license.
- Local PIN hashing test.

Basic six-digit PIN behavior and persistence across respring were confirmed on the development prototype on one device. The renamed release package was rebuilt and checked locally; it has not been installed on a device. Face ID, native passcode security and Apple Pay are not provided.
