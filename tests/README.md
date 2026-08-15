# Test Rehberi

Bu dizin, mehmet projesinin kalite güvencesini sağlar. Testler standart
kütüphane olan `unittest` ile yazılmıştır — ekstra bağımlılık gerekmez.

## Çalıştırma

Proje kök dizininden:

```bash
python3 -m unittest discover -s tests -t . -v
```

## Test Dosyaları

- `test_maturity.py` — `scripts/maturity.py` skorlama motorunun saf
  fonksiyonlarını sentetik repo'lar üzerinde doğrular (sıfır skor, tam skor,
  syntax hatası, geçmiş kaydı, kaçış-hazır eşiği).
- `test_docs.py` — gerçek reponun AGENTS.md simülasyon kurallarına
  uyduğunu doğrular (CHANGELOG, README, PERSONALITY, lisans, workflow).