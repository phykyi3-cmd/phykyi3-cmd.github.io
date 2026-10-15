import os, struct, json, re, base64

font_dir = '/Users/sithu/Desktop/Gemini 4/fonts'

def get_font_info(filename):
    path = os.path.join(font_dir, filename)
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'rb') as f: data = f.read()
        if len(data) < 12: return None
        num_tables = struct.unpack('>H', data[4:6])[0]
        tables = {}
        for i in range(num_tables):
            tag = data[12 + i*16 : 16 + i*16].decode('latin1', errors='ignore')
            off = struct.unpack('>I', data[12 + i*16 + 8 : 12 + i*16 + 12])[0]
            tables[tag] = off
        if 'name' not in tables: return None
        off = tables['name']
        _, count, string_offset = struct.unpack('>HHH', data[off:off+6])
        name_records = {}
        for i in range(count):
            plat, enc, lang, name_id, n_len, n_off = struct.unpack('>HHHHHH', data[off+6+i*12 : off+6+(i+1)*12])
            val_bytes = data[off + string_offset + n_off : off + string_offset + n_off + n_len]
            if plat in (0, 3) or enc == 1:
                try: val = val_bytes.decode('utf-16-be')
                except: val = val_bytes.decode('latin1', errors='ignore')
            else:
                val = val_bytes.decode('utf-8', errors='ignore')
            val = val.strip('\x00').strip()
            if val and (name_id not in name_records or len(val) > len(name_records[name_id])):
                name_records[name_id] = val
        
        has_u1000 = False
        if 'cmap' in tables:
            coff = tables['cmap']
            _, num_sub = struct.unpack('>HH', data[coff:coff+4])
            for i in range(num_sub):
                plat, enc, sub_off = struct.unpack('>HHI', data[coff+4+i*8 : coff+4+i*8+8])
                fmt = struct.unpack('>H', data[coff+sub_off : coff+sub_off+2])[0]
                if fmt == 4:
                    seg_x2 = struct.unpack('>H', data[coff+sub_off+6 : coff+sub_off+8])[0]
                    seg = seg_x2 // 2
                    ends = struct.unpack(f'>{seg}H', data[coff+sub_off+14 : coff+sub_off+14+seg*2])
                    starts = struct.unpack(f'>{seg}H', data[coff+sub_off+16+seg*2 : coff+sub_off+16+seg*4])
                    for s, e in zip(starts, ends):
                        if 0x1000 <= e and s <= 0x1049:
                            has_u1000 = True
                            break
                if has_u1000: break

        return {
            'file': filename,
            'family': name_records.get(1, ''),
            'subfamily': name_records.get(2, ''),
            'full': name_records.get(4, ''),
            'ps': name_records.get(6, ''),
            'unicode': has_u1000,
            'size': f"{len(data)//1024} KB"
        }
    except Exception as e:
        return None

# Load font db
files = sorted(os.listdir(font_dir))
font_db = {}
for f in files:
    if f.endswith(('.ttf', '.TTF', '.otf', '.OTF')):
        info = get_font_info(f)
        if info: font_db[f] = info

print(f"Loaded {len(font_db)} fonts from workspace fonts/.")

