# DoluMu?
### Yoğunluk İzleme Sistemi

Bu proje, video görüntüleri kullanarak belirli alanlardaki insan yoğunluğunu gerçek zamanlı izlemek için geliştirilmiştir. Sistem, YOLOv5 modelini kullanarak insanları tespit eder ve kullanıcı dostu bir arayüz ile yoğunluk verilerini sunar.

#### Özellikler

* **Gerçek Zamanlı İzleme**: Belirlenen alanlarda anlık insan sayımı.
* **Özelleştirilebilir Alanlar**: Kullanıcılar videoda izlenecek alanı belirlemek için dikdörtgen çizebilir.
* **Veri Görselleştirme**: Alanların kapasiteye göre doluluk oranlarını halka grafik olarak gösterir.
* **Detaylı Analiz**: Saatlik yoğunluk değişim grafikleri.

#### Kullanılan Teknolojiler

* **Python**: Projenin temel programlama dili.
* **YOLOv5**: İnsan tespiti için kullanılan nesne algılama modeli.
* **OpenCV**: Görüntü işleme ve video analizi için kullanıldı.
* **Tkinter**: Kullanıcı arayüzü oluşturmak için kullanılan GUI kütüphanesi.
* **Matplotlib**: Grafik ve veri görselleştirme için kullanıldı.

#### Kurulum

1. **Depoyu Klonlayın**:
    ```bash
    git clone https://github.com/your-repo/crowd-monitoring-system.git
    cd crowd-monitoring-system
    ```

2. **Bağımlılıkları Yükleyin**:
    Python 3.x ve gerekli paketleri kurun:
    ```bash
    pip install -r requirements.txt
    ```

3. **YOLOv5 Modelini Kurun**:
    ```bash
    pip install torch torchvision torchaudio
    ```

#### Kullanım

1. **Video Dosyalarını Hazırlayın**: İzlenecek video dosyalarının doğru şekilde kodda tanımlandığından emin olun.
2. **Uygulamayı Çalıştırın**: Uygulamayı başlatın:
    ```bash
    python app.py
    ```
3. **İzlenecek Alanı Çizin**: Her video için izlenecek alanı dikdörtgenle belirleyin.
4. **Verileri Görüntüleyin**: Arayüzdeki alanları seçip doluluk oranlarını inceleyin ve detaylı grafikleri görüntüleyin.
