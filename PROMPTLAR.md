# YZ ile Çalışma Günlüğü / Prompt Listesi

Bu bölüm, ödev boyunca kullanılan yapay zekâ destekli çalışma akışını belgelemektedir.

## 1. Prompt

"Küçük işletme kasa defteri için Python komut satırı uygulaması tasarla. En az 3 doğrulamalı girdi, liste/sözlük kullanımı, CSV kaydı ve menü döngüsü olsun."

### YZ yanıtı
Yapay zekâ önerilen menü, veri yapısı ve temel fonksiyonları verdi.

### Karar
İlk tasarım kabul edildi, ancak fonksiyonların adı ve çıktı biçimi sadeleştirildi.

## 2. Prompt

"Gelir ve gider kaydında tutar, tarih ve kategori için doğrulama ekle. Hatalı girişte program çökmemeli, kullanıcıya açıklayıcı hata mesajı dönsün."

### YZ yanıtı
`ValueError` tabanlı doğrulama örneği önerdi.

### Karar
Bu yaklaşım benimsendi; doğrulama hataları kullanıcıya net şekilde gösterildi.

## 3. Prompt

"Uygulamaya test senaryoları ekle. En az 5 test olsun; iki tanesi hatalı giriş için olacak."

### YZ yanıtı
`unittest` tabanlı test dosyası önerdi.

### Karar
Yapı kabul edildi; geçersiz tutar ve geçersiz işlem türü senaryoları eklendi.

## 4. Prompt

"CSV kaydı için dosya yazma ve okuma fonksiyonlarını ekle. Program program kapandığında verinin kaybolmaması için dosya tutumu olsun."

### YZ yanıtı
`csv.DictWriter` ile yazma, `csv.DictReader` ile okuma örneği verdi.

### Karar
Kayıtların devamlılığını sağlayan yöntem kabul edildi.

## 5. Prompt

"README ve rapor için Türkçe açıklama yaz. Kullanıcı, problem, tasarım, YZ günlüğü ve yansıtma bölümleri olsun."

### YZ yanıtı
Ödev için gerekli belge yapısını ve bölümleri verdi.

### Karar
Yapının sonunda hazır rapor ve açıklama dosyaları oluşturuldu.

## YZ hatası yakalama örneği

Bir aşamada YZ, menü seçimlerinde tüm işlemleritek bir fonksiyonda toplamak istemişti. Bu, kodun okunabilirliğini ve hata ayıklamayı zorlaştırıyordu. Bu yüzden tek bir büyük fonksiyon yerine ayrı fonksiyonlar kullanma kararı alındı. Gerçekten gerekli açıklayıcı ayrım, hata kontrolünde ve yeniden kullanılabilirlikte daha güçlü bir sonuç verdi.

## Kısa not

Yapay zekâ, kod iskeleti ve hata çözümünde güçlü bir yardımcı oldu; ancak her öneri test edilerek, her satır anlaşılarak dahil edildi. Bu sayede kodun doğruluğundan ve çalışma garantisinden ben sorumlu oldum.
