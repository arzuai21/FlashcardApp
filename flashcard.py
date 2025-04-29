import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

# Uygulama hafızası
saved_sets = {}
current_set_name = None
flashcards = []
current_card = 0

# Kart verilerini dosyaya kaydetme
def kartlari_kaydet():
    global saved_sets
    with open("flashcards.json", "w") as f:
        json.dump(saved_sets, f)
    messagebox.showinfo("Başarılı", "Kartlar başarıyla kaydedildi!")

# Kart verilerini dosyadan okuma
def kartlari_yukle():
    global saved_sets
    if os.path.exists("flashcards.json"):
        with open("flashcards.json", "r") as f:
            saved_sets = json.load(f)

# Kart Durumları: her kart "öğrenildi" ya da "öğrenilmedi" olarak işaretlenebilir
# Kartlar şu formatta olacak: (soru, cevap, durum)
# durum: 0 -> öğrenilmedi, 1 -> öğrenildi
def kart_ekle():
    global flashcards

    soru = simpledialog.askstring("Ön Yüz", "Kartın ön yüzüne ne yazmak istersin?")
    if soru:
        cevap = simpledialog.askstring("Arka Yüz", "Kartın arka yüzüne ne yazmak istersin?")
        if cevap:
            flashcards.append((soru, cevap, 0))  # Durum 0 (öğrenilmedi) olarak başlat
            guncelle_karti()

def kart_sil():
    global flashcards, current_card
    if flashcards:
        flashcards.pop(current_card)
        if current_card >= len(flashcards):
            current_card = max(0, len(flashcards) - 1)
        guncelle_karti()

def karti_duzenle():
    global flashcards, current_card
    if flashcards:
        yeni_soru = simpledialog.askstring("Ön Yüzü Düzenle", "Yeni ön yüz yazısını gir:", initialvalue=flashcards[current_card][0])
        yeni_cevap = simpledialog.askstring("Arka Yüzü Düzenle", "Yeni arka yüz yazısını gir:", initialvalue=flashcards[current_card][1])
        if yeni_soru and yeni_cevap:
            flashcards[current_card] = (yeni_soru, yeni_cevap, flashcards[current_card][2])  # Durumu koru
            guncelle_karti()

def karti_kaydet():
    global saved_sets, current_set_name, flashcards
    if not flashcards:
        messagebox.showinfo("Bilgi", "Kaydedilecek kart yok!")
        return
    isim = simpledialog.askstring("Set İsmi", "Bu kart setine bir isim ver:")
    if isim:
        saved_sets[isim] = flashcards.copy()
        current_set_name = isim
        kartlari_kaydet()  # Set kaydedildiğinde dosyaya yaz
        messagebox.showinfo("Başarılı", f"{isim} seti kaydedildi!")

def set_sec(set_adi):
    global saved_sets, flashcards, current_set_name, current_card
    if set_adi in saved_sets:
        flashcards = saved_sets[set_adi].copy()
        current_set_name = set_adi
        current_card = 0
        guncelle_karti()

def kart_degistir(ileri=True):
    global current_card, flashcards
    if flashcards:
        if ileri:
            current_card = (current_card + 1) % len(flashcards)
        else:
            current_card = (current_card - 1) % len(flashcards)
        guncelle_karti()

def kart_tiklandi(event):
    if front_label.winfo_ismapped():
        front_label.pack_forget()
        back_label.pack(padx=20, pady=20)
    else:
        back_label.pack_forget()
        front_label.pack(padx=20, pady=20)

def guncelle_karti():
    global front_label, back_label
    for widget in card_frame.winfo_children():
        widget.destroy()
    if flashcards:
        soru, cevap, durum = flashcards[current_card]
        front_label = tk.Label(card_frame, text=soru, font=("Arial", 24, "bold"), bg="white", width=20, height=8, relief="raised", bd=4)
        front_label.pack(padx=20, pady=20)

        back_label = tk.Label(card_frame, text=cevap, font=("Arial", 24, "bold"), bg="lightgreen", width=20, height=8, relief="raised", bd=4)
        back_label.pack_forget()

        # Kart öğrenildiyse, arka tarafı göster
        if durum == 1:
            back_label.pack(padx=20, pady=20)

        card_frame.bind("<Button-1>", kart_tiklandi)
        front_label.bind("<Button-1>", kart_tiklandi)
        back_label.bind("<Button-1>", kart_tiklandi)

def karti_ogrenildi_yap():
    global flashcards, current_card
    if flashcards:
        soru, cevap, durum = flashcards[current_card]
        if durum == 0:  # Sadece öğrenilmemişse
            flashcards[current_card] = (soru, cevap, 1)  # Durumunu "öğrenildi" yap
            guncelle_karti()

def yeni_set():
    global flashcards, current_set_name
    flashcards = []  # Yeni set için boş liste
    current_set_name = None
    guncelle_karti()

# Ana pencere
window = tk.Tk()
window.title("Flashcard App")
window.geometry("500x700")
window.configure(bg="#f0f0f0")

# Menü Butonu
def hamburger_menu():
    menu_window = tk.Toplevel(window)
    menu_window.title("Menü")
    menu_window.geometry("300x400")

    # Yeni Kart Seti Ekle
    yeni_set_buton = tk.Button(menu_window, text="Yeni Kart Seti Ekle", font=("Arial", 14), command=yeni_set)
    yeni_set_buton.pack(pady=20)

    # Kaydedilmiş Kart Setlerini Göster
    for set_adi in saved_sets:
        buton = tk.Button(menu_window, text=set_adi, font=("Arial", 14), command=lambda set_adi=set_adi: set_sec(set_adi))
        buton.pack(pady=10)

# Menü Butonu
menu_button = tk.Button(window, text="≡", font=("Arial", 20), command=hamburger_menu)
menu_button.pack(anchor="nw", pady=10, padx=10)

# Kart alanı
card_frame = tk.Frame(window, bg="#f0f0f0")
card_frame.pack(expand=True)

# Kontrol butonları
button_frame = tk.Frame(window, bg="#f0f0f0")
button_frame.pack(pady=20)

geri_button = tk.Button(button_frame, text="← Geri", command=lambda: kart_degistir(ileri=False))
geri_button.grid(row=0, column=0, padx=10)

ileri_button = tk.Button(button_frame, text="İleri →", command=lambda: kart_degistir(ileri=True))
ileri_button.grid(row=0, column=1, padx=10)

alt_button_frame = tk.Frame(window, bg="#f0f0f0")
alt_button_frame.pack(pady=10)

ekle_button = tk.Button(alt_button_frame, text="Kart Ekle", command=kart_ekle)
ekle_button.grid(row=0, column=0, padx=5)

sil_button = tk.Button(alt_button_frame, text="Kart Sil", command=kart_sil)
sil_button.grid(row=0, column=1, padx=5)

duzenle_button = tk.Button(alt_button_frame, text="Kartı Düzenle", command=karti_duzenle)
duzenle_button.grid(row=0, column=2, padx=5)

kaydet_button = tk.Button(alt_button_frame, text="Kaydet", command=karti_kaydet)
kaydet_button.grid(row=0, column=3, padx=5)

ogren_button = tk.Button(alt_button_frame, text="Öğrenildi Yap", command=karti_ogrenildi_yap)
ogren_button.grid(row=0, column=4, padx=5)

# Başlangıçta kartları yükle
kartlari_yukle()

window.mainloop()



