class BinaryMultiplierTM:
    def __init__(self, sayi1: str, sayi2: str):
        bant_kapasitesi = (len(sayi1) + 2) * (len(sayi2) + 2) + 50
        self.tape_array = list(f"{sayi1}*{sayi2}=") + ['_'] * bant_kapasitesi
        self.pointer = 0
        self.current_state = 'DURUM_SAYI1_GEC'  
        self.adim_sayaci = 0

        self.ara_toplam_str = ''
        self.yazma_imleci = 0
        self.islem_bitiyor_mu = False 

    def _get_tape_string(self) -> str:
        return "".join(self.tape_array)

    def display_transition(self, okunan_karakter, yazilan_karakter, kafa_yonu, onceki_durum):
        # Okunan ve yazılan semboller boşluk ise tabloda B olarak gösterilsin
        gosterim_okunan = 'B' if okunan_karakter == '_' else okunan_karakter
        gosterim_yazilan = 'B' if yazilan_karakter == '_' else yazilan_karakter

        temiz_bant = self._get_tape_string().rstrip('_')
        
        if self.pointer >= len(temiz_bant):
            temiz_bant = temiz_bant.ljust(self.pointer + 1, '_')
        
        temiz_bant = temiz_bant.replace('_', 'B')
        
        bant_gorunumu = (
            temiz_bant[:self.pointer]
            + "[" + temiz_bant[self.pointer] + "]"
            + temiz_bant[self.pointer + 1:]
        )
        
        mevcut_adim = self.adim_sayaci + 1
        print(f" {mevcut_adim:<5} | {onceki_durum:<23} | {gosterim_okunan:^7} | {gosterim_yazilan:^10} | {kafa_yonu:^7} | {bant_gorunumu}")

    def read_symbol(self):
        while self.pointer >= len(self.tape_array):
            self.tape_array.append('_')
        return self.tape_array[self.pointer]

    def write_symbol(self, sembol):
        while self.pointer >= len(self.tape_array):
            self.tape_array.append('_')
        self.tape_array[self.pointer] = sembol

    def move_head(self, yon_komutu):
        if yon_komutu == 'R':
            self.pointer += 1
        elif yon_komutu == 'L':
            self.pointer = max(0, self.pointer - 1)

    def _get_multiplicand(self):
        tam_metin = self._get_tape_string()
        sol_taraf = tam_metin.split('*')[0]
        return ''.join(karakter for karakter in sol_taraf if karakter in '01') or '0'

    def _get_current_result(self):
        tam_metin = self._get_tape_string()
        ayrilmis_kisimlar = tam_metin.split('=')
        sag_taraf = ayrilmis_kisimlar[1] if len(ayrilmis_kisimlar) > 1 else ''
        return ''.join(karakter for karakter in sag_taraf if karakter in '01') or '0'

    def _shift_left_multiplicand(self):
        tam_metin = self._get_tape_string()
        yildiz_indeksi = tam_metin.index('*')
        guncel_deger = ''.join(karakter for karakter in tam_metin[:yildiz_indeksi] if karakter in '01')
        kaydirilmis_deger = (guncel_deger + '0').lstrip('0') or '0'
        
        hizali_metin = kaydirilmis_deger.zfill(yildiz_indeksi)
        if len(hizali_metin) > yildiz_indeksi:
            ekstra_fark = len(hizali_metin) - yildiz_indeksi
            self.tape_array = list(' ' * ekstra_fark) + self.tape_array
            self.pointer += ekstra_fark
            tam_metin2 = "".join(self.tape_array)
            yildiz_indeksi = tam_metin2.index('*')
            
        for i, harf in enumerate(hizali_metin):
            self.tape_array[i] = harf

    def execute_simulation(self):
        print("Turing Simülasyonu Akışı Başlatılıyor...\n")
        
        # EKRAN ÇIKTIISI BAŞLIĞI
        print("-" * 118)
        print(f" {'ADIM':<5} | {'DURUM':<23} | {'OKUNAN':^7} | {'YAZILAN':^10} | {'YÖN':^7} | {'BANT İÇERİĞİ'}")
        print("-" * 118)

        MAX_ADIM = 25000

        while self.adim_sayaci < MAX_ADIM:
            okunan_deger = self.read_symbol()
            yazilacak_deger = okunan_deger
            kamera_yonu = 'S'
            eski_state = self.current_state

            if self.current_state in ('DURUM_BASARILI', 'DURUM_HATALI'):
                self.display_transition(okunan_deger, yazilacak_deger, 'S', eski_state)
                break

         
            elif self.current_state == 'DURUM_SAYI1_GEC':
                if okunan_deger in ('0', '1'):
                    kamera_yonu = 'R'
                elif okunan_deger == '*':
                    self.current_state = 'DURUM_SAYI2_GEC'
                    kamera_yonu = 'R'
                else:
                    self.current_state = 'DURUM_HATALI'

            elif self.current_state == 'DURUM_SAYI2_GEC':
                if okunan_deger in ('0', '1'):
                    kamera_yonu = 'R'
                elif okunan_deger == '=':
                    self.current_state = 'DURUM_ISLENECEK_BIT_BUL'
                    kamera_yonu = 'L'
                else:
                    self.current_state = 'DURUM_HATALI'

            elif self.current_state == 'DURUM_ISLENECEK_BIT_BUL':
                if okunan_deger in ('X', 'Y'):
                    kamera_yonu = 'L'

                elif okunan_deger == '0':
                    yazilacak_deger = 'Y'
                    son_mu = (self.tape_array[self.pointer - 1] == '*')
                    self.islem_bitiyor_mu = son_mu
                    if son_mu:
                        self.current_state = 'DURUM_YILDIZA_DON_TEMIZLE'
                    else:
                        self.current_state = 'DURUM_KAYDIRMA_ICIN_GERI_GIT'
                    kamera_yonu = 'L'

                elif okunan_deger == '1':                  
                    yazilacak_deger = 'X'
                    son_mu = (self.tape_array[self.pointer - 1] == '*')
                    self.islem_bitiyor_mu = son_mu

                    val1 = self._get_multiplicand()
                    val2 = self._get_current_result()
                    matematiksel_toplam = int(val1, 2) + int(val2, 2)        #Sonuç hesaplanıyor 
                    self.ara_toplam_str = bin(matematiksel_toplam)[2:]
                    self.yazma_imleci = 0

                    self.current_state = 'DURUM_ESITTIR_BUL_YAZ'
                    kamera_yonu = 'R'

                elif okunan_deger == '*':
                    self.current_state = 'DURUM_YILDIZA_DON_TEMIZLE'
                    kamera_yonu = 'L'
                else:
                    self.current_state = 'DURUM_HATALI'

            elif self.current_state == 'DURUM_ESITTIR_BUL_YAZ':
                if okunan_deger != '=':
                    kamera_yonu = 'R'
                else:
                    self.current_state = 'DURUM_SONUC_YAZ'
                    kamera_yonu = 'R'

            elif self.current_state == 'DURUM_SONUC_YAZ':
                if self.yazma_imleci < len(self.ara_toplam_str):
                    yazilacak_deger = self.ara_toplam_str[self.yazma_imleci]
                    self.yazma_imleci += 1
                    kamera_yonu = 'R'
                else:
                    self.current_state = 'DURUM_ESITTIRE_GERI_DON'
                    kamera_yonu = 'L'

            elif self.current_state == 'DURUM_ESITTIRE_GERI_DON':
                if okunan_deger != '=':
                    kamera_yonu = 'L'
                else:
                    if self.islem_bitiyor_mu:
                        self.current_state = 'DURUM_YILDIZA_DON_TEMIZLE'
                    else:
                        self.current_state = 'DURUM_KAYDIRMA_ICIN_GERI_GIT'
                    kamera_yonu = 'L'

            elif self.current_state == 'DURUM_KAYDIRMA_ICIN_GERI_GIT':
                if okunan_deger != '=':
                    kamera_yonu = 'R'
                else:
                    self._shift_left_multiplicand()
                    if self.islem_bitiyor_mu:
                        self.current_state = 'DURUM_YILDIZA_DON_TEMIZLE'
                    else:
                        self.current_state = 'DURUM_ISLENECEK_BIT_BUL'
                    kamera_yonu = 'L'

            elif self.current_state == 'DURUM_YILDIZA_DON_TEMIZLE':
                if okunan_deger != '*':
                    kamera_yonu = 'L'
                else:
                    self.current_state = 'DURUM_ORIJINAL_BANT_YAP'
                    kamera_yonu = 'R'

            elif self.current_state == 'DURUM_ORIJINAL_BANT_YAP':
                if okunan_deger == 'X':
                    yazilacak_deger = '1'
                    kamera_yonu = 'R'
                elif okunan_deger == 'Y':
                    yazilacak_deger = '0'
                    kamera_yonu = 'R'
                elif okunan_deger == '=':
                    self.current_state = 'DURUM_BASARILI'
                    kamera_yonu = 'S'
                else:
                    kamera_yonu = 'R'
            else:
                self.current_state = 'DURUM_HATALI'

            self.write_symbol(yazilacak_deger)
            self.display_transition(okunan_deger, yazilacak_deger, kamera_yonu, eski_state)
            self.move_head(kamera_yonu)
            self.adim_sayaci += 1
        else:
            print(f"\nSİSTEM UYARISI: {MAX_ADIM} adım sınırı aşıldığı için simülasyon zorla durduruldu!")

