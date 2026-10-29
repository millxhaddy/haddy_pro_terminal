import pandas as pd
"""
========================================================================================
HADDY PRO - TERMINAL MILLX
MODUL: PANGKALAN DATA 1,000 DIALOG ROH AI DRILL-SERGEANT (THE 1,000 DIALOGUE VAULT)
========================================================================================
"""

import random

# Komponen Ayat Pembuka (Prefix), Intipati Teguran (Core), & Amaran Maut (Suffix)
PREFIXES = [
    "Dengar sini baik-baik!", "Buka mata dan telinga kau!", "Jangan jadi bodoh depan skrin!",
    "Otak kau letak kat mana?!", "Berhenti berangan jadi jutawan segera!", "Pasaran bukan kasino bapa kau!",
    "Tarik nafas dan buang ego kau!", "Kau nak rugi macam dulu lagi ke?!", "Komputer tak terima alasan lembik!",
    "Tangan kau jangan gatal nak klik!", "Hentikan drama emosi kau!", "Duduk tegak dan patuhi SOP!"
]

CORE_FOMO = [
    "Saham sedang terbang tinggi bukan tiket untuk kau terjun ke pucuk!",
    "Beli saham kerana berita viral adalah cara terpantas sedekah modal kat jerung!",
    "Kau nampak lilin hijau panjang, kau terus rasa nak beli? Itu jerung sedang cari pembeli naif!",
    "Ingat tragedi kaunter DJT! Terbang tinggi dua hari, lebur beribu ringgit!",
    "Bila media sosial mula heboh pasal sesuatu kaunter, waktu itulah jerung mula membuang barang!",
    "Kejar pucuk adalah tabiat penjudi amatur, bukan pelabur institusi berkaliber!"
]

CORE_STOPLOSS = [
    "Bila lantai sokongan bocor, potong serta-merta! Harapan takkan menaikkan harga saham!",
    "Rugi kecil dua peratus kau tolak, sekarang kau nak tanggung rugi ngeri dua puluh peratus?!",
    "Stop Loss bukan hiasan skrin! Ia adalah nyawa dan perisai akaun kau!",
    "Jangan sesekali alihkan Stop Loss ke bawah semata-mata takut rugi direalisasikan!",
    "Ingat tragedi Hecla Mining rugi empat ribu enam ratus ringgit kerana degil tak mahu Cut Loss!",
    "Memotong kerugian dengan pantas adalah tanda pelabur berani dan bijak!"
]

CORE_ALLOCATION = [
    "Meletakkan lapan puluh peratus modal dalam satu kaunter adalah tindakan bunuh diri!",
    "Tengok apa jadi pada UMC! Untung empat ribu ringgit lesap bertukar rugi sebab terlebih saiz!",
    "GFM rugi belas peratus sebab kau membiarkan modal RM sembilan ribu terperangkap hidup-hidup!",
    "Diversifikasi bukan suka-suka; ia adalah benteng pertahanan daripada kejutan pasaran!",
    "Maksimum pendedahan satu kaunter adalah dua puluh lima peratus modal! Jangan tamak!",
    "Bahagikan modal kepada beberapa bakul kukuh, bukan pertaruhkan semua pada satu nasib!"
]

CORE_REVENGE = [
    "Bila baru lepas kena Stop Loss, tutup laptop dan pergi bertenang! Jangan buat revenge trade!",
    "Kau masuk balik kaunter yang sama sebab nak balas dendam? Pasaran tak kenal siapa kau!",
    "Ego kau yang calar takkan pulih dengan membuat dagangan tergesa-gesa!",
    "Revenge trading adalah jalan paling singkat untuk membakar baki akaun Moomoo kau!",
    "Kerugian hari ini adalah kos perniagaan. Esok pasaran masih buka dengan setup baharu!"
]

CORE_RR = [
    "Nisbah R:R kurang daripada dua perpuluhan lima adalah matematik sampah!",
    "Kau sanggup rugi seringgit semata-mata nak untung lima puluh sen? Di mana logik kau?!",
    "Kemenangan tujuh puluh peratus sekalipun akan musnah jika purata rugi kau lebih besar dari untung!",
    "Hanya ambil peluang yang memberi ganjaran minimum dua kali ganda had risiko!",
    "Kaji had sokongan dan rintangan sebelum letak sebarang pesanan di broker!"
]

CORE_MILLION = [
    "Matlamat Satu Juta Ringgit memerlukan ketenangan batu karang, bukan kegelojohan!",
    "Konsisten tiga peratus sebulan dengan modal kompaun adalah senjata rahsia jutawan senyap!",
    "Fasa bawah RM seratus ribu adalah fasa membina asas. Sabar dan teruskan suntikan simpanan!",
    "Disiplin menjaga modal kecil hari ini yang akan melayakkan kau menguruskan dana sejuta esok!"
]

SUFFIXES = [
    "Patuhi peraturan ini atau keluar dari pasaran!",
    "Jangan berani kompromi walau satu sen!",
    "Mesin tidak menerima alasan manusia!",
    "Fikir guna logik matematik, bukan nafsu tamak!",
    "Ingat matlamat Satu Juta Ringgit kau!",
    "Sekali kau langgar disiplin, aku bunyikan siren kecemasan!"
]

def generate_1000_dialogues():
    """Menjana tepat 1,000 dialog berautonomi tanpa ulangan verbatim."""
    dialogues = []
    seen = set()
    categories = [
        ("FOMO & Pucuk", CORE_FOMO),
        ("Stop Loss & Realiti", CORE_STOPLOSS),
        ("Pendedahan Modal & UMC/GFM", CORE_ALLOCATION),
        ("Anti-Dendam / Revenge Trade", CORE_REVENGE),
        ("Matematik R:R & DDNK", CORE_RR),
        ("Misi Kompaun RM 1 Juta", CORE_MILLION)
    ]
    
    count = 1
    # Loop sistematik untuk menjana 1,000 variasi unik
    while len(dialogues) < 1000:
        cat_name, core_pool = categories[count % len(categories)]
        prefix = random.choice(PREFIXES)
        core = random.choice(core_pool)
        suffix = random.choice(SUFFIXES)
        
        entry_text = f"[{cat_name}] {prefix} {core} {suffix}"
        if entry_text not in seen:
            seen.add(entry_text)
            dialogues.append({
                "No": count,
                "Kategori": cat_name,
                "Tengkingan_AI": entry_text
            })
            count += 1
            
    return pd.DataFrame(dialogues)

# Ujian penjanaan
if __name__ == "__main__":
    df = generate_1000_dialogues()
    print(f"✅ Berjaya menjana tepat {len(df)} dialog garang!")