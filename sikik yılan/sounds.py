import pygame
import os
import numpy as np
from constants import SES_ACIK, MUZIK_ACIK, SES_SEVIYESI, MUZIK_SEVIYESI

class SesYoneticisi:
    def __init__(self, ayar_yoneticisi=None):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.ayar_yoneticisi = ayar_yoneticisi
        
        # Ayarlardan yükle veya varsayılanları kullan
        if ayar_yoneticisi:
            ayarlar = ayar_yoneticisi.ayarlari_yukle()
            self.ses_acik = ayarlar.get("ses_acik", SES_ACIK)
            self.muzik_acik = ayarlar.get("muzik_acik", MUZIK_ACIK)
            self.ses_seviyesi = ayarlar.get("ses_seviyesi", SES_SEVIYESI)
            self.muzik_seviyesi = ayarlar.get("muzik_seviyesi", MUZIK_SEVIYESI)
        else:
            self.ses_acik = SES_ACIK
            self.muzik_acik = MUZIK_ACIK
            self.ses_seviyesi = SES_SEVIYESI
            self.muzik_seviyesi = MUZIK_SEVIYESI
        
        # Ses efektleri
        self.sesler = {
            "yem_ye": None,
            "altin_elma": None,
            "elmas": None,
            "bomba": None,
            "olum": None,
            "menu_tikla": None,
            "dondur": None
        }
        
        self.muzikler = {
            "Normal": None,
            "Bomb Modu": None,
            "menu": None
        }
        
        # Kullanıcı müzikleri
        self.kullanici_muzikleri = []
        self.muzik_klasoru = "music"
        
        self.mevcut_muzik = None
        self._sesleri_yukle()
        self._kullanici_muziklerini_yukle()
    
    def _kullanici_muziklerini_yukle(self):
        """music klasöründeki müzik dosyalarını yükle"""
        try:
            # Sistem müzikleri - menüde gösterilmeyecek (dosya ismi içinde bu kelimeler geçiyorsa)
            sistem_muzik_kelimeleri = ['level complete', 'game over', 'lost a life', 'level_complete', 'game_over', 'lost_a_life']
            
            if os.path.exists(self.muzik_klasoru):
                dosyalar = [f for f in os.listdir(self.muzik_klasoru) 
                           if f.lower().endswith(('.mp3', '.wav', '.ogg')) and not f.startswith('.')]
                
                for dosya in dosyalar:
                    # Dosya isminde sistem müziği kelimesi var mı kontrol et
                    dosya_kucuk = dosya.lower()
                    sistem_muzigi = any(kelime in dosya_kucuk for kelime in sistem_muzik_kelimeleri)
                    
                    if sistem_muzigi:
                        continue  # Sistem müziğini atlat
                    
                    tam_yol = os.path.join(self.muzik_klasoru, dosya)
                    isim = os.path.splitext(dosya)[0]  # Uzantısız isim
                    self.kullanici_muzikleri.append((isim, tam_yol))
                
                if self.kullanici_muzikleri:
                    try:
                        print(f"[OK] {len(self.kullanici_muzikleri)} kullanici muzigi yuklendi")
                    except UnicodeEncodeError:
                        print(f"{len(self.kullanici_muzikleri)} kullanici muzigi yuklendi")
        except Exception as e:
            print(f"Kullanici muzikleri yuklenirken hata: {e}")
    
    def kullanici_muzikleri_getir(self):
        """Kullanıcı müziklerinin listesini döndürür (sistem müzikleri hariç)"""
        return self.kullanici_muzikleri.copy()
    
    def kullanici_muziklerini_getir(self):
        """Kullanıcı müziklerinin listesini döndür (sistem müzikleri hariç)"""
        return self.kullanici_muzikleri
    
    def _sesleri_yukle(self):
        """Ses dosyalarını yükle veya oluştur"""
        try:
            self._kaliteli_sesler_olustur()
        except Exception as e:
            print(f"Sesler yüklenirken hata: {e}")
    
    def _ses_olustur(self, frekanslar, sure, wave_type="sine", amplitude=0.3):
        """Kaliteli ton sesi oluştur (çoklu frekans desteği)"""
        try:
            sample_rate = 22050
            n_samples = int(sure * sample_rate)
            t = np.linspace(0, sure, n_samples, False)
            
            # Frekansları liste yap (tek değer de olabilir)
            if not isinstance(frekanslar, list):
                frekanslar = [frekanslar]
            
            # Başlangıç dalgası
            wave = np.zeros(n_samples)
            
            # Her frekans için dalga ekle
            for frekans in frekanslar:
                if wave_type == "sine":
                    wave += np.sin(frekans * t * 2 * np.pi)
                elif wave_type == "square":
                    wave += np.sign(np.sin(frekans * t * 2 * np.pi))
                elif wave_type == "saw":
                    wave += 2 * (t * frekans - np.floor(t * frekans + 0.5))
            
            # Normalize et
            wave = wave / len(frekanslar) * amplitude
            
            # ADSR envelope (Attack, Decay, Sustain, Release)
            attack = min(int(0.01 * sample_rate), n_samples // 4)  # 10ms attack
            decay = min(int(0.05 * sample_rate), n_samples // 4)   # 50ms decay
            release = min(int(0.1 * sample_rate), n_samples // 3)  # 100ms release
            
            envelope = np.ones(n_samples)
            
            # Attack
            if attack > 0 and attack < n_samples:
                envelope[:attack] = np.linspace(0, 1, attack)
            
            # Decay
            if decay > 0 and attack + decay < n_samples:
                envelope[attack:attack+decay] = np.linspace(1, 0.7, decay)
            
            # Release (fade out)
            if release > 0 and release < n_samples:
                envelope[-release:] = np.linspace(0.7, 0, release)
            
            wave = wave * envelope
            
            # Stereo yap
            wave = np.column_stack((wave, wave))
            
            # 16-bit formatına çevir
            wave = (wave * 32767).astype(np.int16)
            
            # Pygame sound oluştur
            sound = pygame.sndarray.make_sound(wave)
            return sound
        except Exception as e:
            print(f"Ses oluşturma hatası: {e}")
            return None
    
    def _kaliteli_sesler_olustur(self):
        """Kaliteli ses efektleri oluştur"""
        try:
            # Yem yeme - neşeli yukarı çıkan akor (C-E-G)
            self.sesler["yem_ye"] = self._ses_olustur([523, 659, 784], 0.12, "sine", 0.25)
            
            # Altın elma - başarı fanfarı (parlak akor)
            self.sesler["altin_elma"] = self._ses_olustur([880, 1047, 1319], 0.25, "sine", 0.3)
            
            # Elmas - kristal ses (çok yüksek harmonikler)
            self.sesler["elmas"] = self._ses_olustur([1047, 1319, 1568, 2093], 0.2, "sine", 0.2)
            
            # Bomba - tehlikeli düşük ses (kare dalga)
            self.sesler["bomba"] = self._ses_olustur([110, 165], 0.4, "square", 0.2)
            
            # Ölüm - dramatik düşen ses (minor akor)
            self.sesler["olum"] = self._ses_olustur([392, 311, 233], 0.6, "saw", 0.25)
            
            # Menü tıklama - kısa click
            self.sesler["menu_tikla"] = self._ses_olustur([1000], 0.04, "sine", 0.15)
            
            # Dondurma - yumuşak buz sesi
            self.sesler["dondur"] = self._ses_olustur([440, 554], 0.25, "sine", 0.2)
            
            # Müzikleri oluştur
            self._muzik_olustur()
            
        except Exception as e:
            print(f"Kaliteli sesler oluşturulurken hata: {e}")
    
    def _nota_olustur(self, frekans, sure, amplitude=0.15):
        """Müzik notası oluştur"""
        try:
            sample_rate = 22050
            n_samples = int(sure * sample_rate)
            t = np.linspace(0, sure, n_samples, False)
            
            # Sinüs dalgası + harmonikler (daha zengin ses)
            wave = np.sin(frekans * t * 2 * np.pi) * 0.6  # Ana ton
            wave += np.sin(frekans * 2 * t * 2 * np.pi) * 0.2  # Oktav
            wave += np.sin(frekans * 3 * t * 2 * np.pi) * 0.1  # 3. harmonik
            
            wave = wave * amplitude
            
            # Envelope (yumuşak başla, yumuşak bitir)
            attack = int(0.02 * sample_rate)
            release = int(0.05 * sample_rate)
            
            envelope = np.ones(n_samples)
            if attack < n_samples:
                envelope[:attack] = np.linspace(0, 1, attack)
            if release < n_samples:
                envelope[-release:] = np.linspace(1, 0, release)
            
            wave = wave * envelope
            
            return wave
        except Exception as e:
            print(f"Nota oluşturma hatası: {e}")
            return np.array([])
    
    def _muzik_olustur(self):
        """Oyun müziklerini oluştur - daha iyi melodiler"""
        try:
            # Notalar (frekanslar)
            notalar = {
                'C4': 262, 'D4': 294, 'E4': 330, 'F4': 349, 'G4': 392, 'A4': 440, 'B4': 494,
                'C5': 523, 'D5': 587, 'E5': 659, 'F5': 698, 'G5': 784, 'A5': 880, 'B5': 988,
                'C6': 1047, 'D6': 1175, 'E6': 1319,
                'R': 0  # Rest (sessizlik)
            }
            
            # Normal mod - klasik 8-bit oyun müziği tarzı
            normal_melodi = [
                ('C5', 0.2), ('C5', 0.2), ('C5', 0.2), ('G4', 0.4),
                ('A4', 0.2), ('A4', 0.2), ('A4', 0.2), ('G4', 0.6),
                ('F4', 0.2), ('F4', 0.2), ('F4', 0.2), ('E4', 0.4),
                ('D4', 0.2), ('D4', 0.2), ('C4', 0.6),
                
                ('G4', 0.2), ('G4', 0.2), ('C5', 0.4),
                ('G4', 0.2), ('F4', 0.2), ('E4', 0.6),
                ('F4', 0.2), ('E4', 0.2), ('D4', 0.4),
                ('C4', 0.8),
            ]
            
            # Bomba modu - hızlı, tempolu
            bomba_melodi = [
                ('E5', 0.15), ('E5', 0.15), ('E5', 0.15), ('E5', 0.15),
                ('C5', 0.15), ('E5', 0.3), ('G5', 0.6),
                ('G4', 0.6),
                
                ('C5', 0.3), ('G4', 0.3), ('E4', 0.3),
                ('A4', 0.3), ('B4', 0.3), ('A4', 0.3),
                ('G4', 0.2), ('E5', 0.2), ('G5', 0.2),
                ('A5', 0.3), ('F5', 0.15), ('G5', 0.6),
            ]
            
            # Menü müziği - sakin, minimal
            menu_melodi = [
                ('C4', 0.4), ('E4', 0.4), ('G4', 0.4), ('E4', 0.4),
                ('C4', 0.4), ('D4', 0.4), ('E4', 0.8),
                ('R', 0.2),
                ('D4', 0.4), ('F4', 0.4), ('A4', 0.4), ('F4', 0.4),
                ('D4', 0.4), ('E4', 0.4), ('D4', 0.8),
                ('R', 0.4),
            ]
            
            # Melodileri wav dosyalarına çevir
            self._melodi_kaydet(normal_melodi, notalar, "normal")
            self._melodi_kaydet(bomba_melodi, notalar, "bomba")
            self._melodi_kaydet(menu_melodi, notalar, "menu")
            
        except Exception as e:
            print(f"Müzik oluşturulurken hata: {e}")
    
    def _melodi_kaydet(self, melodi, notalar, isim):
        """Melodiyi oluştur ve hafızada tut"""
        try:
            sample_rate = 22050
            tum_wave = np.array([])
            
            # Her notayı ekle
            for nota_adi, sure in melodi:
                if nota_adi == 'R':  # Sessizlik
                    n_samples = int(sure * sample_rate)
                    wave = np.zeros(n_samples)
                else:
                    frekans = notalar.get(nota_adi, 440)
                    wave = self._nota_olustur(frekans, sure, 0.12)
                
                tum_wave = np.concatenate([tum_wave, wave])
            
            # Melodiyi 3 kez tekrarla (daha uzun müzik)
            tum_wave = np.tile(tum_wave, 3)
            
            # Stereo yap
            tum_wave = np.column_stack((tum_wave, tum_wave))
            
            # 16-bit formatına çevir
            tum_wave = (tum_wave * 32767).astype(np.int16)
            
            # Geçici dosyaya kaydet
            import tempfile
            temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            temp_path = temp_file.name
            temp_file.close()
            
            # WAV dosyası yaz
            from scipy.io import wavfile
            wavfile.write(temp_path, sample_rate, tum_wave)
            
            # Müzik dictionary'sine ekle
            if isim == "normal":
                self.muzikler["Normal"] = temp_path
            elif isim == "bomba":
                self.muzikler["Bomb Modu"] = temp_path
            elif isim == "menu":
                self.muzikler["menu"] = temp_path
                
        except ImportError:
            print("scipy yüklü değil, müzik oluşturulamıyor")
        except Exception as e:
            print(f"Melodi kaydetme hatası: {e}")
    
    def efekt_cal(self, efekt_adi):
        """Ses efekti çal"""
        if not self.ses_acik:
            return
        
        if efekt_adi in self.sesler and self.sesler[efekt_adi]:
            try:
                self.sesler[efekt_adi].set_volume(self.ses_seviyesi)
                self.sesler[efekt_adi].play()
            except:
                pass
    
    def muzik_cal(self, muzik_adi_veya_yol):
        """Arka plan müziği çal - isim veya dosya yolu"""
        if not self.muzik_acik:
            return
        
        if muzik_adi_veya_yol == self.mevcut_muzik:
            return
        
        try:
            pygame.mixer.music.stop()
            
            # Önce programlı müziklere bak
            if muzik_adi_veya_yol in self.muzikler and self.muzikler[muzik_adi_veya_yol]:
                pygame.mixer.music.load(self.muzikler[muzik_adi_veya_yol])
                pygame.mixer.music.set_volume(self.muzik_seviyesi)
                pygame.mixer.music.play(-1)  # Sonsuz döngü
                self.mevcut_muzik = muzik_adi_veya_yol
            # Kullanıcı müziği dosya yolu mu?
            elif os.path.exists(muzik_adi_veya_yol):
                pygame.mixer.music.load(muzik_adi_veya_yol)
                pygame.mixer.music.set_volume(self.muzik_seviyesi)
                pygame.mixer.music.play(-1)  # Sonsuz döngü
                self.mevcut_muzik = muzik_adi_veya_yol
        except Exception as e:
            print(f"Müzik çalarken hata: {e}")
    
    def muzik_durdur(self):
        """Müziği durdur"""
        try:
            pygame.mixer.music.stop()
            self.mevcut_muzik = None
        except:
            pass
    
    def muzik_cal_bir_kez(self, dosya_adi):
        """Müziği bir kez çal (döngüsüz) - dosya adı ile"""
        if not self.muzik_acik:
            return
        
        try:
            # music klasöründe dosyayı ara
            dosya_yolu = os.path.join(self.muzik_klasoru, dosya_adi)
            if os.path.exists(dosya_yolu):
                pygame.mixer.music.stop()
                pygame.mixer.music.load(dosya_yolu)
                pygame.mixer.music.set_volume(self.muzik_seviyesi)
                pygame.mixer.music.play(0)  # Sadece 1 kez çal
                self.mevcut_muzik = dosya_yolu
        except Exception as e:
            print(f"Müzik çalarken hata: {e}")
    
    def ses_ac_kapat(self):
        """Ses efektlerini aç/kapat"""
        self.ses_acik = not self.ses_acik
        # Ayarları kaydet
        if self.ayar_yoneticisi:
            self.ayar_yoneticisi.ayarlari_kaydet({"ses_acik": self.ses_acik})
    
    def muzik_ac_kapat(self):
        """Müziği aç/kapat"""
        self.muzik_acik = not self.muzik_acik
        if not self.muzik_acik:
            self.muzik_durdur()
        # Ayarları kaydet
        if self.ayar_yoneticisi:
            self.ayar_yoneticisi.ayarlari_kaydet({"muzik_acik": self.muzik_acik})
    
    def ses_seviyesi_ayarla(self, seviye):
        """Ses efekti seviyesini ayarla (0.0-1.0)"""
        self.ses_seviyesi = max(0.0, min(1.0, seviye))
    
    def muzik_seviyesi_ayarla(self, seviye):
        """Müzik seviyesini ayarla (0.0-1.0)"""
        self.muzik_seviyesi = max(0.0, min(1.0, seviye))
        try:
            pygame.mixer.music.set_volume(self.muzik_seviyesi)
        except:
            pass
