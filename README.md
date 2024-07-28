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
* **Tkinter(Windows için)**: Kullanıcı arayüzü oluşturmak için kullanılan GUI kütüphanesi.
* **PySide6(Macos içi)**: Python programlama dili için Qt toolkit kullanılarak modern ve güçlü GUI (grafik kullanıcı arayüzü) uygulamaları geliştirmek için kullanılan bir kütüphane.
* **Matplotlib**: Grafik ve veri görselleştirme için kullanıldı.

#### Kurulum

1. **Depoyu Klonlayın**:
    ```bash
    git clone https://github.com/DemirEkinArikan/DoluMu.git
    cd DoluMu
    ```
2. **PyTorch Yükleyin**:
   ```bash
    pip install torch
    ``` 
3. **OpenCV Yükleyin**:
    ```bash
    pip install opencv-python
    ```
4. **numpy yükleyin**:
   ```bash
    pip install numpy
    ```
5. **matplotlib yükleyin**:
   ```bash
    pip install matplotlib
    ```
6. **pillow yükleyin**:
   ```bash
    pip install pillow
    ```
7. **pandas yükleyin**:
   ```bash
    pip install pandas
    ```
8. **tarfile dosyasını yükleyin**:
   ```bash
    pip install backports.tarfile
    ```
   
* **Tkinter, json and datetime kütüphaneleri pythonda hazır olarak bulunmaktadır ekstra kurulum gerektirmez.**
  
#### MACOS İşletim Sistemi:
* Eğer macos işletim sistemi kullanıyorsanız ek olarak bu modülü yükleyiniz:
* ```bash
    pip install PySide6
    ```
#### Kullanım

1. **Video Dosyalarını Hazırlayın**: İzlenecek video dosyalarının doğru şekilde kodda tanımlandığından emin olun.
2. **Uygulamayı Çalıştırın**:
   * Uygulamayı başlatın (Windows için):
    ```bash
    python Apsiyon/apsiyon_windows.py
    ```
   * Uygulamayı başlatın (Macos için):
   ```bash
    python Apsiyon/apsiyon_macos.py
    ```
3. **İzlenecek Alanı Çizin**: Her tesis için izlenecek alanı dikdörtgen içine alıp belirleyin ve sonrasında enter tuşuna basınız.

* #### Önemli Not: Windows işletim sistemi için apsiyon_windows.py, macos işletim sistemi için apsiyon_macos.py dosyasını kullanınız.

* **Not**: Model yüklendikten sonra ilk çalıştırdığınızda modelin büyüklüğünden ötürü ilk seferde çalışmayabilir bu yüzden programı sonlandırıp tekrardan çalıştırmak gerekebilir.

* **Not**: Bu yazılımda kullandığımız video_01.mp4 videosu, geliştirdiğimiz insan tanıma algoritmasının başarılı çalıştığını göstermesi açısından hareketli insan görüntüleri içeren bir örnek videodur. Uygun veriyle çalışan sistemler tesisler ve havuzlar olacaktır.
