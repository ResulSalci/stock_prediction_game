# Market Signal

Gercek hisse verisiyle oynanan bir tahmin/trading oyunu. yfinance uzerinden
rastgele bir hissenin rastgele bir gecmis donemini ceker, 60 gunluk grafigi
gosterir, sen yon (long/short) ve pozisyon buyuklugu secersin, sonra gercek
sonraki 30 gun acilir ve kar/zarar hesaplanir.

## Kurulum

    pip install -r requirements.txt

## Calistirma

    python run.py

## Notlar

- Internet baglantisi gereklidir (yfinance canli veri ceker).
- Hisse adi, tahmin yapana kadar gizlenir.
- charts/ klasorune her tur icin grafikler PNG olarak kaydedilir.
- Bu bir oyundur, yatirim tavsiyesi degildir.