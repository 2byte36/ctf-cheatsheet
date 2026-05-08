# Forensics Operator Playbook

## Mindset

Forensics challenges are evidence reconstruction. Preserve inputs, identify artifact types, extract deterministically, and correlate facts. Unknown executables and scripts are suspicious until proven otherwise.

## Initial Triage

```bash
pwd
find . -maxdepth 3 -type f -printf '%p\t%s bytes\n' | sort | tee notes/inventory.txt
find . -maxdepth 3 -type f -exec file -k {} \; | tee notes/filetypes.txt
find . -maxdepth 3 -type f -exec sha256sum {} \; | tee notes/hashes.txt
mkdir -p work extracts carved logs
```

Fast pivots:

```bash
strings -a -n 6 artifact | rg -i 'flag|ctf|key|token|secret|pass|http|ftp|powershell|cmd\.exe'
exiftool artifact
binwalk artifact
xxd -l 256 artifact
```

## Artifact Routing

| Artifact | Workflow |
|---|---|
| Archive/backup | `7z l`, recursive extraction, password hints, duplicate entries, corrupted headers |
| Disk image | partition table, filesystem metadata, deleted files, snapshots, free space |
| Memory dump | OS profile, processes, command lines, network, file scan, YARA/string scan |
| PCAP | protocol hierarchy, endpoints, streams, objects, DNS labels, TLS keys, covert timing |
| Windows artifact | EVTX, registry, SAM, Recycle Bin, ADS, MFT, USN, PowerShell, Defender |
| Linux artifact | logs, shell history, cron/systemd, SSH, containers, browser profiles |
| Media/stego | metadata, post-EOF, chunks, bitplanes, spectrogram, frame diff, QR/barcode |
| Peripheral/signal | USB HID, Bluetooth, MIDI, UART, I2C, logic analyzer, power/acoustic side channel |
| Malware-like | static strings/imports/resources/config/C2, no direct execution |

## Core Commands

PCAP:

```bash
capinfos capture.pcap
tshark -r capture.pcap -q -z io,phs
tshark -r capture.pcap -Y 'http.request' -T fields -e frame.time -e ip.src -e http.host -e http.request.uri
tshark -r capture.pcap -Y 'dns.qry.name' -T fields -e frame.time_epoch -e ip.src -e dns.qry.name
tshark -r capture.pcap --export-objects http,extracts/
```

Disk:

```bash
mmls image.dd
fls -o OFFSET -r image.dd | tee work/fls.txt
icat -o OFFSET image.dd INODE > extracts/file.bin
tsk_recover -o OFFSET image.dd extracts/recovered
```

Memory:

```bash
vol3 -f memory.dmp windows.info
vol3 -f memory.dmp windows.pslist
vol3 -f memory.dmp windows.cmdline
vol3 -f memory.dmp windows.netscan
vol3 -f memory.dmp windows.filescan | rg -i 'flag|secret|\.txt|\.zip'
vol3 -f memory.dmp windows.yarascan --yara-string 'flag{'
```

Browser:

```bash
sqlite3 History "select datetime(last_visit_time/1000000-11644473600,'unixepoch'),url,title from urls order by last_visit_time desc limit 30;"
```

## Common Indicators

- Magic bytes do not match extension.
- PNG/JPEG/PDF/ZIP has post-EOF overlay.
- PCAP contains long DNS labels, repeated ICMP payloads, unusual timing, or exported files.
- Memory dump contains encrypted file key, process command line, clipboard, browser token, or dumped archive.
- Windows has ADS, suspicious event IDs, PowerShell history, Defender logs, Recycle Bin records.
- Linux has shell history, cron jobs, SSH keys, container layers, browser SQLite databases.
- Media has frame differences, hidden thumbnails, palette/quantization anomalies, spectrogram text, LSB patterns.

## Manual Before Automation

- Look at the artifact structure before bulk carving.
- For PCAPs, inspect protocol hierarchy before following arbitrary streams.
- For disk, map partitions before recovery.
- For memory, identify OS/processes before dumping every file.
- For media, inspect metadata and visual/audio representation first.
- For malware-like files, recover constants and config statically.

## Rabbit Holes

- Carving everything before checking metadata.
- Executing suspicious payloads.
- Treating compressed data as encrypted.
- Missing Office-as-ZIP and DOCX XML paths.
- Ignoring timestamps/usernames/path correlations.
- Forgetting browser local storage and cookies.
- Losing provenance of extracted files.

## Specialized Families

- Disk recovery: ZFS, APFS/BTRFS snapshots, FAT/ext orphan recovery, RAID XOR, VMDK sparse parsing.
- Network covert channels: packet intervals, TCP flags, DNS label bytes, ICMP payload/length/timing.
- Stego: PNG chunk order, JPEG DCT/quant tables, APNG/GIF frames, PDF xref objects, terminal escape art.
- Hardware/signal: VGA/HDMI/DisplayPort, UART/I2C, keyboard acoustic, punched cards, 3D printer G-code.
- Malware: RC4/AES C2, Telegram bot APIs, Poison Ivy/DarkComet/Cobalt Strike patterns, PowerShell/JS obfuscation.

## Source Deep Dives

- Main workflow: [ctf-forensic/SKILL.md](../../ctf-forensic/SKILL.md)
- Disk/memory: [disk-and-memory.md](../../ctf-forensic/ctf-forensics/disk-and-memory.md)
- Disk recovery: [disk-recovery.md](../../ctf-forensic/ctf-forensics/disk-recovery.md)
- Network: [network.md](../../ctf-forensic/ctf-forensics/network.md), [network-advanced.md](../../ctf-forensic/ctf-forensics/network-advanced.md)
- Stego/media: [steganography.md](../../ctf-forensic/ctf-forensics/steganography.md), [stego-image.md](../../ctf-forensic/ctf-forensics/stego-image.md)
- Windows/Linux: [windows.md](../../ctf-forensic/ctf-forensics/windows.md), [linux-forensics.md](../../ctf-forensic/ctf-forensics/linux-forensics.md)
- Signals/peripherals: [signals-and-hardware.md](../../ctf-forensic/ctf-forensics/signals-and-hardware.md), [peripheral-capture.md](../../ctf-forensic/ctf-forensics/peripheral-capture.md)
- Malware-style: [c2-and-protocols.md](../../ctf-forensic/ctf-malware/c2-and-protocols.md)

