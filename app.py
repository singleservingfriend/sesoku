import os
import time
import threading
from collections import deque

import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import requests
import sounddevice as sd
import speech_recognition as sr

from flask import Flask, render_template
from flask_socketio import SocketIO

# -------------------- Flask ve SocketIO Ayarları --------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='threading')

@app.route('/')
def index():
    return render_template('index.html')

# Fonksiyonlar üzerinden web arayüzüne mesaj gönderme
def emit_speech(text):
    socketio.emit('speech', text)

def emit_sound(text):
    socketio.emit('sound', text)

# -------------------- MODEL, ETİKET ve SES AYARLARI --------------------
MODEL_PATH = "./yamnet_model"
LABELS_PATH = "./yamnet_class_map.csv"

# Modeli yerelden yükle, yoksa indir ve kaydet
if os.path.exists(MODEL_PATH):
    print("✅ Yerel model bulundu, yükleniyor...")
    yamnet_model = tf.saved_model.load(MODEL_PATH)
else:
    print("🌐 Model bulunamadı, internetten indiriliyor...")
    yamnet_model = hub.load("https://tfhub.dev/google/yamnet/1")
    print("💾 Model kaydediliyor...")
    tf.saved_model.save(yamnet_model, MODEL_PATH)

# Etiket dosyası: Yerelde yoksa indir
if not os.path.exists(LABELS_PATH):
    print("🌐 Etiket dosyası indiriliyor...")
    response = requests.get("https://raw.githubusercontent.com/tensorflow/models/master/research/audioset/yamnet/yamnet_class_map.csv")
    with open(LABELS_PATH, "wb") as f:
        f.write(response.content)

# Etiketleri yükle (CSV'nin başlığı atlanıyor)
with open(LABELS_PATH, "r", encoding="utf8") as f:
    class_labels = [line.strip().split(",")[2] for line in f.readlines()[1:]]

# Mikrofon ve sliding window parametreleri
RATE = 16000                    # Örnekleme hızı (16 kHz)
CHUNK = RATE * 2                # Her callback’te alınan parça (2 saniye)
OVERLAP_INTERVAL = 0.5          # Her 0.5 saniyede bir pencere işlenecek
WINDOW_SIZE = RATE * 2          # İşlenecek pencere uzunluğu (2 saniye)
audio_buffer = deque(maxlen=RATE * 4)  # Son 4 saniyeyi saklayacak

# Eşik değerler
MIN_CONFIDENCE = 0.3            # Genel sesler için minimum güven
MIN_SPEECH_CONFIDENCE = 0.3     # Konuşma için daha düşük eşik

# Konuşma ile ilgili sınıflar (CSV'deki etiketlere göre)
SPEECH_CLASSES = [
    "Konuşma",
    "Çocuk konuşması, çocuk konuşuyor",
    "Sohbet",
    "Anlatım, monolog",
    "Bebek mırıltısı",
    "Konuşma sentezleyici",
]

# GLOBAL BUFFER için kilit
buffer_lock = threading.Lock()

# -------------------- YENİ KONUŞMA ALGILAMA FONKSİYONU --------------------
def listen_and_transcribe():
    """
    Konuşma olduğu sürece dinler, bittikten sonra tek seferde transkribe eder.
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    print("🎤 Mikrofon dinlemeye hazır, konuşabilirsiniz.")
    
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)  # Ortam gürültüsünü algılar
        while True:
            print("Dinleniyor...")
            try:
                # Konuşma tamamlanana kadar bekle ve kaydet
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)
                
                # Google API üzerinden tanıma işlemi
                text = recognizer.recognize_google(audio, language="tr-TR")
                print("✅ Çeviri:", text)
                emit_speech(text)  # Web arayüzüne gönder
                
            except sr.UnknownValueError:
                print("Anlaşılamayan ses.")
            except sr.WaitTimeoutError:
                print("🛑 Sessizlik algılandı, dinleme durduruldu.")
                break
            except sr.RequestError as e:
                print("API hatası:", e)
                break

# -------------------- SOUND ALGILAMA --------------------
def classify_and_emit_sound(audio_data):
    """
    Audio veriyi YAMNet modeli ile sınıflandırır.
    Eğer en yüksek skor konuşma değilse, Sound mesajını web arayüzüne gönderir.
    """
    audio_data = np.array(audio_data, dtype=np.float32)
    scores, embeddings, spectrogram = yamnet_model(audio_data)
    scores_np = scores.numpy()
    avg_scores = np.mean(scores_np, axis=0)

    top_index = np.argmax(avg_scores)
    top_label = class_labels[top_index].strip().lower()
    max_conf = avg_scores[top_index]

    # Eğer konuşma değilse ve yeterince güvenliyse, sound mesajı gönder
    if top_label not in [s.lower() for s in SPEECH_CLASSES] and max_conf >= MIN_CONFIDENCE:
        if top_label in ["silence", "sessizlik"]:
            return
        emit_sound({"label": top_label, "opacity": float(max_conf)})

# -------------------- SLIDING WINDOW SOUND İŞLEME --------------------
def sliding_window_processor():
    """Buffer'dan WINDOW_SIZE örneğini alıp belirli aralıklarla işleme koyar."""
    while True:
        time.sleep(OVERLAP_INTERVAL)
        with buffer_lock:
            if len(audio_buffer) >= WINDOW_SIZE:
                window = list(audio_buffer)[-WINDOW_SIZE:]
            else:
                continue
        classify_and_emit_sound(window)

# -------------------- SES BUFFER KAYIT --------------------
def audio_callback(indata, frames, time_info, status):
    """Her çağrıda alınan audio verisini global buffer'a ekler."""
    if status:
        print(status)
    samples = indata[:, 0].tolist()
    with buffer_lock:
        audio_buffer.extend(samples)

# -------------------- ARKA PLANDA SES DİNLEME --------------------
def run_audio_stream():
    """Ses kaydını başlatır ve arka plan threadlerini çalıştırır."""
    processor_thread = threading.Thread(target=sliding_window_processor, daemon=True)
    processor_thread.start()

    print("🎤 Gerçek zamanlı ses algılama başlıyor...")
    with sd.InputStream(samplerate=RATE, channels=1, callback=audio_callback, blocksize=CHUNK):
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n🛑 Dinleme durduruldu.")

# -------------------- ARKA PLANDA KONUŞMA DİNLEME --------------------
def run_speech_recognition():
    """
    Arka planda konuşmayı sürekli dinleyen bir iş parçacığı başlatır.
    """
    while True:
        listen_and_transcribe()
        time.sleep(1)  # Sessizlik sonrası 1 saniye bekleyip tekrar başlat

# -------------------- UYGULAMA BAŞLATMA --------------------
if __name__ == '__main__':
    # Konuşmayı arka planda dinleyen thread başlat
    speech_thread = threading.Thread(target=run_speech_recognition, daemon=True)
    speech_thread.start()

    # Ses (sound) algılamayı arka planda başlat
    audio_thread = threading.Thread(target=run_audio_stream, daemon=True)
    audio_thread.start()
    
    # Flask-SocketIO web sunucusunu başlat
    socketio.run(app, host='0.0.0.0', port=5000)
