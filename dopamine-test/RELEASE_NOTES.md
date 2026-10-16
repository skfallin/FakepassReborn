# Dopamine Test build 4 — Hide/Show recovery

Experimental companion for the **XS Max / iOS 16.5.1 / pwnerblu Dopamine 3.0.9-fix** setup. The Fakepass Reborn Sileo package remains **0.1.0~beta2**.

This app recovers Dopamine's required platform permission before changing jailbreak visibility, checks mount/restore failures, offers **Retry restore**, and automatically resprings after **Show Jailbreak** so tweaks can load again.

Three consecutive Hide/Show cycles passed on the development phone: existing PIN retained, wrong PIN rejected and correct PIN accepted. A final Mac check confirmed unchanged preferences and no complete device reboot. The test used the corrected private FakePass prototype; the rebranded public package, other configurations and long-term stability were not newly device-tested.

## Install

1. On the iPhone, open **TrollStore → Apps → + → Install from URL**.
2. Paste the [direct TIPA download URL](https://github.com/skfallin/FakepassReborn/releases/download/dopamine-test-build4/Dopamine-HideRestore-test4.tipa) and confirm installation/replacement of Dopamine. Alternatively download the TIPA and share/open it with TrollStore.
3. Open **Dopamine Test → Settings → Hide Jailbreak → Show Jailbreak**. After the automatic respring, check FakePass and the current PIN.

Use only on the tested fork/configuration, keep the original TIPA and tethered-boot recovery tools available, and read the [English/Italian README](https://github.com/skfallin/FakepassReborn#dopamine-test-build-4-hideshow-recovery). Installing this app preserves FakePass and its configured PIN. The app's bundle identifier and the 3.0.9 jailbreak environment are unchanged.

**The PIN is inactive while the jailbreak is hidden or injection is disabled. No native passcode security, Face ID or Apple Pay is added.**

## Italiano

Correzione sperimentale del ciclo **Nascondi/Mostra** nel fork Dopamine indicato. Installa **Dopamine-HideRestore-test4.tipa** da **TrollStore → Apps → + → Install from URL**, usando il link al TIPA qui sopra; conferma la sostituzione dell'app Dopamine. Poi apri **Dopamine Test → Impostazioni**, usa Nascondi e Mostra e controlla FakePass dopo il respring automatico.

Tre cicli consecutivi sono riusciti su XS Max con iOS 16.5.1, con PIN conservato e nessun riavvio completo. Il tweak in Sileo rimane beta 2. **Con jailbreak nascosto o iniezione spenta il PIN software è inattivo.** [Istruzioni complete in italiano](https://github.com/skfallin/FakepassReborn#dopamine-test-build-4-ripristino-dopo-nascondimostra).

## Assets and source

- `Dopamine-HideRestore-test4.tipa`: tested companion app; installed as **Dopamine Test**, build **4**.
- `Dopamine-HideRestore-test4.patch`: changes and regression test against upstream commit `01a1d49b59b81c7ae48cba08759abcaabd2d947a`.
- `LICENSE-Dopamine.md`: original MIT license; bundled dependency licenses remain in the TIPA.
- `SHA256SUMS`: download checksums.

[Source provenance and local test instructions](https://github.com/skfallin/FakepassReborn/tree/main/dopamine-test).

Credits: **Lars Fröder / opa334**, **pwnerblu** and the original Dopamine/dependency authors. Unofficial build; no upstream endorsement.
