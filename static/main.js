// main.js

var socket = io();

// Yeni metin veya opaklık geldiğinde güncelleme yapan yardımcı fonksiyon
function updateElementWithFade(element, newText, newOpacity = 1) {
    // Eğer mevcut metin yeni metinden farklı ise fade-out yap, güncelle ve fade-in uygula
    if (element.innerHTML.trim() !== newText.trim()) {
        element.style.opacity = 0;  // fade-out başlat
        setTimeout(function() {
            element.innerHTML = newText;
            element.style.opacity = newOpacity;  // fade-in yap
        }, 300); // 300ms bekle
    } else {
        // Sadece opaklık değeri değişiyorsa, CSS transition otomatik çalışır
        element.style.opacity = newOpacity;
    }
}

// Speech mesajlarını işliyoruz
socket.on('speech', function(msg) {
    var speechEl = document.getElementById("speech");
    updateElementWithFade(speechEl, msg, 1);
});

// Sound mesajlarını işliyoruz (burada 'data' nesnesinde label ve opacity değeri var)
socket.on('sound', function(data) {
    var soundEl = document.getElementById("sound");
    updateElementWithFade(soundEl, data.label, data.opacity);
});
