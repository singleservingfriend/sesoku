sesoku

# 🗣️ Speech & Sound Detector

Bu proje, **Flask** ve **TensorFlow YAMNet** kullanarak **canlı ses analizi** yapar.  
Mikrofon girişini dinleyerek **konuşmayı algılar**, transkribe eder ve **diğer sesleri sınıflandırır**.  
WebSocket üzerinden verileri gerçek zamanlı olarak bir arayüze gönderir.

## 🚀 Özellikler
✅ **Gerçek zamanlı konuşma algılama ve transkripsiyon**  
✅ **Arka planda sürekli dinleme ve sessizlik sonrası transkript gönderme**  
✅ **Müzik, gürültü, sessizlik gibi diğer sesleri de algılama**  
✅ **Flask-SocketIO ile WebSocket üzerinden anlık veri gönderme**  

---

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
