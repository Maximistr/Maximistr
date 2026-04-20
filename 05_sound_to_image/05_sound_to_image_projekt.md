# Sound to Image Transfer

## Popis a cíl projektu

Aplikace **Sound to Image Transfer** slouží k převodu zvukových souborů na obrazy a obrazů na zvuk. Jedná se o nástroj pro steganografii a vizualizaci zvuku, vhodný pro:
- Experimentování s audio-vizuálními transformacemi
- Přenosu dat skrze obrazové či zvukové formáty
- Vizualizace zvukových vln a spektrogramů

Aplikace nabízí grafické rozhraní (GUI) i příkazový řádek pro snadné použití.

## Funkcionalita programu

Aplikace zahrnuje následující technické prvky a funkce:

### 1. **Spektrogram generátor**
   - Převod WAV souboru na spektrogramový obrázek (vizualizace frekvencí v čase)
   - Použití matplotlib pro vytváření spektrogramů
   - Výstup ve formátu PNG

### 2. **Bezeztrátový přenos audio → obraz**
   - Vkládání audio dat přímo do pixelů PNG obrázku
   - Skladování metadat (počet kanálů, sample width, frame rate, počet snímků)
   - Možnost extrahování původního zvuku bez ztráty dat

### 3. **Bezeztrátový přenos obraz → zvuk**
   - Vkládání obrazu do WAV souboru (8-bit mono, 44100 Hz)
   - Skladování metadat (šířka, výška, mode obrazu)
   - Obnova původního obrázku v originální kvalitě

### 4. **Steganografie**
   - Vkládání libovolného obrázku do zvuku
   - Extrahování obrázku ze zvuku
   - Podpora více formátů (PNG, JPG, BMP, atd.)

### 5. **Uživatelské rozhraní**
   - Tkinter GUI s přehledným výběrem módů
   - Funkce pro procházení souborů (file dialog)
   - Chybové hlášky při neplatných vstupech

### 6. **Příkazový řádek (CLI)**
   - Podpora pro automatizaci a skriptování
   - Různé režimy: `encode_audio`, `decode_audio`, `encode_image`, `decode_image`
   - Help s parametry

## Technická část

### Použité knihovny
- **wave** - Čtení a zápis WAV souborů
- **numpy** - Práce s poli dat a bitovými operacemi
- **matplotlib** - Generování spektrogramů
- **PIL (Pillow)** - Manipulace s obrázky
- **struct** - Binární packing/unpacking metadat
- **tkinter** - Vytváření GUI

### Algoritmy a datové struktury

#### Magic Bytes (Ověřovací mechanismus)
- `b'WAV!'` - Identifikátor pro audio vložené v obrázku
- `b'IMG!'` - Identifikátor pro obraz vložený ve zvuku
- Slouží k validaci dat při extrahování

#### Metadata Formáty

**Audio v obrázku (16 bajtů):**
```
[Magic (4B)] [Kanály (2B)] [Sample Width (2B)] [Frame Rate (4B)] [Počet snímků (4B)]
```

**Obraz ve zvuku (13+ bajtů):**
```
[Magic (4B)] [Šířka (4B)] [Výška (4B)] [Délka módu (1B)] [Mode string] [Obrazová data]
```

#### Převod pixelů
- RGB obrázky: 3 bajty = 1 pixel
- Spektrogram: matplotlib NFFT=1024, noverlap=512
- Padding nulami pro zarovnání rozměrů

### Pracovní postup

1. **Spektrogram:** WAV → matplotlib → PNG
2. **Audio→Obraz:** WAV + metadata → RGB bajty → PNG
3. **Obraz→Zvuk:** PNG → RGB bajty → WAV (1 kanál, 8-bit, 44100Hz)
4. **Obraz→Audio:** PNG → RGB bajty → WAV s metadaty
5. **Extrahování:** PNG/WAV → metadata validace → obraz/zvuk

### Režimy aplikace

| Režim | Vstup | Výstup | Popis |
| :---: | :---: | :---: | :--- |
| `spectrogram` | WAV | PNG | Vizualizace zvuku |
| `encode_audio` | WAV | PNG | Audio → Obraz (bezeztrátový) |
| `decode_audio` | PNG | WAV | Obraz → Audio (bezeztrátový) |
| `encode_image` | PNG/JPG | WAV | Obraz → Zvuk (steganografie) |
| `decode_image` | WAV | PNG | Zvuk → Obraz (steganografie) |
