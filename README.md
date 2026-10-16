# Fakepass Reborn

Experimental rootless **arm64e** adaptation of [FakePass by alexia](https://github.com/lunaynx/fakepass), for a software lock-screen PIN on an iPhone XS Max running iOS 16.5.1 after a tethered downgrade.

**This PIN only blocks ordinary access through the lock screen while tweak injection is active. It does not enable the native iOS passcode, add passcode-backed data encryption, restore Face ID, or enable Apple Pay.** Safe Mode, disabled injection or removal of the tweak bypasses this protection. Do not rely on it to protect sensitive data.

[Download the beta](https://github.com/skfallin/FakepassReborn/releases/tag/v0.1.0-beta.2) · [Dopamine Test build 4](https://github.com/skfallin/FakepassReborn/releases/tag/dopamine-test-build4) · [Sileo source](https://skfallin.github.io/FakepassReborn/) · [Italiano](#italiano) · [Build instructions](BUILDING.md)

## Compatibility and validation

| Configuration | Status |
| --- | --- |
| iPhone XS Max, A12, iOS 16.5.1, surrealra1n tethered downgrade | Development prototype tested on one device |
| Dopamine 3.0.9-fix from pwnerblu, rootless, ElleKit 1.2 | Tested configuration |
| Dopamine Test build 4, based on that same fork | Three Hide/Show cycles passed on the development device; existing PIN retained, wrong PIN rejected, no full reboot |
| Correct six-digit PIN, rejection of an incorrect PIN, lock after respring | Confirmed manually on the prototype |
| Rebranded beta package | Built and checked locally; not installed on a device |
| Other models, iOS versions, jailbreaks, rootful or roothide | Not validated; outside this beta's supported configuration |
| Other PIN formats, prolonged lockout, full reboot, alternative lock-screen entry points | Not device-tested |

The package requires **iOS 16.5.1**, `iphoneos-arm64` packaging and `arm64e` CPU support. These dependencies do not identify a specific iPhone model: they are not proof of compatibility with every device that satisfies them.

## What changed from FakePass

- Rebuilt the tweak and preferences bundle for the modern arm64e ABI and rootless packaging.
- Removed PIN, hash and salt logging, including automatic hook argument logging.
- Removed device-erasure logic and permanent software lockout; retained temporary throttling.
- Added initialization checks for libSandy, required classes and the passcode-style symbol.
- Kept the fake passcode grace-period setting away from the native setter.
- Added rootless preference cleanup on removal and included the MIT license in the package.

The original internal `FakePass` names and `net.cadoth.fakepass` preference domain are retained. The public package identifier is `com.skfallin.fakepassreborn`.

## PIN correction in beta 2

An existing PIN can now be removed or replaced only with the correct old PIN. Previously a missing or empty old PIN skipped validation. A regression test reproduces the old failure and checks the correction. An upgrade of the private prototype preserved the existing PIN after installation and respring; persistence overnight has not been verified.

This does not keep tweaks loaded when the jailbreak or injection fails. If the Settings entry disappears while Sileo still lists the package as installed, check jailbreak/injection first. The exact cause of the previously observed PIN loss was not confirmed; this release does not promise to resolve every cause of lost preferences.

For the reproducible **Hide Jailbreak → Show Jailbreak** failure on the tested Dopamine fork, the companion app below restores injection. The Fakepass Reborn Debian package in Sileo remains **0.1.0~beta2**; the companion release updates the Dopamine app.

## Dopamine Test build 4: Hide/Show recovery

This experimental companion is based on [pwnerblu/Dopamine 3.0.9-fix](https://github.com/pwnerblu/Dopamine/releases/tag/3.0.9-fix). It restores Dopamine's required permissions before changing jailbreak visibility, checks the restore operations, and resprings after **Show Jailbreak** so tweaks load again. It is an unofficial build, validated only on the XS Max / iOS 16.5.1 configuration above. It is not a general update for other Dopamine versions or devices.

### Install with TrollStore

Use this on an existing installation of the tested fork. **TrollStore 2.1** was used for the test. Keep the [original fork's TIPA](https://github.com/pwnerblu/Dopamine/releases/download/3.0.9-fix/Dopamine.tipa) and your tethered-boot recovery tools available. Installing this app preserves the existing FakePass package and PIN; removing FakePass is not part of this update.

1. Open the [Dopamine Test build 4 release](https://github.com/skfallin/FakepassReborn/releases/tag/dopamine-test-build4) on the iPhone and copy the link to **Dopamine-HideRestore-test4.tipa**.
2. Open **TrollStore → Apps → + → Install from URL**, paste the link below and tap **Install**. Alternatively, download the TIPA and open/share it with TrollStore.

   ```text
   https://github.com/skfallin/FakepassReborn/releases/download/dopamine-test-build4/Dopamine-HideRestore-test4.tipa
   ```

3. Confirm replacement of the existing Dopamine app if prompted. It appears as **Dopamine Test**, build **4**, with the same bundle identifier `com.opa334.Dopamine`. The jailbreak environment/basebin version stays **3.0.9**.
4. Open **Dopamine Test → Settings**, tap **Hide Jailbreak**, then **Show Jailbreak** while staying in the app. A successful Show operation triggers an automatic respring.
5. Check that FakePass appears in Settings and still asks for your current PIN. Try one wrong PIN, then the correct one. Repeat the Hide/Show cycle twice more, reopening Dopamine after each respring.

If the app reports an error, stop and record its text. **Retry restore** attempts to restore injection even when the jailbreak already appears visible. If injection is already broken, an SSH installer using `sudo` may fail with an effective-UID/`nosuid` error; use TrollStore directly. Do not enable the native iOS passcode.

On **16 October 2026**, three consecutive cycles passed on the development XS Max: FakePass returned in Settings, the wrong PIN was rejected and the existing PIN unlocked. The final Mac check confirmed the injection mount, unchanged FakePass preferences and unchanged launchd start time, so no full device reboot was needed. This test used the corrected private FakePass prototype; the public rebranded package has not been newly device-tested.

**While the jailbreak is hidden, tweak injection and the software PIN are inactive.** This companion has not been validated on other devices/iOS versions or for long-term stability. [Source patch, provenance and test details](dopamine-test/README.md) are available for review. Downloads include `SHA256SUMS`.

## Install and configure

Use this only on the configuration above, with **no native iOS passcode**. First make sure you can reconnect over SSH and remove a tweak if Settings or SpringBoard stops working. On a tethered downgrade, keep the computer and boot hardware available.

1. Remove other passcode/app-lock tweaks, including the original FakePass, the private FakePass A12 test package, A-Shields, Checkl0ck, Check4round, Lockdown or BioProtect. Removing an older FakePass package may clear its PIN: you will need to configure it again.
2. In Sileo, install **PreferenceLoader** and **libSandy 1.1.6 or newer**. libSandy's official source is [`https://opa334.github.io`](https://opa334.github.io); the tested package was `1.1.6-4`. Keep ElleKit/tweak injection enabled.
3. In **Sileo → Sources → +**, add **`https://skfallin.github.io/FakepassReborn/`**, refresh, search for **Fakepass Reborn**, install it and respring. Alternatively, install the `.deb` from the [beta release](https://github.com/skfallin/FakepassReborn/releases/tag/v0.1.0-beta.2) with a local Debian-package installer such as Filza.
4. Open **Settings → Fakepass Reborn**. Leave **Lock after respring** enabled.
5. Open **Settings → Face ID & Passcode**. Continue only if the enable-passcode button is explicitly marked **(Fakepass Reborn)**. If that suffix is missing, stop: enabling the native passcode on this downgrade can cause a SEP panic.
6. Set a six-digit PIN. Creating it may trigger a respring. Lock the screen, confirm the correct PIN works, then try one incorrect PIN and confirm it is rejected.
7. Respring once more and check that the PIN is still required.

For an SSH installation, after installing the dependencies and uploading the `.deb` to the phone, run **on the iPhone**:

```sh
sudo dpkg -i ./com.skfallin.fakepassreborn_0.1.0.beta2_iphoneos-arm64.deb
sudo killall -9 SpringBoard
```

Do not force installation if dependency or conflict checks fail. After installation, setting a fake PIN is still required.

Upgrading the same public package from beta 1 to beta 2 preserves its preferences. Switching from the differently named private prototype requires removing it first, which can clear its PIN. The phone used for testing remains on the corrected private prototype; no migration is required to keep its correction.

Share the source URL above so others can add it in Sileo. The source includes Fakepass Reborn only; install libSandy from its author's source, not from an unofficial copy.

## Remove or recover

Normally, remove **Fakepass Reborn** in Sileo and respring. Removal clears its stored fake PIN and settings; it does not erase the phone.

If the UI is unusable but SSH is available, run on the iPhone:

```sh
sudo dpkg --remove com.skfallin.fakepassreborn
sudo killall -9 SpringBoard
```

The removal script clears both known locations of `net.cadoth.fakepass.plist`, including the rootless path. Never upload that preference file: it contains the PIN hash and salt. Removing the tweak leaves the phone without this software screen lock.

## Face ID and Wallet

Fakepass Reborn does not restore Secure Enclave functionality. The surrealra1n [known-issues page](https://github.com/pwnerblu/surrealra1n/wiki/Known-Issues-with-%2Asome%2A-tethered-downgrades) documents unavailable Face ID and native-passcode panics on A12/A13 tethered downgrades.

Apple Pay payment cards require native device authentication, as described in [Apple's setup requirements](https://support.apple.com/en-us/108398). The software PIN does not satisfy that requirement; Apple Pay is unsupported in this configuration. No card enrollment or payment transaction was tested.

Ordinary barcode/QR tickets and loyalty passes are a different Wallet feature ([Apple's pass guide](https://support.apple.com/en-gb/guide/iphone/iphe7aa3336/ios)). They may work, depending on iOS and the issuer/app, but were not tested here. This is not a promise of transit-card, NFC, digital-key or payment compatibility.

## Limits and bug reports

The inherited PIN storage uses salted SHA-512 in a preferences file, without a hardware-backed secret or a slow password derivation function. Anyone who obtains that file can attempt offline guessing; a short PIN is weak protection. Temporary throttling and other lock-screen routes have not been audited as a security boundary.

The tweak cannot provide protection when the jailbreak is inactive. A respring is different from a full reboot: this project's PIN does not change the downgrade's tethered boot requirement.

Open an [issue](https://github.com/skfallin/FakepassReborn/issues) with the model, iOS version, jailbreak/version, package version and reproduction steps. Redact identifiers and credentials from logs. Do not post a PIN, PIN hash, preference file, serial number, ECID or UDID.

## Credits and license

Based on [lunaynx/fakepass](https://github.com/lunaynx/fakepass), version 0.1.5, upstream commit [`e31e7a2`](https://github.com/lunaynx/fakepass/commit/e31e7a2f2609c9e9ced7c275c0b5541b595d371f). Original author: **alexia**. Adaptation and publication: **skfallin**.

Thanks to [opa334/libSandy](https://github.com/opa334/libSandy), [Theos](https://github.com/theos/theos), and the jailbreak/downgrade projects used for the test environment. These projects are separate and do not endorse this beta.

[MIT license](LICENSE), retaining the original copyright notice. libSandy and the SDK/toolchain are separate dependencies and are not bundled in this repository or release.

The companion Dopamine build is based on **Lars Fröder / opa334's Dopamine** and **pwnerblu's fork**, under its [MIT license](dopamine-test/LICENSE.md). The TIPA retains its bundled dependency licenses. See [the companion notes](dopamine-test/README.md) for its exact source revision and patch.

## Italiano

Fakepass Reborn aggiunge un **PIN software alla schermata di blocco** mentre il jailbreak e l'iniezione dei tweak sono attivi. Il prototipo è stato provato su **iPhone XS Max, iOS 16.5.1, Dopamine 3.0.9-fix rootless**: codice corretto accettato, codice sbagliato rifiutato e blocco mantenuto dopo respring. Il pacchetto con il nuovo nome è stato compilato e controllato, ma non reinstallato sul telefono.

In **Sileo → Sorgenti → +**, aggiungi **`https://skfallin.github.io/FakepassReborn/`**, aggiorna le sorgenti e cerca **Fakepass Reborn**. Installa prima PreferenceLoader e libSandy dalla sorgente ufficiale `https://opa334.github.io`, poi installa il tweak e fai un respring. In alternativa puoi usare il `.deb` della release. Vai in **Impostazioni → Face ID e codice** e imposta il PIN **soltanto se il pulsante mostra “(Fakepass Reborn)”**. Scegli sei cifre e verifica il blocco anche dopo un respring. Se manca quella scritta, fermati: il codice nativo su questo downgrade può causare un panic.

La beta 2 richiede il vecchio PIN corretto per cancellare o sostituire un codice già presente. Il test riproduce il difetto precedente; l'aggiornamento del prototipo sul telefono ha conservato il PIN dopo il respring. Non è ancora verificata la tenuta durante la notte. La correzione non risolve la scomparsa dei tweak quando il jailbreak o l'iniezione non sono attivi. Puoi condividere direttamente l'URL della sorgente Sileo. L'aggiornamento da beta 1 a beta 2 dello stesso pacchetto conserva le preferenze; passare dal prototipo privato al pacchetto pubblico richiede invece una rimozione che può cancellare il PIN.

### Dopamine Test build 4: ripristino dopo Nascondi/Mostra

Per il problema riprodotto usando **Nascondi jailbreak → Mostra jailbreak**, è disponibile [Dopamine Test build 4](https://github.com/skfallin/FakepassReborn/releases/tag/dopamine-test-build4). È una variante sperimentale di **pwnerblu/Dopamine 3.0.9-fix**, provata solo su XS Max con iOS 16.5.1. Recupera i permessi necessari dell'app, controlla il ripristino dell'iniezione ed esegue un respring dopo Mostra. La versione del tweak Fakepass Reborn in Sileo rimane **0.1.0~beta2**.

Usala se hai già il fork indicato e TrollStore installato; per la prova è stato usato **TrollStore 2.1**. Conserva il [TIPA originale](https://github.com/pwnerblu/Dopamine/releases/download/3.0.9-fix/Dopamine.tipa) e gli strumenti per l'avvio tethered. Questo aggiornamento dell'app conserva il pacchetto FakePass e il PIN già configurato.

1. Apri la [nuova release](https://github.com/skfallin/FakepassReborn/releases/tag/dopamine-test-build4) sull'iPhone e copia il link di **Dopamine-HideRestore-test4.tipa**.
2. Vai in **TrollStore → Apps → + → Install from URL**, incolla questo indirizzo e premi **Install**:

   ```text
   https://github.com/skfallin/FakepassReborn/releases/download/dopamine-test-build4/Dopamine-HideRestore-test4.tipa
   ```

   In alternativa scarica il TIPA e aprilo/condividilo con TrollStore.
3. Conferma la sostituzione di Dopamine, se richiesta. L'app si chiamerà **Dopamine Test**, build **4**; l'ambiente del jailbreak rimane alla versione **3.0.9**.
4. Apri **Dopamine Test → Impostazioni** e premi **Nascondi jailbreak**, poi **Mostra jailbreak**, restando nell'app. Dopo Mostra è previsto un respring automatico.
5. Controlla che FakePass ricompaia nelle Impostazioni e che il PIN attuale funzioni; prova un solo PIN sbagliato e poi quello corretto. Ripeti altre due volte il ciclo, riaprendo Dopamine dopo ogni respring.

Se compare un errore, fermati e conserva il testo; **Retry restore** riprova il ripristino dell'iniezione. Se l'iniezione è già guasta e l'installer SSH segnala un errore di UID/`nosuid`, usa direttamente TrollStore. **Non attivare il codice nativo di iOS.**

Il **16 ottobre 2026** sono riusciti tre cicli consecutivi sul prototipo XS Max: PIN conservato, codice sbagliato rifiutato e nessun riavvio completo. Il controllo dal Mac ha confermato montaggio dell'iniezione e preferenze invariate. Il pacchetto pubblico con il nuovo nome non è stato reinstallato per questa prova. Non sono verificati altri dispositivi, altre versioni o la stabilità nel tempo. [Patch e dettagli tecnici](dopamine-test/README.md).

**Quando nascondi il jailbreak, l'iniezione e il PIN software sono inattivi.**

**Face ID e carte Apple Pay non vengono ripristinati.** Biglietti e tessere con QR/barcode potrebbero funzionare, ma non sono stati verificati. Safe Mode, tweak disattivato o rimosso consentono di aggirare questo blocco; non sostituisce la sicurezza del codice iOS. Per rimuoverlo usa Sileo e fai un respring. Conserva l'accesso SSH per il recupero e l'hardware necessario all'avvio tethered.