# ----------------------------------------------------------------------
def main():
    print("=" * 70)
    print("      IKILI (BINARY) CARPMA - TURING MAKINESI SIMULATORU")
    print("=" * 70)

    # İki adet binary sayı alınması
    ilk_sayi = input("1. Çarpanı (Binary) Giriniz: ").strip()
    ikinci_sayi = input("2. Çarpanı (Binary) Giriniz: ").strip()

    if not ilk_sayi or not ikinci_sayi:
        print("Sistem Hatası: Girdi alanları boş bırakılamaz!")
        return
   
    if not all(karakter in '01' for karakter in ilk_sayi) or not all(karakter in '01' for karakter in ikinci_sayi):
        print("Sistem Hatası: Sadece ikili sistem sayıları (0 ve 1) girilmelidir!")
        return

    # Bant formatının * ve = ile oluşturulması
    saglama_degeri = int(ilk_sayi, 2) * int(ikinci_sayi, 2)
    print(f"\nHazırlanan Bant Formatı: {ilk_sayi}*{ikinci_sayi}=")
    print(f"Olması Gereken Sonuç: {saglama_degeri} ({bin(saglama_degeri)[2:]})\n")

    simulator = BinaryMultiplierTM(ilk_sayi, ikinci_sayi)
    simulator.execute_simulation()

    print("-" * 118) 

    # Sonucun binary ve decimal olarak gösterilmesi
    bandin_son_formati = "".join(simulator.tape_array).rstrip('_').replace('_', 'B')
    ayrilmis_sonuc = bandin_son_formati.split('=')
    ham_ikili_sonuc = ayrilmis_sonuc[1] if len(ayrilmis_sonuc) > 1 else ''
    kesin_ikili_sonuc = ''.join(karakter for karakter in ham_ikili_sonuc if karakter in '01') or '0'
    kesin_onlu_sonuc = int(kesin_ikili_sonuc, 2)

    print("\n" + "*" * 70)
    print("SİMÜLASYON İŞLEMİ TAMAMLANDI")
    print("*" * 70)
    print(f"Bant Üzerindeki Son Durum : {bandin_son_formati}")
    print(f"Toplam İşlem Adımı        : {simulator.adim_sayaci}")
    print(f"Hesaplanan Binary Sonuç   : {kesin_ikili_sonuc}")
    print(f"Hesaplanan Decimal Sonuç  : {kesin_onlu_sonuc}")
    print(f"Matematiksel Doğrulama    : {int(ilk_sayi,2)} x {int(ikinci_sayi,2)} = {saglama_degeri}")

if __name__ == "__main__":
    main()