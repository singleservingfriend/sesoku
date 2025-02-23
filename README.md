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

### 1️⃣ **Gereksinimler**
Projeyi çalıştırmadan önce aşağıdaki bağımlılıkları yükleyin.

**Python ve Pip Gereksinimleri**
```bash
sudo apt update && sudo apt install python3 python3-pip -y  (Linux için)
```
FFmpeg Gereksinimi
(Eğer ses kaydı ile ilgili hata alırsanız FFmpeg yükleyin.)
```bash
sudo apt install ffmpeg  # Linux
brew install ffmpeg  # macOS
choco install ffmpeg  # Windows (Chocolatey kullanıyorsanız)
```
2️⃣ Bağımlılıkları Kur
Python bağımlılıklarını yükleyin:
```bash
pip install -r requirements.txt
```
3️⃣ Projeyi Çalıştır
Aşağıdaki komutları kullanarak projeyi başlatın:
```bash
python app.py
```
Çalıştırdıktan sonra, aşağıdaki adres üzerinden erişebilirsiniz:
🔗 http://localhost:5000

1️- Proje çalıştırıldığında mikrofon dinlemeye başlar.
2️- Konuşma algılandığında sessizlik bitene kadar bekler.
3️- Konuşma bittikten sonra transkripti ekrana ve web arayüzüne basar.
4️- Diğer ses türleri (gürültü, müzik vs.) için de algılama yapar ve web arayüzüne basar.

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
🤝 Katkıda Bulunma
Projeye katkıda bulunmak isterseniz:

Fork yapın 🍴
Pull Request gönderin 📌
Sorularınız veya önerileriniz için Issue açabilirsiniz 📝
📜 Lisans
Bu proje MIT lisansı altında yayımlanmıştır.
Detaylar için LICENSE dosyasına bakabilirsiniz.
