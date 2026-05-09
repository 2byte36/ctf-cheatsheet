# Reverse Android APK

## When to suspect this

- Artifact is `.apk`, `.aab`, Android app, mobile challenge.
- Prompt mentions device, app, package, activity, JNI, Firebase, certificate.
- APK contains Java/Kotlin plus native `.so` libraries.

## Fast triage checklist

- Unzip/list APK contents.
- Run jadx for Java/Kotlin.
- Inspect manifest, package, activities, exported components.
- Search strings/resources for flag/key/API endpoints.
- Check native libraries and JNI methods.
- Check assets, Firebase config, shared preferences assumptions.
- If dynamic needed, use emulator/Frida carefully.

## Manual confirmation

```bash
file app.apk
unzip -l app.apk | head -80
jadx -d jadx_out app.apk
rg -n -i 'flag|ctf|secret|key|firebase|api|correct|wrong' jadx_out
apktool d app.apk -o apktool_out
```

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| jadx | Java/Kotlin decompile | `jadx -d out app.apk` | Source-like code |
| apktool | Resources/smali/manifest | `apktool d app.apk` | Manifest/resources |
| `strings` | Native libs/assets | `strings lib.so | rg flag` | Constants |
| Ghidra | Native `.so` reversing | Import `.so` | JNI validation |
| Frida | Runtime hooks | `frida -U -f pkg -l hook.js` | Bypass/dump values |

## Payload starter pack

Search:

```bash
rg -n -i 'flag|ctf|secret|password|token|firebase|base64|xor|native|System.loadLibrary' jadx_out apktool_out
find . -name '*.so' -exec file {} \; -exec strings -a -n 5 {} \; | rg -i 'flag|ctf|secret'
```

Frida hook concept:

```javascript
Java.perform(function() {
  var Cls = Java.use("com.example.Checker");
  Cls.check.implementation = function(s) {
    console.log("check arg:", s);
    var ret = this.check(s);
    console.log("ret:", ret);
    return true;
  };
});
```

## Exploit skeleton

```bash
#!/usr/bin/env bash
set -euo pipefail
APK="${1:?app.apk}"
OUT="${2:-work/apk}"
mkdir -p "$OUT"
unzip -l "$APK" | tee "$OUT/list.txt"
jadx -d "$OUT/jadx" "$APK"
apktool d -f "$APK" -o "$OUT/apktool"
rg -n -i 'flag|ctf|secret|key|correct|wrong|firebase|native|loadLibrary' "$OUT" | tee "$OUT/interesting.txt" || true
find "$OUT" -name '*.so' -exec file {} \; -exec strings -a -n 5 {} \; | tee "$OUT/native_strings.txt"
```

## Escalation path

- If Java validation found, invert logic.
- If native JNI, reverse `.so` and hook `RegisterNatives` or target method.
- If cert hash used as key, compute APK certificate digest.
- If app uses Firebase/cloud API, inspect config and rules in CTF scope.
- If anti-debug/root checks, patch smali or hook methods.

## Common bypasses

- Patch smali return value.
- Hook Java methods with Frida.
- Dump native strings/memory.
- Rebuild APK with modified code.
- Bypass certificate pinning in CTF API challenges.

## Rabbit holes

- Installing app before static search.
- Ignoring native libraries.
- Missing assets/raw resources.
- Assuming Firebase config alone is a vulnerability.
- Fighting emulator setup when jadx reveals answer.

## Final solve checklist

- Manifest/package and validation path identified.
- Java/native split understood.
- Flag or input recovered and locally verified.
- Dynamic hooks documented if used.

