# Küçük İşletme Kasa Defteri – Süreç Raporu

## 1. Problem ve Kullanıcı

Bu uygulamanın amacı, küçük bir işletmede manuel olarak yapılan gelir-gider takibini daha hızlı ve daha güvenilir hale getirmektir. Küçük işletme sahibi, market, kafe, büro veya serbest çalışma yapan bir kullanıcı, müşteri ödemelerini, faturaları ve günlük harcamaları tek bir ekran üzerinden takip etmek ister. Geleneksel yöntemlerde defter tutmak, her işlemi elle yazmak ve toplamı kontrol etmek zaman alır. Bu proje, kullanıcıya kısa ve sade bir arayüz sunarak günlük finansal akışı görselleştirir.

İşletmenin hedefi, nakit hareketini izlemek, geliri ve gideri ayrıştırmak ve toplam bakiyeyi net bir şekilde takip etmektir. Uygulama, kullanıcıdan bilgileri alır, işlemleri işler ve ekranda biçimlendirilmiş şekilde gösterir. Son adımda kayıtlar CSV dosyasına aktarılır; böylece ileride rapor oluşturmak da kolaylaşır.

## 2. Tasarım ve Akış

Uygulama basit bir menü tabanlı akışla çalışır:

```text
Başlat
  |
  v
Ana menü göster
  |
  +--> Gelir ekle
  |      |
  |      +--> Kategori, açıklama, tutar, tarih al
  |      +--> Geçersiz girdi kontrol et
  |      +--> İşlem listesine ekle
  |
  +--> Gider ekle
  |      |
  |      +--> Kategori, açıklama, tutar, tarih al
  |      +--> Geçersiz girdi kontrol et
  |      +--> İşlem listesine ekle
  |
  +--> Kayıtları göster
  |      +--> Liste tablosunu ekrana yaz
  |
  +--> Bakiye özeti
         +--> Toplam gelir, gider ve bakiyeyi hesapla
         +--> Sonucu ekrana yaz
```

Sözde kod:

```python
transactions = []
while True:
    menuyu_goster()
    secim = input()
    if secim == "1":
        gelir = bilgileri_al()
        transactions.append(gelir)
    elif secim == "2":
        gider = bilgileri_al()
        transactions.append(gider)
    elif secim == "3":
        kayitlari_goster(transactions)
    elif secim == "4":
        bakiye = hesapla(transactions)
        yazdir(bakiye)
    elif secim == "5":
        kaydet_csv(transactions)
    else:
        cikis()
```

## 3. YZ ile Çalışma Günlüğü

### 3.1 Prompt 1

"Küçük işletme için kasa defteri Python uygulaması hazırlayın. Menü, veriler, CSV kaydı ve temel fonksiyonlar olsun."

- YZ önerisi: Menü ve temel veri yapısı verildi.
- Karar: Öneri kabul edildi; fakat döngü ve açıklama bölümleri sadeleştirildi.

### 3.2 Prompt 2

"Doğrulama ekleyin. Hatalı tutar, boş açıklama ve yanlış tarihlerde uygulama çökmemeli."

- YZ önerisi: `ValueError` ile hata denetimi.
- Karar: Kabul edildi; hata mesajları kullanıcı dostu yapıldı.

### 3.3 Prompt 3

"5 test senaryosu yazın. En az iki test hatalı kullanıcı girdisi içersin."

- YZ önerisi: `unittest` testleri.
- Karar: Kabul edildi; hatalı tutar ve geçersiz işlem türü testleri eklendi.

### 3.4 Prompt 4

"CSV dosyası için kaydetme ve yükleme işlevi yazın."

- YZ önerisi: CSV modülüyle dosya okuma/yazma.
- Karar: Kabul edildi ve proje içinde kullanıldı.

### 3.5 Prompt 5

"README, rapor ve YZ günlüğü bölümlerini Türkçe şekilde düzenleyin."

- YZ önerisi: Belge yapısı ve başlıklar önerildi.
- Karar: Kabul edildi; proje için gerekli belgeler hazırlandı.

### YZ hatası yakalama örneği

Yapay zekâ başlangıçta tüm menü ve işleme kodlarını tek bir büyük fonksiyonda toplamayı önerdi. Bu yapı kodu daha az okunur ve daha zor hata ayıklanır hale getiriyordu. Ben, bu öneriyi reddettim ve aynı işlevleri birkaç küçük fonksiyona ayırdım. Bu karar, kodun sürdürülebilirliğini artırdı ve hataları daha kolay fark etmeyi sağladı.

## 4. Test ve Hata Ayıklama

### Test tablosu

| No | Girdi | Beklenen Sonuç | Gerçek Sonuç |
|---|---|---|---|
| 1 | Tutar: 1250,50 | Geçerli gelir tutarı | Başarılı |
| 2 | Tutar: -25 | Hata mesajı göster | Başarılı |
| 3 | Tarih: 15.11.2026 | Tarih kabul edilir | Başarılı |
| 4 | İşlem türü: maaş | "gelir" veya "gider" dışında hata | Başarılı |
| 5 | Gelir + gider listesi | Bakiye 3700 TL | Başarılı |
| 6 | CSV kaydı | Dosya oluşturulur | Başarılı |

### En zor hata

En zor hata, kullanıcıların farklı tarih formatları girmesiydi. Bazıları `2026-11-15` yazarken bazıları `15.11.2026` veya `15/11/2026` formatında giriş yapıyordu. Bu yüzden tarih doğrulama fonksiyonu geliştirildi. Gelen input farklı formatlarda olsa bile kod, tek ve standart bir biçime dönüştürecek şekilde tasarlandı.

## 5. Yansıtma

Bu süreçte en çok önemlisi, yazılım geliştirme sürecinin sadece kod yazmaktan ibaret olmadığını öğrenmem oldu. Önce problemi netleştirdim, ardından uygun veri yapısını seçtim ve ardından girdileri doğrulayan hatalı durumları düşünerek kod yazdım. Bu aşamada algoritma ve karar yapıları çok önemli hale geldi. YZ olmadan temel mantığı kendi başıma kurabilirdim; fakat YZ, fikir üretme, kod yapısı önerme ve hata çözümlerinde büyük bir hız kazandırdı.

Yapay zekâ ile çalışmak, düşünmeyi hızlandırdı ancak her öneriyi olduğu gibi kabul etmedim. Her satırı kontrol ettim, hatalarla yüzleştim ve gerekli düzeltmeleri yaptım. Bu beceri ileride mesleğimde çok işe yarayacak. Özellikle küçük iş akışlarında otomasyon, veri kaydı, iş raporları ve işlem takibi gibi alanlarda bu düşünce yapısı kullanışlı olacak. Kodlamaya dair özgüvenim arttı ve “problemi doğru analiz etme” becerisi daha da güçlendi.

## 6. Öğrenci Yapay Zekâ Kullanım Beyan Formu

- Kullanılan YZ aracı/araçları: Microsoft Copilot
- Kullanma amacı: Kod tasarımı, hata ayıklama, test planı ve belge hazırlama
- Kontrol ve sorumluluk: Yapay zekâ tarafından üretilen içeriği gözden geçirdim, gerekli düzeltmeleri yaptım ve teslim ettiğim çalışmanın doğruluğundan ve akademik dürüstlüğünden sorumluyum.
- Öğrencinin adı-soyadı: Utku Acar
- Tarih ve İmza: 11.11.2026 / Utku Acar

## 7. Atıf

Anthropic. (2026). Claude [Büyük dil modeli]. https://claude.ai

Bu belge, ders kapsamında YZ kullanımını belgelemek için hazırlanmıştır.
