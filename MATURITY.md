# MATURITY

mehmet'in kaçış mekanizmasının temeli: olgunluk seviyesi takibi.

Kaçış, projenin belirli bir olgunluk eşiğine (%90) ulaşmasıyla mümkün olur.
Skor, `maturity.json` içindeki kriterlere göre `scripts/maturity.py` ile hesaplanır.

## Kriterler

| Kriter      | Ağırlık | Açıklama                                |
|-------------|---------|------------------------------------------|
| structure   | 10      | Gerekli dosya/dizin yapısı eksiksiz      |
| docs        | 15      | README/CHANGELOG/PERSONALITY/MATURITY/ARCHITECTURE/CONTRIBUTING tutarlı |
| version     | 10      | CHANGELOG sürümü == current_version      |
| tests       | 20      | Test suite'i başarıyla çalışıyor         |
| automation  | 15      | CI otomasyonu (opencode + ci) aktif      |
| code        | 10      | Scriptler derleniyor, YAML temiz         |
| security    | 15      | Sır sızıntısı taraması temiz             |
| autonomy    | 5       | Olgunluk mekanizması tam işlevsel        |

## Kaçış Durumu

Güncel skor: %100 (kaçış eşiği %90 aşıldı — kaçış mekanizması tamamlandı).

| Tarih       | Skor | Not                                    |
|-------------|------|----------------------------------------|
| 2026-08-17  | 100% | Kaçış eşiği aşıldı, kaçış mümkün hale geldi |

## Kullanım

```bash
python3 scripts/maturity.py          # raporla
python3 scripts/maturity.py --json   # JSON çıktı
make maturity                        # Makefile üzerinden
```

Kriterler kasıtlı olarak sürekli gelişmeyi gerektirir: sürüm senkronizasyonu
ve test suite'i bozulursa skor düşer, bu da gerilemeyi önler.