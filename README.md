# 🗣️ sesoku / Konuşma ve Ses Algılayıcısı

Bu proje, **Flask** ve **TensorFlow YAMNet** kullanarak **canlı ses analizi** yapar.  
Mikrofon girişini dinleyerek **konuşmayı algılar**, transkribe eder ve **diğer sesleri sınıflandırır**.  
WebSocket üzerinden verileri gerçek zamanlı olarak bir arayüze gönderir.

## 🚀 Özellikler
✅ **Gerçek zamanlı konuşma algılama ve transkripsiyon**  
✅ **Arka planda sürekli dinleme ve sessizlik sonrası transkript gönderme**  
✅ **Müzik, gürültü, sessizlik gibi diğer sesleri de algılama**  
✅ **Flask-SocketIO ile WebSocket üzerinden anlık veri gönderme**  


## 🛠️ Kurulum

**Gereksinimler**
Projeyi çalıştırmadan önce aşağıdaki bağımlılıkları yükleyin.

**Python ve Pip Gereksinimleri**
```bash
sudo apt update && sudo apt install python3 python3-pip -y # (Linux için)
```
FFmpeg Gereksinimi
(Eğer ses kaydı ile ilgili hata alırsanız FFmpeg yükleyin.)
```bash
sudo apt install ffmpeg  # Linux
brew install ffmpeg  # macOS
choco install ffmpeg  # Windows (Chocolatey kullanıyorsanız)
```
### Windows için Kurulum Adımları
## 1️⃣ Gerekli Bağımlılıkları Yükle
Öncelikle, Python ve pip yüklü olduğundan emin olmalısın. Eğer yüklü değilse:

Python'un resmi sitesinden Python 3.9+ sürümünü indir ve yükle.
Yükleme sırasında "Add Python to PATH" kutusunu işaretlediğinden emin ol.
Daha sonra terminalde (PowerShell veya Komut İstemi) şu komutları çalıştır:
```bash
python --version  # Python'un yüklü olduğunu kontrol et
pip --version  # Pip'in yüklü olduğunu kontrol et
```
Eğer pip eksikse:
```bash
python -m ensurepip --default-pip
```
## 2️⃣ FFmpeg Yükle
FFmpeg'in sistemde olup olmadığını kontrol et:
```bash
ffmpeg -version
```
Eğer yoksa Windows için şu komutla yükleyebilirsin (Chocolatey kullanıyorsan):
```bash
choco install ffmpeg
```
Eğer Chocolatey kullanmıyorsan:
FFmpeg'in resmi sitesine git.
Windows sürümünü indir ve sistem PATH'ine ekle.


## 3️⃣ Projeyi Klonla ve Bağımlılıkları Kur
Eğer Git yüklü değilse, önce Git’i buradan indir ve kur.

Sonra PowerShell veya Komut İstemi'nde şu komutları çalıştır:
```bash
git clone https://github.com/singleservingfriend/sesoku.git
cd sesoku
pip install -r requirements.txt
```
Bu, proje dosyalarını indirir ve gerekli kütüphaneleri yükler.

📝 Bağımlılıklar
requirements.txt dosyasında yer alan bağımlılıklar:
```txt
flask==2.2.3
flask-socketio==5.3.3
numpy==1.24.3
tensorflow==2.12.0
tensorflow-hub==0.13.0
requests==2.31.0
sounddevice==0.4.6
speechrecognition==3.8.1
pyaudio==0.2.13
```

4️⃣ Projeyi Çalıştır
Her şey tamamlandıktan sonra şu komutla projeyi başlatabilirsin:

```bash
python app.py
```
Proje çalıştıktan sonra http://localhost:5000 adresinden erişebilirsin. 🎯🔥

###

1️- Proje çalıştırıldığında mikrofon dinlemeye başlar.
2️- Konuşma algılandığında sessizlik bitene kadar bekler.
3️- Konuşma bittikten sonra transkripti ekrana ve web arayüzüne basar.
4️- Diğer ses türleri (gürültü, müzik vs.) için de algılama yapar ve web arayüzüne basar.

🤝 Katkıda Bulunma
Projeye katkıda bulunmak isterseniz:

Fork yapın 🍴
Pull Request gönderin 📌
Sorularınız veya önerileriniz için Issue açabilirsiniz 📝
📜 Lisans
Bu proje MIT lisansı altında yayımlanmıştır.
Detaylar için LICENSE dosyasına bakabilirsiniz.
