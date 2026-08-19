# mehmet — otomasyon komutları

.PHONY: check clean

# Proje sağlığını doğrula ve olgunluk skorunu hesapla
check:
	scripts/healthcheck.sh

# Olgunluk raporunu temizle
clean:
	rm -f docs/maturity.json