# Master Catalog Configuration
# Each entry specifies metadata, preferred file in font_db, and fallbacks
CATALOG_SPECS = [
    # ---------------- ART HOUSE SERIES & HEAVY HEADING ----------------
    {
        'id': 'arthouse-w01',
        'name': 'W01 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W01',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 95,
        'isWin': True,
        'file': 'W01Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W1 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'acgif;pOf pmvkH;tvS',
        'tags': ['w1', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w02',
        'name': 'W02 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W02',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 92,
        'isWin': True,
        'file': 'W02Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W2 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': "pmvkH;tvS 'DZdkif;",
        'tags': ['w2', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w03',
        'name': 'W03 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W03',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 90,
        'isWin': True,
        'file': 'W03Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W3 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'oD[dkMfrS nmPfjuD;Sifonf',
        'tags': ['w3', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w04',
        'name': 'W04 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W04',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 92,
        'isWin': True,
        'file': 'W04Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W4 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'r*Fvmyg jrefrmjynf',
        'tags': ['w4', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w05',
        'name': 'W05 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W05',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 90,
        'isWin': True,
        'file': 'W05Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W5 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'acgif;pOf pmvkH;tvS',
        'tags': ['w5', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w06',
        'name': 'W06 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W06',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 92,
        'isWin': True,
        'file': 'W06Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W6 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': "pmvkH;tvS 'DZdkif;",
        'tags': ['w6', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w07',
        'name': 'W07 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W07',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 90,
        'isWin': True,
        'file': 'W07Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W7 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'oD[dkMfrS nmPfjuD;Sifonf',
        'tags': ['w7', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w08',
        'name': 'W08 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W08',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 92,
        'isWin': True,
        'file': 'W08Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W8 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'r*Fvmyg jrefrmjynf',
        'tags': ['w8', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w09',
        'name': 'W09 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W09',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 90,
        'isWin': True,
        'file': 'W09Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W9 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'acgif;pOf pmvkH;tvS',
        'tags': ['w9', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w10',
        'name': 'W10 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W10',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 95,
        'isWin': True,
        'file': 'W10Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W10 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': "pmvkH;tvS 'DZdkif;",
        'tags': ['w10', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w11',
        'name': 'W11 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W11',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 90,
        'isWin': True,
        'file': 'W11Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W11 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'oD[dkMfrS nmPfjuD;Sifonf',
        'tags': ['w11', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w12',
        'name': 'W12 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W12',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 92,
        'isWin': True,
        'file': 'W12Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W12 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'r*Fvmyg jrefrmjynf',
        'tags': ['w12', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w13',
        'name': 'W13 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W13',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 90,
        'isWin': True,
        'file': 'W13Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W13 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'acgif;pOf pmvkH;tvS',
        'tags': ['w13', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w14',
        'name': 'W14 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W14',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 92,
        'isWin': True,
        'file': 'W14Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W14 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': "pmvkH;tvS 'DZdkif;",
        'tags': ['w14', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w15',
        'name': 'W15 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W15',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 90,
        'isWin': True,
        'file': 'W15Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W15 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'oD[dkMfrS nmPfjuD;Sifonf',
        'tags': ['w15', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w16',
        'name': 'W16 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W16',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 92,
        'isWin': True,
        'file': 'W16Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W16 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'r*Fvmyg jrefrmjynf',
        'tags': ['w16', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w17',
        'name': 'W17 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W17',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 90,
        'isWin': True,
        'file': 'W17Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W17 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'acgif;pOf pmvkH;tvS',
        'tags': ['w17', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w18',
        'name': 'W18 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W18',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 92,
        'isWin': True,
        'file': 'W18Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W18 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': "pmvkH;tvS 'DZdkif;",
        'tags': ['w18', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w19',
        'name': 'W19 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W19',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 90,
        'isWin': True,
        'file': 'W19Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W19 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'oD[dkMfrS nmPfjuD;Sifonf',
        'tags': ['w19', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w20',
        'name': 'W20 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W20',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 92,
        'isWin': True,
        'file': 'W20Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W20 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'r*Fvmyg jrefrmjynf',
        'tags': ['w20', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w21',
        'name': 'W21 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W21',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 95,
        'isWin': True,
        'file': 'W21Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W21 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'acgif;pOf pmvkH;tvS',
        'tags': ['w21', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w21-bold',
        'name': 'W21 Art House Bold',
        'mmName': 'အာ့ထ်ဟောက်စ် W21 (စာလုံးထူ)',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 97,
        'isWin': True,
        'file': 'W21Art House-Bold.TTF',
        'description': 'Art House စီးရီး၏ ပိုမိုထူထဲခိုင်မာသော W21 စာလုံးထူ (Bold) ဖောင့်။ ခေါင်းစဉ်များအတွက် အထူးပေါ်လွင်သည်။',
        'sampleWin': 'r*Fvmyg jrefrmjynf',
        'tags': ['w21', 'arthouse', 'art', 'heading', 'poster', 'win', 'bold']
    },
    {
        'id': 'arthouse-w22',
        'name': 'W22 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W22',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 92,
        'isWin': True,
        'file': 'W22Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W22 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': "pmvkH;tvS 'DZdkif;",
        'tags': ['w22', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w23',
        'name': 'W23 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W23',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 90,
        'isWin': True,
        'file': 'W23Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W23 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'oD[dkMfrS nmPfjuD;Sifonf',
        'tags': ['w23', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w24',
        'name': 'W24 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W24',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 92,
        'isWin': True,
        'file': 'W24Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W24 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'r*Fvmyg jrefrmjynf',
        'tags': ['w24', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w25',
        'name': 'W25 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W25',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 90,
        'isWin': True,
        'file': 'W25Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W25 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'acgif;pOf pmvkH;tvS',
        'tags': ['w25', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w26',
        'name': 'W26 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W26',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 92,
        'isWin': True,
        'file': 'W26Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W26 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': "pmvkH;tvS 'DZdkif;",
        'tags': ['w26', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w27',
        'name': 'W27 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W27',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 90,
        'isWin': True,
        'file': 'W27Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W27 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'oD[dkMfrS nmPfjuD;Sifonf',
        'tags': ['w27', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w28',
        'name': 'W28 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W28',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 92,
        'isWin': True,
        'file': 'W28Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W28 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'r*Fvmyg jrefrmjynf',
        'tags': ['w28', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w29',
        'name': 'W29 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W29',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 90,
        'isWin': True,
        'file': 'W29Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W29 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'acgif;pOf pmvkH;tvS',
        'tags': ['w29', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w30',
        'name': 'W30 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W30',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 98,
        'isWin': True,
        'file': 'W30Art House.TTF',
        'description': 'Art House မှ နာမည်ကျော် လက်ရေးလှနှင့် ဇာတ်ကောင်ခေါင်းစဉ်သုံး စာလုံးအလှဖောင့်။',
        'sampleWin': 'acgif;pOf pmvkH;tvS',
        'tags': ['w30', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w31',
        'name': 'W31 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W31',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 90,
        'isWin': True,
        'file': 'W31Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W31 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'oD[dkMfrS nmPfjuD;Sifonf',
        'tags': ['w31', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w31-bold',
        'name': 'W31 Art House Bold',
        'mmName': 'အာ့ထ်ဟောက်စ် W31 (စာလုံးထူ)',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 97,
        'isWin': True,
        'file': 'W31Art House-Bold.TTF',
        'description': 'Art House စီးရီး၏ ပိုမိုထူထဲခိုင်မာသော W31 စာလုံးထူ (Bold) ဖောင့်။ ခေါင်းစဉ်များအတွက် အထူးပေါ်လွင်သည်။',
        'sampleWin': 'r*Fvmyg jrefrmjynf',
        'tags': ['w31', 'arthouse', 'art', 'heading', 'poster', 'win', 'bold']
    },
    {
        'id': 'arthouse-w32',
        'name': 'W32 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W32',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 96,
        'isWin': True,
        'file': 'W32Art House.TTF',
        'description': 'ပိုစတာဒီဇိုင်းနှင့် ဗီဒီယိုခေါင်းစဉ်များအတွက် ဆန်းပြားသော Art House W32 ဖောင့်။',
        'sampleWin': "pmvkH;tvS 'DZdkif;",
        'tags': ['w32', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w33',
        'name': 'W33 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W33',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 90,
        'isWin': True,
        'file': 'W33Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W33 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'acgif;pOf pmvkH;tvS',
        'tags': ['w33', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w34',
        'name': 'W34 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W34',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 92,
        'isWin': True,
        'file': 'W34Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W34 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': "pmvkH;tvS 'DZdkif;",
        'tags': ['w34', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w35',
        'name': 'W35 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W35',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 95,
        'isWin': True,
        'file': 'W35Art House.TTF',
        'description': 'အနုပညာလက်ရာဆန်သော စာလုံးထူ Art House W35။',
        'sampleWin': 'jrefrmazmifh tvS',
        'tags': ['w35', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w36',
        'name': 'W36 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W36',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 92,
        'isWin': True,
        'file': 'W36Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W36 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'r*Fvmyg jrefrmjynf',
        'tags': ['w36', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w37',
        'name': 'W37 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W37',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 90,
        'isWin': True,
        'file': 'W37Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W37 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'acgif;pOf pmvkH;tvS',
        'tags': ['w37', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w37-bold',
        'name': 'W37 Art House Bold',
        'mmName': 'အာ့ထ်ဟောက်စ် W37 (စာလုံးထူ)',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 97,
        'isWin': True,
        'file': 'W37Art House-Bold.TTF',
        'description': 'Art House စီးရီး၏ ပိုမိုထူထဲခိုင်မာသော W37 စာလုံးထူ (Bold) ဖောင့်။ ခေါင်းစဉ်များအတွက် အထူးပေါ်လွင်သည်။',
        'sampleWin': 'r*Fvmyg jrefrmjynf',
        'tags': ['w37', 'arthouse', 'art', 'heading', 'poster', 'win', 'bold']
    },
    {
        'id': 'arthouse-w38',
        'name': 'W38 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W38',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 92,
        'isWin': True,
        'file': 'W38Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W38 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': "pmvkH;tvS 'DZdkif;",
        'tags': ['w38', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w39',
        'name': 'W39 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W39',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 90,
        'isWin': True,
        'file': 'W39Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W39 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'oD[dkMfrS nmPfjuD;Sifonf',
        'tags': ['w39', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w40',
        'name': 'W40 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W40',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 92,
        'isWin': True,
        'file': 'W40Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W40 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'r*Fvmyg jrefrmjynf',
        'tags': ['w40', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w46',
        'name': 'W46 Art House Edition 2007',
        'mmName': 'အာ့ထ်ဟောက်စ် W46 (၂၀၀၇)',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2007',
        'license': 'Freeware (Design Use)',
        'popular': 94,
        'isWin': True,
        'file': 'W46Art House-2ndEdition2007.ttf',
        'description': 'ဂန္တဝင် Art House W46 စာလုံးအလှ ဖောင့်ဗားရှင်း ၂၀၀၇ (Art House Graphic Studio Mandalay)။',
        'sampleWin': "pmvkH;tvS 'DZdkif;",
        'tags': ['w46', 'arthouse', 'art', 'heading', 'poster', 'win', '2007', 'edition']
    },
    {
        'id': 'arthouse-w47',
        'name': 'W47 Art House Edition 2007',
        'mmName': 'အာ့ထ်ဟောက်စ် W47 (၂၀၀၇)',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2007',
        'license': 'Freeware (Design Use)',
        'popular': 94,
        'isWin': True,
        'file': 'W47Art House-2ndEdition2007.ttf',
        'description': 'ဂန္တဝင် Art House W47 စာလုံးအလှ ဖောင့်ဗားရှင်း ၂၀၀၇ (Art House Graphic Studio Mandalay)။',
        'sampleWin': 'oD[dkMfrS nmPfjuD;Sifonf',
        'tags': ['w47', 'arthouse', 'art', 'heading', 'poster', 'win', '2007', 'edition']
    },
    {
        'id': 'arthouse-w48',
        'name': 'W48 Art House Edition 2007',
        'mmName': 'အာ့ထ်ဟောက်စ် W48 (၂၀၀၇)',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2007',
        'license': 'Freeware (Design Use)',
        'popular': 97,
        'isWin': True,
        'file': 'W48Art House-2ndEdition2007.ttf',
        'description': 'အလွန်လှပလူကြိုက်များသော Art House W48 အလှဖောင့်။ မဂ္ဂဇင်းနှင့် ပိုစတာဒီဇိုင်းသုံး။',
        'sampleWin': 'acgif;pOf pmvkH;tvS',
        'tags': ['w48', 'arthouse', 'art', 'heading', 'poster', 'win', 'bold', '2007', 'edition']
    },
    {
        'id': 'arthouse-w49',
        'name': 'W49 Art House Edition 2007',
        'mmName': 'အာ့ထ်ဟောက်စ် W49 (၂၀၀၇)',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2007',
        'license': 'Freeware (Design Use)',
        'popular': 94,
        'isWin': True,
        'file': 'W49Art House-2ndEdition2007.ttf',
        'description': 'ဂန္တဝင် Art House W49 စာလုံးအလှ ဖောင့်ဗားရှင်း ၂၀၀၇ (Art House Graphic Studio Mandalay)။',
        'sampleWin': 'acgif;pOf pmvkH;tvS',
        'tags': ['w49', 'arthouse', 'art', 'heading', 'poster', 'win', '2007', 'edition']
    },
    {
        'id': 'arthouse-w50',
        'name': 'W50 Art House Edition 2007',
        'mmName': 'အာ့ထ်ဟောက်စ် W50 (၂၀၀၇)',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2007',
        'license': 'Freeware (Design Use)',
        'popular': 94,
        'isWin': True,
        'file': 'W50Art House-2ndEdition2007.ttf',
        'description': 'ဂန္တဝင် Art House W50 စာလုံးအလှ ဖောင့်ဗားရှင်း ၂၀၀၇ (Art House Graphic Studio Mandalay)။',
        'sampleWin': "pmvkH;tvS 'DZdkif;",
        'tags': ['w50', 'arthouse', 'art', 'heading', 'poster', 'win', 'bold', '2007', 'edition']
    },
    {
        'id': 'arthouse-w51',
        'name': 'W51 Art House Edition 2007',
        'mmName': 'အာ့ထ်ဟောက်စ် W51 (၂၀၀၇)',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2007',
        'license': 'Freeware (Design Use)',
        'popular': 94,
        'isWin': True,
        'file': 'W51Art House-2ndEdition2007.ttf',
        'description': 'ဂန္တဝင် Art House W51 စာလုံးအလှ ဖောင့်ဗားရှင်း ၂၀၀၇ (Art House Graphic Studio Mandalay)။',
        'sampleWin': 'oD[dkMfrS nmPfjuD;Sifonf',
        'tags': ['w51', 'arthouse', 'art', 'heading', 'poster', 'win', '2007', 'edition']
    },
    {
        'id': 'arthouse-w52',
        'name': 'W52 Art House Edition 2007',
        'mmName': 'အာ့ထ်ဟောက်စ် W52 (၂၀၀၇)',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2007',
        'license': 'Freeware (Design Use)',
        'popular': 98,
        'isWin': True,
        'file': 'W52Art House-2ndEdition2007.ttf',
        'description': 'ခေတ်မီဆန်းပြားသော Art House W52 စာလုံးအထူဖောင့်။ ပိုစတာနှင့် ဗီဒီယိုခေါင်းစဉ်များအတွက် အလွန်ထင်ရှားသည်။',
        'sampleWin': 'acgif;pOf pmvkH;tvS',
        'tags': ['w52', 'arthouse', 'art', 'heading', 'poster', 'win', 'bold', '2007', 'edition']
    },
    {
        'id': 'arthouse-w56',
        'name': 'W56 Art House Edition 2007',
        'mmName': 'အာ့ထ်ဟောက်စ် W56 (၂၀၀၇)',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2007',
        'license': 'Freeware (Design Use)',
        'popular': 94,
        'isWin': True,
        'file': 'W56Art House-2ndEdition2007.ttf',
        'description': 'ဂန္တဝင် Art House W56 စာလုံးအလှ ဖောင့်ဗားရှင်း ၂၀၀၇ (Art House Graphic Studio Mandalay)။',
        'sampleWin': 'r*Fvmyg jrefrmjynf',
        'tags': ['w56', 'arthouse', 'art', 'heading', 'poster', 'win', '2007', 'edition']
    },
    {
        'id': 'arthouse-w57',
        'name': 'W57 Art House Edition 2007',
        'mmName': 'အာ့ထ်ဟောက်စ် W57 (၂၀၀၇)',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2007',
        'license': 'Freeware (Design Use)',
        'popular': 94,
        'isWin': True,
        'file': 'W57Art House-2ndEdition2007.ttf',
        'description': 'ဂန္တဝင် Art House W57 စာလုံးအလှ ဖောင့်ဗားရှင်း ၂၀၀၇ (Art House Graphic Studio Mandalay)။',
        'sampleWin': 'acgif;pOf pmvkH;tvS',
        'tags': ['w57', 'arthouse', 'art', 'heading', 'poster', 'win', '2007', 'edition']
    },
    {
        'id': 'arthouse-w58',
        'name': 'W58 Art House Edition 2007',
        'mmName': 'အာ့ထ်ဟောက်စ် W58 (၂၀၀၇)',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2007',
        'license': 'Freeware (Design Use)',
        'popular': 94,
        'isWin': True,
        'file': 'W58Art House-2ndEdition2007.ttf',
        'description': 'ဂန္တဝင် Art House W58 စာလုံးအလှ ဖောင့်ဗားရှင်း ၂၀၀၇ (Art House Graphic Studio Mandalay)။',
        'sampleWin': "pmvkH;tvS 'DZdkif;",
        'tags': ['w58', 'arthouse', 'art', 'heading', 'poster', 'win', '2007', 'edition']
    },
    {
        'id': 'arthouse-w60',
        'name': 'W60 Art House Edition 2007',
        'mmName': 'အာ့ထ်ဟောက်စ် W60 (၂၀၀၇)',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2007',
        'license': 'Freeware (Design Use)',
        'popular': 100,
        'isWin': True,
        'file': 'W60Art House-2ndEdition2007.ttf',
        'description': 'မြန်မာစာလုံးထူဖောင့်များထဲတွင် အကျော်ကြားဆုံးဖြစ်ပြီး ယူကျုခေါင်းစဉ်၊ ပိုစတာနှင့် စာတန်းထိုးများအတွက် အထူးသင့်တော်သည်။ (Win Layout သုံးဖောင့်ဖြစ်သဖြင့် ရိုက်ထည့်သမျှ Unicode စာသားများကို Auto-Engine ဖြင့် မူရင်း Art House အတိုင်း အလိုအလျောက် ပြောင်းလဲပြသပေးပါသည်)',
        'sampleWin': 'r*Fvmyg jrefrmjynf',
        'tags': ['w60', 'arthouse', 'art', 'heading', 'poster', 'win', 'bold', '2007', 'edition']
    },
    {
        'id': 'arthouse-w61',
        'name': 'W61 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W61',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 90,
        'isWin': True,
        'file': 'W61Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W61 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'acgif;pOf pmvkH;tvS',
        'tags': ['w61', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w61-bold',
        'name': 'W61 Art House Bold',
        'mmName': 'အာ့ထ်ဟောက်စ် W61 (စာလုံးထူ)',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 97,
        'isWin': True,
        'file': 'W61Art House-Bold.TTF',
        'description': 'Art House စီးရီး၏ ပိုမိုထူထဲခိုင်မာသော W61 စာလုံးထူ (Bold) ဖောင့်။ ခေါင်းစဉ်များအတွက် အထူးပေါ်လွင်သည်။',
        'sampleWin': 'r*Fvmyg jrefrmjynf',
        'tags': ['w61', 'arthouse', 'art', 'heading', 'poster', 'win', 'bold']
    },
    {
        'id': 'arthouse-w61-extrabold',
        'name': 'W61 Art House ExtraBold',
        'mmName': 'အာ့ထ်ဟောက်စ် W61 (စာလုံးအလွန်ထူ)',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 97,
        'isWin': True,
        'file': 'W61Art House-ExtraBold.TTF',
        'description': 'Art House စီးရီး၏ အလွန်ထူထဲသော W61 ExtraBold ဖောင့်။ ပိုစတာနှင့် ကြော်ငြာစာလုံးများအတွက် အထူးသင့်တော်သည်။',
        'sampleWin': 'r*Fvmyg jrefrmjynf',
        'tags': ['w61', 'arthouse', 'art', 'heading', 'poster', 'win', 'bold']
    },
    {
        'id': 'arthouse-w61-italic',
        'name': 'W61 Art House Italic',
        'mmName': 'အာ့ထ်ဟောက်စ် W61 (စာလုံးစောင်း)',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 93,
        'isWin': True,
        'file': 'W61Art House-Italic.TTF',
        'description': 'Art House စီးရီး၏ စာလုံးစောင်းဟန် W61 Italic အနုပညာဖောင့်။',
        'sampleWin': 'oD[dkMfrS nmPfjuD;Sifonf',
        'tags': ['w61', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w62',
        'name': 'W62 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W62',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 92,
        'isWin': True,
        'file': 'W62Art House.TTF',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W62 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': "pmvkH;tvS 'DZdkif;",
        'tags': ['w62', 'arthouse', 'art', 'heading', 'poster', 'win', 'bold']
    },
    {
        'id': 'arthouse-w62-bold',
        'name': 'W62 Art House Bold',
        'mmName': 'အာ့ထ်ဟောက်စ် W62 (စာလုံးထူ)',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 97,
        'isWin': True,
        'file': 'W62Art House-Bold.TTF',
        'description': 'Art House စီးရီး၏ ပိုမိုထူထဲခိုင်မာသော W62 စာလုံးထူ (Bold) ဖောင့်။ ခေါင်းစဉ်များအတွက် အထူးပေါ်လွင်သည်။',
        'sampleWin': 'r*Fvmyg jrefrmjynf',
        'tags': ['w62', 'arthouse', 'art', 'heading', 'poster', 'win', 'bold']
    },
    {
        'id': 'arthouse-w63',
        'name': 'W63 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W63',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 90,
        'isWin': True,
        'file': 'W63Art House.ttf',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W63 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'oD[dkMfrS nmPfjuD;Sifonf',
        'tags': ['w63', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w64',
        'name': 'W64 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W64',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 92,
        'isWin': True,
        'file': 'W64Art House.ttf',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W64 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'r*Fvmyg jrefrmjynf',
        'tags': ['w64', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w65',
        'name': 'W65 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W65',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 90,
        'isWin': True,
        'file': 'W65Art House.ttf',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W65 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'acgif;pOf pmvkH;tvS',
        'tags': ['w65', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w66',
        'name': 'W66 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W66',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 92,
        'isWin': True,
        'file': 'W66Art House.ttf',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W66 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': "pmvkH;tvS 'DZdkif;",
        'tags': ['w66', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w67',
        'name': 'W67 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W67',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 90,
        'isWin': True,
        'file': 'W67Art House.ttf',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W67 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'oD[dkMfrS nmPfjuD;Sifonf',
        'tags': ['w67', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w68',
        'name': 'W68 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W68',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 92,
        'isWin': True,
        'file': 'W68Art House.ttf',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W68 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'r*Fvmyg jrefrmjynf',
        'tags': ['w68', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w69',
        'name': 'W69 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W69',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 90,
        'isWin': True,
        'file': 'W69Art House.ttf',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W69 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': 'acgif;pOf pmvkH;tvS',
        'tags': ['w69', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'arthouse-w70',
        'name': 'W70 Art House',
        'mmName': 'အာ့ထ်ဟောက်စ် W70',
        'category': 'arthouse',
        'categoryLabel': 'Art House Series',
        'designer': 'Art House Graphic Studio (Mandalay)',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 95,
        'isWin': True,
        'file': 'W70Art House.ttf',
        'description': 'Art House Graphic Studio (Mandalay) မှ ဖန်တီးခဲ့သော ဂန္တဝင် W70 မြန်မာစာလုံးအလှဖောင့်။',
        'sampleWin': "pmvkH;tvS 'DZdkif;",
        'tags': ['w70', 'arthouse', 'art', 'heading', 'poster', 'win']
    },
    {
        'id': 'uni-myanmar-bagan',
        'name': 'Uni-Myanmar Bagan',
        'mmName': 'ပုဂံ ရိုးရာဟန် စာလုံးထူ',
        'category': 'arthouse',
        'categoryLabel': 'Art House & Bold',
        'designer': 'Bagan Type Studio',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 99,
        'isWin': False,
        'file': 'Uni-Myanmar Bagan.ttf',
        'githubRel': 'lecramyajiv/fonts-myanmar-extra/master/TTF/Myanmar-Black.ttf',
        'description': 'ပုဂံခေတ် ရိုးရာလက်ရာအငွေ့အသက်ပါရှိသည့် ယူနီကုဒ် ပုဂံဖောင့်ဖြစ်ပြီး ခေါင်းစဉ်များအတွက် အထူးပေါ်လွင်သည်။ (Unicode 100% စံချိန်မီ)',
        'tags': ['bagan', 'uni-myanmar', 'traditional', 'ပုဂံ', 'bold']
    },
    {
        'id': 'uni-myanmar-black',
        'name': 'Uni-Myanmar Black',
        'mmName': 'ယူနီ-မြန်မာ ဘလက်ခ် (အလွန်ထူ)',
        'category': 'arthouse',
        'categoryLabel': 'Art House & Bold',
        'designer': 'AungMyoKyaw / Unicode Studio',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 99,
        'isWin': False,
        'file': 'Uni-MyanmarBlack.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarBlack/MyanmarBlack.ttf',
        'description': 'Art House စာလုံးထူများကဲ့သို့ ထူထဲပြည့်ဝပြီး Unicode စံချိန်မီ ရေးဆွဲထားသော Heavy Black ဖောင့်။ YouTube သမ်နေးလ်နှင့် ပိုစတာများတွင် လူသုံးအများဆုံး။',
        'tags': ['black', 'bold', 'heavy', 'headline', 'thumbnail']
    },
    {
        'id': 'uni-myanmar-headone',
        'name': 'Uni-Myanmar HeadOne',
        'mmName': 'ဟက်ဒ်ဝမ်း ခေါင်းစဉ်ဖောင့်',
        'category': 'arthouse',
        'categoryLabel': 'Art House & Bold',
        'designer': 'HeadOne Studio',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 96,
        'isWin': False,
        'file': 'Uni-MyanmarHeadOne.ttf',
        'githubRel': 'lecramyajiv/fonts-myanmar-extra/master/TTF/Myanmar-HeadOne.ttf',
        'description': 'သတင်းစာနှင့် မီဒီယာဗီဒီယိုခေါင်းစဉ်များအတွက် အထူးဒီဇိုင်းထုတ်ထားသော HeadOne ခေါင်းစဉ်ဖောင့်။',
        'tags': ['headone', 'heading', 'bold', 'media']
    },

    # ---------------- MASTERPIECE & ROUND SERIES ----------------
    {
        'id': 'masterpiece-uni-round',
        'name': 'Masterpiece Uni Round',
        'mmName': 'မာစတာပိစ် စာလုံးဝိုင်း',
        'category': 'masterpiece',
        'categoryLabel': 'Masterpiece Series',
        'designer': 'Masterpiece / Saturngod',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 100,
        'isWin': False,
        'file': 'Uni-MasterpieceUniRound.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MasterpieceUniRound/MasterpieceUniRound.ttf',
        'description': 'iPhone / macOS တို့တွင် လူကြိုက်အများဆုံးဖြစ်ခဲ့သော စာလုံးအဝိုင်းဒီဇိုင်းဖောင့်ဖြစ်ပြီး သပ်ရပ်ချောမွေ့သော ခေတ်မီဟန်အပြည့်ရှိသည်။',
        'tags': ['masterpiece', 'round', 'ios', 'mac', 'modern']
    },
    {
        'id': 'masterpiece-uni-hand',
        'name': 'Masterpiece Uni Hand',
        'mmName': 'မာစတာပိစ် လက်ရေးဖောင့်',
        'category': 'masterpiece',
        'categoryLabel': 'Masterpiece Series',
        'designer': 'Masterpiece Studio',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 97,
        'isWin': False,
        'file': 'MasterpieceUniHand.ttf',
        'githubRel': 'lecramyajiv/fonts-myanmar-extra/master/TTF/MasterpieceUniHand.ttf',
        'description': 'သဘာဝကျကျ ရေးသားထားသော မာစတာပိစ်လက်ရေးဟန် ယူနီကုဒ်ဖောင့်။',
        'tags': ['masterpiece', 'handwriting', 'hand']
    },
    {
        'id': 'masterpiece-yaychanzin',
        'name': 'Masterpiece YayChanZin',
        'mmName': 'မာစတာပိစ် ရေချမ်းစင်',
        'category': 'masterpiece',
        'categoryLabel': 'Masterpiece Series',
        'designer': 'Masterpiece Studio',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 96,
        'isWin': False,
        'file': 'MasterpieceYayChanZin.ttf',
        'githubRel': 'lecramyajiv/fonts-myanmar-extra/master/TTF/MasterpieceYayChanZin.ttf',
        'description': 'မြန်မာ့ရေချမ်းစင် ရိုးရာအငွေ့အသက်နှင့် မာစတာပိစ်ဒီဇိုင်း ပေါင်းစပ်ဖန်တီးထားသော ဖောင့်။',
        'tags': ['masterpiece', 'yaychanzin', 'traditional']
    },
    {
        'id': 'uni-myanmar-cherry-pro',
        'name': 'Uni-Myanmar Cherry Pro',
        'mmName': 'ချက်ရီ ပရို အလှဖောင့်',
        'category': 'masterpiece',
        'categoryLabel': 'Masterpiece & Round',
        'designer': 'Cherry Pro Team',
        'version': '3.0',
        'license': 'Free Open Source',
        'popular': 99,
        'isWin': False,
        'file': 'Uni-Myanmar Cherry Pro.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/CherryUnicode/Cherry_Unicode.ttf',
        'description': 'လူငယ်ကြိုက် ချက်ရီပန်း ဒီဇိုင်းပါရှိသော Uni-Myanmar Cherry Pro ချစ်စရာအလှဖောင့်။',
        'tags': ['cherry', 'pro', 'cute', 'round']
    },
    {
        'id': 'uni-myanmar-cherry-win',
        'name': 'Uni-Myanmar Cherry Win',
        'mmName': 'ချက်ရီ ဝင်း ဖောင့်အလှ',
        'category': 'masterpiece',
        'categoryLabel': 'Masterpiece & Round',
        'designer': 'Cherry Type Team',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 95,
        'isWin': False,
        'file': 'Uni-Myanmar Cherry Win.ttf',
        'tags': ['cherry', 'win', 'cute']
    },
    {
        'id': 'uni-choco-cooky',
        'name': 'Uni-Myanmar Choco Cooky',
        'mmName': 'ချိုကိုကွတ်ကီး ဖောင့်အလှ',
        'category': 'masterpiece',
        'categoryLabel': 'Masterpiece & Round',
        'designer': 'Cooky Type Studio',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 98,
        'isWin': False,
        'file': 'Uni-Choco Cooky.ttf',
        'tags': ['choco', 'cooky', 'cute', 'round']
    },
    {
        'id': 'uni-kitty',
        'name': 'Uni-Myanmar Kitty',
        'mmName': 'ကိတ်တီ ချစ်စရာဖောင့်',
        'category': 'masterpiece',
        'categoryLabel': 'Masterpiece & Round',
        'designer': 'Kitty Studio',
        'version': '1.5',
        'license': 'Freeware',
        'popular': 97,
        'isWin': False,
        'file': 'Uni-Myanmar Kitty.ttf',
        'tags': ['kitty', 'cute', 'round']
    },
    {
        'id': 'uni-sweetie',
        'name': 'Uni-Myanmar Sweetie',
        'mmName': 'ဆွီတီ အလှဖောင့်',
        'category': 'masterpiece',
        'categoryLabel': 'Masterpiece & Round',
        'designer': 'Sweetie Type',
        'version': '1.5',
        'license': 'Freeware',
        'popular': 98,
        'isWin': False,
        'file': 'Uni-Myanmar Sweetie.ttf',
        'tags': ['sweetie', 'cute', 'round']
    },
    {
        'id': 'uni-jasmine',
        'name': 'Uni-Jasmine Unicode',
        'mmName': 'စံပယ်ဖြူ ယူနီကုဒ်',
        'category': 'masterpiece',
        'categoryLabel': 'Masterpiece & Round',
        'designer': 'AungMyoKyaw',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 96,
        'isWin': False,
        'file': 'Uni- JasmineUnicode.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/JasmineUnicode/Jasmine_Unicode.ttf',
        'tags': ['jasmine', 'cute', 'flower']
    },
    {
        'id': 'uni-kyarpan',
        'name': 'Uni-Myanmar Kyarpan',
        'mmName': 'ကြာပန်း အလှဖောင့်',
        'category': 'masterpiece',
        'categoryLabel': 'Masterpiece & Round',
        'designer': 'Kyarpan Studio',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 95,
        'isWin': False,
        'file': 'Uni-Myanmar Kyarpan.ttf',
        'tags': ['kyarpan', 'cute', 'flower']
    },
    {
        'id': 'uni-sabae',
        'name': 'Uni-Myanmar Sabae',
        'mmName': 'စံပယ် ဖောင့်အလှ',
        'category': 'masterpiece',
        'categoryLabel': 'Masterpiece & Round',
        'designer': 'AungMyoKyaw',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 96,
        'isWin': False,
        'file': 'Uni-MyanmarSabae.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarSabae/MyanmarSabae.ttf',
        'tags': ['sabae', 'cute', 'round']
    },
    {
        'id': 'uni-sagar',
        'name': 'Uni-Myanmar Sagar',
        'mmName': 'စကား ဖောင့်အလှ',
        'category': 'masterpiece',
        'categoryLabel': 'Masterpiece & Round',
        'designer': 'AungMyoKyaw',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 95,
        'isWin': False,
        'file': 'Uni-MyanmarSagar.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarSagar/MyanmarSagar.ttf',
        'tags': ['sagar', 'cute']
    },
    {
        'id': 'uni-khyay',
        'name': 'Uni-Myanmar Khyay',
        'mmName': 'ခရေ အလှဖောင့်',
        'category': 'masterpiece',
        'categoryLabel': 'Masterpiece & Round',
        'designer': 'Khyay Type Project',
        'version': '2.0',
        'license': 'SIL OFL',
        'popular': 99,
        'isWin': False,
        'file': 'Uni-MyanmarKhyay.ttf',
        'githubRel': 'lecramyajiv/fonts-myanmar-extra/master/TTF/Myanmar-Khyay.ttf',
        'tags': ['khyay', 'cute', 'round', 'capcut']
    },

    # ---------------- AKA & HANDWRITING COLLECTION ----------------
    {
        'id': 'aka02-regular',
        'name': 'Aka02-Regular (အကာ ၀၂)',
        'mmName': 'အကာ ၀၂ လက်ရေးလှဖောင့်',
        'category': 'handwriting',
        'categoryLabel': 'Aka Handwriting',
        'designer': 'Aka Type Design',
        'version': '2.0',
        'license': 'Freeware (Design Use)',
        'popular': 98,
        'isWin': False,
        'file': 'Aka02-Regular.ttf',
        'description': 'Aka စီးရီးထဲတွင် အကျော်ကြားဆုံးနှင့် အသုံးအများဆုံး လက်ရေးလှဖောင့်ဖြစ်ပြီး သဘာဝလက်ရေးဟန် အလွန်လှပသည်။',
        'tags': ['aka', 'aka02', 'handwriting', 'script']
    },
    {
        'id': 'aka03-regular',
        'name': 'Aka03-Regular (အကာ ၀၃)',
        'mmName': 'အကာ ၀၃ လက်ရေးလှ',
        'category': 'handwriting',
        'categoryLabel': 'Aka Handwriting',
        'designer': 'Aka Type Design',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 96,
        'isWin': False,
        'file': 'Aka03-Regular.ttf',
        'description': 'Aka စီးရီးမှ ချစ်စရာလက်ရေးလှ Aka03 ဖောင့်။',
        'tags': ['aka', 'aka03', 'handwriting']
    },
    {
        'id': 'aka05-regular',
        'name': 'Aka05-Regular (အကာ ၀၅)',
        'mmName': 'အကာ ၀၅ ဒီဇိုင်းစာလုံး',
        'category': 'handwriting',
        'categoryLabel': 'Aka Handwriting',
        'designer': 'Aka Type Design',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 95,
        'isWin': False,
        'file': 'Aka05-Regular.ttf',
        'tags': ['aka', 'aka05', 'handwriting']
    },
    {
        'id': 'aka06-regular',
        'name': 'Aka06-Regular (အကာ ၀၆)',
        'mmName': 'အကာ ၀၆ လက်ရေးလှ',
        'category': 'handwriting',
        'categoryLabel': 'Aka Handwriting',
        'designer': 'Aka Type Design',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 94,
        'isWin': False,
        'file': 'Aka06-Regular.ttf',
        'tags': ['aka', 'aka06', 'handwriting']
    },
    {
        'id': 'aka08-regular',
        'name': 'Aka08-Regular (အကာ ၀၈)',
        'mmName': 'အကာ ၀၈ လက်ရေးလှ',
        'category': 'handwriting',
        'categoryLabel': 'Aka Handwriting',
        'designer': 'Aka Type Design',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 95,
        'isWin': False,
        'file': 'Aka08-Regular.ttf',
        'tags': ['aka', 'aka08', 'handwriting']
    },
    {
        'id': 'aka09-regular',
        'name': 'Aka09-Regular (အကာ ၀၉)',
        'mmName': 'အကာ ၀၉ လက်ရေးလှ',
        'category': 'handwriting',
        'categoryLabel': 'Aka Handwriting',
        'designer': 'Aka Type Design',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 96,
        'isWin': False,
        'file': 'Aka09-Regular.ttf',
        'tags': ['aka', 'aka09', 'handwriting']
    },
    {
        'id': 'aka10-light',
        'name': 'Aka10-Light (အကာ ၁၀)',
        'mmName': 'အကာ ၁၀ ပါးလွှာအလှ',
        'category': 'handwriting',
        'categoryLabel': 'Aka Handwriting',
        'designer': 'Aka Type Design',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 94,
        'isWin': False,
        'file': 'Aka10-Light.ttf',
        'tags': ['aka', 'aka10', 'light', 'handwriting']
    },
    {
        'id': 'aka11-bold',
        'name': 'Aka011-Bold (အကာ ၁၁ စာလုံးထူ)',
        'mmName': 'အကာ ၁၁ စာလုံးထူအလှ',
        'category': 'handwriting',
        'categoryLabel': 'Aka Handwriting',
        'designer': 'Aka Type Design',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 97,
        'isWin': False,
        'file': 'Aka011-Bold.ttf',
        'description': 'Aka စီးရီးမှ ခေါင်းစဉ်သုံး စာလုံးထူ Aka011-Bold ဖောင့်။',
        'tags': ['aka', 'aka011', 'bold', 'handwriting']
    },
    {
        'id': 'aka11-regular',
        'name': 'Aka011-Regular (အကာ ၁၁ မူရင်း)',
        'mmName': 'အကာ ၁၁ လက်ရေးလှ',
        'category': 'handwriting',
        'categoryLabel': 'Aka Handwriting',
        'designer': 'Aka Type Design',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 95,
        'isWin': False,
        'file': 'Aka011-Regular.ttf',
        'tags': ['aka', 'aka011', 'handwriting']
    },
    {
        'id': 'uni-burmese-01',
        'name': 'Uni-Burmese Handwriting 01 (Style 1)',
        'mmName': 'မြန်မာလက်ရေးလှ စတိုင် ၀၁',
        'category': 'handwriting',
        'categoryLabel': 'Handwriting Series',
        'designer': 'Burmese Handwriting Team',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 93,
        'isWin': False,
        'file': 'Uni-Burmese Handwriting 01_Style 01_Regular.ttf',
        'tags': ['burmese', 'handwriting', 'style01']
    },
    {
        'id': 'uni-burmese-02',
        'name': 'Uni-Burmese Handwriting 01 (Style 2)',
        'mmName': 'မြန်မာလက်ရေးလှ စတိုင် ၀၂',
        'category': 'handwriting',
        'categoryLabel': 'Handwriting Series',
        'designer': 'Burmese Handwriting Team',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 92,
        'isWin': False,
        'file': 'Uni-Burmese Handwriting 01_Style 02_Regular.ttf',
        'tags': ['burmese', 'handwriting', 'style02']
    },
    {
        'id': 'uni-burmese-03',
        'name': 'Uni-Burmese Handwriting 01 (Style 3)',
        'mmName': 'မြန်မာလက်ရေးလှ စတိုင် ၀၃',
        'category': 'handwriting',
        'categoryLabel': 'Handwriting Series',
        'designer': 'Burmese Handwriting Team',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 94,
        'isWin': False,
        'file': 'Uni-Burmese Handwriting 01_Style 03_Regular.ttf',
        'tags': ['burmese', 'handwriting', 'style03']
    },
    {
        'id': 'uni-burmese-04',
        'name': 'Uni-Burmese Handwriting 01 (Style 4)',
        'mmName': 'မြန်မာလက်ရေးလှ စတိုင် ၀၄',
        'category': 'handwriting',
        'categoryLabel': 'Handwriting Series',
        'designer': 'Burmese Handwriting Team',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 91,
        'isWin': False,
        'file': 'Uni-Burmese Handwriting 01_Style 04_Regular.ttf',
        'tags': ['burmese', 'handwriting', 'style04']
    },
    {
        'id': 'uni-burmese-05',
        'name': 'Uni-Burmese Handwriting 01 (Style 5)',
        'mmName': 'မြန်မာလက်ရေးလှ စတိုင် ၀၅',
        'category': 'handwriting',
        'categoryLabel': 'Handwriting Series',
        'designer': 'Burmese Handwriting Team',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 93,
        'isWin': False,
        'file': 'Uni-Burmese Handwriting 01_Style 05_Regular.ttf',
        'tags': ['burmese', 'handwriting', 'style05']
    },
    {
        'id': 'tharlon',
        'name': 'Tharlon (သာလွန်ဖောင့်)',
        'mmName': 'သာလွန် လက်ရေးလှဖောင့်',
        'category': 'handwriting',
        'categoryLabel': 'Handwriting Series',
        'designer': 'Tharlon Type Project',
        'version': '2.0',
        'license': 'SIL OFL',
        'popular': 99,
        'isWin': False,
        'file': 'Uni-Tharlon-regular.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/Tharlon/TharLon.ttf',
        'description': 'မြန်မာစာပေ၊ ဝတ္ထုစာအုပ်များနှင့် စာစီစာရိုက်တွင် အလွန်ရေပန်းစားသော သာလွန်ဖောင့်။',
        'tags': ['tharlon', 'handwriting', 'book', 'novel']
    },
    {
        'id': 'uni-notes',
        'name': 'Uni-Myanmar Notes',
        'mmName': 'နုဒ်စ် လက်ရေးဖောင့်',
        'category': 'handwriting',
        'categoryLabel': 'Handwriting Series',
        'designer': 'Notes Type Team',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 95,
        'isWin': False,
        'file': 'Uni-Myanmar Notes.ttf',
        'tags': ['notes', 'handwriting']
    },
    {
        'id': 'uni-flower',
        'name': 'Uni-Myanmar Flower',
        'mmName': 'ပန်းပွင့် အလှဖောင့်',
        'category': 'handwriting',
        'categoryLabel': 'Handwriting Series',
        'designer': 'Flower Studio',
        'version': '1.3',
        'license': 'Freeware',
        'popular': 94,
        'isWin': False,
        'file': 'Uni-Myanmar Flower v1.30 For Windows 8 10.ttf',
        'tags': ['flower', 'cute', 'handwriting']
    },
    {
        'id': 'uni-handwriting-native',
        'name': 'Uni-Myanmar Handwriting',
        'mmName': 'မြန်မာလက်ရေး မူရင်းဟန်',
        'category': 'handwriting',
        'categoryLabel': 'Handwriting Series',
        'designer': 'Community Type',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 93,
        'isWin': False,
        'file': 'Uni-Myanmar Handwriting.ttf',
        'tags': ['handwriting', 'script']
    },
    {
        'id': 'uni-holiday',
        'name': 'Uni-Myanmar Holiday',
        'mmName': 'ဟောလီးဒေး အလှဖောင့်',
        'category': 'handwriting',
        'categoryLabel': 'Handwriting Series',
        'designer': 'Holiday Type Studio',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 94,
        'isWin': False,
        'file': 'Uni-Myanmar Holiday.ttf',
        'tags': ['holiday', 'handwriting', 'cute']
    },
    {
        'id': 'uni-love',
        'name': 'Uni-Myanmar Love',
        'mmName': 'လပ်ဗ် အချစ်ဖောင့်',
        'category': 'handwriting',
        'categoryLabel': 'Handwriting Series',
        'designer': 'Love Type',
        'version': '1.3',
        'license': 'Freeware',
        'popular': 95,
        'isWin': False,
        'file': 'Uni-Myanmar Love v1.30 Windows 8.ttf',
        'tags': ['love', 'cute', 'heart']
    },

    # ---------------- UNI-MYANMAR SIGNATURE COLLECTION ----------------
    {
        'id': 'uni-myanmar-april',
        'name': 'Uni-Myanmar April',
        'mmName': 'ယူနီ-မြန်မာ ဧပြီဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Uni-Myanmar Community',
        'version': '2.1',
        'license': 'Free Open Source',
        'popular': 98,
        'isWin': False,
        'file': 'Uni-Myanmar April.ttf',
        'description': 'ခေတ်မီဆန်းပြားပြီး စာဖတ်ရှုရ လွယ်ကူသပ်ရပ်သော Display စတိုင် Uni-Myanmar April ဖောင့်။',
        'tags': ['april', 'display', 'modern']
    },
    {
        'id': 'uni-myanmar-ayar-wazo',
        'name': 'Uni-Myanmar Ayar Wazo',
        'mmName': 'ယူနီ-မြန်မာ ဧရာဝဆိုဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Ayar Myanmar Group',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 96,
        'isWin': False,
        'file': 'Uni-Myanmar Ayar Wazo.ttf',
        'description': 'စာပေရေးသားမှုများနှင့် ဆောင်းပါးများအတွက် အထူးသင့်လျော်သော Ayar Wazo ဖောင့်။',
        'tags': ['ayar', 'wazo', 'literature']
    },
    {
        'id': 'uni-myanmar-ayar-typewriter',
        'name': 'Uni-Myanmar Ayar Typewriter',
        'mmName': 'ဧရာ လက်နှိပ်စက်ဟန်ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Ayar Myanmar Group',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 95,
        'isWin': False,
        'file': 'Uni-Myanmar Ayar Tyepwriter.ttf',
        'description': 'ရှေးခေတ်လက်နှိပ်စက်ဖြင့် ရိုက်နှိပ်ထားသောဟန် ပေါ်လွင်သည့် Typewriter ဖောင့်။',
        'tags': ['typewriter', 'retro', 'vintage']
    },
    {
        'id': 'uni-myanmar-cool-jazz',
        'name': 'Uni-Myanmar Cool Jazz',
        'mmName': 'ကူးလ်ဂျက်ဇ် ဖောင့်အလှ',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Jazz Studio',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 97,
        'isWin': False,
        'file': 'Uni-Myanmar Cool Jazz.ttf',
        'description': 'တေးဂီတ၊ သီချင်းစာသားနှင့် ဗီဒီယိုစာတန်းများအတွက် အလွန်လိုက်ဖက်သော Cool Jazz ဖောင့်။',
        'tags': ['cool', 'jazz', 'music', 'cute']
    },
    {
        'id': 'uni-myanmar-kamjing',
        'name': 'Uni-Myanmar Kamjing',
        'mmName': 'ကမ်ဂျင်း ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Kamjing Studio',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 92,
        'isWin': False,
        'file': 'Uni- Kamjing.ttf',
        'tags': ['kamjing', 'clean']
    },
    {
        'id': 'uni-myanmar-kt02',
        'name': 'Uni-Myanmar KT_02',
        'mmName': 'ကေတီ ၀၂ ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'KT Design Studio',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 94,
        'isWin': False,
        'file': 'Uni- KT_02.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/KT_Unicode/KT_02.ttf',
        'tags': ['kt', 'kt02']
    },
    {
        'id': 'uni-myanmar-kt03',
        'name': 'Uni-Myanmar KT_03',
        'mmName': 'ကေတီ ၀၃ ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'KT Design Studio',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 93,
        'isWin': False,
        'file': 'Uni- KT_03.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/KT_Unicode/KT_03.ttf',
        'tags': ['kt', 'kt03', 'bold']
    },
    {
        'id': 'uni-myanmar-miui',
        'name': 'Uni-Myanmar MIUI Unicode',
        'mmName': 'အမ်အိုင်ယူအိုင် ယူနီကုဒ်ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Xiaomi Community',
        'version': '3.2',
        'license': 'Free Open Source',
        'popular': 96,
        'isWin': False,
        'file': 'Uni- MIUI Unicode.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarPaOhRosemary/MIUI%20Unicode.ttf',
        'description': 'Xiaomi စမတ်ဖုန်းများတွင် လူကြိုက်များသော သပ်ရပ်ခေတ်မီသည့် MIUI ယူနီကုဒ်စတိုင်။',
        'tags': ['miui', 'xiaomi', 'mobile', 'clean']
    },
    {
        'id': 'uni-myanmar-angoun',
        'name': 'Uni-Myanmar Angoun',
        'mmName': 'မြန်မာ အငုံ (ကနုတ်ဟန်)',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Danh Hong / Community',
        'version': '2.0',
        'license': 'SIL OFL',
        'popular': 96,
        'isWin': False,
        'file': 'Uni-MyanmarAngoun.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarAngoun/MyanmarAngoun.ttf',
        'description': 'စာလုံးအနားသတ်များတွင် အလှအပကွေးညွှတ်မှုပါဝင်သော နာမည်ကြီး အငုံဖောင့်။',
        'tags': ['angoun', 'fancy', 'traditional']
    },
    {
        'id': 'uni-myanmar-chat',
        'name': 'Uni-Myanmar Chatu',
        'mmName': 'စတူ ဖောင့်အလှ',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Chatu Type',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 94,
        'isWin': False,
        'file': 'Uni-MyanmarChatu.ttf',
        'githubRel': 'lecramyajiv/fonts-myanmar-extra/master/TTF/Myanmar-Chatu.ttf',
        'tags': ['chatu', 'cute']
    },
    {
        'id': 'uni-myanmar-chat-light',
        'name': 'Uni-Myanmar Chatu Light',
        'mmName': 'စတူ ပါးလွှာအလှ',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Chatu Type',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 93,
        'isWin': False,
        'file': 'Uni-MyanmarChatuLight.ttf',
        'tags': ['chatu', 'light']
    },
    {
        'id': 'uni-myanmar-gantgaw',
        'name': 'Uni-Myanmar Gantgaw',
        'mmName': 'ကန့်ကော် ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'AungMyoKyaw',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 95,
        'isWin': False,
        'file': 'Uni-MyanmarGantgaw.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarGantGaw/MyanmarGantGaw.ttf',
        'tags': ['gantgaw', 'flower']
    },
    {
        'id': 'uni-myanmar-kuttar',
        'name': 'Uni-Myanmar Kuttar',
        'mmName': 'ကုတ္တား ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'AungMyoKyaw',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 92,
        'isWin': False,
        'file': 'Uni-MyanmarKuttar.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarKuttar/MyanmarKuttar.ttf',
        'tags': ['kuttar']
    },
    {
        'id': 'uni-myanmar-nayone',
        'name': 'Uni-Myanmar Nayone',
        'mmName': 'နယုန် ဖောင့်အလှ',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'AungMyoKyaw',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 94,
        'isWin': False,
        'file': 'Uni-MyanmarNayone.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarNayone/MyanmarNayone.ttf',
        'tags': ['nayone']
    },
    {
        'id': 'uni-myanmar-njaun',
        'name': 'Uni-Myanmar Njaun',
        'mmName': 'ညောင် ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'AungMyoKyaw',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 91,
        'isWin': False,
        'file': 'Uni-MyanmarNjaun.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarNjaun/MyanmarNjaun.ttf',
        'tags': ['njaun']
    },
    {
        'id': 'uni-myanmar-padaung',
        'name': 'Uni-Myanmar Padaung',
        'mmName': 'ပဒေါင်း ရိုးရာဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Padaung Studio',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 94,
        'isWin': False,
        'file': 'Uni-Myanmar Padaung.ttf',
        'tags': ['padaung', 'traditional']
    },
    {
        'id': 'uni-myanmar-pangram',
        'name': 'Uni-Myanmar Pangram',
        'mmName': 'ပန်ဂရမ် ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Pangram Studio',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 95,
        'isWin': False,
        'file': 'Uni-Myanmar Pangram.ttf',
        'tags': ['pangram', 'modern']
    },
    {
        'id': 'uni-myanmar-phetsot',
        'name': 'Uni-Myanmar Phetsot',
        'mmName': 'ဖက်ဆုပ် ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'AungMyoKyaw',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 92,
        'isWin': False,
        'file': 'Uni-MyanmarPhetsot.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarPhetsot/MyanmarPhetsot.ttf',
        'tags': ['phetsot']
    },
    {
        'id': 'uni-myanmar-pixel',
        'name': 'Uni-Myanmar Pixel',
        'mmName': 'ပစ်ဇယ် ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Pixel Art Team',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 95,
        'isWin': False,
        'file': 'Uni-MyanmarPixel.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarPixel/MyanmarPixel.ttf',
        'description': '၈-ဘစ်ဂိမ်းများနှင့် Retro ဒီဇိုင်းများအတွက် စတုရန်းပစ်ဇယ်ပုံစံ ဖောင့်။',
        'tags': ['pixel', 'retro', 'game', '8bit']
    },
    {
        'id': 'uni-myanmar-pixelsmooth',
        'name': 'Uni-Myanmar Pixel Smooth',
        'mmName': 'ပစ်ဇယ် စမုဒ်ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Pixel Art Team',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 94,
        'isWin': False,
        'file': 'Uni-MyanmarPixelSmooth.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarPixel/MyanmarPixelSmooth.ttf',
        'tags': ['pixel', 'smooth', 'game']
    },
    {
        'id': 'uni-myanmar-ponenyet',
        'name': 'Uni-Myanmar Ponenyet',
        'mmName': 'ပုဏ္ဏားရက် ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'AungMyoKyaw',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 91,
        'isWin': False,
        'file': 'Uni-MyanmarPonenyet.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarPonenyet/MyanmarPonenyet.ttf',
        'tags': ['ponenyet']
    },
    {
        'id': 'uni-myanmar-pyu-pro',
        'name': 'Uni-Myanmar Pyu Pro',
        'mmName': 'ပျူ ပရို ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Pyu Type Studio',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 96,
        'isWin': False,
        'file': 'Uni-Myanmar Pyu Pro.ttf',
        'tags': ['pyu', 'ancient', 'historical']
    },
    {
        'id': 'uni-myanmar-sanpya',
        'name': 'Uni-Myanmar Sanpya',
        'mmName': 'စံပြ ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'AungMyoKyaw',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 95,
        'isWin': False,
        'file': 'Uni-MyanmarSanpya.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarSanpya/MyanmarSanpya.ttf',
        'tags': ['sanpya', 'standard']
    },
    {
        'id': 'uni-myanmar-sanspro',
        'name': 'Uni-Myanmar SansPro',
        'mmName': 'ဆန်းစ်ပရို ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Unicode Community',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 98,
        'isWin': False,
        'file': 'Uni-MyanmarSansPro.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarSansPro/MyanmarSansPro.ttf',
        'description': 'ခေတ်မီ UI/UX ဒီဇိုင်းနှင့် ဝက်ဘ်ဆိုဒ်များအတွက် အလွန်ရှင်းလင်းသော Sans-Serif ဖောင့်။',
        'tags': ['sanspro', 'ui', 'modern', 'clean']
    },
    {
        'id': 'uni-myanmar-square',
        'name': 'Uni-Myanmar Square',
        'mmName': 'စတုရန်း ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'AungMyoKyaw',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 93,
        'isWin': False,
        'file': 'Uni-MyanmarSquare.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarSquare/MyanmarSquare.ttf',
        'tags': ['square', 'modern']
    },
    {
        'id': 'uni-myanmar-squarelight',
        'name': 'Uni-Myanmar Square Light',
        'mmName': 'စတုရန်း ပါးလွှာအလှ',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'AungMyoKyaw',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 92,
        'isWin': False,
        'file': 'Uni-MyanmarSquareLight.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarSquare/MyanmarSquareLight.ttf',
        'tags': ['square', 'light']
    },
    {
        'id': 'uni-myanmar-tagaung',
        'name': 'Uni-Myanmar Tagaung',
        'mmName': 'တကောင်း ရိုးရာဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Tagaung Type Studio',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 94,
        'isWin': False,
        'file': 'Uni-Myanmar Tagaung.ttf',
        'tags': ['tagaung', 'traditional']
    },
    {
        'id': 'uni-myanmar-tagu',
        'name': 'Uni-Myanmar Tagu',
        'mmName': 'တန်ခူး ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'AungMyoKyaw',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 93,
        'isWin': False,
        'file': 'Uni-MyanmarTagu.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarTagu/MyanmarTagu.ttf',
        'tags': ['tagu']
    },
    {
        'id': 'uni-myanmar-taunggyi',
        'name': 'Uni-Myanmar Taunggyi',
        'mmName': 'တောင်ကြီး ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'AungMyoKyaw',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 94,
        'isWin': False,
        'file': 'Uni-MyanmarTaungyi.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarTaungyi/MyanmarTaungyi.ttf',
        'tags': ['taunggyi', 'shan']
    },
    {
        'id': 'uni-myanmar-textmelano',
        'name': 'Uni-Myanmar TextMelano',
        'mmName': 'မက်လာနို စာသားဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Melano Studio',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 95,
        'isWin': False,
        'file': 'Uni-MyanmarTextMelano.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarTextMelano/MyanmarTextMelano.ttf',
        'tags': ['melano', 'reading', 'book']
    },
    {
        'id': 'uni-myanmar-thuriya',
        'name': 'Uni-Myanmar Thuriya',
        'mmName': 'သူရိယ ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'AungMyoKyaw',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 95,
        'isWin': False,
        'file': 'Uni-MyanmarThuriya.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarThuriya/MyanmarThuriya.ttf',
        'tags': ['thuriya', 'sun']
    },
    {
        'id': 'uni-myanmar-yinmar',
        'name': 'Uni-Myanmar Yinmar',
        'mmName': 'ယင်းမာ ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'AungMyoKyaw',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 93,
        'isWin': False,
        'file': 'Uni-MyanmarYinmar.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarYinmar/MyanmarYinmar.ttf',
        'tags': ['yinmar']
    },
    {
        'id': 'uni-myanmar-punk',
        'name': 'Uni-Myanmar Punk',
        'mmName': 'မြန်မာ ပန့်ခ် ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Punk Type Studio',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 96,
        'isWin': False,
        'file': 'Uni-Myanmar_Punk.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarPunk/Myanmar_Punk.ttf',
        'description': 'ရော့ခ်နှင့် ပန့်ခ်ဂီတစတိုင် ထူးခြားဆန်းပြားသော ဒီဇိုင်းဖောင့်။',
        'tags': ['punk', 'rock', 'grunge']
    },
    {
        'id': 'uni-myanmar-rosemarry',
        'name': 'Uni-Myanmar Rosemary',
        'mmName': 'ရို့စ်မေရီ ဖောင့်အလှ',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Rosemarry Studio',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 94,
        'isWin': False,
        'file': 'Uni-Myanmar_Rosemarry.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarRosemarry/Myanmar_Rosemarry.ttf',
        'tags': ['rosemary', 'cute']
    },
    {
        'id': 'uni-khawell',
        'name': 'Uni-Myanmar Khawell',
        'mmName': 'ခဝဲ ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Khawell Type',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 92,
        'isWin': False,
        'file': 'Uni-Myanmar Khawell.ttf',
        'tags': ['khawell']
    },
    {
        'id': 'uni-khittar',
        'name': 'Uni-Myanmar Khittar',
        'mmName': 'ခေတ္တာ ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Khittar Team',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 93,
        'isWin': False,
        'file': 'Uni-Myanmar Khittar.ttf',
        'tags': ['khittar']
    },
    {
        'id': 'uni-waso',
        'name': 'Uni-Myanmar Waso',
        'mmName': 'ဝါဆို ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'AungMyoKyaw',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 94,
        'isWin': False,
        'file': 'Uni-MyanmarWaso.ttf',
        'githubRel': 'lecramyajiv/fonts-myanmar-extra/master/TTF/Myanmar-Waso.ttf',
        'tags': ['waso']
    },
    {
        'id': 'uni-census',
        'name': 'Uni-Myanmar Census',
        'mmName': 'သန်းခေါင်စာရင်း ယူနီကုဒ်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Census Myanmar / UNFPA',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 93,
        'isWin': False,
        'file': 'Uni-Myanmarcensus.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MyanmarCensus/myanmarcensus.ttf',
        'tags': ['census', 'official']
    },
    {
        'id': 'uni-jojar',
        'name': 'Uni-Myanmar Jojar',
        'mmName': 'ဂျိုဂျာ ဖောင့်အလှ',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Jojar Type',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 92,
        'isWin': False,
        'file': 'Uni-Myanmar Jojar.ttf',
        'tags': ['jojar', 'cute']
    },
    {
        'id': 'uni-yein-pro',
        'name': 'Uni-Myanmar Yein Pro',
        'mmName': 'ယိမ်း ပရို ဖောင့်',
        'category': 'uni-myanmar',
        'categoryLabel': 'Uni-Myanmar Series',
        'designer': 'Yein Studio',
        'version': '1.0',
        'license': 'Freeware',
        'popular': 93,
        'isWin': False,
        'file': 'Uni-Myanmar Yein Pro v1.00.ttf',
        'tags': ['yein', 'pro']
    },

    # ---------------- UNICODE STANDARD & OFFICIAL ----------------
    {
        'id': 'pyidaungsu-bold',
        'name': 'Pyidaungsu Bold (ပြည်ထောင်စု စာလုံးထူ)',
        'mmName': 'ပြည်ထောင်စု စာလုံးထူ (ရုံးသုံးစံ)',
        'category': 'unicode',
        'categoryLabel': 'Unicode Standard',
        'designer': 'Myanmar NLP / MCF',
        'version': '2.5.3',
        'license': 'Free Open Source',
        'popular': 100,
        'isWin': False,
        'file': 'Pyidaungsu-2.5.3_Bold.ttf',
        'githubRel': 'moekyawsoe/Myanmar-Fonts/master/PYIDAUNGSU-2.5.2_BOLD.TTF',
        'description': 'မြန်မာနိုင်ငံ ရုံးလုပ်ငန်းများနှင့် တရားဝင်စာရွက်စာတမ်းများတွင် သတ်မှတ်ထားသော စံချိန်မီ Pyidaungsu Bold စာလုံးထူဖောင့်။',
        'tags': ['pyidaungsu', 'official', 'office', 'bold', 'standard']
    },
    {
        'id': 'pyidaungsu-regular',
        'name': 'Pyidaungsu Regular (ပြည်ထောင်စု)',
        'mmName': 'ပြည်ထောင်စု ရိုးရိုး (ရုံးသုံးစံ)',
        'category': 'unicode',
        'categoryLabel': 'Unicode Standard',
        'designer': 'Myanmar NLP / MCF',
        'version': '2.5.3',
        'license': 'Free Open Source',
        'popular': 100,
        'isWin': False,
        'file': 'Uni-pyidaungsu.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/Pyidaungsu/pyidaungsu.ttf',
        'description': 'မြန်မာနိုင်ငံ အစိုးရနှင့် ကုမ္ပဏီရုံးသုံး စာရွက်စာတမ်းများအားလုံးအတွက် တရားဝင် ယူနီကုဒ်ဖောင့်။',
        'tags': ['pyidaungsu', 'official', 'standard', 'regular']
    },
    {
        'id': 'padauk-regular',
        'name': 'SIL Padauk Regular (ပိတောက်ဖောင့်)',
        'mmName': 'ပိတောက် ယူနီကုဒ် (SIL)',
        'category': 'unicode',
        'categoryLabel': 'Unicode Standard',
        'designer': 'SIL International',
        'version': '5.001',
        'license': 'SIL Open Font License',
        'popular': 99,
        'isWin': False,
        'file': 'Uni-Padauk.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/Padauk/Padauk.ttf',
        'description': 'SIL International မှ အပြည်ပြည်ဆိုင်ရာ စံချိန်မီ ရေးဆွဲထားသော ပိတောက်ဖောင့်။',
        'tags': ['padauk', 'sil', 'unicode', 'book']
    },
    {
        'id': 'padauk-bold',
        'name': 'SIL Padauk Bold (ပိတောက် စာလုံးထူ)',
        'mmName': 'ပိတောက် စာလုံးထူ',
        'category': 'unicode',
        'categoryLabel': 'Unicode Standard',
        'designer': 'SIL International',
        'version': '5.001',
        'license': 'SIL OFL',
        'popular': 98,
        'isWin': False,
        'file': 'Uni-Padauk-bold.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/Padauk/Padauk-bold.ttf',
        'tags': ['padauk', 'bold', 'sil']
    },
    {
        'id': 'padauk-kyaungchikote',
        'name': 'Padauk Kyaungchikote (ပိတောက် ကြောင်ချီကုတ်)',
        'mmName': 'ပိတောက် ကြောင်ချီကုတ် စာလုံးထူ',
        'category': 'unicode',
        'categoryLabel': 'Unicode Standard',
        'designer': 'SIL / Community',
        'version': '2.0',
        'license': 'SIL OFL',
        'popular': 97,
        'isWin': False,
        'file': 'Uni-Padauk Kyaungchikote.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/PadaukKyaungchikote/Padauk%20Kyaungchikote.ttf',
        'description': 'ထူထဲပေါ်လွင်သော ကြောင်ချီကုတ် ပိတောက်စတိုင် ဖောင့်။',
        'tags': ['padauk', 'kyaungchikote', 'bold']
    },
    {
        'id': 'padauk-sagar',
        'name': 'Padauk Sagar (ပိတောက် စကား)',
        'mmName': 'ပိတောက် စကားဖောင့်',
        'category': 'unicode',
        'categoryLabel': 'Unicode Standard',
        'designer': 'SIL / AungMyoKyaw',
        'version': '2.0',
        'license': 'SIL OFL',
        'popular': 95,
        'isWin': False,
        'file': 'Uni-PadaukSagar.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/PadaukSagar/PadaukSagar.ttf',
        'tags': ['padauk', 'sagar']
    },
    {
        'id': 'padauk-sgaw-bold',
        'name': 'Padauk Sgaw Bold',
        'mmName': 'ပိတောက် စကော စာလုံးထူ',
        'category': 'unicode',
        'categoryLabel': 'Unicode Standard',
        'designer': 'SIL International',
        'version': '2.0',
        'license': 'SIL OFL',
        'popular': 94,
        'isWin': False,
        'file': 'Uni-PadaukSgaw-Bold.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/PadaukSgaw/PadaukSgaw-Bold.ttf',
        'tags': ['padauk', 'sgaw', 'karen']
    },
    {
        'id': 'padauk-grand-pro',
        'name': 'Padauk Grand Pro v2',
        'mmName': 'ပိတောက် ဂရန်း ပရို',
        'category': 'unicode',
        'categoryLabel': 'Unicode Standard',
        'designer': 'SIL Community',
        'version': '2.0',
        'license': 'SIL OFL',
        'popular': 95,
        'isWin': False,
        'file': 'Uni-PadaukGrandPro v2.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/PadaukGrandPro/PadaukGrandPro%20v2.ttf',
        'tags': ['padauk', 'grand']
    },
    {
        'id': 'myanmar3',
        'name': 'Myanmar3 (မြန်မာသုံ့ ယူနီကုဒ်)',
        'mmName': 'မြန်မာ ၃ မူရင်းစံချိန်မီ',
        'category': 'unicode',
        'categoryLabel': 'Unicode Standard',
        'designer': 'Myanmar Unicode Group',
        'version': '3.0',
        'license': 'Free Open Source',
        'popular': 97,
        'isWin': False,
        'file': 'Uni-mm3-multi-os.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/Myanmar3/mm3-multi-os.ttf',
        'tags': ['myanmar3', 'mm3', 'classic']
    },
    {
        'id': 'panglong',
        'name': 'PangLong (ပင်လုံ ယူနီကုဒ်ဖောင့်)',
        'mmName': 'ပင်လုံ သမိုင်းဝင်ဖောင့်',
        'category': 'unicode',
        'categoryLabel': 'Unicode Standard',
        'designer': 'Panglong Type Team',
        'version': '2011',
        'license': 'Free Open Source',
        'popular': 95,
        'isWin': False,
        'file': 'Uni-PangLong_2011feb7.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/PangLong/PangLong_2011feb7.ttf',
        'tags': ['panglong', 'historical', 'shan']
    },
    {
        'id': 'mon3-anonta',
        'name': 'MON3 Anonta 1',
        'mmName': 'မွန် ၃ အနန္တ ဖောင့်',
        'category': 'unicode',
        'categoryLabel': 'Unicode Standard',
        'designer': 'Mon Unicode Community',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 95,
        'isWin': False,
        'file': 'Uni-Mon3.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/MON3_Anonta/MON3Anonta1.ttf',
        'tags': ['mon', 'anonta', 'mon3']
    },
    {
        'id': 'samsung-myanmar',
        'name': 'Samsung Myanmar',
        'mmName': 'ဆမ်ဆောင်း မြန်မာဖောင့်',
        'category': 'unicode',
        'categoryLabel': 'Unicode Standard',
        'designer': 'Samsung Electronics',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 97,
        'isWin': False,
        'file': 'Uni-Samsung Myanmar.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/SamsungMyanmar/Samsung%20Myanmar.ttf',
        'description': 'Samsung Galaxy စမတ်ဖုန်းများတွင် မြင်တွေ့ရသော စံသတ်မှတ်ချက် ယူနီကုဒ်ဖောင့်။',
        'tags': ['samsung', 'galaxy', 'mobile', 'clean']
    },
    {
        'id': 'shan-unicode',
        'name': 'Shan Unicode',
        'mmName': 'ရှမ်း ယူနီကုဒ်ဖောင့်',
        'category': 'unicode',
        'categoryLabel': 'Unicode Standard',
        'designer': 'Shan Type Project',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 94,
        'isWin': False,
        'file': 'Uni-Shan Unicode.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/ShanUnicode/Shan%20Unicode.ttf',
        'tags': ['shan', 'taiyai', 'unicode']
    },
    {
        'id': 'paoh-dragon',
        'name': 'PaOh Dragon App Unicode',
        'mmName': 'ပအိုဝ်း ဒရက်ဂွန် ဖောင့်',
        'category': 'unicode',
        'categoryLabel': 'Unicode Standard',
        'designer': 'Dragon Type',
        'version': '1.3',
        'license': 'Free Open Source',
        'popular': 93,
        'isWin': False,
        'file': 'Uni-PaOh Dragon App v1.30 For Windows 8 10.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/PaohDragonApp/PaohDragonApp.ttf',
        'tags': ['paoh', 'dragon']
    },

    # ---------------- WIN MYANMAR PUBLISHING FONTS ----------------
    {
        'id': 'win-uni-innwa',
        'name': 'WinUni Innwa (ဝင်းယူနီ အင်းဝ)',
        'mmName': 'ဝင်းယူနီ အင်းဝ (Unicode စံ)',
        'category': 'win',
        'categoryLabel': 'Win Publishing',
        'designer': 'Win Myanmar / Unicode Community',
        'version': '2.0',
        'license': 'Free Legacy Distribution',
        'popular': 100,
        'isWin': False,
        'file': 'Uni-winuniinnwa.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/WinUniInnwa/WinUniInnwa.ttf',
        'description': 'ဂန္တဝင် Win Innwa ပုံနှိပ်တိုက်ဖောင့်ကို ယူနီကုဒ်စနစ်နှင့် တိုက်ရိုက်ကိုက်ညီအောင် ဖန်တီးထားသော ထိပ်တန်းဖောင့်။ စာအုပ်စာစောင်နှင့် ပုံနှိပ်လုပ်ငန်းများတွင် အထူးသင့်တော်သည်။',
        'tags': ['win', 'innwa', 'winuni', 'printing', 'pagemaker']
    },
    {
        'id': 'win-innwa',
        'name': 'Win Innwa (ဝင်းအင်းဝ မူရင်း)',
        'mmName': 'ဝင်းအင်းဝ (Win Researcher 1)',
        'category': 'win',
        'categoryLabel': 'Win Publishing',
        'designer': 'Win Myanmar Systems',
        'version': '4.0',
        'license': 'Free Legacy Distribution',
        'popular': 99,
        'isWin': True,
        'file': 'WININNWA.TTF',
        'githubRel': 'moekyawsoe/Myanmar-Fonts/master/WININNWA.TTF',
        'description': 'မြန်မာနိုင်ငံရှိ စာစီစာရိုက်ဆိုင်များနှင့် ပုံနှိပ်တိုက်များတွင် မရှိမဖြစ် အသုံးပြုခဲ့သော နံပါတ် (၁) Win Innwa ပုံနှိပ်ဖောင့်။',
        'sampleWin': 'oD[dkMfrS nmPfjuD;Sifonf',
        'tags': ['win', 'innwa', 'printing', 'classic']
    },
    {
        'id': 'win-kalaw',
        'name': 'Win Kalaw (ဝင်းကလော ခေါင်းစဉ်ဖောင့်)',
        'mmName': 'ဝင်းကလော (စာလုံးထူအလှ)',
        'category': 'win',
        'categoryLabel': 'Win Publishing',
        'designer': 'Win Myanmar Systems',
        'version': '4.0',
        'license': 'Free Legacy Distribution',
        'popular': 95,
        'isWin': True,
        'file': 'WINNWAB0.TTF',
        'githubRel': 'moekyawsoe/Myanmar-Fonts/master/WINNWAB0.TTF',
        'description': 'ပုံနှိပ်စာအုပ် မျက်နှာဖုံးများနှင့် ဖိတ်စာခေါင်းစဉ်များတွင် Win Innwa နှင့် တွဲဖက်သုံးသော စာလုံးထူဖောင့်။',
        'sampleWin': 'oD[dkMfrS nmPfjuD;Sifonf',
        'tags': ['win', 'kalaw', 'bold', 'printing']
    },
    {
        'id': 'win-researcher',
        'name': 'Win Researcher (ဝင်း ရီဆာချာ)',
        'mmName': 'ဝင်း ရီဆာချာ',
        'category': 'win',
        'categoryLabel': 'Win Publishing',
        'designer': 'Win Myanmar Systems',
        'version': '4.0',
        'license': 'Free Legacy',
        'popular': 94,
        'isWin': True,
        'file': 'WRES.TTF',
        'githubRel': 'moekyawsoe/Myanmar-Fonts/master/WRES.TTF',
        'description': 'သုတေသနစာတမ်းများနှင့် မဂ္ဂဇင်းသုံး Win Researcher ဖောင့်။',
        'sampleWin': 'oD[dkMfrS nmPfjuD;Sifonf',
        'tags': ['win', 'researcher', 'publishing']
    },

    # ---------------- ZAWGYI & LEGACY FONTS ----------------
    {
        'id': 'zawgyi-one',
        'name': 'Zawgyi-One (ဇော်ဂျီဖောင့် မူရင်း)',
        'mmName': 'ဇော်ဂျီဝမ်း (ဖိုင်ဟောင်းများဖတ်ရန်)',
        'category': 'zawgyi',
        'categoryLabel': 'Zawgyi Legacy',
        'designer': 'Zawgyi.net / Alpha Mandalar',
        'version': '3.1',
        'license': 'Freeware',
        'popular': 96,
        'isWin': False,
        'file': 'Uni-Padauk-Zawgyi.ttf',
        'githubRel': 'moekyawsoe/Myanmar-Fonts/master/ZAWGYI-ONE_V3.1.TTF',
        'description': 'ယခင်နှစ်များက ရိုက်နှိပ်သိမ်းဆည်းထားသော Excel, Word ဖိုင်ဟောင်းများနှင့် မီဒီယာပို့စ်ဟောင်းများကို မူရင်းမပျက် ပြန်လည်ဖတ်ရှုနိုင်သော ဖောင့်။',
        'tags': ['zawgyi', 'zg', 'legacy', 'archive']
    },
    {
        'id': 'zawdecode',
        'name': 'ZawDecode Converter Font',
        'mmName': 'ဇော်ဒီကုဒ် ဟိုက်ဘရစ်ဖောင့်',
        'category': 'zawgyi',
        'categoryLabel': 'Zawgyi Legacy',
        'designer': 'Open Source Community',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 92,
        'isWin': False,
        'file': 'Uni-NotoSansMyanmarUI-Regular-ZawDecode.ttf',
        'description': 'ဇော်ဂျီစာများကို ယူနီကုဒ်စနစ်တွင် အလွယ်တကူ ဖတ်ရှုနိုင်အောင် ကူညီပေးသော ZawDecode ဖောင့်။',
        'tags': ['zawdecode', 'converter', 'legacy']
    },
    {
        'id': 'parabaik-utn',
        'name': 'Parabaik Unicode (ပုရပိုက်)',
        'mmName': 'ပုရပိုက် ရိုးရာဖောင့်',
        'category': 'zawgyi',
        'categoryLabel': 'Zawgyi Legacy',
        'designer': 'AungMyoKyaw / UTN',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 93,
        'isWin': False,
        'file': 'Uni-Parabaik_UTN11-3.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/Parabaik/Parabaik_UTN11-3.ttf',
        'description': 'ရှေးဟောင်းပုရပိုက်နှင့် ပေစာဟန် ပါရှိသော သမိုင်းဝင် Parabaik ဖောင့်။',
        'tags': ['parabaik', 'traditional', 'ancient']
    },
    {
        'id': 'thanlwin-regular',
        'name': 'Thanlwin Regular (သံလွင်ဖောင့်)',
        'mmName': 'သံလွင် ယူနီကုဒ်',
        'category': 'zawgyi',
        'categoryLabel': 'Zawgyi Legacy',
        'designer': 'Thanlwin Team',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 91,
        'isWin': False,
        'file': 'Uni-Thanlwin-Regular.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/Thanlwin/ThanLwin.ttf',
        'tags': ['thanlwin', 'legacy']
    },
    {
        'id': 'thanlwin-bold',
        'name': 'Thanlwin Bold (သံလွင် စာလုံးထူ)',
        'mmName': 'သံလွင် စာလုံးထူ',
        'category': 'zawgyi',
        'categoryLabel': 'Zawgyi Legacy',
        'designer': 'Thanlwin Team',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 92,
        'isWin': False,
        'file': 'Uni-Thanlwin-Bold.ttf',
        'tags': ['thanlwin', 'bold']
    },
    {
        'id': 'namkhon-grand',
        'name': 'Namkhon Grand (နမ်ခွန်)',
        'mmName': 'နမ်ခွန် ဂရန်း ဖောင့်',
        'category': 'zawgyi',
        'categoryLabel': 'Zawgyi Legacy',
        'designer': 'Namkhon Type Project',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 93,
        'isWin': False,
        'file': 'Uni-NK Grand.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/Namkhon/NK%20Grand.ttf',
        'tags': ['namkhon', 'grand', 'ethnic']
    },
    {
        'id': 'yoeyar-one-bold',
        'name': 'YoeYar-One Bold (ရိုးရာဝမ်း စာလုံးထူ)',
        'mmName': 'ရိုးရာဝမ်း စာလုံးထူ',
        'category': 'zawgyi',
        'categoryLabel': 'Zawgyi Legacy',
        'designer': 'YoeYar Team',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 94,
        'isWin': False,
        'file': 'Uni-YoeYar-One Bold.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/YoeYarOne/YoeYar-One%20Bold.ttf',
        'tags': ['yoeyar', 'bold', 'traditional']
    },
    {
        'id': 'yoeyar-one-regular',
        'name': 'YoeYar-One Regular (ရိုးရာဝမ်း မူရင်း)',
        'mmName': 'ရိုးရာဝမ်း ရိုးရိုး',
        'category': 'zawgyi',
        'categoryLabel': 'Zawgyi Legacy',
        'designer': 'YoeYar Team',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 92,
        'isWin': False,
        'file': 'Uni-YoeYar-One Regular.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/YoeYarOne/YoeYar-One%20Regular.ttf',
        'tags': ['yoeyar', 'traditional']
    },
    {
        'id': 'yunghkio',
        'name': 'Yunghkio Unicode',
        'mmName': 'ယုံချို ယူနီကုဒ်',
        'category': 'zawgyi',
        'categoryLabel': 'Zawgyi Legacy',
        'designer': 'Yunghkio Team',
        'version': '2.0',
        'license': 'Free Open Source',
        'popular': 92,
        'isWin': False,
        'file': 'Uni-Yunghkio.ttf',
        'githubRel': 'AungMyoKyaw/Myanmar-Unicode-Fonts/master/Yunghkio/Yunghkio.ttf',
        'tags': ['yunghkio', 'ethnic']
    },
    {
        'id': 'mymyanmar-universal',
        'name': 'MyMyanmar Universal',
        'mmName': 'မိုင်မြန်မာ ယူနီဗာဆယ်',
        'category': 'zawgyi',
        'categoryLabel': 'Zawgyi Legacy',
        'designer': 'MyMyanmar Team',
        'version': '2.0',
        'license': 'Freeware',
        'popular': 93,
        'isWin': False,
        'file': 'Uni-MyMyanmarUniversal.ttf',
        'tags': ['mymyanmar', 'universal']
    }
]

# Enrich every catalog entry with exact font_db matching
font_rules = []
enriched_catalog = []

for spec in CATALOG_SPECS:
    fname = spec.get('file', '')
    info = font_db.get(fname)
    
    ps_name = info['ps'] if info else spec['name'].replace(' ', '')
    full_name = info['full'] if info else spec['name']
    family_name = info['family'] if info else spec['name']
    size = info['size'] if info else '350 KB'
    
    spec['fileName'] = fname
    spec['size'] = size
    spec['ps'] = ps_name
    spec['full'] = full_name
    spec['family'] = family_name
    spec['description'] = spec.get('description') or f"{spec['name']} မြန်မာဖောင့် (Myanmar Font Hub)"
    spec['designer'] = spec.get('designer') or 'Myanmar Type Community'
    spec['mmName'] = spec.get('mmName') or spec['name']
    spec['tags'] = spec.get('tags') or [spec['name'].lower()]
    spec['popular'] = spec.get('popular', 85)
    
    # Determine download url:
    # 1. githubRel if specified
    # 2. or local file
    if spec.get('githubRel'):
        spec['directUrl'] = f"https://raw.githubusercontent.com/{spec['githubRel']}"
    else:
        # fallback to local file in fonts/ directory
        spec['directUrl'] = f"./fonts/{fname}"

    # Default sample text
    if spec.get('isWin'):
        spec['defaultSample'] = spec.get('sampleWin', 'r*Fvmyg Art House စာလုံးအလှ')
    else:
        spec['defaultSample'] = 'သီဟိုဠ်မှ ဉာဏ်ကြီးရှင်သည် အာယုဝဍ္ဎနဆေးညွှန်းစာကို ဇလွန်ဈေးဘေး ဗာဒံပင်ထက် အဓိဋ္ဌာန်လျက် ဂဃနဏဖတ်ခဲ့သည်။'

    # Build @font-face CSS
    # Priority: local(PostScriptName) -> local(FullName) -> local(FamilyName) -> url('./fonts/...') -> url('https://...')
    local_srcs = []
    if ps_name: local_srcs.append(f"local('{ps_name}')")
    if full_name and full_name != ps_name: local_srcs.append(f"local('{full_name}')")
    if family_name and family_name not in (ps_name, full_name): local_srcs.append(f"local('{family_name}')")
    
    src_parts = list(local_srcs)
    if fname:
        src_parts.append(f"url('./fonts/{fname}') format('truetype')")
    if spec.get('githubRel'):
        src_parts.append(f"url('https://raw.githubusercontent.com/{spec['githubRel']}') format('truetype')")
    src_chain = ", ".join(src_parts)

    css_rule = f"""
@font-face {{
    font-family: 'font-{spec['id']}';
    src: {src_chain};
    font-display: swap;
}}
.font-preview-{spec['id']} {{
    font-family: 'font-{spec['id']}', '{family_name}', 'Noto Sans Myanmar', sans-serif !important;
}}
"""
    font_rules.append(css_rule.strip())
    enriched_catalog.append(spec)

all_font_faces_css = "\n".join(font_rules)
catalog_json = json.dumps(enriched_catalog, ensure_ascii=False, indent=2)

print(f"Enriched {len(enriched_catalog)} fonts with authentic @font-face rules.")

# Now write complete HTML template


with open('/Users/sithu/Desktop/Gemini 4/zeemotion_logo.png', 'rb') as f:
    LOGO_BASE64 = base64.b64encode(f.read()).decode('ascii')

PANGRAM_WIN_STR = "oD[dkMfrS nmPfjuD;Sifonf tm,k0!~e aq;nTef;pmudk ZvGefaps;ab; Am'Hyifxuf t\"d|mefvsu *CeP zwfcJhonf/"
HEADLINE_WIN_STR = "r*Fvmyg jrefrmjynf - tvSyqHk; jrefrm'DZdkif;rsm;"
WIN_CMAP = {
    'က': 'u', 'ခ': 'c', 'ဂ': '*', 'ဃ': 'C', 'င': 'i',
    'စ': 'p', 'ဆ': 'q', 'ဇ': 'Z', 'ဈ': 'Q', 'ဉ': 'n', 'ည': 'n',
    'ဋ': '#', 'ဌ': 'X', 'ဍ': '!', 'ဎ': '~', 'ဏ': 'P',
    'တ': 'w', 'ထ': 'x', 'ဒ': "'", 'ဓ': '"', 'န': 'e',
    'ပ': 'y', 'ဖ': 'z', 'ဗ': 'A', 'ဘ': 'b', 'မ': 'r',
    'ယ': ',', 'ရ': '&', 'လ': 'v', 'ဝ': '0', 'သ': 'o', 'ဟ': '[', 'ဠ': 'M', 'အ': 't',
    'ျ': 's', 'ြ': 'j', 'ွ': 'G', 'ှ': 'S',
    'ေ': 'a', 'ာ': 'm', 'ါ': 'g', 'ိ': 'd', 'ီ': 'D',
    'ု': 'k', 'ူ': 'l', 'ဲ': 'J',
    'ံ': 'H', '့': 'h', 'း': ';', '်': 'f',
    '၀': '0', '၁': '1', '၂': '2', '၃': '3', '၄': '4',
    '၅': '5', '၆': '6', '၇': '7', '၈': '8', '၉': '9',
    '၊': '?', '။': '/'
}

pangram_win_json = json.dumps(PANGRAM_WIN_STR)
headline_win_json = json.dumps(HEADLINE_WIN_STR)
cmap_json = json.dumps(WIN_CMAP, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="my" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes, viewport-fit=cover">
    <title>Zee Motion Font Studio — Official Myanmar Font Hub (Phone & Laptop)</title>
    
    <!-- PWA & Mobile Web App Manifest -->
    <link rel="manifest" href="./manifest.json">
    <link rel="apple-touch-icon" sizes="180x180" href="./icons/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="./icons/favicon-32.png">
    <link rel="icon" type="image/x-icon" href="./favicon.ico">
    <meta name="theme-color" content="#070a13">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Zee Motion">
    <meta name="application-name" content="Zee Motion Font Studio">

    <!-- Open Graph & Social Cards -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="Zee Motion Font Studio — Official Myanmar Font Hub">
    <meta property="og:description" content="မြန်မာဖောင့် ၁၇၀+ စုစည်းမှုနှင့် မူရင်းစတိုင် တိုက်ရိုက်စမ်းသပ်ဒေါင်းလုဒ်ဆွဲနိုင်သော Official App (Mobile & Laptop)">
    <meta property="og:image" content="./icons/icon-512.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Zee Motion Font Studio — Official Myanmar Font Hub">
    <meta name="twitter:description" content="မြန်မာဖောင့် ၁၇၀+ စုစည်းမှုနှင့် မူရင်းစတိုင် တိုက်ရိုက်စမ်းသပ်ဒေါင်းလုဒ်ဆွဲနိုင်သော Official App">
    <meta name="twitter:image" content="./icons/icon-512.png">

    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Khyay&family=Tharlon&family=Noto+Sans+Myanmar:wght@300;400;500;600;700;800&family=Noto+Serif+Myanmar:wght@400;600;700&family=Padauk:wght@400;700&display=swap" rel="stylesheet">
    
    <style>
        :root {{
            --sat: env(safe-area-inset-top);
            --sab: env(safe-area-inset-bottom);
        }}
        body {{
            font-family: 'Inter', 'Noto Sans Myanmar', sans-serif;
            background-color: #070a13;
        }}

        /* Custom Scrollbar */
        ::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        ::-webkit-scrollbar-track {{
            background: #070a13;
        }}
        ::-webkit-scrollbar-thumb {{
            background: #1e293b;
            border-radius: 9999px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: #334155;
        }}

        .no-scrollbar::-webkit-scrollbar {{
            display: none;
        }}
        .no-scrollbar {{
            -ms-overflow-style: none;
            scrollbar-width: none;
        }}

        .glass-panel {{
            background: rgba(11, 15, 25, 0.92);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
        }}

        /* ================= AUTHENTIC FONT-FACE DEFINITIONS FOR ALL 172 FONTS ================= */
{all_font_faces_css}
    </style>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        gold: {{ 400: '#fbbf24', 500: '#f59e0b', 600: '#d97706' }},
                        jade: {{ 400: '#34d399', 500: '#10b981', 600: '#059669' }}
                    }}
                }}
            }}
        }}
    </script>
</head>
<body class="bg-[#070a13] text-slate-100 min-h-screen flex flex-col selection:bg-amber-500 selection:text-slate-950">

    <!-- Top Sticky Header -->
    <header class="sticky top-0 z-40 glass-panel border-b border-slate-800/80">
        <div class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 h-16 sm:h-20 flex items-center justify-between gap-2 sm:gap-4">
            
            <!-- Brand Logo & Title -->
            <a href="./index.html" class="flex items-center gap-2 sm:gap-3.5 shrink-0">
                <div class="w-9 h-9 sm:w-12 sm:h-12 rounded-xl sm:rounded-2xl overflow-hidden p-0.5 sm:p-1 bg-white/10 backdrop-blur-md border border-white/20 shadow-md shadow-emerald-500/10 shrink-0">
                    <img src="data:image/png;base64,{LOGO_BASE64}" alt="Zee Motion Logo" class="w-full h-full object-contain drop-shadow" />
                </div>
                <div>
                    <div class="flex items-center gap-1.5 sm:gap-2">
                        <h1 class="text-base sm:text-2xl font-black tracking-tight bg-gradient-to-r from-lime-300 via-emerald-400 to-cyan-400 bg-clip-text text-transparent whitespace-nowrap">
                            Zee Motion
                        </h1>
                        <span class="text-[10px] sm:text-[11px] font-bold text-slate-300 px-1.5 sm:px-2 py-0.5 rounded-lg bg-slate-800/90 border border-slate-700 whitespace-nowrap">
                            Font Studio
                        </span>
                        <span class="hidden xl:inline-block text-[11px] font-semibold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                            ✓ Official App (100% Verified)
                        </span>
                    </div>
                    <p class="hidden sm:block text-xs text-slate-400 mt-0.5 truncate">မြန်မာဖောင့် ၁၇၀+ အစုံအလင် • ဖုန်းနှင့် Laptop အားလုံးအတွက်</p>
                    <p class="sm:hidden text-[9px] text-amber-400 font-medium whitespace-nowrap">Official Myanmar Font App</p>
                </div>
            </a>

            <!-- Quick Actions -->
            <div class="flex items-center gap-1.5 sm:gap-2.5">
                
                <!-- Install App Button (Both Mobile & Laptop) -->
                <button onclick="installPwa()" id="pwaInstallHeaderBtn" class="pwa-install-btn px-2.5 sm:px-3 py-1.5 sm:py-2 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 text-xs sm:text-sm font-bold shadow-md shadow-emerald-500/20 transition flex items-center gap-1.5">
                    <span class="text-xs sm:text-sm">📲</span>
                    <span class="text-[11px] sm:text-xs">သွင်းမည်</span>
                </button>

                <!-- Official Guide Button -->
                <button onclick="openModal('guideModal')" class="px-2.5 sm:px-3.5 py-1.5 sm:py-2 rounded-xl bg-slate-800/90 hover:bg-slate-700 text-slate-200 text-xs sm:text-sm font-medium border border-slate-700 transition flex items-center gap-1.5">
                    <span class="text-amber-400 text-xs sm:text-sm">💡</span>
                    <span class="hidden md:inline">ဖောင့်သွင်းနည်းလမ်းညွှန်</span>
                    <span class="md:hidden text-[11px]">လမ်းညွှန်</span>
                </button>

                <!-- Favorites Filter -->
                <button onclick="toggleFavoritesFilter()" id="favFilterBtn" class="px-2.5 sm:px-3.5 py-1.5 sm:py-2 rounded-xl bg-slate-800/90 hover:bg-slate-700 text-slate-200 text-xs sm:text-sm font-medium border border-slate-700 transition flex items-center gap-1.5">
                    <svg class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-rose-400" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                    </svg>
                    <span class="hidden md:inline">သိမ်းထားသော</span>
                    <span id="favCountBadge" class="px-1.5 py-0.5 text-[10px] sm:text-xs rounded-full bg-slate-900 text-amber-400">0</span>
                </button>

                <!-- Desktop / Laptop Quick Downloads -->
                <a href="./Art_House_W01_to_W70_Fonts.zip" download="Art_House_W01_to_W70_Fonts.zip" class="hidden md:flex px-3 py-2 rounded-xl bg-amber-500/15 hover:bg-amber-500/25 text-amber-300 font-semibold text-xs border border-amber-500/30 transition items-center gap-1.5">
                    <span>🎨</span>
                    <span>Art House ZIP</span>
                </a>

                <button onclick="downloadSelectedBundle()" class="hidden sm:flex px-3.5 py-2 rounded-xl bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-400 hover:to-orange-400 text-slate-950 font-semibold text-xs sm:text-sm shadow-md shadow-amber-500/20 transition items-center gap-1.5">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
                    </svg>
                    <span class="hidden lg:inline">Mega Pack Download</span>
                    <span class="lg:hidden">Mega Pack</span>
                </button>

                <!-- App Share Button -->
                <button onclick="shareApp()" class="p-2 sm:px-3 sm:py-2 rounded-xl bg-slate-800/90 hover:bg-slate-700 text-slate-300 text-xs font-medium border border-slate-700 transition flex items-center gap-1" title="App မျှဝေမည်">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                    </svg>
                    <span class="hidden xl:inline">Share</span>
                </button>
            </div>
        </div>
    </header>

    <!-- Main Content Container (pb-24 ensures mobile bottom navigation doesn't block content) -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-3 sm:px-6 lg:px-8 py-4 sm:py-6 space-y-5 sm:space-y-6 pb-28 md:pb-12">
        
        <!-- Hero Banner -->
        <section class="relative overflow-hidden rounded-2xl sm:rounded-3xl bg-gradient-to-br from-slate-900 via-slate-900/95 to-slate-950 border border-slate-800 p-4 sm:p-7 shadow-2xl">
            <div class="relative z-10 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-5 sm:gap-6">
                <div class="space-y-2.5 sm:space-y-3 max-w-2xl min-w-0">
                    <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-medium">
                        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                        <span>မူရင်းဖောင့် အစစ်အမှန်များ • Phone & Laptop Compatible</span>
                    </div>
                    <h2 class="text-xl sm:text-2xl lg:text-3xl font-extrabold text-white leading-snug">
                        မြန်မာဖောင့်အစုံအလင် <span class="text-amber-400" id="heroFontCount">၁၇၀+ ခုကျော်</span> (မူရင်းစတိုင်အစစ်ဖြင့် စမ်းသပ်နိုင်သည်)
                    </h2>
                    <p class="text-slate-300 text-xs sm:text-sm leading-relaxed">
                        ဖောင့်တစ်ခုချင်းစီအတွက် မူရင်း @font-face အစစ်အမှန်များကို တိုက်ရိုက်ချိတ်ဆက်ပေးထားပါသည်။ Art House W01 မှ W70 အထိ၊ Masterpiece Uni Round၊ Aka လက်ရေးလှများနှင့် Win/Unicode စံချိန်မီဖောင့်များအားလုံးကို ကတ်တိုင်းတွင် စာရိုက်စမ်းသပ်၍ အလွယ်တကူ ဒေါင်းလုဒ်ရယူနိုင်ပါသည်။
                    </p>
                </div>

                <!-- Responsive Counters (Never clips on mobile or laptop) -->
                <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-2 gap-2 sm:gap-2.5 w-full lg:w-80 xl:w-96 shrink-0">
                    <div class="bg-slate-950/70 border border-slate-800/90 rounded-2xl p-2 sm:p-3 text-center min-w-0">
                        <div class="text-base sm:text-2xl font-bold text-amber-400 truncate" id="totalFontsStat">172+</div>
                        <div class="text-[10px] sm:text-xs text-slate-400 mt-0.5 truncate">စုစုပေါင်း ဖောင့်များ</div>
                    </div>
                    <div class="bg-slate-950/70 border border-slate-800/90 rounded-2xl p-2 sm:p-3 text-center min-w-0">
                        <div class="text-base sm:text-2xl font-bold text-emerald-400 truncate">100%</div>
                        <div class="text-[10px] sm:text-xs text-slate-400 mt-0.5 truncate">မူရင်းစစ်မှန် (True Fonts)</div>
                    </div>
                    <div class="bg-slate-950/70 border border-slate-800/90 rounded-2xl p-2 sm:p-3 text-center min-w-0">
                        <div class="text-base sm:text-2xl font-bold text-sky-400 truncate">TTF / OTF</div>
                        <div class="text-[10px] sm:text-xs text-slate-400 mt-0.5 truncate">ဖုန်း / ကွန်ပျူတာ</div>
                    </div>
                    <div class="bg-slate-950/70 border border-slate-800/90 rounded-2xl p-2 sm:p-3 text-center min-w-0">
                        <div class="text-base sm:text-2xl font-bold text-purple-400 truncate">Live Engine</div>
                        <div class="text-[10px] sm:text-xs text-slate-400 mt-0.5 truncate">တိုက်ရိုက်စမ်းရန်</div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Search & Filter Controls -->
        <section class="bg-slate-900/90 border border-slate-800 rounded-2xl sm:rounded-3xl p-3.5 sm:p-5 shadow-xl space-y-3.5 sm:space-y-4">
            <div class="flex flex-col lg:flex-row gap-3 sm:gap-4 items-stretch lg:items-center justify-between">
                
                <!-- Search Input -->
                <div class="relative flex-1">
                    <svg class="w-5 h-5 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                    </svg>
                    <input 
                        type="text" 
                        id="searchInput" 
                        placeholder="ဖောင့်အမည် ရှာရန် (ဥပမာ - W60, W70, Aka02, Masterpiece, Bagan)..."
                        class="w-full pl-11 pr-10 py-2.5 sm:py-3 bg-slate-950 border border-slate-800 rounded-xl sm:rounded-2xl text-slate-100 placeholder-slate-500 text-xs sm:text-sm focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 transition"
                    >
                    <button id="clearSearchBtn" onclick="clearSearch()" class="hidden absolute right-3 top-1/2 -translate-y-1/2 w-6 h-6 rounded-full bg-slate-800 text-slate-400 hover:text-white flex items-center justify-center text-xs">
                        ✕
                    </button>
                </div>

                <!-- Global Controls: Size & Quick Samples (Horizontally scrollable on mobile) -->
                <div class="flex flex-wrap items-center gap-2 sm:gap-3 shrink-0">
                    <div class="flex items-center gap-2 bg-slate-950 px-3 py-1.5 sm:py-2 rounded-xl sm:rounded-2xl border border-slate-800">
                        <span class="text-[11px] sm:text-xs text-slate-400">အရွယ်အစား:</span>
                        <input 
                            type="range" 
                            id="fontSizeSlider" 
                            min="14" 
                            max="48" 
                            value="22" 
                            class="w-20 sm:w-28 accent-amber-500 cursor-pointer h-2"
                        >
                        <span id="fontSizeValue" class="text-[11px] sm:text-xs font-mono text-amber-400 w-8 text-right">22px</span>
                    </div>

                    <button onclick="toggleGlobalBold()" id="globalBoldBtn" class="px-3 py-1.5 sm:py-2 rounded-xl sm:rounded-2xl bg-slate-950 border border-slate-800 text-slate-300 text-xs font-semibold hover:border-amber-500 transition">
                        B စာလုံးထူ
                    </button>

                    <!-- Horizontal scrollable sample text pills -->
                    <div class="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-0.5">
                        <button onclick="setGlobalSample('သီဟိုဠ်မှ ဉာဏ်ကြီးရှင်')" class="px-2.5 py-1.5 rounded-xl bg-slate-950 hover:bg-slate-800 border border-slate-800 text-slate-300 text-[11px] whitespace-nowrap transition">
                            သီဟိုဠ်မှ ဉာဏ်ကြီးရှင်
                        </button>
                        <button onclick="setGlobalSample('မင်္ဂလာပါ မြန်မာပြည်')" class="px-2.5 py-1.5 rounded-xl bg-slate-950 hover:bg-slate-800 border border-slate-800 text-slate-300 text-[11px] whitespace-nowrap transition">
                            မင်္ဂလာပါ မြန်မာပြည်
                        </button>
                        <button onclick="setGlobalSample('ခေါင်းစဉ် စာလုံးအလှ')" class="px-2.5 py-1.5 rounded-xl bg-slate-950 hover:bg-slate-800 border border-slate-800 text-slate-300 text-[11px] whitespace-nowrap transition">
                            ခေါင်းစဉ် စာလုံးအလှ
                        </button>
                    </div>
                </div>
            </div>

            <!-- Category Filter Tabs (Swipeable on touch screens) -->
            <div class="flex items-center gap-2 overflow-x-auto no-scrollbar scroll-smooth pt-1 pb-1">
                <button onclick="setCategory('all')" data-cat="all" class="cat-tab active px-3.5 sm:px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold whitespace-nowrap transition bg-amber-500 text-slate-950 shadow-md shadow-amber-500/20">
                    အားလုံး (<span id="catCount-all">172</span>)
                </button>
                <button onclick="setCategory('arthouse')" data-cat="arthouse" class="cat-tab px-3.5 sm:px-4 py-2 rounded-xl text-xs sm:text-sm font-medium whitespace-nowrap transition bg-slate-800/80 text-slate-300 hover:bg-slate-800">
                    🎨 Art House & စာလုံးထူများ (<span id="catCount-arthouse">0</span>)
                </button>
                <button onclick="setCategory('masterpiece')" data-cat="masterpiece" class="cat-tab px-3.5 sm:px-4 py-2 rounded-xl text-xs sm:text-sm font-medium whitespace-nowrap transition bg-slate-800/80 text-slate-300 hover:bg-slate-800">
                    💎 Masterpiece & Round (<span id="catCount-masterpiece">0</span>)
                </button>
                <button onclick="setCategory('handwriting')" data-cat="handwriting" class="cat-tab px-3.5 sm:px-4 py-2 rounded-xl text-xs sm:text-sm font-medium whitespace-nowrap transition bg-slate-800/80 text-slate-300 hover:bg-slate-800">
                    ✍️ Aka & လက်ရေးလှဖောင့်များ (<span id="catCount-handwriting">0</span>)
                </button>
                <button onclick="setCategory('uni-myanmar')" data-cat="uni-myanmar" class="cat-tab px-3.5 sm:px-4 py-2 rounded-xl text-xs sm:text-sm font-medium whitespace-nowrap transition bg-slate-800/80 text-slate-300 hover:bg-slate-800">
                    📂 Uni-Myanmar စုစည်းမှုများ (<span id="catCount-uni-myanmar">0</span>)
                </button>
                <button onclick="setCategory('unicode')" data-cat="unicode" class="cat-tab px-3.5 sm:px-4 py-2 rounded-xl text-xs sm:text-sm font-medium whitespace-nowrap transition bg-slate-800/80 text-slate-300 hover:bg-slate-800">
                    🌟 Unicode စံချိန်မီ & ရုံးသုံး (<span id="catCount-unicode">0</span>)
                </button>
                <button onclick="setCategory('win')" data-cat="win" class="cat-tab px-3.5 sm:px-4 py-2 rounded-xl text-xs sm:text-sm font-medium whitespace-nowrap transition bg-slate-800/80 text-slate-300 hover:bg-slate-800">
                    🖨️ Win Myanmar (ပုံနှိပ်ဖောင့်များ) (<span id="catCount-win">0</span>)
                </button>
                <button onclick="setCategory('zawgyi')" data-cat="zawgyi" class="cat-tab px-3.5 sm:px-4 py-2 rounded-xl text-xs sm:text-sm font-medium whitespace-nowrap transition bg-slate-800/80 text-slate-300 hover:bg-slate-800">
                    📜 Zawgyi & Legacy (<span id="catCount-zawgyi">0</span>)
                </button>
            </div>
        </section>

        <!-- Search Status Bar -->
        <div class="flex items-center justify-between gap-2 px-1">
            <p class="text-xs sm:text-sm text-slate-400">
                ရှာဖွေတွေ့ရှိသော မူရင်းဖောင့်အရေအတွက်: <span id="resultCount" class="text-white font-bold">172</span> ခု
            </p>
            <div class="flex items-center gap-2 text-xs text-slate-400">
                <span class="hidden sm:inline">စီစဉ်မှု:</span>
                <select id="sortSelect" onchange="renderFonts()" class="bg-slate-900 border border-slate-800 rounded-xl px-2.5 sm:px-3 py-1.5 text-slate-200 text-xs focus:outline-none focus:border-amber-500">
                    <option value="popular">လူသုံးအများဆုံး (Popular)</option>
                    <option value="name">အမည် အစဉ်လိုက် (A - Z)</option>
                    <option value="category">အမျိုးအစားအလိုက် (Category)</option>
                </select>
            </div>
        </div>

        <!-- Fonts Grid with Live Specimen Cards -->
        <section id="fontGrid" class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
            <!-- Dynamically populated via renderFonts() -->
        </section>

        <!-- Empty State -->
        <div id="emptyState" class="hidden text-center py-16 bg-slate-900/50 rounded-3xl border border-slate-800/80">
            <div class="w-16 h-16 rounded-2xl bg-slate-800 mx-auto flex items-center justify-center text-2xl mb-4">
                🔍
            </div>
            <h3 class="text-base sm:text-lg font-bold text-white mb-1">မည်သည့်ဖောင့်မှ မတွေ့ရှိပါ</h3>
            <p class="text-xs sm:text-sm text-slate-400 max-w-md mx-auto">
                အခြားစာလုံးပေါင်း သို့မဟုတ် အမျိုးအစားခလုတ်များကို ပြောင်းလဲရှာဖွေကြည့်ပါ။
            </p>
            <button onclick="clearSearch()" class="mt-4 px-4 py-2 rounded-xl bg-amber-500 text-slate-950 font-semibold text-xs sm:text-sm">
                ရှာဖွေမှုကို ရှင်းလင်းမည်
            </button>
        </div>

        <!-- Official Repositories & Open Source Section -->
        <section class="mt-12 pt-8 border-t border-slate-800/80 space-y-4">
            <div class="flex items-center justify-between">
                <div>
                    <h3 class="text-base sm:text-lg font-bold text-white flex items-center gap-2">
                        <span>🌐</span> တရားဝင် မြန်မာဖောင့် ရင်းမြစ် GitHub Repositories များ
                    </h3>
                    <p class="text-xs text-slate-400 mt-0.5">Community မှ open-source ပြုလုပ်ထားသော GitHub repositories များနှင့် တရားဝင် ဒေါင်းလုဒ်လင့်ခ်များ</p>
                </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <a href="https://github.com/AungMyoKyaw/Myanmar-Unicode-Fonts" target="_blank" rel="noopener" class="p-4 rounded-2xl bg-slate-900/70 border border-slate-800 hover:border-amber-500/50 transition group block">
                    <div class="flex items-center justify-between text-xs text-slate-400 mb-2">
                        <span class="px-2 py-0.5 rounded bg-slate-800 text-[10px] font-mono">GitHub</span>
                        <span class="group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition">↗</span>
                    </div>
                    <h4 class="font-bold text-slate-200 group-hover:text-amber-400 transition text-sm">AungMyoKyaw / Fonts</h4>
                    <p class="text-xs text-slate-400 mt-1 line-clamp-2">Masterpiece, MyanmarBlack, Pyidaungsu နှင့် Unicode ဖောင့်စုံ</p>
                </a>

                <a href="https://github.com/lecramyajiv/fonts-myanmar-extra" target="_blank" rel="noopener" class="p-4 rounded-2xl bg-slate-900/70 border border-slate-800 hover:border-amber-500/50 transition group block">
                    <div class="flex items-center justify-between text-xs text-slate-400 mb-2">
                        <span class="px-2 py-0.5 rounded bg-slate-800 text-[10px] font-mono">Open Source</span>
                        <span class="group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition">↗</span>
                    </div>
                    <h4 class="font-bold text-slate-200 group-hover:text-amber-400 transition text-sm">Fonts Myanmar Extra</h4>
                    <p class="text-xs text-slate-400 mt-1 line-clamp-2">Masterpiece Lakwel, HeadOne, Chatu နှင့် ဒေသန္တရဖောင့်များ</p>
                </a>

                <a href="https://github.com/moekyawsoe/myanmar-fonts" target="_blank" rel="noopener" class="p-4 rounded-2xl bg-slate-900/70 border border-slate-800 hover:border-amber-500/50 transition group block">
                    <div class="flex items-center justify-between text-xs text-slate-400 mb-2">
                        <span class="px-2 py-0.5 rounded bg-slate-800 text-[10px] font-mono">Collection</span>
                        <span class="group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition">↗</span>
                    </div>
                    <h4 class="font-bold text-slate-200 group-hover:text-amber-400 transition text-sm">Moekyawsoe Myanmar Fonts</h4>
                    <p class="text-xs text-slate-400 mt-1 line-clamp-2">Win Innwa, Zawgyi-One, Pyidaungsu ပုံနှိပ်ဖောင့်အစုံ</p>
                </a>

                <a href="https://fonts.google.com/?query=myanmar" target="_blank" rel="noopener" class="p-4 rounded-2xl bg-slate-900/70 border border-slate-800 hover:border-amber-500/50 transition group block">
                    <div class="flex items-center justify-between text-xs text-slate-400 mb-2">
                        <span class="px-2 py-0.5 rounded bg-slate-800 text-[10px] font-mono">Google Fonts</span>
                        <span class="group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition">↗</span>
                    </div>
                    <h4 class="font-bold text-slate-200 group-hover:text-amber-400 transition text-sm">Google Myanmar Fonts</h4>
                    <p class="text-xs text-slate-400 mt-1 line-clamp-2">Noto Sans, Noto Serif, Padauk, Tharlon နှင့် Khyay ဖောင့်များ</p>
                </a>
            </div>
        </section>

    </main>

    <!-- Mobile Bottom Navigation Bar (Phone Only) -->
    <nav class="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-slate-900/95 backdrop-blur-md border-t border-slate-800 px-2 py-2 flex items-center justify-around text-center" style="padding-bottom: max(env(safe-area-inset-bottom), 8px);">
        <button onclick="setCategory('all'); window.scrollTo({{top: 0, behavior: 'smooth'}});" class="flex flex-col items-center gap-1 text-slate-300 hover:text-amber-400 text-[10px] font-medium p-1">
            <span class="text-base">🏠</span>
            <span>အားလုံး</span>
        </button>
        <button onclick="setCategory('arthouse');" class="flex flex-col items-center gap-1 text-slate-300 hover:text-amber-400 text-[10px] font-medium p-1">
            <span class="text-base">🎨</span>
            <span>Art House</span>
        </button>
        <button onclick="openModal('guideModal')" class="flex flex-col items-center gap-1 text-slate-300 hover:text-amber-400 text-[10px] font-medium p-1">
            <span class="text-base">📱</span>
            <span>ဖောင့်သွင်းနည်း</span>
        </button>
        <button onclick="toggleFavoritesFilter()" class="flex flex-col items-center gap-1 text-slate-300 hover:text-amber-400 text-[10px] font-medium p-1 relative">
            <span class="text-base">❤️</span>
            <span>သိမ်းထား</span>
            <span id="mobileFavCountBadge" class="hidden absolute -top-1 right-1 w-4 h-4 text-[9px] rounded-full bg-rose-500 text-white flex items-center justify-center font-bold">0</span>
        </button>
        <button onclick="installPwa()" class="flex flex-col items-center gap-1 text-emerald-400 hover:text-emerald-300 text-[10px] font-bold p-1">
            <span class="text-base">📲</span>
            <span>အက်ပ်သွင်း</span>
        </button>
    </nav>

    <!-- Floating PWA Install Banner -->
    <div id="pwaInstallBanner" class="hidden fixed bottom-20 md:bottom-6 left-3 right-3 md:left-auto md:right-6 md:max-w-md z-40 bg-slate-900/95 backdrop-blur-md border border-emerald-500/40 rounded-2xl p-3.5 shadow-2xl flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-xl shrink-0">
            📲
        </div>
        <div class="flex-1 min-w-0">
            <h4 class="text-xs sm:text-sm font-bold text-white truncate">Zee Motion Font Studio အက်ပ်</h4>
            <p class="text-[11px] text-slate-400 truncate">ဖုန်း (သို့) ကွန်ပျူတာ Home Screen တွင် Official App အဖြစ် သွင်းပါ</p>
        </div>
        <div class="flex items-center gap-1.5 shrink-0">
            <button onclick="installPwa()" class="px-3 py-1.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-xs font-bold shadow-md transition">
                သွင်းမည်
            </button>
            <button onclick="dismissPwaBanner()" class="p-1.5 text-slate-400 hover:text-white rounded-lg">
                ✕
            </button>
        </div>
    </div>

    <!-- Footer -->
    <footer class="border-t border-slate-900 bg-slate-950/80 py-8 text-center text-xs text-slate-500 space-y-2 pb-24 md:pb-8">
        <p>© 2026 Zee Motion — ရနိုင်သမျှ မြန်မာဖောင့် ၁၇၀+ အစုံအလင် စုစည်းရာ Official Font Hub</p>
        <p>ဖောင့်မူပိုင်ခွင့်များအားလုံးသည် မူရင်းဖန်တီးသူ ဒီဇိုင်နာများနှင့် Graphic Studios များထံ၌သာ ရှိပါသည်။</p>
    </footer>

    <!-- Toast Notifications -->
    <div id="toastContainer" class="fixed top-4 right-4 z-50 flex flex-col gap-2 pointer-events-none"></div>

    <!-- Font Detail Modal -->
    <div id="fontDetailModal" class="fixed inset-0 z-50 hidden bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-3 sm:p-4">
        <div class="bg-slate-900 border border-slate-800 rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-4 sm:p-6 shadow-2xl space-y-4">
            <div class="flex items-start justify-between border-b border-slate-800 pb-3">
                <div>
                    <div class="flex items-center gap-2">
                        <h3 id="modalFontTitle" class="text-lg sm:text-xl font-bold text-white">Font Name</h3>
                        <span id="modalFontBadge" class="text-xs px-2.5 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20">Category</span>
                    </div>
                    <p id="modalFontDesigner" class="text-xs text-slate-400 mt-1">Designer info</p>
                </div>
                <button onclick="closeModal('fontDetailModal')" class="p-2 rounded-xl bg-slate-800 text-slate-400 hover:text-white">✕</button>
            </div>

            <!-- Waterfall Preview -->
            <div class="space-y-3">
                <h4 class="text-xs font-semibold text-slate-400 uppercase tracking-wider">စာလုံးအရွယ်အစား နမူနာများ (Waterfall)</h4>
                <div id="modalWaterfall" class="space-y-3 bg-slate-950 p-4 rounded-2xl border border-slate-800 overflow-x-hidden"></div>
            </div>

            <!-- Character Map -->
            <div class="space-y-2">
                <h4 class="text-xs font-semibold text-slate-400 uppercase tracking-wider">အက္ခရာဇယား (Glyphs Preview)</h4>
                <div id="modalCharMap" class="grid grid-cols-6 sm:grid-cols-8 gap-2 bg-slate-950 p-3 rounded-2xl border border-slate-800 text-center text-sm font-medium max-h-40 overflow-y-auto"></div>
            </div>

            <!-- CSS Code Snippet -->
            <div class="space-y-2">
                <div class="flex items-center justify-between text-xs text-slate-400">
                    <span class="font-semibold uppercase tracking-wider">Web Font CSS ကုဒ်</span>
                    <button onclick="copyCssSnippet()" class="text-amber-400 hover:text-amber-300 font-medium">ကုဒ် ကူးယူမည် (Copy)</button>
                </div>
                <pre class="bg-slate-950 p-3 rounded-xl border border-slate-800 text-xs font-mono text-emerald-400 overflow-x-auto"><code id="modalCssCode"></code></pre>
            </div>

            <div class="flex items-center justify-end gap-3 pt-3 border-t border-slate-800">
                <button onclick="closeModal('fontDetailModal')" class="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 text-xs sm:text-sm font-medium hover:bg-slate-700">
                    ပိတ်မည်
                </button>
                <button id="modalDownloadBtn" class="px-4 py-2 rounded-xl bg-gradient-to-r from-amber-500 to-orange-500 text-slate-950 font-bold text-xs sm:text-sm shadow-lg shadow-amber-500/20">
                    ဖောင့်ကို ဒေါင်းလုဒ်ဆွဲမည်
                </button>
            </div>
        </div>
    </div>

    <!-- Official Device Installation & Usage Guide Modal -->
    <div id="guideModal" class="fixed inset-0 z-50 hidden bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-3 sm:p-4">
        <div class="bg-slate-900 border border-slate-800 rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-4 sm:p-6 shadow-2xl space-y-4">
            <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                <h3 class="text-base sm:text-lg font-bold text-white flex items-center gap-2">
                    <span>💡</span> ဖုန်းနှင့် Laptop တွင် ဖောင့်သွင်းနည်း လမ်းညွှန်
                </h3>
                <button onclick="closeModal('guideModal')" class="p-2 rounded-xl bg-slate-800 text-slate-400 hover:text-white">✕</button>
            </div>

            <!-- Guide Tabs -->
            <div class="flex items-center gap-2 overflow-x-auto no-scrollbar border-b border-slate-800 pb-2">
                <button onclick="switchGuideTab('tab-ios')" id="btn-tab-ios" class="guide-tab-btn active px-3 py-1.5 rounded-xl bg-amber-500 text-slate-950 font-bold text-xs whitespace-nowrap">
                    📱 iPhone / iOS
                </button>
                <button onclick="switchGuideTab('tab-android')" id="btn-tab-android" class="guide-tab-btn px-3 py-1.5 rounded-xl bg-slate-800 text-slate-300 font-medium text-xs whitespace-nowrap">
                    🤖 Android ဖုန်းများ
                </button>
                <button onclick="switchGuideTab('tab-desktop')" id="btn-tab-desktop" class="guide-tab-btn px-3 py-1.5 rounded-xl bg-slate-800 text-slate-300 font-medium text-xs whitespace-nowrap">
                    💻 Laptop (Mac / Windows)
                </button>
                <button onclick="switchGuideTab('tab-pwa')" id="btn-tab-pwa" class="guide-tab-btn px-3 py-1.5 rounded-xl bg-slate-800 text-slate-300 font-medium text-xs whitespace-nowrap">
                    📲 Official App သွင်းနည်း
                </button>
            </div>

            <!-- Tab 1: iOS -->
            <div id="tab-ios" class="guide-content space-y-3 text-xs sm:text-sm text-slate-300 leading-relaxed">
                <div class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 space-y-2">
                    <h4 class="font-bold text-amber-400 flex items-center gap-1.5">
                        <span>🍏</span> နည်းလမ်း ၁ - iFont အက်ပ်ဖြင့် iPhone စနစ်ထဲ ထည့်သွင်းနည်း (System-wide)
                    </h4>
                    <ol class="list-decimal list-inside space-y-1.5 text-slate-300">
                        <li>Zee Motion ထဲမှ မိမိနှစ်သက်ရာဖောင့်ကို <span class="text-amber-400 font-semibold">Free Download</span> နှိပ်၍ ဒေါင်းလုဒ်ဆွဲပါ။</li>
                        <li>App Store မှ အခမဲ့ရနိုင်သော <strong class="text-white">iFont: find install any font</strong> အက်ပ်ကို ဒေါင်းလုဒ်ရယူပါ။</li>
                        <li>ဒေါင်းထားသော `.ttf` ဖိုင်ကို ဖွင့်ပြီး <strong class="text-white">Share > Open with iFont</strong> ကို ရွေးပါ။</li>
                        <li>iFont အက်ပ်ထဲတွင် <span class="text-emerald-400 font-semibold">Install</span> နှိပ်ပြီး Safari မှ Profile ဒေါင်းလုဒ်ကို <span class="text-emerald-400">Allow</span> လုပ်ပေးပါ။</li>
                        <li>iPhone ၏ <strong class="text-white">Settings > Profile Downloaded > Install</strong> နှိပ်၍ Passcode ရိုက်ထည့်ကာ အတည်ပြုပါ။ Pages, Keynote, Canva နှင့် ဗီဒီယိုအက်ပ်များတွင် စနစ်ဖောင့်အဖြစ် အသုံးပြုနိုင်ပါပြီ။</li>
                    </ol>
                </div>

                <div class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 space-y-2">
                    <h4 class="font-bold text-sky-400 flex items-center gap-1.5">
                        <span>🎬</span> နည်းလမ်း ၂ - CapCut iOS တွင် တိုက်ရိုက်ထည့်သွင်းနည်း
                    </h4>
                    <p class="text-slate-400">
                        CapCut ဖွင့်ပါ > Text ထည့်ပါ > <strong class="text-white">Font > Add Font (+) > Upload File</strong> ကို နှိပ်ပြီး ဒေါင်းလုဒ်ဆွဲထားသော `.ttf` ဖိုင်ကို ရွေးချယ်ပေးရုံဖြင့် ချက်ချင်း အသုံးပြုနိုင်ပါသည်။
                    </p>
                </div>
            </div>

            <!-- Tab 2: Android -->
            <div id="tab-android" class="guide-content hidden space-y-3 text-xs sm:text-sm text-slate-300 leading-relaxed">
                <div class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 space-y-2">
                    <h4 class="font-bold text-emerald-400 flex items-center gap-1.5">
                        <span>🎬</span> CapCut, PixelLab, InShot, Canva တွင် ဖောင့်ထည့်သွင်းနည်း
                    </h4>
                    <ol class="list-decimal list-inside space-y-1.5 text-slate-300">
                        <li>Zee Motion မှ ဖောင့်ကို ဒေါင်းလုဒ်ဆွဲပါ (ဖုန်း၏ `Download` ဖိုဒါထဲသို့ ရောက်ရှိသွားပါမည်)။</li>
                        <li><strong class="text-white">CapCut Mobile</strong> တွင် Text > Font > <span class="text-amber-400 font-bold">+ (Add Font)</span> > ဖုန်းထဲမှ .ttf ဖိုင်ကို ရွေးပေးပါ။</li>
                        <li><strong class="text-white">PixelLab</strong> တွင် Font > My Fonts > ဖိုဒါအိုင်ကွန် (+) ကို နှိပ်ပြီး `Download` ဖိုဒါထဲမှ ဖောင့်ကို ရွေးပါ။</li>
                        <li><strong class="text-white">InShot</strong> တွင် Text > Font > အိတ်အိုင်ကွန် (Store) ဘေးရှိ Import (+) ကို နှိပ်ပြီး ထည့်သွင်းပါ။</li>
                    </ol>
                </div>

                <div class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 space-y-2">
                    <h4 class="font-bold text-purple-400 flex items-center gap-1.5">
                        <span>📲</span> Samsung, Xiaomi, Oppo, Vivo စနစ်တစ်ခုလုံး ဖောင့်ပြောင်းနည်း
                    </h4>
                    <p class="text-slate-400">
                        Play Store မှ <strong class="text-white">zFont 3</strong> အက်ပ်ကို အသုံးပြု၍ Zee Motion မှ ဒေါင်းလုဒ်ဆွဲထားသော ဖောင့်ကို System Font အဖြစ် လွယ်ကူစွာ သွင်းယူနိုင်ပါသည်။
                    </p>
                </div>
            </div>

            <!-- Tab 3: Desktop / Laptop -->
            <div id="tab-desktop" class="guide-content hidden space-y-3 text-xs sm:text-sm text-slate-300 leading-relaxed">
                <div class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 space-y-2">
                    <h4 class="font-bold text-amber-400 flex items-center gap-1.5">
                        <span>🪟</span> Windows Laptop & PC (Windows 10 / 11)
                    </h4>
                    <p class="text-slate-300">
                        ဒေါင်းလုဒ်ရရှိသော `.ttf` ဖိုင်ပေါ်တွင် <strong class="text-white">Right Click</strong> နှိပ်ပါ > <span class="text-amber-400 font-semibold">Install for all users</span> (သို့မဟုတ် Install) ကို နှိပ်ရုံဖြင့် အလိုအလျောက် သွင်းပေးသွားပါမည်။
                    </p>
                </div>

                <div class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 space-y-2">
                    <h4 class="font-bold text-sky-400 flex items-center gap-1.5">
                        <span>🍎</span> Apple Mac (MacBook, iMac, Mac mini)
                    </h4>
                    <p class="text-slate-300">
                        ဒေါင်းလုဒ်ရရှိသော `.ttf` ဖိုင်ကို <strong class="text-white">Double Click</strong> နှိပ်ပါ > ပွင့်လာသော Font Book ပေါ်တွင် <span class="text-sky-400 font-semibold">Install Font</span> ကို နှိပ်ပါ။
                    </p>
                </div>

                <div class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 space-y-2">
                    <h4 class="font-bold text-purple-400 flex items-center gap-1.5">
                        <span>🎨</span> Photoshop, Premiere Pro, After Effects, CapCut PC
                    </h4>
                    <p class="text-slate-400">
                        ကွန်ပျူတာထဲ ဖောင့်သွင်းပြီးပါက သက်ဆိုင်ရာ Software ကို ပိတ်ပြီး ပြန်ဖွင့်ရုံဖြင့် Font Selector ထဲတွင် ဖောင့်အမည်ဖြင့် တိုက်ရိုက်ရိုက်ထည့် အသုံးပြုနိုင်ပါသည်။
                    </p>
                </div>
            </div>

            <!-- Tab 4: PWA Install -->
            <div id="tab-pwa" class="guide-content hidden space-y-3 text-xs sm:text-sm text-slate-300 leading-relaxed">
                <div class="p-3.5 rounded-2xl bg-slate-950 border border-slate-800 space-y-2">
                    <h4 class="font-bold text-emerald-400 flex items-center gap-1.5">
                        <span>📲</span> Official App အဖြစ် Home Screen တွင် သွင်းယူနည်း (PWA)
                    </h4>
                    <ul class="space-y-2 text-slate-300">
                        <li class="flex items-start gap-2">
                            <span class="text-base">🍎</span>
                            <div>
                                <strong class="text-white">iPhone (Safari):</strong> မျက်နှာပြင်အောက်ခြေရှိ <strong class="text-white">Share (⎋)</strong> အိုင်ကွန်ကို နှိပ်ပါ > အောက်သို့ဆွဲပြီး <span class="text-amber-400 font-semibold">"Add to Home Screen (ပင်မစာမျက်နှာသို့ ထည့်ပါ ⊕)"</span> ကို နှိပ်ပါ။
                            </div>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-base">🤖</span>
                            <div>
                                <strong class="text-white">Android (Chrome):</strong> ညာဘက်အပေါ်ရှိ မီနူး <strong class="text-white">(⋮)</strong> ကို နှိပ်ပါ > <span class="text-emerald-400 font-semibold">"Install app (သို့) Add to Home screen"</span> ကို ရွေးပါ။
                            </div>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-base">💻</span>
                            <div>
                                <strong class="text-white">Laptop (Chrome / Edge):</strong> Address Bar ၏ ညာဘက်စွန်းရှိ <span class="text-sky-400 font-semibold">Install Icon (⊕)</span> ကို နှိပ်၍ သီးခြား App Window အဖြစ် တပ်ဆင်နိုင်ပါသည်။
                            </div>
                        </li>
                    </ul>
                </div>
            </div>

            <div class="flex justify-end pt-2 border-t border-slate-800">
                <button onclick="closeModal('guideModal')" class="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 text-xs sm:text-sm font-medium hover:bg-slate-700">
                    နားလည်ပါပြီ
                </button>
            </div>
        </div>
    </div>

    <script>
        const MYANMAR_FONTS = {catalog_json};
        const PANGRAM_WIN = {pangram_win_json};
        const HEADLINE_WIN = {headline_win_json};
        const WIN_CMAP = {cmap_json};
        const MYANMAR_CHARS = ['က','ခ','ဂ','ဃ','င','စ','ဆ','ဇ','ဈ','ဉ','ည','ဋ','ဌ','ဍ','ဎ','ဏ','တ','ထ','ဒ','ဓ','န','ပ','ဖ','ဗ','ဘ','မ','ယ','ရ','လ','ဝ','သ','ဟ','ဠ','အ'];

        let activeCategory = 'all';
        let currentFontSize = 22;
        let isGlobalBold = false;
        let favoritesOnly = false;
        let savedFavorites = JSON.parse(localStorage.getItem('mm_font_favs_v9') || '[]');
        let winModeState = {{}}; // 'auto' | 'direct'
        let deferredPrompt = null;

        // PWA Registration & Install Event
        window.addEventListener('beforeinstallprompt', (e) => {{
            e.preventDefault();
            deferredPrompt = e;
            document.querySelectorAll('.pwa-install-btn').forEach(btn => btn.classList.remove('hidden'));
            const banner = document.getElementById('pwaInstallBanner');
            if (banner && !localStorage.getItem('dismissedPwaBanner')) {{
                banner.classList.remove('hidden');
            }}
        }});

        function installPwa() {{
            if (deferredPrompt) {{
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then((choiceResult) => {{
                    if (choiceResult.outcome === 'accepted') {{
                        showToast('Zee Motion App အား အောင်မြင်စွာ တပ်ဆင်လိုက်ပါပြီ! 🎉', 'success');
                    }}
                    deferredPrompt = null;
                }});
            }} else {{
                // Fallback: Open PWA guide tab
                openModal('guideModal');
                switchGuideTab('tab-pwa');
            }}
        }}

        function dismissPwaBanner() {{
            const banner = document.getElementById('pwaInstallBanner');
            if (banner) banner.classList.add('hidden');
            localStorage.setItem('dismissedPwaBanner', 'true');
        }}

        // Service Worker
        if ('serviceWorker' in navigator) {{
            window.addEventListener('load', () => {{
                navigator.serviceWorker.register('./sw.js').then((reg) => {{
                    console.log('Zee Motion PWA ServiceWorker active:', reg.scope);
                }}).catch(() => {{}});
            }});
        }}

        // Sharing
        function shareApp() {{
            if (navigator.share) {{
                navigator.share({{
                    title: 'Zee Motion Font Studio',
                    text: 'မြန်မာဖောင့် ၁၇၀+ စုစည်းမှုနှင့် မူရင်းစတိုင် တိုက်ရိုက်စမ်းသပ်ဒေါင်းလုဒ်ဆွဲနိုင်သော Official App',
                    url: window.location.href
                }}).catch(() => {{}});
            }} else {{
                navigator.clipboard.writeText(window.location.href).then(() => {{
                    showToast('ဝက်ဘ်ဆိုက်လင့်ခ်ကို Copy ကူးယူပြီးပါပြီ! 🔗', 'success');
                }}).catch(() => {{}});
            }}
        }}

        function shareFont(fontId) {{
            const font = MYANMAR_FONTS.find(f => f.id === fontId);
            if (!font) return;
            const shareUrl = window.location.origin + window.location.pathname + '?q=' + encodeURIComponent(font.name);
            if (navigator.share) {{
                navigator.share({{
                    title: `${{font.name}} — Zee Motion`,
                    text: `${{font.name}} (${{font.mmName}}) မြန်မာဖောင့်ကို Zee Motion Font Studio တွင် စမ်းသပ်ဒေါင်းလုဒ်ဆွဲပါ`,
                    url: shareUrl
                }}).catch(() => {{}});
            }} else {{
                navigator.clipboard.writeText(shareUrl).then(() => {{
                    showToast(`${{font.name}} ဖောင့်လင့်ခ်ကို Copy ကူးယူပြီးပါပြီ! 🔗`, 'success');
                }}).catch(() => {{}});
            }}
        }}

        // Guide Tabs
        function switchGuideTab(tabId) {{
            document.querySelectorAll('.guide-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.guide-tab-btn').forEach(btn => {{
                btn.className = 'guide-tab-btn px-3 py-1.5 rounded-xl bg-slate-800 text-slate-300 font-medium text-xs whitespace-nowrap';
            }});
            const target = document.getElementById(tabId);
            if (target) target.classList.remove('hidden');
            const targetBtn = document.getElementById('btn-' + tabId);
            if (targetBtn) {{
                targetBtn.className = 'guide-tab-btn active px-3 py-1.5 rounded-xl bg-amber-500 text-slate-950 font-bold text-xs whitespace-nowrap';
            }}
        }}

        // Unicode to Win Converter Engine
        function unicodeToWin(text) {{
            if (!text) return '';
            let out = text;

            // Reorder E-vowel
            out = out.replace(/([က-အ])([ေ])/g, '$2$1');
            out = out.replace(/([က-အ])([ြ-ှ]+)([ေ])/g, '$3$1$2');

            // Medials & vowels
            out = out.replace(/ျွှ/g, 'Gs');
            out = out.replace(/ျှ/g, 'sS');
            out = out.replace(/ြွှ/g, 'Gj');
            out = out.replace(/ြှ/g, 'jS');
            out = out.replace(/ွှ/g, 'GS');
            out = out.replace(/ို/g, 'dkd');
            out = out.replace(/ိ/g, 'd');
            out = out.replace(/ီ/g, 'D');
            out = out.replace(/ု/g, 'k');
            out = out.replace(/ူ/g, 'l');
            out = out.replace(/ဲ/g, 'J');
            out = out.replace(/ံ/g, 'H');
            out = out.replace(/့/g, 'h');
            out = out.replace(/း/g, ';');
            out = out.replace(/်/g, 'f');
            out = out.replace(/ျ/g, 's');
            out = out.replace(/ြ/g, 'j');
            out = out.replace(/ွ/g, 'G');
            out = out.replace(/ှ/g, 'S');
            out = out.replace(/ေ/g, 'a');
            out = out.replace(/ာ/g, 'm');
            out = out.replace(/ါ/g, 'g');

            // Character Map lookup
            let res = '';
            for (let i = 0; i < out.length; i++) {{
                const c = out[i];
                res += WIN_CMAP[c] !== undefined ? WIN_CMAP[c] : c;
            }}
            return res;
        }}

        function initApp() {{
            const totalCount = MYANMAR_FONTS.length;
            document.getElementById('totalFontsStat').textContent = totalCount + '+';
            document.getElementById('heroFontCount').textContent = totalCount + ' ခုကျော်';
            document.getElementById('catCount-all').textContent = totalCount;

            // Compute category counts
            const counts = {{
                'arthouse': 0, 'masterpiece': 0, 'handwriting': 0,
                'uni-myanmar': 0, 'unicode': 0, 'win': 0, 'zawgyi': 0
            }};
            MYANMAR_FONTS.forEach(f => {{
                if (counts[f.category] !== undefined) counts[f.category]++;
            }});
            for (const cat in counts) {{
                const el = document.getElementById('catCount-' + cat);
                if (el) el.textContent = counts[cat];
            }}

            updateFavBadge();
            const urlParams = new URLSearchParams(window.location.search);
            const initialCat = urlParams.get('cat') || window.location.hash.replace('#', '');
            const initialQuery = urlParams.get('q');
            if (initialQuery) {{
                document.getElementById('searchInput').value = initialQuery;
                document.getElementById('clearSearchBtn').classList.remove('hidden');
            }}
            if (initialCat && counts[initialCat] !== undefined) {{
                setCategory(initialCat);
            }} else {{
                renderFonts();
            }}

            // Search input listener
            document.getElementById('searchInput').addEventListener('input', (e) => {{
                const clearBtn = document.getElementById('clearSearchBtn');
                clearBtn.classList.toggle('hidden', !e.target.value.trim());
                renderFonts();
            }});

            // Font size slider listener
            document.getElementById('fontSizeSlider').addEventListener('input', (e) => {{
                currentFontSize = parseInt(e.target.value, 10);
                document.getElementById('fontSizeValue').textContent = currentFontSize + 'px';
                document.querySelectorAll('.live-specimen-textarea').forEach(el => {{
                    el.style.fontSize = currentFontSize + 'px';
                }});
            }});
        }}

        function setCategory(cat) {{
            activeCategory = cat;
            document.querySelectorAll('.cat-tab').forEach(tab => {{
                if (tab.dataset.cat === cat) {{
                    tab.className = 'cat-tab active px-3.5 sm:px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold whitespace-nowrap transition bg-amber-500 text-slate-950 shadow-md shadow-amber-500/20';
                }} else {{
                    tab.className = 'cat-tab px-3.5 sm:px-4 py-2 rounded-xl text-xs sm:text-sm font-medium whitespace-nowrap transition bg-slate-800/80 text-slate-300 hover:bg-slate-800';
                }}
            }});
            renderFonts();
        }}

        function clearSearch() {{
            document.getElementById('searchInput').value = '';
            document.getElementById('clearSearchBtn').classList.add('hidden');
            renderFonts();
        }}

        function toggleGlobalBold() {{
            isGlobalBold = !isGlobalBold;
            const btn = document.getElementById('globalBoldBtn');
            btn.classList.toggle('bg-amber-500', isGlobalBold);
            btn.classList.toggle('text-slate-950', isGlobalBold);
            btn.classList.toggle('bg-slate-950', !isGlobalBold);
            btn.classList.toggle('text-slate-300', !isGlobalBold);
            document.querySelectorAll('.live-specimen-textarea').forEach(el => {{
                el.classList.toggle('font-bold', isGlobalBold);
            }});
        }}

        function setGlobalSample(text) {{
            document.querySelectorAll('.live-specimen-textarea').forEach(el => {{
                const fontId = el.dataset.fontId;
                const font = MYANMAR_FONTS.find(f => f.id === fontId);
                if (font) {{
                    const mode = winModeState[fontId] || 'auto';
                    if (font.isWin && mode === 'auto') {{
                        el.value = unicodeToWin(text);
                    }} else {{
                        el.value = text;
                    }}
                }}
            }});
        }}

        function toggleWinMode(fontId) {{
            const current = winModeState[fontId] || 'auto';
            const next = current === 'auto' ? 'direct' : 'auto';
            winModeState[fontId] = next;

            const btn = document.getElementById('winToggle-' + fontId);
            if (btn) {{
                if (next === 'auto') {{
                    btn.className = 'text-[10px] px-2 py-0.5 rounded-md bg-amber-500/10 text-amber-400 border border-amber-500/20 font-semibold';
                    btn.innerHTML = '⚡ Auto-Win Active';
                }} else {{
                    btn.className = 'text-[10px] px-2 py-0.5 rounded-md bg-slate-800 text-slate-400 border border-slate-700';
                    btn.innerHTML = '⌨️ Direct Win Layout';
                }}
            }}

            const textarea = document.getElementById('specimen-' + fontId);
            if (textarea) {{
                if (next === 'auto') {{
                    textarea.value = unicodeToWin('မင်္ဂလာပါ မြန်မာပြည်');
                }} else {{
                    textarea.value = 'r*Fvmyg jrefrmjynf';
                }}
            }}
        }}

        function handleSpecimenInput(textarea, fontId) {{
            const font = MYANMAR_FONTS.find(f => f.id === fontId);
            if (!font || !font.isWin) return;

            const mode = winModeState[fontId] || 'auto';
            if (mode !== 'auto') return;

            const val = textarea.value;
            const hasMyanmarUnicode = /[က-႟]/.test(val);
            if (hasMyanmarUnicode) {{
                const converted = unicodeToWin(val);
                const start = textarea.selectionStart;
                const end = textarea.selectionEnd;
                textarea.value = converted;
                textarea.setSelectionRange(start, end);
            }}
        }}

        function copySpecimen(fontId) {{
            const textarea = document.getElementById('specimen-' + fontId);
            if (!textarea) return;
            navigator.clipboard.writeText(textarea.value).then(() => {{
                showToast('စာသားကို Copy ကူးယူပြီးပါပြီ!', 'success');
            }}).catch(() => {{
                showToast('Copy ကူးယူမှု မအောင်မြင်ပါ', 'info');
            }});
        }}

        function toggleFavorite(fontId) {{
            const idx = savedFavorites.indexOf(fontId);
            if (idx > -1) {{
                savedFavorites.splice(idx, 1);
                showToast('သိမ်းဆည်းထားသောစာရင်းမှ ဖယ်ရှားလိုက်ပါပြီ', 'info');
            }} else {{
                savedFavorites.push(fontId);
                showToast('သိမ်းဆည်းထားသောစာရင်းသို့ ထည့်သွင်းပြီးပါပြီ ❤️', 'success');
            }}
            localStorage.setItem('mm_font_favs_v9', JSON.stringify(savedFavorites));
            updateFavBadge();
            renderFonts();
        }}

        function updateFavBadge() {{
            const count = savedFavorites.length;
            document.getElementById('favCountBadge').textContent = count;
            const mobileBadge = document.getElementById('mobileFavCountBadge');
            if (mobileBadge) {{
                mobileBadge.textContent = count;
                mobileBadge.classList.toggle('hidden', count === 0);
            }}
        }}

        function toggleFavoritesFilter() {{
            favoritesOnly = !favoritesOnly;
            const btn = document.getElementById('favFilterBtn');
            btn.classList.toggle('bg-rose-500/20', favoritesOnly);
            btn.classList.toggle('border-rose-500/40', favoritesOnly);
            renderFonts();
        }}

        function getCategoryBadgeStyle(cat) {{
            switch (cat) {{
                case 'arthouse': return 'bg-amber-500/10 text-amber-400 border-amber-500/20';
                case 'masterpiece': return 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20';
                case 'handwriting': return 'bg-rose-500/10 text-rose-400 border-rose-500/20';
                case 'uni-myanmar': return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
                case 'unicode': return 'bg-sky-500/10 text-sky-400 border-sky-500/20';
                case 'win': return 'bg-purple-500/10 text-purple-400 border-purple-500/20';
                case 'zawgyi': return 'bg-orange-500/10 text-orange-400 border-orange-500/20';
                default: return 'bg-slate-800 text-slate-300 border-slate-700';
            }}
        }}

        function renderFonts() {{
            const query = document.getElementById('searchInput').value.trim().toLowerCase();
            const sortBy = document.getElementById('sortSelect').value;

            let filtered = MYANMAR_FONTS.filter(f => {{
                const matchesCat = activeCategory === 'all' || f.category === activeCategory;
                const matchesFav = !favoritesOnly || savedFavorites.includes(f.id);
                const matchesQuery = !query || 
                    (f.name && f.name.toLowerCase().includes(query)) ||
                    (f.mmName && f.mmName.toLowerCase().includes(query)) ||
                    (f.designer && f.designer.toLowerCase().includes(query)) ||
                    (f.description && f.description.toLowerCase().includes(query)) ||
                    (Array.isArray(f.tags) && f.tags.some(t => t && t.toLowerCase().includes(query)));
                return matchesCat && matchesFav && matchesQuery;
            }});

            // Sort
            filtered.sort((a, b) => {{
                if (sortBy === 'popular') return b.popular - a.popular;
                if (sortBy === 'name') return a.name.localeCompare(b.name);
                if (sortBy === 'category') return a.category.localeCompare(b.category);
                return 0;
            }});

            document.getElementById('resultCount').textContent = filtered.length;
            const grid = document.getElementById('fontGrid');
            const emptyState = document.getElementById('emptyState');

            if (filtered.length === 0) {{
                grid.innerHTML = '';
                emptyState.classList.remove('hidden');
                return;
            }}
            emptyState.classList.add('hidden');

            grid.innerHTML = filtered.map(font => {{
                const isFav = savedFavorites.includes(font.id);
                const badgeClass = getCategoryBadgeStyle(font.category);
                const isWin = font.isWin;
                const winMode = winModeState[font.id] || 'auto';

                return `
                <article class="bg-slate-900/90 hover:bg-slate-900 border border-slate-800/90 hover:border-slate-700 rounded-2xl sm:rounded-3xl p-4 sm:p-5 shadow-lg transition duration-200 flex flex-col justify-between space-y-4">
                    <div class="space-y-3">
                        <div class="flex items-start justify-between gap-3">
                            <div class="min-w-0 flex-1">
                                <div class="flex flex-wrap items-center gap-1.5 sm:gap-2">
                                    <h3 class="font-bold text-base sm:text-lg text-white truncate">${{font.name}}</h3>
                                    <span class="text-[10px] sm:text-[11px] font-medium px-2 py-0.5 rounded-full border ${{badgeClass}} whitespace-nowrap">
                                        ${{font.categoryLabel}}
                                    </span>
                                    ${{isWin ? `
                                    <button id="winToggle-${{font.id}}" onclick="toggleWinMode('${{font.id}}')" class="text-[10px] px-2 py-0.5 rounded-md ${{winMode === 'auto' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20 font-semibold' : 'bg-slate-800 text-slate-400 border border-slate-700'}}" title="Toggle Win / Direct Conversion">
                                        ${{winMode === 'auto' ? '⚡ Auto-Win Active' : '⌨️ Direct Win Layout'}}
                                    </button>
                                    ` : `
                                    <span class="text-[10px] px-2 py-0.5 rounded-md bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium">
                                        ✓ Unicode
                                    </span>
                                    `}}
                                </div>
                                <p class="text-xs text-slate-400 mt-0.5 truncate">${{font.mmName}} • By ${{font.designer}}</p>
                            </div>

                            <div class="flex items-center gap-1 shrink-0">
                                <button onclick="shareFont('${{font.id}}')" class="p-2 rounded-xl bg-slate-800/80 hover:bg-slate-800 text-slate-400 hover:text-white transition" title="ဖောင့်လင့်ခ် မျှဝေမည်">
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                                    </svg>
                                </button>
                                <button onclick="toggleFavorite('${{font.id}}')" class="p-2 rounded-xl bg-slate-800/80 hover:bg-slate-800 transition" title="သိမ်းဆည်းမည်">
                                    <svg class="w-4 h-4 ${{isFav ? 'text-rose-500 fill-current' : 'text-slate-400'}}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
                                    </svg>
                                </button>
                            </div>
                        </div>

                        <!-- Live Specimen Interactive Typing Box with EXACT True Font-Family -->
                        <div class="bg-slate-950 border border-slate-800/90 rounded-2xl p-3 sm:p-3.5 focus-within:border-amber-500/80 transition relative group">
                            <div class="flex items-center justify-between text-[11px] text-slate-500 mb-1">
                                <span>တိုက်ရိုက်စာရိုက်စမ်းရန် (Live Typing):</span>
                                <div class="flex items-center gap-2">
                                    <span class="font-mono text-slate-400 text-[10px] hidden sm:inline">${{font.family || font.name}}</span>
                                    <button onclick="copySpecimen('${{font.id}}')" class="text-slate-400 hover:text-amber-400 text-[10px] px-1.5 py-0.5 rounded bg-slate-900 border border-slate-800" title="နမူနာစာသား ကူးယူမည်">Copy</button>
                                </div>
                            </div>
                            <textarea 
                                id="specimen-${{font.id}}"
                                data-font-id="${{font.id}}"
                                rows="2"
                                autocomplete="off"
                                autocorrect="off"
                                autocapitalize="off"
                                spellcheck="false"
                                enterkeyhint="done"
                                oninput="handleSpecimenInput(this, '${{font.id}}')"
                                placeholder="ဒီနေရာမှာ စမ်းချင်တဲ့ မြန်မာစာ ရိုက်ထည့်ပါ..."
                                class="live-specimen-textarea font-preview-${{font.id}} ${{isGlobalBold ? 'font-bold' : ''}} w-full bg-transparent text-white focus:outline-none resize-none leading-relaxed transition-all"
                                style="font-size: ${{currentFontSize}}px;"
                            >${{font.defaultSample}}</textarea>
                        </div>

                        <p class="text-xs text-slate-400 leading-relaxed line-clamp-2">
                            ${{font.description}}
                        </p>
                    </div>

                    <div class="pt-3 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-2.5">
                        <div class="flex items-center gap-2 text-xs text-slate-400">
                            <span class="px-2 py-0.5 rounded bg-slate-950 border border-slate-800 font-mono text-[10px]">v${{font.version || '2.0'}}</span>
                            <span class="text-[11px]">📦 ${{font.size}}</span>
                            <span class="text-emerald-400 font-medium text-[11px]">✓ .TTF</span>
                        </div>

                        <div class="flex items-center gap-2">
                            <button onclick="openFontDetails('${{font.id}}')" class="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium transition">
                                အသေးစိတ်
                            </button>
                            <button onclick="downloadFont('${{font.id}}')" class="px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-400 hover:to-orange-400 text-slate-950 text-xs font-bold shadow-md shadow-amber-500/10 transition flex items-center gap-1.5">
                                <span>⬇️</span>
                                <span>Download</span>
                            </button>
                        </div>
                    </div>
                </article>
                `;
            }}).join('');
        }}

        async function downloadFont(fontId) {{
            const font = MYANMAR_FONTS.find(f => f.id === fontId);
            if (!font) return;

            showToast(`${{font.name}} မူရင်းဖောင့်ကို ဒေါင်းလုဒ်ဆွဲနေပါသည်...`, 'info');

            try {{
                const response = await fetch(font.directUrl);
                if (!response.ok) throw new Error('Fetch failed');
                const blob = await response.blob();
                const blobUrl = URL.createObjectURL(blob);

                const a = document.createElement('a');
                a.href = blobUrl;
                a.download = font.fileName || `${{font.name}}.ttf`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(blobUrl);

                showToast(`✅ ${{font.fileName || font.name}} ဒေါင်းလုဒ် အောင်မြင်ပါသည်!`, 'success');
            }} catch (err) {{
                // fallback direct anchor click
                const a = document.createElement('a');
                a.href = font.directUrl;
                a.download = font.fileName || `${{font.name}}.ttf`;
                a.target = '_blank';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                showToast(`ဖောင့်လင့်ခ်မှတစ်ဆင့် ဒေါင်းလုဒ်စတင်ပါသည်`, 'success');
            }}
        }}

        function downloadSelectedBundle() {{
            showToast('Top Curated ဖောင့်အစုံအလင်ကို ဒေါင်းလုဒ်ဆွဲနေပါသည်...', 'success');
            const bundleIds = [
                'arthouse-w60', 'arthouse-w52', 'masterpiece-uni-round',
                'aka02-regular', 'uni-myanmar-bagan', 'uni-myanmar-black',
                'pyidaungsu-bold', 'win-uni-innwa'
            ];
            bundleIds.forEach((id, index) => {{
                setTimeout(() => {{
                    downloadFont(id);
                }}, index * 900);
            }});
        }}

        function openFontDetails(fontId) {{
            const font = MYANMAR_FONTS.find(f => f.id === fontId);
            if (!font) return;

            document.getElementById('modalFontTitle').textContent = font.name;
            document.getElementById('modalFontBadge').textContent = font.categoryLabel;
            document.getElementById('modalFontDesigner').textContent = `${{font.mmName}} • Designer: ${{font.designer}} • ${{font.size}}`;

            const sample = font.isWin ? (font.defaultSample || 'Art House W60 စာလုံးအလှ') : 'မင်္ဂလာပါ မြန်မာပြည် အလှဆုံးဖောင့်များ';
            const sizes = [16, 20, 26, 34, 44];
            document.getElementById('modalWaterfall').innerHTML = sizes.map(sz => `
                <div class="flex items-baseline gap-3 border-b border-slate-900 pb-2 last:border-0">
                    <span class="text-xs font-mono text-slate-500 w-12 shrink-0">${{sz}}px</span>
                    <p class="font-preview-${{font.id}} text-slate-100" style="font-size: ${{sz}}px;">${{sample}}</p>
                </div>
            `).join('');

            document.getElementById('modalCharMap').innerHTML = (font.isWin ? MYANMAR_CHARS.map(ch => unicodeToWin(ch)) : MYANMAR_CHARS).map(ch => `
                <div class="font-preview-${{font.id}} p-2 rounded-xl bg-slate-900 hover:bg-amber-500/20 text-slate-200 transition">
                    ${{ch}}
                </div>
            `).join('');

            document.getElementById('modalCssCode').textContent = `@font-face {{\n  font-family: '${{font.family || font.name}}';\n  src: url('./fonts/${{font.fileName}}') format('truetype');\n  font-display: swap;\n}}`;

            const btn = document.getElementById('modalDownloadBtn');
            btn.onclick = () => downloadFont(font.id);

            openModal('fontDetailModal');
        }}

        function copyCssSnippet() {{
            const code = document.getElementById('modalCssCode').textContent;
            navigator.clipboard.writeText(code).then(() => {{
                showToast('CSS ကုဒ်ကို Copy ကူးယူပြီးပါပြီ!', 'success');
            }}).catch(() => {{
                const temp = document.createElement('textarea');
                temp.value = code;
                document.body.appendChild(temp);
                temp.select();
                document.execCommand('copy');
                document.body.removeChild(temp);
                showToast('CSS ကုဒ်ကို Copy ကူးယူပြီးပါပြီ!', 'success');
            }});
        }}

        function openModal(id) {{
            document.getElementById(id).classList.remove('hidden');
        }}

        function closeModal(id) {{
            document.getElementById(id).classList.add('hidden');
        }}

        function showToast(message, type = 'info') {{
            const container = document.getElementById('toastContainer');
            const toast = document.createElement('div');
            const borderCol = type === 'success' ? 'border-emerald-500/50 bg-slate-900/95 text-emerald-300' : 'border-amber-500/50 bg-slate-900/95 text-amber-300';
            
            toast.className = `pointer-events-auto px-4 py-3 rounded-2xl border ${{borderCol}} shadow-2xl text-xs sm:text-sm font-medium flex items-center gap-2 transition-all duration-300`;
            toast.innerHTML = `<span>${{message}}</span>`;
            container.appendChild(toast);

            setTimeout(() => {{
                toast.style.opacity = '0';
                toast.style.transform = 'translateY(10px)';
                setTimeout(() => toast.remove(), 300);
            }}, 3200);
        }}

        window.onload = initApp;
    </script>
</body>
</html>
"""

# Write to target paths:
target_paths = [
    '/private/var/folders/9k/t5ny8j990wd9hny_03971ybc0000gn/T/canvas-FF884419-83D5-49AA-97C1-3439C346CC38.html',
    '/Users/sithu/Desktop/Gemini 4/index.html',
    '/Users/sithu/Desktop/Gemini 4/myanmar_font_hub.html'
]

for p in target_paths:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Successfully generated: {p} ({len(html_content):,} bytes)")
