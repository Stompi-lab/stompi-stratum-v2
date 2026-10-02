# Stompi Stratum V2

Öffentlicher Quellcode für Solo-Mining mit Stratum V2 im Stompi-Netzwerk. Die Basis ist die Stratum V2 Reference Implementation (SRI). Die Stompi-Ergänzungen unterstützen STP-Adressen und eine Vardiff-Berechnung anhand der tatsächlich akzeptierten Arbeit.

## Miner verbinden

| Einstellung | V1 | V2 |
| --- | --- | --- |
| Server | `v1.stompi.tech` | `v2.stompi.tech` |
| Port | `3333` | `3334` |
| Benutzer | Eigene STP-Adresse | Eigene STP-Adresse |
| Optional | `STP_ADRESSE.worker` | `STP_ADRESSE.worker` |
| Passwort | `x` | Nach Vorgabe der nativen V2-Oberfläche |

Öffentlicher V2-Pool-Schlüssel:

```text
9bekteT2vX3aA7AvBXVMtCv6dMFoDMZvgb7Yfv95Q3aXgsTRuM9
```

Im Miner Stratum V2 auswählen und den öffentlichen Pool-Schlüssel eintragen. Die Blockbelohnung geht beim Solo-Mining direkt an die angegebene STP-Adresse. Eine gültige Share ist noch kein gefundener Block. Mining-Erträge sind erst nach der vorgeschriebenen Coinbase-Reife ausgebbar.

## Was wurde angepasst?

- STP-Adressen in Auszahlungsskripten und Mining-Benutzernamen.
- Adresse allein oder Adresse mit Worker-Suffix genügt.
- Fehlerhafte STP-Adressen werden abgewiesen.
- Abgelehnte Shares erhöhen nicht die für Vardiff erfasste Arbeit.
- Shares alter Jobs werden mit der Schwierigkeit ihres Jobs gewichtet.
- Konfigurationsgenerator mit Netzwerk-/Adressprüfung und neuen lokalen Pool-Schlüsseln.
- Korrigierter CPU-Patch für den externen Template Provider, einschließlich der erforderlichen Mutex-Deklaration.

Die internen Upstream-Namen bleiben erhalten. Das Repository enthält keine Homepage, Serververwaltung oder produktiven Schlüssel. Die vorhandenen Upstream-Beispielschlüssel sind öffentliche Testdaten und dürfen nicht für einen eigenen öffentlichen Pool verwendet werden.

## Eigener Pool

Die vollständige [Build-Anleitung](docs/BUILD.md) beschreibt Rust 1.88.0, Systempakete, Stompi Core mit IPC, den externen Template Provider und die Generierung einer eigenen Konfiguration. Der Pool wird aus dem Quellcode gebaut; dieses Paket enthält keine fertigen Binärdateien.

Die Konfiguration enthält den privaten Pool-Schlüssel, wird mit Dateirechten 0600 angelegt und gehört nicht auf GitHub. Miner benötigen nur den öffentlichen Pool-Schlüssel. Der Monitoring-Port bleibt lokal.

## Prüfstand

[docs/VALIDATION.md](docs/VALIDATION.md) trennt die auf dem Server ausgeführten Tests, die bestätigten Mining-Blöcke und die lokale Paketprüfung. Die GitHub-CI führt die gezielten Tests und den Pool-Build aus; ihr erster Lauf steht noch aus. Die Netzwerk-Schwierigkeit und das Zehn-Minuten-Ziel werden durch die Stompi-Chain geregelt, nicht durch Vardiff.

Copyright (c) 2026 Stompi für die eigenen Ergänzungen. Bestehende Upstream-Lizenzen und Copyright-Hinweise bleiben erhalten.
