import streamlit as st
import random
import json
import re
import time

st.set_page_config(page_title="Shinobi Life", page_icon="🍥", layout="centered")
st.markdown("""<style>
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@keyframes slideIn{from{opacity:0;transform:translateX(-40px)}to{opacity:1;transform:none}}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(255,170,0,.55)}50%{box-shadow:0 0 0 14px rgba(255,170,0,0)}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-24px)}}
@keyframes ride{from{left:-12%}to{left:104%}}
.stMarkdown p,div[data-testid="stExpander"],div[data-testid="stAlert"]{animation:fadeIn .5s ease}
div[data-testid="stProgress"] div[role="progressbar"]>div{transition:width .9s ease}
div.stButton>button{transition:transform .15s}
div.stButton>button:hover:not(:disabled){transform:scale(1.03)}
.ev-card{border:2px solid #ffaa00;border-radius:12px;padding:14px;margin:8px 0;background:rgba(255,170,0,.12);animation:slideIn .5s ease,pulse 1.6s ease 2}
.scene{position:relative;height:46px;overflow:hidden}
.sprite{position:absolute;top:4px;font-size:30px}
.s-nar{left:46%;animation:spin 3s linear infinite}
.s-kur{left:46%;animation:bounce .9s ease-in-out infinite}
.s-tr{animation:ride 5s linear infinite}
@keyframes rise{0%{transform:translateY(0) rotate(0);opacity:0}10%{opacity:.4}100%{transform:translateY(-115vh) rotate(300deg);opacity:0}}
@keyframes shake{0%,100%{transform:translateX(0)}20%,60%{transform:translateX(-10px)}40%,80%{transform:translateX(10px)}}
@keyframes glow{0%,100%{filter:drop-shadow(0 0 0 transparent)}50%{filter:drop-shadow(0 0 8px #ffcc00)}}
@keyframes zoomIn{from{opacity:0;transform:scale(.6)}to{opacity:1;transform:none}}
.fxbg span{position:fixed;bottom:-40px;font-size:26px;opacity:0;pointer-events:none;z-index:0;animation:rise 12s linear infinite}
.shake{animation:shake .5s}
.arc-card{border:2px solid #7c5cff;border-radius:12px;padding:14px;margin:8px 0;background:rgba(124,92,255,.13);animation:slideIn .5s ease,pulse 1.6s ease 2}
.gem{display:inline-block;animation:glow 2s ease-in-out infinite}
.grave{border-left:4px solid #888;padding:6px 12px;margin:6px 0;background:rgba(128,128,128,.1);border-radius:6px;animation:fadeIn .6s}
.pop{animation:zoomIn .5s ease}
.news{font-size:13px;opacity:.85;animation:fadeIn .6s}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
@keyframes blink{50%{opacity:0}}
.dlg{display:flex;gap:12px;align-items:flex-start;border:3px solid #6b7cff;border-radius:14px;padding:12px;margin:8px 0;background:linear-gradient(180deg,rgba(40,50,120,.35),rgba(20,25,60,.35));animation:slideIn .4s ease}
.dlg-ico{font-size:44px;animation:bob 1.8s ease-in-out infinite}
.dlg-body{flex:1}
.dlg-name{font-weight:700;font-size:16px}
.dlg-name span{font-weight:400;font-size:12px;opacity:.7;margin-left:6px}
.dlg-txt{margin-top:4px;line-height:1.5}
.dlg-txt::after{content:" ▼";color:#6b7cff;animation:blink 1s infinite}
.duel-card{text-align:center;border:2px solid rgba(128,128,128,.4);border-radius:12px;padding:10px;background:rgba(128,128,128,.08)}
.sprite-big{font-size:64px;animation:bob 1.6s ease-in-out infinite}
.sprite-big.foe{animation-delay:.4s}
.hp{background:#333;border-radius:8px;height:14px;overflow:hidden;margin:6px 0 2px}
.hpf{height:100%;transition:width .8s ease}

.bl-logo{font-weight:900;font-size:22px;letter-spacing:1px;color:#ff7a1a;text-shadow:0 2px 0 #7a2e00}
.bl-gems{text-align:right;font-weight:800;border:2px solid #fff;border-radius:18px;padding:2px 10px;color:#fff;background:#000;display:inline-block;float:right}
.bl-prof{display:flex;align-items:center;gap:10px;background:#e8f3e8;border-bottom:1px solid #c9d3df;padding:6px 10px;border-radius:8px;margin:4px 0 8px}
.bl-name b{font-size:19px;color:#0057a3;text-decoration:underline}
.bl-name small{color:#456}
.bl-bank{margin-left:auto;text-align:right;color:#1f9d3a}
.bl-bank b{font-size:21px}
.bl-bank small{color:#567}
.bl-head{background:#0057a3;color:#fff;font-weight:900;letter-spacing:1px;font-size:22px;text-align:center;padding:10px;border-radius:6px}
.bl-age{color:#0057a3;font-weight:800;font-size:18px;margin-top:12px}
.bl-line{font-size:15px;line-height:1.35;margin:2px 0}
.bl-stat{display:flex;align-items:center;gap:8px;margin:5px 0}
.bl-stat .lab{width:105px;text-align:right;color:#0057a3;font-weight:700;font-size:15px}
.bl-stat .ico{width:26px;text-align:center}
.bl-stat .bar{flex:1;height:26px;background:#d5dbe3;position:relative;border-radius:2px;overflow:hidden}
.bl-stat .bar div{height:100%;transition:width .8s ease}
.bl-stat .bar b{position:absolute;right:8px;top:3px;color:#fff;font-size:14px;text-shadow:0 1px 2px #0006}
.bl-rowinfo{background:#fff;border-bottom:1px solid #cfd8e3;padding:12px;color:#0057a3}
.bl-rowinfo b{font-size:18px;display:block}
.bl-mini{display:flex;align-items:center;gap:8px;font-size:14px;color:#456}
.bl-mini .mb{flex:1;max-width:260px;height:10px;background:#d5dbe3}
.bl-mini .mb div{height:100%;background:#2e9d3e}
[class*="st-key-row_"] button{justify-content:flex-start;text-align:left;border:0;border-bottom:1px solid #cfd8e3;border-radius:0;background:#fff;color:#0057a3;font-weight:700;font-size:16px;padding:14px 12px}
[class*="st-key-row_"] button:hover{background:#eef4fb;color:#003f75}
.st-key-navbar{position:fixed;bottom:0;left:0;right:0;z-index:999;background:#0057a3;padding:6px 6px 10px;box-shadow:0 -3px 10px #0005}
.st-key-navbar button{background:transparent;color:#fff;border:0;font-weight:700;font-size:12px;padding:8px 2px}
.st-key-navbar button:hover{background:#ffffff22;color:#fff}
.st-key-nav_age button{background:#1aa84a;border-radius:50%;width:76px;height:76px;margin:-30px auto 0;border:4px solid #fff;font-size:15px;box-shadow:0 3px 8px #0006}
.st-key-hamb button{background:#000;color:#fff;border:2px solid #fff;border-radius:50%;width:42px;height:42px;padding:0}
</style>""", unsafe_allow_html=True)


# ───────────────────────── DONNÉES ─────────────────────────
PA = 4  # actions par an
SAVE_V = 7

# ───────────────────────── UNIVERS ─────────────────────────
UNIV = {
    "Naruto": {
        "icon": "🍥", "cls": "nar", "fx": ["🍃", "🍥", "🌀"], "mait": "Ninjutsu", "monnaie": "ryōs", "job": "Faire une mission", "jobage": 12,
        "fact": ["Konoha", "Suna", "Kiri", "Kumo", "Iwa", "Ame", "Taki"],
        "pre": "Élève de l'Académie",
        "ranks": ["Élève de l'Académie", "Genin", "Chūnin", "Jōnin", "Élite ANBU", "Kage"],
        "intro": "Tu viens au monde dans un village caché où le chakra coule dans toutes les veines.",
        "pnj": ["Haruto", "Mizuki", "Daichi", "Sakura-Hime", "Rentaro", "Kagero", "Tsubaki", "Ibuki", "Raiden", "Kohaku", "Shion", "Gengetsu"],
        "mile": {4: "Tes premiers signes de chakra apparaissent.", 6: "Tu entres à l'Académie ninja : le papier de chakra révèle ta nature.",
                 12: "Tu obtiens ton bandeau frontal : tu es Genin !", 15: "Tu peux désormais passer les examens supérieurs."},
        "goal": "Devenir un ninja d'élite (Jōnin ou plus)",
    },
    "Kuroko": {
        "icon": "🏀", "cls": "kur", "fx": ["🏀", "⭐", "👟"], "mait": "Basket", "monnaie": "yens", "job": "Jouer un match rémunéré", "jobage": 14,
        "fact": ["Lycée Seirin", "Lycée Kirisaki Daiichi", "Lycée Fukuda Sōgō", "Lycée Kaijō", "Lycée Shūtoku", "Lycée Yōsen", "Lycée Tōō", "Lycée Rakuzan"],
        "pre": "Collégien",
        "ranks": ["Joueur de banc", "Titulaire", "As de l'équipe", "Capitaine", "Génération des Miracles", "Légende du Basket"],
        "intro": "Tu viens au monde dans une famille où le basket est une religion.",
        "pnj": ["Akira", "Shiori", "Taiga-kun", "Midori", "Seiji", "Reo", "Nagisa", "Atsushi", "Kōsuke", "Junpei", "Hyūga-senpai", "Satsuki"],
        "mile": {6: "Tu entres à l'école primaire.", 12: "Tu entres au collège et touches un vrai ballon de match.",
                 15: "Tu entres au lycée : l'Inter-High et la Winter Cup t'attendent."},
        "goal": "Faire gagner ton lycée, puis devenir joueur pro en NBA",
    },
    "Tokyo Revengers": {
        "icon": "🏍️", "cls": "tr", "fx": ["🏍️", "🔥", "👊"], "mait": "Combat", "monnaie": "yens", "job": "Faire une ronde du quartier", "jobage": 14,
        "fact": ["Toman", "Moebius", "Valhalla", "Black Dragons", "Brahman", "Rokuhara Tandai", "Tenjiku", "Kantō Manji"],
        "pre": "Collégien",
        "ranks": ["Simple membre", "Soldat", "Capitaine de division", "Commandant", "Bras droit", "Chef du gang"],
        "intro": "Tu viens au monde dans un quartier de Tokyo où les gangs font la loi.",
        "pnj": ["Takeru", "Emma", "Ryuji", "Hinata-chan", "Kazuma", "Mikey-kun", "Chifuyu", "Nahoya", "Draken-san", "Baji", "Kakucho", "Hakkai"],
        "mile": {6: "Tu entres à l'école primaire.", 12: "Tu entres au collège, les premières bagarres commencent.",
                 15: "Tu entres au lycée : les gangs te remarquent."},
        "goal": "Dominer le Japon (contrôler 9 territoires sur 12)",
    },
}
RANK_TH = [0, 50, 150, 300, 600, 1000]
RANK_AGE = [0, 12, 14, 18, 25, 30]  # âge minimum pour chaque rang

NAT = {"Feu": "🔥", "Eau": "💧", "Vent": "🌪️", "Foudre": "⚡", "Terre": "🪨", "Glace": "❄️", "Bois": "🌳", "Lave": "🌋"}
BASE_NAT = ["Feu", "Eau", "Vent", "Foudre", "Terre"]

# ───────────────────────── NARUTO : villages & clans ─────────────────────────
VILL = {
    "Konoha": dict(ico="🍃", kage="Hokage", w=5, nat=["Feu", "Vent", "Foudre", "Eau", "Terre"]),
    "Suna": dict(ico="🏜️", kage="Kazekage", w=3, nat=["Vent", "Terre", "Feu", "Foudre", "Eau"]),
    "Kiri": dict(ico="🌫️", kage="Mizukage", w=3, nat=["Eau", "Feu", "Vent", "Terre", "Foudre"]),
    "Kumo": dict(ico="⛈️", kage="Raikage", w=3, nat=["Foudre", "Terre", "Eau", "Feu", "Vent"]),
    "Iwa": dict(ico="⛰️", kage="Tsuchikage", w=3, nat=["Terre", "Feu", "Foudre", "Vent", "Eau"]),
}
VILL_ICO = dict({k: v["ico"] for k, v in VILL.items()}, Ame="🌧️", Taki="💦")
# v: village, nat: natures innées (None = selon le village), eye: pupille héréditaire, eage: âge d'éveil
CLANS = {
    "Uchiwa": dict(v="Konoha", ico="🔴", nat=["Feu"], eye="Sharingan", eage=9, bonus=dict(mait=4, intel=3), pw=4, w=3,
                   d="Clan prestigieux de Konoha. Il porte le Sharingan et excelle au Katon. Ses techniques sont celles des yeux."),
    "Hyūga": dict(v="Konoha", ico="⚪", nat=None, eye="Byakugan", eage=4, bonus=dict(mait=4, force=2), pw=4, w=3,
                  d="Clan noble de Konoha. Le Byakugan voit à 360° et le Poing Souple frappe le réseau de chakra."),
    "Senju": dict(v="Konoha", ico="🌳", nat=["Eau", "Terre"], bonus=dict(force=5, sante=6, chakra=8), pw=5, w=2,
                  d="Clan légendaire à la vitalité hors norme. Eau + Terre : le Mokuton (Bois) est à portée pour les plus doués."),
    "Nara": dict(v="Konoha", ico="🦌", nat=None, bonus=dict(intel=14), w=3, d="Génies tacticiens. Leur technique secrète manipule les ombres."),
    "Akimichi": dict(v="Konoha", ico="🍖", nat=None, bonus=dict(force=8, sante=8), w=3, d="Clan robuste dont les techniques transforment les calories en puissance."),
    "Yamanaka": dict(v="Konoha", ico="🌸", nat=None, bonus=dict(intel=6, mait=3), w=3, d="Spécialistes de l'esprit : transfert de conscience et lecture mentale."),
    "Aburame": dict(v="Konoha", ico="🪲", nat=None, bonus=dict(intel=5, mait=4), w=3, d="Clan qui héberge des insectes Kikaichū dans son corps."),
    "Inuzuka": dict(v="Konoha", ico="🐕", nat=None, bonus=dict(force=6, mait=3), w=3, d="Clan fusionnel avec ses chiens ninjas : crocs et flair surdéveloppés."),
    "Uzumaki": dict(v="Konoha", ico="🌀", nat=None, bonus=dict(chakra=15, sante=6), pw=3, w=2, biju=.12,
                    d="Réputés pour leur chakra immense et leurs sceaux. Les hôtes de bijū naissent souvent parmi eux."),
    "Sabaku": dict(v="Suna", ico="🏜️", nat=["Vent", "Terre"], bonus=dict(force=4, mait=3), w=3, d="Famille de Suna maîtrisant le sable et le fer."),
    "Hozuki": dict(v="Kiri", ico="💧", nat=["Eau"], bonus=dict(force=4, chakra=5), w=3, d="Clan de Kiri capable de transformer son corps en eau."),
    "Yuki": dict(v="Kiri", ico="❄️", nat=["Eau", "Vent", "Glace"], bonus=dict(mait=4, intel=3), pw=4, w=2, d="Clan de Kiri héritier du Hyōton (Glace)."),
    "Kaguya": dict(v="Kiri", ico="🦴", nat=None, bonus=dict(force=8, sante=5), w=2, d="Clan belliqueux dont le sang durcit les os en armes."),
    "Yotsuki": dict(v="Kumo", ico="⚡", nat=["Foudre"], bonus=dict(force=5, mait=3), w=3, d="Famille d'élite de Kumo : vitesse et armures de foudre."),
    "Kurotsuchi": dict(v="Iwa", ico="🌋", nat=["Terre", "Feu"], bonus=dict(force=4, mait=3), w=3, d="Famille d'Iwa. Feu + Terre ouvre la voie à la Lave."),
}
PRESTIGE = ["Uchiwa", "Hyūga", "Senju", "Uzumaki"]

# ───────────────────────── Familles ─────────────────────────
SURN = ["Aizawa", "Hoshino", "Kuroda", "Minami", "Sakurai", "Fujiwara", "Takeda", "Mizuno", "Kitano", "Hayashi", "Ishida", "Nakamura",
        "Yamashita", "Okabe", "Tachibana", "Morita", "Ogawa", "Shinohara", "Kagawa", "Noda", "Uehara", "Sugawara", "Nishimura",
        "Tsukishima", "Kuwabara", "Hasegawa", "Ayase", "Kurosawa", "Higashi", "Matsuda"]
PM = ["Hiroshi", "Takashi", "Ren", "Isamu", "Daiki", "Kenta", "Shinji", "Masaru"]
PF = ["Aiko", "Yumi", "Rin", "Naomi", "Sakura", "Haruka", "Mio", "Kaoru"]
KM = ["Kaito", "Ryota", "Sora", "Haruki", "Yuto", "Daichi", "Akito", "Taiki"]
KF = ["Hana", "Mei", "Yuna", "Sayaka", "Riko", "Akane", "Nanami", "Chihiro"]
# nom, description, bonus, richesse, poids
FAM = {
    "Kuroko": [
        ("Famille de basketteurs", "Ton père a joué en semi-pro : un ballon traîne toujours dans le salon.", dict(mait=4, force=2), 2, 3),
        ("Famille modeste", "Les fins de mois sont serrées, mais la maison est chaleureuse.", dict(bonheur=4, sante=2), 1, 3),
        ("Famille de médecins", "Études et rigueur : tes parents veulent que tu réussisses.", dict(intel=8), 3, 2),
        ("Famille d'entrepreneurs", "Les affaires marchent, tu ne manqueras de rien.", dict(rep=3), 3, 2),
        ("Mère célibataire", "Ta mère jongle entre trois emplois pour t'élever.", dict(force=2, intel=3, bonheur=-2), 1, 2),
        ("Famille de sportifs", "Ton grand frère est un athlète local : tu veux le dépasser.", dict(force=4, mait=2), 2, 2),
    ],
    "Tokyo Revengers": [
        ("Famille ordinaire", "Un quartier tranquille, des parents travailleurs.", dict(bonheur=3), 2, 3),
        ("Famille de yakuza", "Ton nom fait taire les voisins, pour le meilleur et pour le pire.", dict(rep=8, force=3, bonheur=-3), 3, 1),
        ("Famille de dojo", "Ton grand-père tient un dojo de karaté depuis trente ans.", dict(force=6, mait=3), 2, 2),
        ("Mère célibataire", "Ta mère travaille de nuit dans un izakaya.", dict(force=2, intel=2), 1, 3),
        ("Famille bourgeoise de Shibuya", "Une grande maison, mais une pression constante.", dict(intel=5, rep=2), 4, 1),
        ("Famille brisée", "Un père absent : la rue t'a élevé.", dict(force=4, rep=3, bonheur=-5), 1, 2),
    ],
}
TRAITS = ["loyal", "ambitieux", "rusé", "bienveillant", "jaloux", "courageux"]
ROLE_ICO = {"ami": "🤝", "rival": "😤", "amour": "💗", "famille": "👪", "mentor": "🎓", "equipier": "🤜", "enfant": "👶"}

# ───────────────────────── Tokyo Revengers : monde des gangs ─────────────────────────
TERRS = ["Shibuya", "Shinjuku", "Roppongi", "Ikebukuro", "Ueno", "Asakusa", "Yokohama", "Chiba", "Osaka", "Nagoya", "Fukuoka", "Sapporo"]
GFORCE = {"Toman": 90, "Moebius": 55, "Valhalla": 75, "Black Dragons": 60, "Brahman": 50, "Rokuhara Tandai": 80, "Tenjiku": 95, "Kantō Manji": 85}
GRANG_TH = [0, 30, 80, 150, 250, 0]   # gxp requis pour atteindre chaque rang de gang
GRANG_REP = [0, 5, 20, 35, 50, 0]
DOMINATION = 9

# ───────────────────────── Kuroko : NBA ─────────────────────────
NBA = {"Raptors": 1.3, "Knicks": 1.35, "Nets": 1.4, "Spurs": 1.45, "Bulls": 1.5, "Heat": 1.55, "Suns": 1.6, "Mavericks": 1.65,
       "Lakers": 1.7, "Warriors": 1.75, "Nuggets": 1.8, "Celtics": 1.85}
LYCEES_SEL = {"Lycée Seirin": .95, "Lycée Kaijō": .8, "Lycée Shūtoku": .7, "Lycée Tōō": .7, "Lycée Yōsen": .65, "Lycée Rakuzan": .5}

# ───────────────────────── Boutique de l'âme (méta) ─────────────────────────
PERKS = {
    "beaute": ("💄 Beauté éclatante", 60, "Tu naîtras avec un charme hors du commun (beauté 95).", None),
    "beaute_choix": ("🪞 Beauté au choix", 40, "Tu choisis toi-même le niveau de beauté de ton personnage.", None),
    "esprit": ("🧠 Esprit précoce", 80, "+20 intelligence et +10 maîtrise dès la naissance.", None),
    "fer": ("💪 Constitution de fer", 80, "Santé à 100 et +15 force.", None),
    "fortune": ("💰 Famille fortunée", 100, "Famille très riche et 500 de départ.", None),
    "second": ("⏳ Seconde chance", 120, "Tu reviens à la vie une fois.", None),
    "prestige": ("🌟 Naissance prestigieuse", 180, "Naruto : clan prestigieux. Kuroko : talent rare. Tokyo Revengers : famille influente.", None),
    "talent_choix": ("🎯 Destin au choix", 200, "Choisis ton clan (Naruto), ton talent (Kuroko) ou ton origine (Tokyo Revengers).", None),
    "nat_choix": ("🔮 Nature de chakra au choix", 120, "Tu choisis ta nature de chakra de naissance.", "Naruto"),
    "biju": ("🦊 Bijū de naissance", 300, "Un bijū est scellé en toi dès la naissance.", "Naruto"),
    "don": ("✨ Don exceptionnel", 150, "Naruto : double nature. Kuroko : potentiel de Zone élevé. Tokyo Revengers : +20 force.", None),
}
BEAUTES = {"Banale": 25, "Charmante": 55, "Séduisante": 75, "Sublime": 95}

# id, description, condition sur les records, gemmes
META_DEFIS = [
    ("m1", "Vivre jusqu'à 18 ans", lambda r: r.get("age", 0) >= 18, 40),
    ("m2", "Vivre jusqu'à 40 ans", lambda r: r.get("age", 0) >= 40, 80),
    ("m3", "Mourir de vieillesse", lambda r: "vieillesse" in r.get("flags", []), 100),
    ("m4", "Gagner 5 duels dans une même vie", lambda r: r.get("wins", 0) >= 5, 50),
    ("m5", "Gagner 15 duels dans une même vie", lambda r: r.get("wins", 0) >= 15, 100),
    ("m6", "Atteindre 80 de réputation", lambda r: r.get("rep", 0) >= 80, 60),
    ("m7", "Apprendre 5 techniques", lambda r: r.get("tech", 0) >= 5, 70),
    ("m8", "Avoir un enfant", lambda r: r.get("enfants", 0) >= 1, 60),
    ("m9", "Continuer ta lignée en jouant ton enfant", lambda r: r.get("gen", 0) >= 1, 100),
    ("m10", "Posséder 3000 d'argent", lambda r: r.get("argent", 0) >= 3000, 60),
    ("m11", "Atteindre le 4e rang de ton univers", lambda r: r.get("rang", 0) >= 3, 80),
    ("m12", "Devenir ninja d'élite (Jōnin)", lambda r: "elite" in r.get("flags", []), 120),
    ("m13", "Faire gagner un lycée (Inter-High ou Winter Cup)", lambda r: r.get("titres_l", 0) >= 1, 120),
    ("m14", "Signer en NBA", lambda r: "pro" in r.get("flags", []), 150),
    ("m15", "Contrôler 6 territoires", lambda r: r.get("terr", 0) >= 6, 120),
    ("m16", "Fonder ton propre gang", lambda r: "chef" in r.get("flags", []), 80),
    ("m17", "Devenir porteur d'un bijū", lambda r: "biju" in r.get("flags", []), 100),
    ("m18", "Entrer dans la Zone", lambda r: r.get("zone", 0) >= 1, 70),
    ("m19", "Vivre une vie dans chacun des 3 univers", lambda r: len(r.get("univs", [])) >= 3, 150),
    ("m20", "Atteindre un karma extrême (±80)", lambda r: r.get("karma_abs", 0) >= 80, 60),
    ("m21", "Accomplir l'objectif ultime d'un univers", lambda r: "ultime" in r.get("flags", []), 250),
]


BIJU = [("Shukaku", "🦝"), ("Matatabi", "🐱"), ("Isobu", "🐢"), ("Son Gokū", "🐒"), ("Kokuō", "🐴"),
        ("Saiken", "🐌"), ("Chōmei", "🪲"), ("Gyūki", "🐙"), ("Kurama", "🦊")]

PUP = {"Sharingan": ("🔴", 70, 20), "Byakugan": ("⚪", 80, 20), "Mangekyō Sharingan": ("🩸", 130, 35), "Rinnegan": ("🟣", 170, 45)}
# nom, icône, description, bonus de naissance, puissance par niveau, rareté (poids)
TALENTS = {
    "fantome": ("Joueur fantôme", "👻", "Une présence quasi invisible : tes passes surgissent de nulle part.", dict(intel=10, mait=3), 4, 3),
    "freestyle": ("Freestyle", "🌀", "Un style de jeu imprévisible que personne ne sait lire.", dict(mait=6, force=3), 5, 1),
    "tir": ("Tir à trois points parfait", "🎯", "Depuis n'importe où, tes tirs retombent dans le panier.", dict(mait=8), 5, 2),
    "empereur": ("Œil de l'Empereur", "👁️", "Tu vois chaque mouvement avant qu'il n'arrive.", dict(intel=12, mait=4), 5, 1),
    "belial": ("Œil de Bélial", "😈", "Une vision sombre qui lit même les intentions adverses.", dict(intel=10, force=3), 5, 1),
    "copie": ("Copie parfaite", "🪞", "Tu reproduis les gestes de n'importe quel joueur.", dict(mait=5, intel=6), 5, 2),
    "bestial": ("Instinct bestial", "🐆", "Des réflexes et une agilité hors norme.", dict(force=8, mait=3), 5, 2),
    "viking": ("Viking", "🛡️", "Une défense titanesque : personne ne passe.", dict(force=10, sante=8), 5, 2),
    "rebond": ("Rebond prodigieux", "🦘", "Tu sautes plus haut que tout le monde.", dict(force=6, mait=4), 4, 3),
    "passe": ("Passe de génie", "🎼", "Chaque passe trouve son coéquipier.", dict(intel=8, mait=4), 4, 3),
}
# nom : (lycée, niveau de difficulté, talent)
GM = {
    "Akashi": ("Lycée Rakuzan", 1.8, "Œil de l'Empereur"),
    "Aomine": ("Lycée Tōō", 1.7, "Freestyle"),
    "Murasakibara": ("Lycée Yōsen", 1.6, "Viking"),
    "Midorima": ("Lycée Shūtoku", 1.5, "Tir parfait"),
    "Kise": ("Lycée Kaijō", 1.4, "Copie parfaite"),
}

# (multiplicateur de ton score, ajout de points, multiplicateur du score adverse)
TALENT_FX = {
    "fantome": (1.25, 4, 1.0), "freestyle": (1.3, 3, 1.0), "tir": (1.1, 10, 1.0), "empereur": (1.1, 0, .7),
    "belial": (1.15, 4, .75), "copie": (1.25, 4, .9), "bestial": (1.3, 3, .95), "viking": (1.0, 0, .6),
    "rebond": (1.15, 8, .95), "passe": (1.2, 6, 1.0),
}
TALK = {
    "Akashi": [
        ("Lui demander des conseils tactiques", .9, {"intel": 4, "gmi": 6}, "Akashi t'explique comment lire un match d'un seul regard.", {"gmi": -3}, "Il juge ta question trop naïve."),
        ("Lui proposer une partie de shōgi", .5, {"intel": 6, "gmi": 10, "bonheur": 3}, "Tu tiens bien plus longtemps que prévu.", {"gmi": -2, "bonheur": -3}, "Il te bat en dix coups."),
        ("Remettre en cause une de ses consignes", .4, {"rep": 6, "gmi": 12}, "Il apprécie ton audace.", {"gmi": -12, "rep": -4}, "Il déteste qu'on le contredise."),
    ],
    "Aomine": [
        ("Proposer un 1 contre 1 décontracté", .6, {"mait": 5, "gmi": 8}, "Il rit et te montre un geste.", {"gmi": -2, "sante": -4}, "Il te retourne en deux dribbles."),
        ("Lui demander de t'entraîner", .7, {"mait": 6, "force": 2, "gmi": 6}, "Une séance courte mais redoutable.", {"gmi": -4}, "Il s'endort sur un banc."),
        ("Lui reprocher sa nonchalance", .35, {"gmi": 12, "rep": 4}, "Ça le secoue, et il t'en respecte plus.", {"gmi": -10}, "Il te regarde de haut."),
    ],
    "Murasakibara": [
        ("Lui offrir des friandises", .9, {"gmi": 10, "argent": -20}, "Il est comblé de bonheur.", {"gmi": 2}, "Il n'aimait pas cette marque."),
        ("Lui demander de t'apprendre la défense", .6, {"force": 5, "gmi": 6}, "Il te montre comment fermer la raquette.", {"gmi": -2}, "Il a la flemme de t'expliquer."),
        ("Le défier de bloquer ton tir", .5, {"mait": 5, "gmi": 8}, "Tu le surprends une fois sur deux.", {"gmi": 1, "bonheur": -2}, "Il bloque tout en bâillant."),
    ],
    "Midorima": [
        ("Lui demander son objet porte-bonheur du jour", .8, {"bonheur": 4, "gmi": 6}, "Il te prête un petit objet étrange.", {"gmi": -2}, "Il refuse, 'ce n'est pas ton signe du jour'."),
        ("Observer son tir à l'entraînement", .8, {"mait": 5, "gmi": 5}, "Chaque tir est une leçon de précision.", {"gmi": -1}, "Il te chasse de la salle."),
        ("Le taquiner sur ses superstitions", .4, {"gmi": 8, "bonheur": 3}, "Il pique un fard mais sourit.", {"gmi": -8}, "Il se vexe profondément."),
    ],
    "Kise": [
        ("Lui demander de te montrer un de ses gestes", .85, {"mait": 5, "gmi": 8}, "Il reproduit le geste avec une facilité déconcertante.", {"gmi": -2}, "Il est trop occupé par ses fans."),
        ("Poser pour une photo avec lui", .9, {"rep": 4, "bonheur": 4, "gmi": 5}, "La photo fait le tour de l'école.", {"gmi": 1}, "Tu as les yeux fermés sur la photo."),
        ("Le défier en copiant ses mouvements", .45, {"mait": 6, "gmi": 10}, "Tu l'amuses beaucoup.", {"gmi": 1, "bonheur": -3}, "Il te copie en mieux."),
    ],
}
# nom : (âges, tours, récompense)
COMP = {
    "college": ("Tournoi inter-collèges", (12, 14), ["Premier tour", "Demi-finale", "Finale"], {"xp": 60, "rep": 10, "argent": 120}),
    "inter": ("Inter-High", (15, 18), ["Éliminatoires", "Quart de finale", "Demi-finale", "Finale"], {"xp": 100, "rep": 15, "argent": 250}),
    "winter": ("Winter Cup", (15, 18), ["Premier tour", "Quart de finale", "Demi-finale", "Finale"], {"xp": 150, "rep": 25, "argent": 400}),
}
COMP["nba"] = ("Playoffs NBA", (19, 45), ["Premier tour", "Demi-finale de conférence", "Finale de conférence", "Finales NBA"], {"xp": 200, "rep": 30, "argent": 1500})
ZONES = ["Aucune", "Zone", "Porte de la Zone", "Direct Drive Zone"]
ZONE_REQ = [(0, 0, 0), (3, 50, 15), (7, 65, 16), (12, 80, 17)]  # (entraînements, maîtrise, âge)
SPORTS = {"Boxe": "🥊", "Muay-thaï": "🦵", "Judo": "🥋", "Karaté": "👊", "Jiu-jitsu": "🤼", "Kickboxing": "🦶"}
WIN_PREFIX = ("🌟", "⚔️ Tu bats", "📖", "🏆", "✨", "👁️ Tu voles", "🤝", "🏀 Victoire", "🎖️", "👑", "🇺🇸", "🗺️")
LOSE_PREFIX = ("💥", "😞", "🚩")
STATS = [("sante", "❤️ Santé"), ("bonheur", "😊 Bonheur"), ("intel", "🧠 Intelligence"), ("force", "💪 Force"), ("mait", "🎯 Maîtrise"),
         ("chakra", "🌀 Chakra"), ("rep", "⭐ Réputation"), ("beaute", "💄 Beauté")]
# a = âge minimum
TECH = {
    "clone": dict(n="Multi-clonage", u="Naruto", a=8, p=100, req=("mait", 10), pw=5),
    "subst": dict(n="Substitution", u="Naruto", a=9, p=150, req=("mait", 15), pw=6),
    "terre": dict(n="Mur de terre", u="Naruto", a=11, p=300, req=("nat", "Terre", 2), pw=12),
    "feu": dict(n="Boule de feu suprême", u="Naruto", a=12, p=400, req=("nat", "Feu", 2), pw=14),
    "eau": dict(n="Dragon d'eau", u="Naruto", a=12, p=400, req=("nat", "Eau", 2), pw=14),
    "vent": dict(n="Lame de vent", u="Naruto", a=12, p=400, req=("nat", "Vent", 2), pw=14),
    "foudre": dict(n="Éclair tranchant", u="Naruto", a=15, p=800, req=("nat", "Foudre", 3), pw=22),
    "glace": dict(n="Miroirs de glace", u="Naruto", a=18, p=1500, req=("nat", "Glace", 1), pw=30),
    "bois": dict(n="Forêt profonde", u="Naruto", a=18, p=1500, req=("nat", "Bois", 1), pw=30),
    "sage": dict(n="Mode Sage", u="Naruto", a=25, p=3000, req=("mait", 70), pw=40),
    "genjutsu": dict(n="Genjutsu du Sharingan", u="Naruto", a=16, p=500, req=("pup", "Sharingan"), pw=18),
    "hakke": dict(n="Paume du Hakke", u="Naruto", a=16, p=500, req=("pup", "Byakugan"), pw=20),
    "tsukuyomi": dict(n="Tsukuyomi", u="Naruto", a=18, p=2500, req=("pup", "Mangekyō Sharingan"), pw=40),
    "shinra": dict(n="Shinra Tensei", u="Naruto", a=20, p=4000, req=("pup", "Rinnegan"), pw=55),
    "passe": dict(n="Passe fantôme", u="Kuroko", a=12, p=200, req=("mait", 20), pw=8),
    "trois": dict(n="Tir à trois points", u="Kuroko", a=13, p=400, req=("mait", 30), pw=12),
    "dribble": dict(n="Dribble brise-chevilles", u="Kuroko", a=14, p=700, req=("mait", 40), pw=16),
    "meteore": dict(n="Tir météore", u="Kuroko", a=16, p=1500, req=("mait", 60), pw=28),
    "zone": dict(n="La Zone", u="Kuroko", a=17, p=3000, req=("zone", 1), pw=38),
    "kick": dict(n="Coup de pied circulaire", u="Tokyo Revengers", a=12, p=200, req=("force", 25), pw=8),
    "contre": dict(n="Contre-attaque", u="Tokyo Revengers", a=13, p=400, req=("force", 35), pw=12),
    "charge": dict(n="Charge de division", u="Tokyo Revengers", a=15, p=900, req=("force", 50), pw=20),
    "acier": dict(n="Mental d'acier", u="Tokyo Revengers", a=16, p=1500, req=("rep", 50), pw=26),
    "leap": dict(n="Time Leap", u="Tokyo Revengers", a=20, p=4000, req=("mait", 70), pw=45),
}

# nom, prix, description, effets, univers, âge min
SHOP = {
    "cadeau": ("🎁 Cadeau", 50, "Pour améliorer une relation", {"cadeau": 1}, None, 4),
    "ramen": ("🍜 Bol de ramen", 80, "+15 santé, +5 bonheur", {"sante": 15, "bonheur": 5}, None, 3),
    "boisson": ("🥤 Boisson énergétique", 60, "+1 action cette année", {"pa": 1}, None, 6),
    "manuel": ("📘 Manuel d'entraînement", 400, "+4 force, +4 maîtrise, +3 intel", {"force": 4, "mait": 4, "intel": 3}, None, 8),
    "kunai": ("🗡️ Kunai en acier trempé", 200, "+5 maîtrise", {"mait": 5}, "Naruto", 8),
    "shoes": ("👟 Chaussures de pro", 300, "+6 maîtrise", {"mait": 6}, "Kuroko", 8),
    "chakra": ("📜 Parchemin de chakra", 300, "+10 chakra", {"chakra": 10}, "Naruto", 10),
    "nature": ("🔮 Parchemin de nature", 1000, "Éveille une nouvelle nature de chakra", {"nature": 1}, "Naruto", 10),
    "xp": ("🧪 Potion d'expérience", 500, "+40 XP", {"xp": 40}, None, 10),
    "veste": ("🧥 Veste du gang", 250, "+8 réputation, +3 force", {"rep": 8, "force": 3}, "Tokyo Revengers", 13),
    "leap": ("⏳ Amulette Time Leap", 1500, "Te ramène à la vie une fois", {"revive": 1}, None, 16),
}

# (univers, âge min, âge max, texte, [(label, p_succès, eff_ok, txt_ok, eff_ko, txt_ko)], condition optionnelle)
EV = [
    # Petite enfance
    (None, 1, 2, "Tu fais tes premiers pas devant tes parents.",
     [("Avancer seul", .75, {"force": 2, "bonheur": 4}, "Tu marches ! Tes parents applaudissent.", {"sante": -2}, "Tu tombes sur les fesses."),
      ("Rester dans les bras", 1, {"bonheur": 2}, "Câlins.", {}, "")]),
    (None, 2, 4, "C'est l'heure de tes premiers mots.",
     [("« Maman ! »", 1, {"bonheur": 3}, "Ta mère fond en larmes de joie.", {}, ""),
      ("« Papa ! »", 1, {"bonheur": 3}, "Ton père est aux anges.", {}, ""),
      ("« Ramen ! »", 1, {"bonheur": 4, "intel": 1}, "Toute la famille éclate de rire.", {}, "")]),
    (None, 3, 5, "À la garderie, un enfant te prend ton jouet.",
     [("Le reprendre", .5, {"force": 1, "rep": 2}, "Tu récupères ton jouet.", {"bonheur": -3}, "Tu pleures, la maîtresse te console."),
      ("Laisser faire", 1, {"bonheur": -1, "intel": 1}, "Tu te trouves un autre jeu.", {}, "")]),
    (None, 5, 8, "Contrôle surprise à l'école !",
     [("Réviser tard", .8, {"intel": 4, "bonheur": -2}, "Bonne note !", {"sante": -3}, "Tu t'endors sur ta copie."),
      ("Improviser", .4, {"bonheur": 3}, "Ça passe, incroyable.", {"intel": -1, "bonheur": -4}, "Zéro pointé.")]),
    (None, 9, 17, "Contrôle surprise à l'école !",
     [("Réviser tard", .8, {"intel": 4, "bonheur": -2}, "Bonne note !", {"sante": -3}, "Tu t'endors sur ta copie."),
      ("Improviser", .4, {"bonheur": 3}, "Ça passe, incroyable.", {"intel": -1, "bonheur": -4}, "Zéro pointé.")]),
    # Naruto
    ("Naruto", 6, 9, "À l'Académie, on t'apprend à lancer un kunai pour la première fois.",
     [("Viser la cible", .6, {"mait": 4, "rep": 2}, "En plein dans le mille !", {"bonheur": -2}, "Tu rates et tout le monde rit."),
      ("Jouer les clowns", 1, {"bonheur": 4, "intel": -1}, "Tu fais rire la classe.", {}, "")]),
    ("Naruto", 7, 12, "Un vieux ninja te voit jongler avec ton chakra et propose de te donner une leçon.",
     [("Accepter", .8, {"mait": 6, "chakra": 4}, "Tu apprends une astuce précieuse.", {"bonheur": -3}, "Il s'endort en plein cours..."),
      ("Refuser poliment", 1, {"bonheur": 2}, "Tu préfères jouer dehors.", {}, "")]),
    ("Naruto", 12, 25, "Mission de rang D : retrouver le chat d'une noble dame.",
     [("Foncer", .7, {"argent": 80, "xp": 10}, "Mission réussie, le chat t'a griffé mais tu es payé !", {"sante": -5, "bonheur": -3}, "Le chat t'a échappé."),
      ("Pister avec le chakra", .9, {"argent": 60, "xp": 12, "chakra": -3}, "Pisté sans effort !", {}, "")]),
    ("Naruto", 12, 20, "L'examen de promotion approche, le jury t'attend.",
     [("Participer", .55, {"xp": 60, "rep": 10}, "Tu réussis l'examen !", {"sante": -10, "bonheur": -8}, "Tu échoues de justesse."),
      ("Attendre l'an prochain", 1, {"intel": 3}, "Tu t'entraînes encore un an.", {}, "")]),
    ("Naruto", 15, 50, "Un ninja déserteur menace le village.",
     [("L'affronter", .5, {"xp": 50, "rep": 15, "argent": 150}, "Tu le mets hors d'état de nuire !", {"sante": -30, "rep": -3}, "Il t'inflige de graves blessures."),
      ("Alerter les anciens", .95, {"xp": 15, "rep": 3}, "Le village est sauvé grâce à ton alerte.", {}, "")]),
    ("Naruto", 10, 60, "Une rumeur parle d'un parchemin interdit caché dans une grotte.",
     [("Y aller", .4, {"chakra": 15, "mait": 8, "xp": 20}, "Tu trouves le parchemin !", {"sante": -20, "bonheur": -5}, "Piège ! Tu t'en sors de justesse."),
      ("Ignorer", 1, {}, "Tu restes prudent.", {}, "")]),
    # Kuroko
    ("Kuroko", 6, 11, "Des enfants jouent au basket dans un parc et te proposent de te joindre à eux.",
     [("Jouer avec eux", .8, {"mait": 4, "bonheur": 5}, "Tu t'amuses comme un fou.", {"sante": -2}, "Tu te tords la cheville."),
      ("Regarder de loin", 1, {"intel": 1}, "Tu observes leurs gestes.", {}, "")]),
    ("Kuroko", 12, 15, "Le coach te propose de rejoindre l'équipe de basket du collège.",
     [("Rejoindre", .85, {"mait": 8, "force": 3, "rep": 3}, "Tu intègres l'équipe !", {"bonheur": -4}, "Tu finis sur le banc."),
      ("Passer", 1, {"intel": 2}, "Tu te concentres sur les études.", {}, "")]),
    ("Kuroko", 15, 18, "Match d'entraînement contre un lycée rival.",
     [("Jouer à fond", .6, {"mait": 6, "xp": 25, "rep": 6}, "Victoire !", {"bonheur": -6, "sante": -5}, "Défaite amère."),
      ("Rester sur le banc", 1, {"bonheur": -1}, "Tu regardes le match.", {}, "")]),
    ("Kuroko", 13, 40, "Un prodige te propose un 1 contre 1 sur un playground.",
     [("Relever le défi", .45, {"mait": 10, "rep": 8}, "Tu l'accroches jusqu'au bout !", {"mait": 4, "bonheur": -5}, "Écrasé, mais tu as appris."),
      ("Refuser", 1, {}, "Pas aujourd'hui.", {}, "")]),
    ("Kuroko", 14, 30, "Ta présence discrète pourrait devenir une arme : travailler la passe invisible ?",
     [("S'y consacrer", .8, {"mait": 7, "intel": 2}, "Plus personne ne te voit venir !", {"sante": -5}, "Tu te blesses en forçant."),
      ("Continuer comme avant", 1, {}, "Rien ne change.", {}, "")]),
    # Tokyo Revengers
    ("Tokyo Revengers", 6, 11, "Un grand du quartier te propose de faire la course à vélo.",
     [("Accepter", .6, {"force": 2, "rep": 3, "bonheur": 4}, "Tu gagnes la course !", {"sante": -5, "bonheur": -2}, "Chute spectaculaire."),
      ("Refuser", 1, {}, "Tu rentres à la maison.", {}, "")]),
    ("Tokyo Revengers", 13, 25, "Un gang rival t'attend à la sortie.",
     [("Se battre", .55, {"xp": 30, "rep": 10, "force": 3}, "Tu gagnes !", {"sante": -20, "rep": -4}, "Tu te fais rouer de coups."),
      ("Fuir", .9, {"bonheur": -3}, "Tu t'échappes.", {"sante": -5}, "Tu es rattrapé.")]),
    ("Tokyo Revengers", 14, 30, "Un ami est pris pour cible par une bande.",
     [("Le défendre", .6, {"rep": 12, "xp": 25, "bonheur": 5}, "Votre amitié en sort renforcée.", {"sante": -25}, "Tu encaisses les coups pour lui."),
      ("Appeler à l'aide", .9, {"xp": 8}, "Les renforts arrivent.", {}, "")]),
    ("Tokyo Revengers", 15, 40, "Réunion sous le temple : le chef cherche un volontaire.",
     [("Se porter volontaire", .65, {"xp": 40, "rep": 10, "argent": 100}, "Mission accomplie avec honneur.", {"sante": -15, "rep": -3}, "La mission tourne mal."),
      ("Rester discret", 1, {}, "Un autre s'en charge.", {}, "")]),
    ("Tokyo Revengers", 16, 60, "Un flash étrange : tu entrevois un autre futur...",
     [("Tenter de le changer", .5, {"mait": 8, "intel": 4, "xp": 30}, "Tu évites une tragédie.", {"bonheur": -8, "sante": -8}, "Tu t'épuises sans résultat."),
      ("Oublier", 1, {}, "Ce n'était qu'un rêve.", {}, "")]),
    # Vie générale
    (None, 14, 35, "Quelqu'un te plaît vraiment dans ton entourage.",
     [("Se déclarer", .5, {"bonheur": 12}, "Complicité immédiate !", {"bonheur": -8}, "Râteau..."),
      ("Rester ami", 1, {"bonheur": 2}, "Tu gardes ça pour toi.", {}, "")]),
    (None, 3, 75, "Tu tombes malade.",
     [("Voir un médecin", 1, {"argent": -40, "sante": 5}, "Tu guéris vite.", {}, ""),
      ("Ignorer", .5, {}, "Ça passe tout seul.", {"sante": -15}, "Ça empire.")]),
    (None, 18, 60, "Un inconnu te propose un pari risqué.",
     [("Parier 100", .45, {"argent": 200}, "Tu gagnes le double !", {"argent": -100}, "Tu perds ta mise."),
      ("Décliner", 1, {}, "Tu restes sage.", {}, "")]),
    # Bijū
    ("SPECIAL", 0, 99, "Une présence immense s'éveille en toi : une bête à queues cherche un hôte.",
     [("Accepter le pacte", .6, {"biju": 1, "xp": 30}, "Un bijū est scellé en toi !", {"sante": -30, "bonheur": -10}, "Le sceau échoue, tu survives de justesse."),
      ("Refuser", 1, {"bonheur": 2}, "La présence s'efface.", {}, "")], "pacte"),
    ("Naruto", 6, 90, "Le bijū te parle dans ton sommeil.",
     [("Lui répondre", .7, {"lien": 8, "chakra": 2}, "Une conversation étonnamment sincère.", {"bonheur": -5, "lien": -3}, "Il se moque de toi, cauchemar garanti."),
      ("L'ignorer", 1, {"lien": -5}, "Il boude dans sa cage.", {}, "")], "biju"),
    ("Naruto", 6, 90, "On se méfie de toi : on murmure que tu portes une bête.",
     [("Prouver ta valeur", .5, {"rep": 10, "xp": 20}, "Les regards changent peu à peu.", {"rep": -6, "bonheur": -8}, "Ça empire, on t'évite."),
      ("T'isoler", 1, {"bonheur": -4, "lien": 5}, "Seul ton bijū te tient compagnie.", {}, "")], "biju"),
    ("Naruto", 14, 60, "Des chasseurs traquent les porteurs de bijū.",
     [("Fuir", .6, {"xp": 10}, "Tu leur échappes.", {"sante": -15}, "Tu es blessé dans ta fuite."),
      ("Se battre avec la puissance du bijū", .65, {"xp": 60, "rep": 15, "lien": -4}, "Tu les terrasses !", {"sante": -35, "lien": -6}, "Tu perds le contrôle et tu es gravement blessé.")], "biju"),
    ("SPECIAL", 13, 18, "Un joueur de la Génération des Miracles t'a repéré lors d'un match et te propose de rejoindre son équipe.",
     [("Accepter l'invitation", .85, {"recrue": 1, "xp": 40, "rep": 8}, "Tu rejoins l'équipe d'un Miracle !", {"bonheur": -4}, "Le test se passe mal : il te laisse partir."),
      ("Refuser", 1, {"bonheur": -1}, "Tu restes sur ta propre route.", {}, "")], "gm"),
    # Alliances
    (None, 12, 70, "Un de tes alliés te demande de l'aide contre une faction rivale.",
     [("Envoyer des renforts", .65, {"alrel": 12, "xp": 30, "rep": 6}, "Votre alliance sort renforcée.", {"alrel": -5, "sante": -15}, "Vous perdez la bataille."),
      ("Refuser", 1, {"alrel": -12, "karma": -3}, "Ton allié est déçu.", {}, "")], "ally"),
    (None, 12, 70, "Tes alliés organisent un grand banquet pour célébrer votre pacte.",
     [("Y participer", 1, {"alrel": 6, "bonheur": 4, "argent": -30}, "Une soirée mémorable.", {}, ""),
      ("Décliner", 1, {"alrel": -3}, "Ton absence est remarquée.", {}, "")], "ally"),
    # Karma
    (None, 8, 60, "Tu trouves un portefeuille bien rempli dans la rue.",
     [("Le rapporter", 1, {"karma": 8, "rep": 3}, "Le propriétaire te remercie chaleureusement.", {}, ""),
      ("Le garder", .8, {"argent": 150, "karma": -8}, "Tu empoches l'argent.", {"karma": -8, "rep": -5}, "Quelqu'un t'a vu faire...")]),
    (None, 10, 60, "Un camarade blessé te demande de l'aide.",
     [("L'aider", .9, {"karma": 6, "bonheur": 3}, "Il t'est très reconnaissant.", {"sante": -3}, "Tu te blesses un peu en l'aidant."),
      ("Passer ton chemin", 1, {"karma": -4}, "Tu ne te retournes pas.", {}, "")]),
    (None, 12, 60, "Un marchand te propose un marché douteux : voler un client en échange d'une part.",
     [("Accepter", .7, {"argent": 120, "karma": -10}, "L'affaire est conclue, sans témoin.", {"rep": -10, "karma": -10, "bonheur": -4}, "Tu es démasqué."),
      ("Refuser", 1, {"karma": 4}, "Tu gardes la conscience tranquille.", {}, "")]),
    ("SPECIAL", 16, 60, "Un homme au manteau noir orné de nuages rouges t'observe depuis l'ombre : l'Akatsuki cherche des recrues.",
     [("Rejoindre l'Akatsuki", .85, {"akatsuki": 1, "karma": -15, "rep": -40, "xp": 40}, "Tu abandonnes ton village.", {"sante": -20, "karma": -5}, "Tu échoues à leur test et t'enfuis."),
      ("Refuser", 1, {"karma": 5}, "Tu tournes le dos à l'ombre.", {}, "")], "akat"),
]
TECH.update({
    # Natures (2e palier) — il faut posséder la nature
    "phenix": dict(n="Pluie de boules de feu", u="Naruto", a=14, p=700, req=("nat", "Feu", 3), pw=22),
    "prison": dict(n="Prison d'eau", u="Naruto", a=14, p=700, req=("nat", "Eau", 3), pw=22),
    "tornade": dict(n="Grande tornade", u="Naruto", a=14, p=700, req=("nat", "Vent", 3), pw=22),
    "golem": dict(n="Golem de roche", u="Naruto", a=14, p=700, req=("nat", "Terre", 3), pw=22),
    "lance": dict(n="Lance de foudre", u="Naruto", a=17, p=1200, req=("nat", "Foudre", 4), pw=30),
    "lave": dict(n="Libération de la lave", u="Naruto", a=18, p=1500, req=("nat", "Lave", 1), pw=30),
    # Clans
    "ombre": dict(n="Possession de l'ombre", u="Naruto", a=9, p=250, req=("clan", "Nara"), pw=12),
    "baika": dict(n="Expansion Baika", u="Naruto", a=9, p=250, req=("clan", "Akimichi"), pw=12),
    "esprit": dict(n="Transfert d'esprit", u="Naruto", a=10, p=250, req=("clan", "Yamanaka"), pw=12),
    "insectes": dict(n="Insectes Kikaichū", u="Naruto", a=9, p=250, req=("clan", "Aburame"), pw=12),
    "gatsuga": dict(n="Crocs perforants", u="Naruto", a=9, p=250, req=("clan", "Inuzuka"), pw=14),
    "chaines": dict(n="Chaînes de chakra", u="Naruto", a=14, p=600, req=("clan", "Uzumaki"), pw=24),
    "sceau": dict(n="Maître des sceaux", u="Naruto", a=18, p=1500, req=("clan", "Uzumaki"), pw=32),
    "hydrat": dict(n="Hydratation du corps", u="Naruto", a=12, p=500, req=("clan", "Hozuki"), pw=18),
    "os": dict(n="Danse de l'os", u="Naruto", a=13, p=500, req=("clan", "Kaguya"), pw=22),
    "sable": dict(n="Tombeau de sable", u="Naruto", a=14, p=600, req=("clan", "Sabaku"), pw=24),
    "armure": dict(n="Armure de foudre", u="Naruto", a=15, p=700, req=("clan", "Yotsuki"), pw=26),
    # Pupilles
    "kaiten": dict(n="Rotation divine", u="Naruto", a=14, p=600, req=("pup", "Byakugan"), pw=24),
    "amaterasu": dict(n="Amaterasu", u="Naruto", a=20, p=3500, req=("pup", "Mangekyō Sharingan"), pw=50),
    "susanoo": dict(n="Susanoo", u="Naruto", a=22, p=4500, req=("pup", "Mangekyō Sharingan"), pw=60),
    # Kuroko
    "vanish": dict(n="Vanishing Drive", u="Kuroko", a=15, p=900, req=("mait", 50), pw=18),
    "ignite": dict(n="Ignite Pass Kai", u="Kuroko", a=16, p=1600, req=("mait", 60), pw=26),
    "pcopy": dict(n="Perfect Copy", u="Kuroko", a=15, p=1200, req=("talent", "copie"), pw=26),
    "empeye": dict(n="Vision de l'Empereur", u="Kuroko", a=15, p=1200, req=("talent", "empereur"), pw=26),
    "belye": dict(n="Vision de Bélial", u="Kuroko", a=15, p=1200, req=("talent", "belial"), pw=26),
    "longue": dict(n="Tir de très longue portée", u="Kuroko", a=15, p=1200, req=("talent", "tir"), pw=26),
    "mur": dict(n="Mur infranchissable", u="Kuroko", a=15, p=1200, req=("talent", "viking"), pw=26),
    # Tokyo Revengers
    "heavy": dict(n="Frappe du dragon", u="Tokyo Revengers", a=17, p=1800, req=("force", 60), pw=28),
    "kick2": dict(n="Coup de pied légendaire", u="Tokyo Revengers", a=18, p=3000, req=("force", 75), pw=40),
    "aura": dict(n="Aura de chef", u="Tokyo Revengers", a=18, p=2000, req=("rep", 70), pw=22),
})

SHOP.update({
    "nature": ("🔮 Parchemin de nature", 1000, "Tente d'éveiller une 2e nature de chakra (60 %, max 2 natures)", {"nature": 1}, "Naruto", 10),
    "shuriken": ("🌟 Lot de shurikens", 150, "+4 maîtrise", {"mait": 4}, "Naruto", 8),
    "pilule": ("💊 Pilule du soldat", 220, "+25 santé, +5 chakra", {"sante": 25, "chakra": 5}, "Naruto", 10),
    "invoc": ("📜 Parchemin d'invocation", 600, "+8 chakra, +4 réputation", {"chakra": 8, "rep": 4}, "Naruto", 12),
    "bandeau": ("🎖️ Bandeau frontal poli", 120, "+4 réputation", {"rep": 4}, "Naruto", 12),
    "ballon": ("🏀 Ballon dédicacé", 180, "+10 bonheur, +2 maîtrise", {"bonheur": 10, "mait": 2}, "Kuroko", 6),
    "genou": ("🦵 Genouillères de pro", 140, "+10 santé", {"sante": 10}, "Kuroko", 10),
    "mag": ("📰 Magazine de basket", 100, "+3 intel, +2 maîtrise", {"intel": 3, "mait": 2}, "Kuroko", 8),
    "maillot": ("👕 Maillot de lycée", 200, "+5 réputation", {"rep": 5}, "Kuroko", 15),
    "moto": ("🏍️ Moto d'occasion", 700, "+8 réputation, +2 force", {"rep": 8, "force": 2}, "Tokyo Revengers", 14),
    "gants": ("🥊 Gants de boxe", 220, "+4 force", {"force": 4}, "Tokyo Revengers", 10),
    "tokko": ("👘 Tokkō-fuku brodé", 300, "+6 réputation", {"rep": 6}, "Tokyo Revengers", 13),
    "repas": ("🍙 Repas de gang", 90, "+10 santé, +3 bonheur", {"sante": 10, "bonheur": 3}, "Tokyo Revengers", 12),
})
ONCE_SHOP = {"moto", "tokko", "maillot", "bandeau"}  # achetables une seule fois

# ───────── Dialogues avec les PNJ : (libellé, p, eff_ok, txt_ok, eff_ko, txt_ko) ─────────
TALK_GEN = {
    "ami": [
        ("Parler de vos rêves", .9, {"aff": 8, "bonheur": 3}, "Vous rêvez à voix haute jusqu'à la nuit.", {"aff": -2}, "La conversation tourne court."),
        ("T'entraîner ensemble", .8, {"aff": 6, "force": 2, "mait": 2, "sante": -2}, "Vous vous poussez mutuellement.", {"aff": -2, "sante": -4}, "Tu te blesses légèrement."),
        ("Lui confier un secret", .7, {"aff": 12, "bonheur": 3}, "Il te jure de le garder.", {"aff": -8, "rep": -3}, "Il n'a pas su tenir sa langue..."),
    ],
    "equipier": [
        ("Réviser la stratégie d'équipe", .85, {"aff": 6, "intel": 2, "mait": 2}, "Votre cohésion s'améliore.", {"aff": -2}, "Vous n'êtes pas d'accord."),
        ("Partager un repas", .95, {"aff": 8, "bonheur": 3}, "Un moment de complicité.", {"aff": 1}, "Le repas est silencieux."),
        ("Le défier amicalement", .6, {"aff": 6, "mait": 3}, "Il te rend coup pour coup.", {"aff": -4, "bonheur": -2}, "Il le prend mal."),
    ],
    "rival": [
        ("Le provoquer", .5, {"aff": 6, "rep": 3}, "Il respecte ton cran.", {"aff": -4, "bonheur": -2}, "Il te snobe."),
        ("Lui tendre la main", .6, {"aff": 10, "karma": 3}, "Un respect mutuel naît.", {"aff": -3, "bonheur": -2}, "Il refuse ta main."),
        ("Étudier son style de près", .7, {"mait": 3, "intel": 2}, "Tu repères ses habitudes.", {"aff": -2}, "Il te surprend en train de l'épier."),
    ],
    "amour": [
        ("Lui offrir un petit présent", .85, {"aff": 10, "bonheur": 4, "argent": -20}, "Elle/il rougit de plaisir.", {"aff": -2, "argent": -20}, "Le cadeau tombe à plat."),
        ("L'inviter à se promener", .8, {"aff": 9, "bonheur": 5}, "Une balade qui restera gravée.", {"aff": -3}, "Il/elle est trop occupé(e)."),
        ("Avouer tes sentiments avec poésie", .5, {"aff": 15, "bonheur": 6}, "Tu touches en plein cœur.", {"aff": -8, "bonheur": -4}, "Gêne totale."),
    ],
    "famille": [
        ("Aider à la maison", 1, {"aff": 6, "karma": 2}, "Ta famille apprécie ton aide.", {}, ""),
        ("Demander un conseil", .9, {"aff": 4, "intel": 2}, "Un bon conseil de famille.", {"aff": -1}, "Tu n'écoutes pas vraiment."),
        ("Raconter ta journée", 1, {"aff": 5, "bonheur": 3}, "Un moment de chaleur.", {}, ""),
    ],
    "mentor": [
        ("Demander une leçon", .85, {"aff": 4, "mait": 5, "xp": 8}, "Une leçon précieuse.", {"aff": -2, "bonheur": -2}, "Il te trouve trop pressé."),
        ("L'interroger sur son passé", .7, {"aff": 6, "intel": 3}, "Il se confie pour la première fois.", {"aff": -3}, "Il change de sujet."),
        ("Lui demander un défi", .6, {"aff": 5, "mait": 4, "force": 2, "sante": -3}, "Un défi à ta mesure.", {"aff": -2, "sante": -6}, "Tu échoues lamentablement."),
    ],
}

# ───────── Événements supplémentaires (même format que EV) ─────────
EV_NEW = [
    # Naruto
    ("Naruto", 12, 30, "Ton sensei te propose un entraînement spécial en forêt.",
     [("Relever le défi", .65, {"mait": 6, "force": 3, "xp": 15}, "Tu repousses tes limites !", {"sante": -10, "bonheur": -3}, "Tu craques avant la fin."),
      ("Demander à remettre", 1, {"intel": 1}, "Ton sensei hoche la tête, patient.", {}, "")]),
    ("Naruto", 14, 50, "Un ninja d'un autre village traverse la frontière : espion ou égaré ?",
     [("L'intercepter", .55, {"xp": 25, "rep": 8}, "Tu le captures, le village te félicite.", {"sante": -15, "rep": -3}, "Il t'échappe en te blessant."),
      ("Le suivre discrètement", .7, {"xp": 15, "intel": 3}, "Tu découvres ses plans.", {"bonheur": -2}, "Tu le perds de vue."),
      ("Fermer les yeux", 1, {"karma": -2}, "Ce n'est pas ton problème.", {}, "")]),
    ("Naruto", 16, 60, "Un clan rival tend une embuscade à ta patrouille.",
     [("Riposter", .55, {"xp": 35, "rep": 10}, "Tu repousses leurs ninjas !", {"sante": -25, "rep": -4}, "Vous subissez de lourdes pertes."),
      ("Couvrir la retraite", .8, {"xp": 20, "karma": 5}, "Tu sauves tes camarades.", {"sante": -15}, "Tu es blessé en les couvrant.")]),
    ("Naruto", 10, 40, "Un marchand ambulant vend des parchemins aux symboles étranges.",
     [("Acheter (150)", .6, {"argent": -150, "chakra": 8, "mait": 3}, "Le parchemin contient une vraie astuce !", {"argent": -150, "bonheur": -3}, "C'était une contrefaçon."),
      ("Passer son chemin", 1, {}, "Tu gardes tes ryōs.", {}, "")]),
    # Kuroko
    ("Kuroko", 13, 40, "Un magazine de basket veut t'interviewer.",
     [("Accepter", .85, {"rep": 8, "bonheur": 4}, "Ton interview fait le buzz.", {"rep": -3, "bonheur": -2}, "Tes propos sont mal interprétés."),
      ("Refuser", 1, {"mait": 2}, "Tu préfères t'entraîner.", {}, "")]),
    ("Kuroko", 13, 40, "Une rivalité éclate au sein de ton équipe pour une place de titulaire.",
     [("Prouver ta valeur sur le terrain", .6, {"mait": 5, "rep": 5}, "Le coach te donne raison.", {"bonheur": -5, "rep": -2}, "Tu restes remplaçant."),
      ("Discuter franchement", .8, {"intel": 2, "bonheur": 3}, "Vous trouvez un terrain d'entente.", {"bonheur": -2}, "La tension reste.")]),
    ("Kuroko", 12, 40, "Une douleur au genou apparaît après un entraînement intensif.",
     [("Se reposer", 1, {"sante": 6, "mait": -1}, "Tu prends soin de toi.", {}, ""),
      ("Continuer quand même", .5, {"mait": 5, "force": 2}, "Tu progresses sans casse.", {"sante": -20, "bonheur": -5}, "La blessure s'aggrave.")]),
    ("Kuroko", 14, 35, "Un joueur d'une autre équipe te défie en 1 contre 1 devant tout le lycée.",
     [("Relever le défi", .5, {"rep": 8, "mait": 3}, "Tu l'emportes sous les applaudissements.", {"rep": -4, "bonheur": -4}, "Défaite publique."),
      ("Décliner poliment", 1, {"karma": 1}, "Tu gardes ton calme.", {}, "")]),
    # Tokyo Revengers
    ("Tokyo Revengers", 12, 30, "Un dojo du quartier propose un sparring à qui veut.",
     [("S'inscrire", .7, {"force": 4, "mait": 3, "xp": 12}, "Tu apprends vite au contact des pros.", {"sante": -10, "bonheur": -2}, "Tu encaisses de gros coups."),
      ("Passer", 1, {}, "Pas aujourd'hui.", {}, "")]),
    ("Tokyo Revengers", 13, 40, "Une rixe éclate devant le konbini : un lycéen est à terre.",
     [("Intervenir", .6, {"rep": 8, "karma": 5, "xp": 15}, "Tu le sauves et les voyous détalent.", {"sante": -18, "rep": -2}, "Tu prends des coups pour rien."),
      ("Appeler la police", .95, {"karma": 2}, "Les agents arrivent.", {}, "")]),
    ("Tokyo Revengers", 14, 40, "Une assemblée de gangs se tient sous le temple : on t'y invite en observateur.",
     [("Y aller", .75, {"rep": 6, "intel": 3, "xp": 10}, "Tu repères les forces en présence.", {"sante": -8, "rep": -3}, "On te chasse à coups de poing."),
      ("Ignorer", 1, {}, "Tu restes dans ton coin.", {}, "")]),
    # Général
    (None, 16, 50, "Tu croises un ancien camarade qui a mal tourné.",
     [("Tenter de le raisonner", .5, {"karma": 5, "bonheur": 3}, "Il t'écoute enfin.", {"bonheur": -4}, "Il te rit au nez."),
      ("L'éviter", 1, {}, "Tu changes de trottoir.", {}, "")]),
    (None, 20, 60, "Un héritage inattendu : une lointaine parente t'a couché sur son testament.",
     [("Accepter", 1, {"argent": 250, "bonheur": 4}, "Une jolie somme !", {}, "")]),
]

# ───────── Arcs narratifs : suites d'étapes (p : float | ("pw", seuil) | ("st", stat, seuil)) ─────────
def _flags(g): return g["flags"]
def _gr(g): return (g.get("gang") or {}).get("rang", 0)
def _nar_ok(g): return not g["akatsuki"]

ARCS = [
    # ─────────── NARUTO ───────────
    dict(id="chunin", nom="Examen Chūnin", u="Naruto", a=(13, 30), cond=lambda g: g["cap"] == 1 and g["xp"] >= 40 and _nar_ok(g), p=.35, man=True, rep=True,
         steps=[
             dict(t="📝 Épreuve écrite. Les questions sont presque impossibles : on teste surtout ta capacité à tricher sans te faire prendre.", ko="end", ch=[
                 ("Réfléchir par toi-même", ("st", "intel", 70), {"intel": 2, "xp": 8}, "Tu rends une copie solide.", {"bonheur": -4}, "Tu sèches sur la dernière question."),
                 ("Tricher discrètement", .55, {"karma": -3, "xp": 8}, "Personne ne remarque ton manège.", {"rep": -6, "karma": -3}, "Tu es repéré et disqualifié.")]),
             dict(t="🌲 Forêt de la Mort. Prédateurs géants et équipes rivales : il faut un parchemin avant d'atteindre la tour.", ko="end", ch=[
                 ("Foncer vers la tour", ("pw", 63), {"xp": 15, "force": 2}, "Tu franchis la forêt en trombe.", {"sante": -15}, "Un prédateur te met hors course."),
                 ("Tendre une embuscade", ("pw", 54), {"xp": 18, "mait": 2}, "Tu t'empares d'un parchemin par ruse.", {"sante": -12}, "L'embuscade se retourne contre toi."),
                 ("Éviter les combats", .55, {"xp": 8, "intel": 2}, "Tu passes entre les mailles.", {"sante": -8, "bonheur": -3}, "Tu es rattrapé hors du temps imparti.")]),
             dict(t="⚔️ Préliminaires : un combat 1 contre 1 devant les examinateurs.", ko="end", ch=[
                 ("Tout donner", ("pw", 81), {"xp": 20, "rep": 4}, "Tu écrases ton adversaire !", {"sante": -18}, "Tu es mis à terre."),
                 ("Jouer la stratégie", ("st", "intel", 65), {"xp": 18, "intel": 2}, "Tu le piéges avec brio.", {"sante": -10}, "Il déjoue ton plan.")]),
             dict(t="🏟️ Finale : les Kage et les daimyō sont dans les tribunes. Tout le monde te regarde.", ko="end", ch=[
                 ("Attaquer de front", ("pw", 108), {"xp": 25, "rep": 8}, "La foule se lève !", {"sante": -20}, "Tu tombes avec honneur."),
                 ("Piéger ton adversaire", ("st", "intel", 75), {"xp": 25, "rep": 8}, "Un coup de maître !", {"sante": -12}, "Il lit ton jeu.")]),
         ],
         fin=dict(eff={"cap": 2, "xpmin": 150, "rep": 12, "flag": "chunin"}, txt="🎖️ Tu réussis l'examen : tu es promu Chūnin !"),
         ko_txt="Tu échoues à l'examen Chūnin. Tu pourras retenter."),
    dict(id="rangC", nom="Mission de rang C qui tourne mal", u="Naruto", a=(12, 17), cond=lambda g: _nar_ok(g), p=.3, need=2,
         steps=[
             dict(t="Tu escortes un constructeur de pont quand des ninjas déserteurs surgissent de la brume.", ch=[
                 ("Protéger le client", ("pw", 54), {"xp": 12, "rep": 3}, "Le client est sain et sauf.", {"sante": -10}, "Tu es blessé en le protégeant."),
                 ("Contre-attaquer", ("pw", 63), {"xp": 15, "mait": 2}, "Tu en neutralises un !", {"sante": -12}, "Tu es débordé.")]),
             dict(t="Ton équipe est dispersée par une explosion. Qui sauver en premier ?", ch=[
                 ("Sauver ton équipier", .8, {"karma": 6, "xp": 10}, "Tu le ramènes en vie.", {"sante": -12}, "Tu y laisses des plumes."),
                 ("Finir la mission d'abord", .7, {"xp": 12, "karma": -3, "argent": 60}, "Mission remplie, mais à quel prix ?", {"rep": -4}, "Tu perds la cible et ton équipier.")]),
             dict(t="Le chef des déserteurs te défie seul à seul.", ch=[
                 ("Relever le défi", ("pw", 76), {"xp": 25, "rep": 6}, "Tu le terrasses !", {"sante": -20}, "Il te laisse à terre."),
                 ("Chercher des renforts", .8, {"xp": 8}, "Les renforts arrivent à temps.", {"rep": -3}, "Tu arrives trop tard.")]),
         ],
         fin=dict(eff={"xp": 40, "rep": 6, "argent": 200, "flag": "rangC"}, txt="📜 Mission accomplie : ton équipe est honorée.")),
    dict(id="invasion", nom="Invasion de {V}", u="Naruto", a=(14, 45), cond=lambda g: "invasion" not in _flags(g) and _nar_ok(g), p=.1, need=2,
         steps=[
             dict(t="Les alarmes retentissent : des ninjas ennemis franchissent les murailles de {V} !", ch=[
                 ("Organiser la défense", ("st", "intel", 55), {"xp": 15, "rep": 5}, "Les civils sont évacués.", {"rep": -3}, "Ton plan est en retard."),
                 ("Monter au front", ("pw", 80), {"xp": 20, "rep": 5}, "Tu repousses la première vague.", {"sante": -15}, "Tu es repoussé.")]),
             dict(t="Un ninja d'élite ennemi s'attaque au cœur du village.", ch=[
                 ("L'affronter", ("pw", 128), {"xp": 30, "rep": 10}, "Tu le retiens, le temps que les renforts arrivent.", {"sante": -30}, "Tu es gravement blessé."),
                 ("Protéger les civils", .75, {"karma": 6, "rep": 6}, "Tu sauves des dizaines de vies.", {"sante": -10}, "Tu ne peux pas tous les sauver.")]),
             dict(t="Le chef des envahisseurs se dévoile. C'est le moment décisif.", ch=[
                 ("Tout risquer", ("pw", 152), {"xp": 40, "rep": 12}, "L'ennemi bat en retraite !", {"sante": -35}, "Tu t'effondres."),
                 ("Tenir la ligne", .7, {"xp": 20, "rep": 6}, "Le village tient bon.", {"sante": -15}, "La ligne cède.")]),
         ],
         fin=dict(eff={"xp": 80, "rep": 15, "flag": "invasion"}, txt="🛡️ Tu as défendu {V} : on t'acclame comme un héros.")),
    dict(id="jonin", nom="Examen de Jōnin spécial", u="Naruto", a=(18, 45), cond=lambda g: g["cap"] == 2 and _nar_ok(g), p=.3, man=True, rep=True,
         steps=[
             dict(t="Mission de rang A : infiltrer une forteresse ennemie.", ko="end", ch=[
                 ("Infiltration furtive", ("st", "intel", 70), {"xp": 25}, "Tu reviens avec les plans.", {"sante": -12}, "Tu es démasqué."),
                 ("Assaut frontal", ("pw", 128), {"xp": 25}, "Tu ouvres la voie.", {"sante": -22}, "Tu es submergé.")]),
             dict(t="On te confie une équipe de jeunes Genin pour leur première mission.", ko="end", ch=[
                 ("Les guider avec patience", ("st", "intel", 60), {"xp": 20, "karma": 3}, "Ils reviennent grandis.", {"bonheur": -3}, "Ils désobéissent, c'est un fiasco."),
                 ("Les mettre à l'épreuve", ("pw", 96), {"xp": 20}, "Ils te surprennent !", {"sante": -10}, "Mission ratée.")]),
             dict(t="L'épreuve finale : affronter un Jōnin en duel.", ko="end", ch=[
                 ("Donner ton maximum", ("pw", 152), {"xp": 35, "rep": 6}, "Il reconnaît ta valeur.", {"sante": -20}, "Tu n'es pas encore prêt."),
                 ("Miser sur ta technique de voie", ("pw", 136), {"xp": 35, "rep": 6}, "Ta technique le prend par surprise.", {"sante": -15}, "Il la contre.")]),
         ],
         fin=dict(eff={"cap": 3, "xpmin": 300, "rep": 15, "flag": "jonin"}, txt="🎖️ Tu es promu Jōnin : un ninja d'élite !"),
         ko_txt="Tu échoues à l'examen de Jōnin. Tu pourras retenter."),
    dict(id="anbu", nom="Invitation dans l'ANBU", u="Naruto", a=(20, 50), cond=lambda g: g["cap"] == 3 and "anbu" not in _flags(g) and _nar_ok(g), p=.3, man=True, rep=True,
         steps=[
             dict(t="Un homme masqué t'aborde : l'ANBU observe ton parcours. Il te propose l'épreuve du masque.", ko="end", ch=[
                 ("Accepter l'épreuve", ("pw", 150), {"xp": 40}, "Tu portes le masque avec aisance.", {"sante": -20}, "Tu échoues l'épreuve."),
                 ("Négocier tes conditions", ("st", "rep", 60), {"xp": 25, "rep": 4}, "On t'accorde une certaine autonomie.", {"bonheur": -3}, "On te juge arrogant.")]),
             dict(t="Première mission : éliminer un noble corrompu qui vend des secrets à l'étranger.", ko="end", ch=[
                 ("Exécuter l'ordre", ("pw", 158), {"xp": 40, "karma": -5}, "Cible neutralisée, sans témoin.", {"sante": -22}, "Les gardes te blessent."),
                 ("Le livrer vivant", ("st", "intel", 70), {"xp": 40, "karma": 4}, "Il sera jugé publiquement.", {"rep": -4}, "Il s'échappe.")]),
         ],
         fin=dict(eff={"cap": 4, "xpmin": 600, "rep": 10, "flag": "anbu"}, txt="🎭 Tu rejoins l'ANBU. Ton nom disparaît des registres publics."),
         ko_txt="L'ANBU te refuse pour le moment."),
    dict(id="kage", nom="Succession : devenir {K}", u="Naruto", a=(30, 70), cond=lambda g: g["cap"] >= 4 and g["rep"] >= 75 and "kage" not in _flags(g) and _nar_ok(g), p=.3, man=True, rep=True,
         steps=[
             dict(t="Le {K} songe à se retirer. Le conseil des anciens examine ta candidature.", ko="end", ch=[
                 ("Plaider ta cause", ("st", "rep", 95), {"rep": 5}, "Le conseil est conquis.", {"rep": -4}, "Le conseil juge ta réputation insuffisante."),
                 ("Rappeler tes exploits", ("st", "intel", 75), {"rep": 5}, "Les anciens hochent la tête.", {"bonheur": -3}, "Ils restent sceptiques.")]),
             dict(t="L'épreuve : défendre {V} contre une menace redoutable.", ko="end", ch=[
                 ("Affronter la menace seul", ("pw", 196), {"xp": 60, "rep": 10}, "Tu la repousses sous les yeux de tous.", {"sante": -35}, "Tu échoues."),
                 ("Mener l'armée du village", ("st", "intel", 95), {"xp": 50, "rep": 10}, "Ta stratégie sauve {V}.", {"sante": -15}, "Ton plan s'effondre.")]),
             dict(t="Le discours d'investiture devant tout le village.", ko="end", ch=[
                 ("Un discours poignant", ("st", "intel", 80), {"rep": 10}, "Les larmes coulent dans la foule.", {"rep": -3}, "Ta voix se brise."),
                 ("Un discours de force", ("st", "rep", 90), {"rep": 10}, "La foule scande ton nom.", {"rep": -3}, "On murmure.")]),
         ],
         fin=dict(eff={"cap": 5, "xpmin": 1000, "rep": 20, "flag": "kage"}, txt="👑 Tu deviens le {K} de {V} !"),
         ko_txt="Tu n'obtiens pas le titre de {K} cette fois."),
    dict(id="guerre", nom="La Grande Guerre ninja", u="Naruto", a=(22, 55), cond=lambda g: "guerre" not in _flags(g) and _nar_ok(g), p=.1, need=2,
         steps=[
             dict(t="Les villages forment une alliance face à une menace commune. Tu es mobilisé.", ch=[
                 ("Lancer des ponts diplomatiques", ("st", "rep", 50), {"alrel": 10, "rep": 5}, "Les alliances se resserrent.", {"alrel": -3}, "Les tensions subsistent."),
                 ("Rejoindre l'avant-garde", ("pw", 112), {"xp": 30, "rep": 8}, "Tu mènes l'assaut.", {"sante": -20}, "Tu es repoussé.")]),
             dict(t="Au cœur de la bataille, ton escouade est encerclée.", ch=[
                 ("Briser l'encerclement", ("pw", 140), {"xp": 40, "rep": 10}, "Tu ouvres la voie à tes frères d'armes.", {"sante": -30}, "Tu es gravement blessé."),
                 ("Tenir la position", .7, {"xp": 25, "karma": 4}, "Vous tenez jusqu'aux renforts.", {"sante": -15}, "La position tombe.")]),
             dict(t="L'ennemi tente un dernier assaut désespéré.", ch=[
                 ("Tout donner", ("pw", 168), {"xp": 50, "rep": 12}, "La guerre est gagnée.", {"sante": -30}, "Tu tombes au combat."),
                 ("Coordonner les villages", ("st", "intel", 80), {"xp": 40, "alrel": 8}, "Votre coordination est parfaite.", {"alrel": -4}, "La communication est rompue.")]),
         ],
         fin=dict(eff={"xp": 100, "rep": 25, "alrel": 15, "flag": "guerre"}, txt="🏆 Tu survis à la Grande Guerre : ton nom est gravé dans l'histoire.")),
    dict(id="mangekyo", nom="L'éveil du Mangekyō", u="Naruto", a=(13, 40),
         cond=lambda g: "Sharingan" in g["pupilles"] and "Mangekyō Sharingan" not in g["pupilles"] and g["clan"] == "Uchiwa", p=.12,
         steps=[dict(t="Tu perds un être cher sous tes yeux. Ton Sharingan palpite de douleur.", ch=[
             ("Laisser la douleur t'envahir", .85, {"pupille": "Mangekyō Sharingan", "bonheur": -25, "karma": -5, "mait": 6}, "Ton Sharingan évolue en Mangekyō !", {"bonheur": -20, "sante": -15}, "Ton regard se brouille : l'éveil échoue."),
             ("Étouffer ta peine", 1, {"karma": 3, "bonheur": -10}, "Tu gardes ton âme intacte, mais ton Sharingan reste inchangé.", {}, "")])],
         fin=dict(eff={}, txt="")),
    dict(id="rinnegan", nom="Un pouvoir ancien", u="Naruto", a=(30, 80),
         cond=lambda g: ("Mangekyō Sharingan" in g["pupilles"] or g["clan"] in ("Senju", "Uzumaki")) and "Rinnegan" not in g["pupilles"] and g["mait"] >= 75, p=.04,
         steps=[dict(t="Une lumière violette envahit tes pensées : un pouvoir ancien s'éveille.", ch=[
             ("Embrasser ce pouvoir", .7, {"pupille": "Rinnegan", "xp": 80, "rep": 10}, "Ton regard se pare de cercles concentriques : le Rinnegan !", {"sante": -30, "bonheur": -5}, "Le pouvoir te dépasse."),
             ("Le repousser", 1, {"karma": 3}, "Tu préfères rester toi-même.", {}, "")])],
         fin=dict(eff={}, txt="")),
    dict(id="sommet", nom="Sommet des cinq Kage", u="Naruto", a=(25, 70), cond=lambda g: g["cap"] >= 4 and _nar_ok(g), p=.1, need=1,
         steps=[dict(t="Tu es invité comme conseiller au sommet des cinq Kage. Une alliance est possible.", ch=[
             ("Proposer une alliance", ("st", "rep", 70), {"allie": "auto", "rep": 8}, "Un village accepte de s'allier à {V} !", {"rep": -3}, "Aucun accord n'est trouvé."),
             ("Soutenir la paix en coulisses", .8, {"karma": 5, "rep": 4}, "Tu apaises les tensions.", {}, "")])],
         fin=dict(eff={}, txt="")),
    # ─────────── KUROKO ───────────
    dict(id="lycee", nom="Choix du lycée", u="Kuroko", a=(15, 18), cond=lambda g: not g["lycee"], p=1,
         steps=[dict(t="Fin du collège : il faut choisir ton lycée. Chaque équipe a ses forces… et ses exigences.", ch=[
             (f"Viser le {n}", ("st", "mait", s), {"lycee": n, "rep": 3, "xp": 10}, f"Tu es admis au {n} !", {"lycee": "Lycée Seirin", "bonheur": -3}, f"Refusé… tu rejoins le Lycée Seirin, une équipe toute neuve.")
             for n, s in (("Lycée Seirin", 20), ("Lycée Kaijō", 45), ("Lycée Shūtoku", 50), ("Lycée Tōō", 50), ("Lycée Yōsen", 55), ("Lycée Rakuzan", 65))])],
         fin=dict(eff={}, txt="")),
    dict(id="interhigh", nom="L'Inter-High", u="Kuroko", a=(15, 18), cond=lambda g: bool(g["lycee"]) and g["mait"] >= 25, p=.35, man=True, rep=True,
         steps=[
             dict(t="🏀 Éliminatoires de Tokyo : ton équipe doit passer le premier tour.", ko="end", ch=[
                 ("Jouer collectif", ("pw", 88), {"xp": 15, "rep": 3}, "Vous passez sans trembler.", {"bonheur": -4}, "Vous êtes éliminés d'entrée."),
                 ("Prendre le jeu en main", ("pw", 80), {"xp": 18, "rep": 4}, "Tu portes l'équipe sur tes épaules.", {"sante": -5}, "Tu forces et tu rates.")]),
             dict(t="Quart de finale contre un lycée coriace.", ko="end", ch=[
                 ("Défense de fer", ("pw", 120), {"xp": 20, "rep": 4}, "Votre défense étouffe l'adversaire.", {"sante": -6}, "La défense cède."),
                 ("Attaque rapide", ("pw", 112), {"xp": 20, "rep": 4}, "Contre-attaque après contre-attaque !", {"bonheur": -4}, "Ils lisent votre jeu.")]),
             dict(t="Demi-finale face à l'un des Miracles : l'atmosphère est électrique.", ko="end", ch=[
                 ("Marquer le Miracle individuellement", ("pw", 152), {"xp": 25, "rep": 6}, "Tu arrêtes un prodige !", {"sante": -8}, "Il te dépasse comme si de rien n'était."),
                 ("Défendre en équipe", ("pw", 144), {"xp": 25, "rep": 6}, "L'équipe s'impose.", {"bonheur": -4}, "Le talent individuel fait la différence.")]),
             dict(t="La finale de l'Inter-High. La salle est comble.", ko="end", ch=[
                 ("Tenter le tir décisif", ("pw", 184), {"xp": 35, "rep": 10}, "Le buzzer sonne : ça rentre !", {"bonheur": -6}, "Le ballon tourne sur l'arceau… et sort."),
                 ("Faire confiance au jeu collectif", ("pw", 176), {"xp": 35, "rep": 10}, "Une passe magique offre la victoire.", {"bonheur": -6}, "Vous craquez dans les dernières secondes.")]),
         ],
         fin=dict(eff={"titre": "inter", "xp": 100, "rep": 15, "argent": 250}, txt="🏆 Ton lycée remporte l'Inter-High !"),
         ko_txt="Votre parcours à l'Inter-High s'arrête ici."),
    dict(id="wintercup", nom="La Winter Cup", u="Kuroko", a=(16, 18), cond=lambda g: bool(g["lycee"]) and g["mait"] >= 40, p=.3, man=True, rep=True,
         steps=[
             dict(t="❄️ Premier tour de la Winter Cup. Les meilleures équipes du pays sont là.", ko="end", ch=[
                 ("Imposer ton rythme", ("pw", 88), {"xp": 20, "rep": 4}, "Vous prenez rapidement le large.", {"bonheur": -4}, "Vous tombez de haut."),
                 ("Observer d'abord", ("st", "intel", 55), {"xp": 18, "intel": 2}, "Tu repères leurs failles.", {"bonheur": -3}, "Tu es trop passif.")]),
             dict(t="Quart de finale : un lycée au jeu hypnotique.", ko="end", ch=[
                 ("Briser leur rythme", ("pw", 115), {"xp": 25, "rep": 6}, "Ils perdent leurs repères.", {"sante": -6}, "Tu ne parviens pas à les arrêter."),
                 ("Jouer sur la vitesse", ("pw", 108), {"xp": 25, "rep": 6}, "Ils n'arrivent pas à suivre.", {"sante": -6}, "Ils s'adaptent.")]),
             dict(t="Demi-finale : un duel de légendes. La Zone est dans toutes les têtes.", ko="end", ch=[
                 ("Entrer dans la Zone", ("pw", 148), {"xp": 35, "rep": 8, "mait": 3}, "Tu t'embrases : plus rien ne t'arrête !", {"sante": -12, "bonheur": -4}, "La Zone se dérobe à toi."),
                 ("Faire confiance à l'équipe", ("pw", 142), {"xp": 35, "rep": 8}, "L'équipe franchit la barre.", {"bonheur": -5}, "La fatigue est trop forte.")]),
             dict(t="Finale de la Winter Cup contre Rakuzan et son capitaine invincible.", ko="end", ch=[
                 ("Tout tenter jusqu'au bout", ("pw", 182), {"xp": 50, "rep": 15}, "Vous renversez le match dans les ultimes secondes !", {"bonheur": -8}, "Un échec cruel à quelques secondes de la fin."),
                 ("Jouer ta carte maîtresse", ("pw", 176), {"xp": 50, "rep": 15}, "Ton talent fait basculer la finale !", {"bonheur": -8}, "Ils avaient anticipé.")]),
         ],
         fin=dict(eff={"titre": "winter", "xp": 150, "rep": 25, "argent": 400}, txt="🏆 Ton lycée remporte la Winter Cup !"),
         ko_txt="La Winter Cup s'arrête pour toi cette année."),
    dict(id="lastgame", nom="Le Dernier Match", u="Kuroko", a=(17, 26), cond=lambda g: (g["titres"].get("inter", 0) + g["titres"].get("winter", 0) >= 1 or g["rep"] >= 60) and "lastgame" not in _flags(g), p=.2, need=2,
         steps=[
             dict(t="Un match de rue contre les Jabberwock, une équipe américaine réputée sans pitié. Des légendes japonaises s'unissent.", ch=[
                 ("Rejoindre l'équipe japonaise", ("pw", 132), {"xp": 30, "rep": 10}, "Tu fais partie de la sélection !", {"bonheur": -4}, "Le coach ne te retient pas."),
                 ("Observer l'adversaire", ("st", "intel", 70), {"xp": 20, "intel": 3}, "Tu repères leur défaut.", {"bonheur": -3}, "Tu les sous-estimes.")]),
             dict(t="Au premier quart-temps, les Américains dominent physiquement.", ch=[
                 ("Tenir et attendre l'ouverture", ("pw", 144), {"xp": 35, "force": 3}, "Tu ne cèdes pas un pouce.", {"sante": -10}, "Tu es écrasé."),
                 ("Jouer la surprise", ("pw", 150), {"xp": 35, "mait": 3}, "Tes passes surgissent de nulle part.", {"sante": -6}, "Ils anticipent tout.")]),
             dict(t="Dernières minutes. Tout est possible.", ch=[
                 ("Prendre le tir de la victoire", ("pw", 168), {"xp": 50, "rep": 15}, "Le ballon traverse le filet !", {"bonheur": -6}, "Tu manques le tir de la victoire."),
                 ("Servir une passe décisive", ("pw", 162), {"xp": 50, "rep": 15}, "Ta passe offre la victoire.", {"bonheur": -4}, "La passe est interceptée.")]),
         ],
         fin=dict(eff={"xp": 100, "rep": 25, "flag": "lastgame"}, txt="🏆 Le Japon l'emporte ! Tu entres dans l'histoire du basket de rue.")),
    dict(id="nba", nom="Repéré par un recruteur NBA", u="Kuroko", a=(18, 24), cond=lambda g: not g["pro"] and g["mait"] >= 55 and g["rep"] >= 25, p=.5, man=True, rep=True,
         steps=[
             dict(t="🇺🇸 Un recruteur américain t'invite à un camp de détection aux États-Unis.", ko="end", ch=[
                 ("Partir seul aux USA", ("pw", 138), {"xp": 30, "rep": 5}, "Tu te fais remarquer d'emblée.", {"bonheur": -5}, "Le niveau est brutal : tu rentres."),
                 ("Y aller avec ton coach", ("pw", 125), {"xp": 25, "rep": 4}, "Son soutien t'aide à t'adapter.", {"argent": -100}, "Tu manques de repères.")]),
             dict(t="Match test face à des joueurs pro : les scouts prennent des notes.", ko="end", ch=[
                 ("Tout donner en attaque", ("pw", 169), {"xp": 40, "rep": 8}, "Tu plantes 30 points !", {"sante": -8}, "Tu forces ton jeu."),
                 ("Montrer ta polyvalence", ("pw", 156), {"xp": 40, "rep": 8}, "Les scouts notent ta lecture du jeu.", {"bonheur": -4}, "Tu passes inaperçu.")]),
             dict(t="Le jour de la Draft. Ton nom va-t-il être appelé ?", ko="end", ch=[
                 ("Croiser les doigts", ("st", "rep", 55), {"xp": 20}, "Ton nom est appelé !", {"bonheur": -8}, "Aucune équipe ne t'a sélectionné."),
                 ("Négocier avec ton agent", ("st", "intel", 60), {"xp": 20}, "Ton agent obtient un contrat solide.", {"bonheur": -5}, "Les offres sont insuffisantes.")]),
         ],
         fin=dict(eff={"pro": "auto", "xp": 80, "rep": 15, "argent": 400}, txt="🇺🇸 Tu signes un contrat NBA !"),
         ko_txt="Les portes de la NBA restent fermées pour l'instant."),
    # ─────────── TOKYO REVENGERS ───────────
    dict(id="recrutement", nom="Les gangs te remarquent", u="Tokyo Revengers", a=(12, 25), cond=lambda g: not g["gang"] and g["monde"] is not None, p=.6,
         steps=[dict(t="À la sortie du collège, des membres de plusieurs gangs te regardent. Il est temps de choisir ton camp.", ch=[
             ("Rejoindre les Moebius", ("pw", 25), {"gang": "Moebius", "rep": 5, "xp": 10}, "Les Moebius t'accueillent.", {"sante": -8, "bonheur": -3}, "Initiation ratée : on te rit au nez."),
             ("Rejoindre les Black Dragons", ("pw", 35), {"gang": "Black Dragons", "rep": 5, "xp": 10}, "Les Black Dragons te donnent leur veste.", {"sante": -10}, "Ils te jugent trop faible."),
             ("Rejoindre les Brahman", ("pw", 25), {"gang": "Brahman", "rep": 5, "xp": 10}, "Les Brahman t'adoptent.", {"sante": -8}, "Tu échoues à leur test."),
             ("Tenter ta chance chez les Toman", ("pw", 65), {"gang": "Toman", "rep": 10, "xp": 20}, "Mikey lui-même te serre la main.", {"sante": -12, "bonheur": -4}, "Les Toman te renvoient chez toi."),
             ("Rester indépendant", 1, {"intel": 2, "karma": 1}, "Tu gardes ta liberté.", {}, "")])],
         fin=dict(eff={}, txt="")),
    dict(id="christmas", nom="Christmas Showdown", u="Tokyo Revengers", a=(13, 19), cond=lambda g: bool(g["gang"]) and "christmas" not in _flags(g) and g["monde"] is not None, p=.4, need=2,
         steps=[
             dict(t="À la veille de Noël, ton gang défie les Black Dragons sur un terrain vague.", ch=[
                 ("Mener la première charge", ("pw", 76), {"xp": 15, "rep": 4}, "Tu ouvres la voie !", {"sante": -12}, "Tu es renversé dès le début."),
                 ("Observer leurs faiblesses", ("st", "intel", 50), {"xp": 12, "intel": 2}, "Tu repères leur chef.", {"bonheur": -2}, "Tu perds du temps.")]),
             dict(t="Le chef adverse te défie en combat singulier devant les deux gangs.", ch=[
                 ("Accepter", ("pw", 95), {"xp": 25, "rep": 8}, "Tu le fais plier !", {"sante": -18}, "Il te met à terre."),
                 ("Envoyer ton capitaine", .6, {"rep": 3, "xp": 10}, "Le capitaine règle la question.", {"rep": -3}, "On te taxe de lâche.")]),
             dict(t="L'issue de la bataille se joue à un souffle.", ch=[
                 ("Charge finale", ("pw", 104), {"xp": 25, "rep": 8}, "La victoire est à vous !", {"sante": -15}, "Vous battez en retraite."),
                 ("Tenir la position", .65, {"xp": 12, "karma": 3}, "Vous tenez jusqu'à l'aube.", {"sante": -10}, "La ligne cède.")]),
         ],
         fin=dict(eff={"xp": 60, "rep": 12, "flag": "christmas", "gfor": 5}, txt="🎄 Ton gang remporte le Christmas Showdown !")),
    dict(id="halloween", nom="Bloody Halloween", u="Tokyo Revengers", a=(14, 20), cond=lambda g: _gr(g) >= 1 and "halloween" not in _flags(g) and g["monde"] is not None, p=.4, need=2,
         steps=[
             dict(t="🎃 La veille du 31 octobre. Deux gangs rivaux ont rendez-vous au cimetière. Quelque chose cloche.", ch=[
                 ("Préparer un plan", ("st", "intel", 55), {"xp": 15, "intel": 2}, "Ton plan limite le chaos.", {"bonheur": -3}, "Tu n'as pas anticipé le piège."),
                 ("Réunir les troupes", .8, {"xp": 12, "rep": 4}, "Les membres répondent à l'appel.", {"rep": -2}, "Peu de gens se déplacent.")]),
             dict(t="La bataille éclate dans la nuit. Les coups pleuvent de tous côtés.", ch=[
                 ("Se battre en première ligne", ("pw", 112), {"xp": 30, "rep": 10}, "Tu renverses la situation !", {"sante": -22}, "Tu es submergé."),
                 ("Protéger les blessés", .7, {"karma": 6, "rep": 6}, "Tu sauves plusieurs camarades.", {"sante": -12}, "Tu es blessé en les protégeant.")]),
             dict(t="Au petit matin, un ami proche gît au sol, gravement atteint.", ch=[
                 ("Rester à ses côtés", .85, {"karma": 5, "bonheur": -10, "intel": 2}, "Tu veilles sur lui jusqu'aux secours.", {"bonheur": -18}, "Il te quitte dans tes bras."),
                 ("Poursuivre ceux qui ont fait ça", ("pw", 128), {"xp": 25, "rep": 10, "karma": -4}, "Tu leur fais payer.", {"sante": -20}, "Tu tombes dans une embuscade.")]),
         ],
         fin=dict(eff={"xp": 80, "rep": 15, "flag": "halloween", "gfor": 8}, txt="🎃 Tu survis à Bloody Halloween : un tournant pour ton gang.")),
    dict(id="rokuhara", nom="La guerre de Rokuhara Tandai", u="Tokyo Revengers", a=(15, 24), cond=lambda g: _gr(g) >= 2 and "rokuhara" not in _flags(g) and g["monde"] is not None, p=.35, need=2,
         steps=[
             dict(t="Les Rokuhara Tandai, venus du Kansai, exigent un tribut à ton gang. La guerre est inévitable.", ch=[
                 ("Refuser avec fierté", ("st", "rep", 40), {"rep": 8, "xp": 15}, "Ton gang vote la guerre.", {"rep": -3}, "Certains doutent de toi."),
                 ("Chercher des alliés", .7, {"alrel": 8, "xp": 10}, "Un gang voisin vous soutient.", {"alrel": -3}, "Personne ne répond.")]),
             dict(t="Les premiers affrontements éclatent aux quatre coins de la ville.", ch=[
                 ("Prendre un quartier d'assaut", ("pw", 128), {"xp": 30, "rep": 8}, "Tu l'emportes dans ce quartier.", {"sante": -18}, "Tu es repoussé."),
                 ("Tendre une embuscade", ("pw", 120), {"xp": 28, "intel": 2}, "L'ennemi tombe dans le piège.", {"sante": -12}, "L'embuscade échoue.")]),
             dict(t="Le chef de Rokuhara te défie en personne.", ch=[
                 ("Relever le défi", ("pw", 150), {"xp": 40, "rep": 12}, "Tu le terrasses : la guerre est gagnée.", {"sante": -25}, "Tu tombes à genoux."),
                 ("Négocier un cessez-le-feu", ("st", "intel", 65), {"xp": 25, "karma": 3}, "Un accord fragile est trouvé.", {"rep": -4}, "Il refuse tout compromis.")]),
         ],
         fin=dict(eff={"xp": 80, "rep": 15, "gfor": 10, "membres": 6, "flag": "rokuhara"}, txt="⚔️ Rokuhara recule : ton gang en sort grandi.")),
    dict(id="tenjiku", nom="L'arc Tenjiku", u="Tokyo Revengers", a=(16, 26), cond=lambda g: _gr(g) >= 3 and "tenjiku" not in _flags(g) and g["monde"] is not None, p=.35, need=2,
         steps=[
             dict(t="Tenjiku, un gang aussi brutal qu'organisé, tire les ficelles des quartiers voisins. Leurs chefs sont des légendes.", ch=[
                 ("Rassembler tes capitaines", ("st", "rep", 55), {"xp": 20, "rep": 6}, "Toute la division répond présent.", {"rep": -3}, "Tes capitaines hésitent."),
                 ("Infiltrer leur QG", ("pw", 126), {"xp": 25, "intel": 3}, "Tu recueilles des informations précieuses.", {"sante": -15}, "Tu es capturé.")]),
             dict(t="Le choc a lieu sous un pont désert. Les Haitani et Mochizuki bloquent la route.", ch=[
                 ("Attaquer le front", ("pw", 147), {"xp": 40, "rep": 10}, "Tu fais céder leur ligne.", {"sante": -25}, "Tu es écrasé."),
                 ("Briser leur formation", ("st", "intel", 70), {"xp": 35, "rep": 8}, "Ta tactique les désorganise.", {"sante": -12}, "Ils déjouent ton plan.")]),
             dict(t="Face au chef de Tenjiku, tout peut basculer.", ch=[
                 ("Un duel sans merci", ("pw", 182), {"xp": 55, "rep": 15}, "Tu l'emportes de justesse !", {"sante": -30}, "Tu es vaincu."),
                 ("Utiliser le terrain", ("st", "intel", 80), {"xp": 45, "rep": 12}, "Tu retournes la situation.", {"sante": -15}, "Le terrain te trahit.")]),
         ],
         fin=dict(eff={"xp": 100, "rep": 20, "gfor": 15, "terr": 1, "flag": "tenjiku"}, txt="🔥 Tenjiku s'incline : ton gang gagne un territoire !")),
    dict(id="kanto", nom="La guerre du Kantō", u="Tokyo Revengers", a=(17, 32), cond=lambda g: _gr(g) >= 3 and "kanto" not in _flags(g) and g["monde"] is not None, p=.3, need=2,
         steps=[
             dict(t="Un stratège manipule les gangs du Kantō pour les dresser les uns contre les autres.", ch=[
                 ("Démasquer le manipulateur", ("st", "intel", 70), {"xp": 25, "intel": 3}, "Tu découvres sa trame.", {"bonheur": -4}, "Tu tombes dans son piège."),
                 ("Appeler les gangs à l'unité", ("st", "rep", 65), {"rep": 8, "alrel": 8}, "Plusieurs gangs te suivent.", {"rep": -3}, "On te traite de naïf.")]),
             dict(t="L'affrontement général éclate : des centaines de membres se font face.", ch=[
                 ("Mener la première ligne", ("pw", 155), {"xp": 40, "rep": 12}, "Ta charge inspire tous les tiens.", {"sante": -28}, "Tu es submergé."),
                 ("Tenir les arrières", ("pw", 135), {"xp": 30, "karma": 4}, "Tu protèges les tiens.", {"sante": -15}, "La ligne rompt.")]),
             dict(t="Le stratège se dévoile enfin.", ch=[
                 ("Le défier en face à face", ("pw", 169), {"xp": 50, "rep": 15}, "Tu mets fin à son règne.", {"sante": -30}, "Il t'écrase."),
                 ("Le piéger", ("st", "intel", 85), {"xp": 45, "rep": 12}, "Il tombe dans ton filet.", {"sante": -12}, "Il te devance.")]),
         ],
         fin=dict(eff={"xp": 100, "rep": 25, "terr": 1, "flag": "kanto"}, txt="🗾 La guerre du Kantō est tienne : un nouveau quartier rejoint ton gang.")),
    dict(id="divinites", nom="La guerre des Trois Divinités", u="Tokyo Revengers", a=(18, 40), cond=lambda g: nterr(g) >= 3 and "divinites" not in _flags(g) and g["monde"] is not None, p=.3, need=2,
         steps=[
             dict(t="Trois puissantes coalitions se disputent Shibuya, Shinjuku et Ikebukuro. La paix est un souvenir.", ch=[
                 ("Choisir une coalition", ("st", "rep", 70), {"rep": 8, "xp": 20}, "Ta coalition te suit.", {"rep": -3}, "Les coalitions se méfient."),
                 ("Rester neutre et armer ton gang", .7, {"gfor": 5, "membres": 4}, "Ton gang se prépare.", {"rep": -3}, "On te prend pour un lâche.")]),
             dict(t="Une bataille décisive embrase les trois quartiers.", ch=[
                 ("Frapper au centre", ("pw", 182), {"xp": 50, "rep": 15}, "Tu brises leur ligne.", {"sante": -30}, "Tu es repoussé."),
                 ("Isoler un chef", ("st", "intel", 85), {"xp": 40, "rep": 10}, "Tu élimines le stratège.", {"sante": -15}, "Ton plan échoue.")]),
             dict(t="Le dernier combat décide du sort de la ville.", ch=[
                 ("Tout donner", ("pw", 210), {"xp": 60, "rep": 20}, "La ville est à toi.", {"sante": -35}, "Tu tombes avec les honneurs."),
                 ("Imposer la paix", ("st", "rep", 85), {"xp": 50, "karma": 6}, "Les chefs s'inclinent.", {"rep": -4}, "Personne ne te suit.")]),
         ],
         fin=dict(eff={"xp": 120, "rep": 30, "terr": 1, "flag": "divinites"}, txt="👑 Les Trois Divinités s'effacent : tu règnes sur la ville.")),
]
ARC_BY_ID = {a["id"]: a for a in ARCS}

# ═════════════ Techniques liées au talent / au style / au clan ═════════════
STYLES = ["Karatéka", "Boxeur", "Lutteur", "Kickboxeur", "Bagarreur de rue"]
TECH_TAL = {"passe": ["fantome", "passe"], "trois": ["tir", "copie", "empereur"], "dribble": ["freestyle", "bestial", "copie"],
            "meteore": ["rebond", "bestial", "viking", "freestyle"], "vanish": ["fantome"], "ignite": ["passe", "fantome", "copie", "empereur"]}
TECH_STY = {"kick": ["Kickboxeur", "Karatéka"], "contre": ["Boxeur", "Karatéka", "Lutteur"], "charge": ["Lutteur", "Bagarreur de rue"],
            "heavy": ["Lutteur", "Bagarreur de rue", "Boxeur"], "kick2": ["Kickboxeur", "Karatéka"]}
for _k, _v in TECH_TAL.items(): TECH[_k]["tal"] = _v
for _k, _v in TECH_STY.items(): TECH[_k]["sty"] = _v
TECH["sage"]["req"] = ("any", [("clan", "Senju"), ("clan", "Uzumaki"), ("flag", "biju")])
TECH["sage"]["mait_min"] = 70

# ═════════════ Organisations (maître / escouade) : bonus annuels ═════════════
ORGS = {
    "escouade": dict(nom="Escouade ninja", pw=8, xp=8, rep=1),
    "ermite": dict(nom="Disciple d'un ermite", pw=6, xp=5, mait=2),
    "taijutsu": dict(nom="Élève de taijutsu", pw=5, force=2, mait=1),
    "medic": dict(nom="Apprenti médecin", pw=4, sante=6, xp=3),
    "street": dict(nom="Équipe de street basket", pw=8, xp=6, rep=1),
    "senpai": dict(nom="Protégé d'un ancien", pw=6, xp=5, force=1),
    "yakuza": dict(nom="Protégé des yakuza", pw=10, argent=80, karma=-3, rep=1),
}

# ═════════════ Carte : lieux à explorer (1 action) ═════════════
LIEUX = {
    "Naruto": [("academie", "🏫", "Académie ninja"), ("terrain", "🥋", "Terrain d'entraînement"), ("marche", "🏮", "Marché du village"),
               ("foret", "🌲", "Forêt environnante"), ("porte", "⛩️", "Porte du village"), ("ramen", "🍜", "Stand de ramen")],
    "Kuroko": [("gymnase", "🏀", "Gymnase du lycée"), ("rue", "🏙️", "Terrain de rue"), ("ecole", "🏫", "Salle de classe"),
               ("salle", "🏋️", "Salle de musculation"), ("konbini", "🏪", "Konbini"), ("stade", "🏟️", "Grand stade")],
    "Tokyo Revengers": [("temple", "⛩️", "Temple Musashi"), ("vague", "🏚️", "Terrain vague"), ("konbini", "🏪", "Konbini"),
                        ("dojo", "🥋", "Dojo du quartier"), ("shibuya", "🌃", "Rues de Shibuya"), ("bar", "🍶", "Bar de nuit")],
}
TROUVAILLES = [("Tu trouves une bourse oubliée.", {"argent": 60}), ("Un passant te donne un bon conseil.", {"intel": 2, "xp": 5}),
               ("Tu aides un enfant perdu, on te remercie.", {"karma": 3, "bonheur": 3}), ("Une petite brise te fait du bien.", {"bonheur": 4}),
               ("Tu t'entraînes un peu en chemin.", {"force": 1, "mait": 1})]

# ═════════════ Rencontres : PNJ (kind : recruteur / rival / ami / marchand) ═════════════
def _E(id, u, nom, ico, titre, kind, niv, lieux, amin, cond, intro, talk, offre="", org=None):
    return dict(id=id, u=u, nom=nom, ico=ico, titre=titre, kind=kind, niv=niv, lieux=lieux, amin=amin, cond=cond, intro=intro, talk=talk, offre=offre, org=org)

ENC = [
    # ───── Naruto ─────
    _E("kakashi", "Naruto", "Kakashi", "🎭", "Jōnin de Konoha", "recruteur", 1.5, ["terrain", "porte", "foret"], 12,
       lambda g: g["village"] == "Konoha" and not g["patron"] and not g["akatsuki"],
       "« Yo. Je te regardais t'entraîner depuis un moment. »", ["« Le travail d'équipe passe avant tout. »", "« Ceux qui trahissent les règles sont des déchets… mais ceux qui trahissent leurs amis sont pires. »", "« Tu as du potentiel, mais il faut le canaliser. »"],
       "« Je forme une escouade. Ça te dirait d'en faire partie ? »", "escouade"),
    _E("jonin_gen", "Naruto", "Maître Raiko", "🥷", "Jōnin du village", "recruteur", 1.4, ["terrain", "porte", "foret"], 12,
       lambda g: g["village"] != "Konoha" and not g["patron"] and not g["akatsuki"],
       "« Un nouveau visage prometteur… Montre-moi ce que tu vaux. »", ["« Un ninja sans discipline est un danger pour tous. »", "« Le village a besoin de gens comme toi. »"],
       "« Rejoins mon escouade : tu progresseras vite. »", "escouade"),
    _E("jiraiya", "Naruto", "Jiraiya", "🐸", "Ermite des crapauds", "recruteur", 1.9, ["foret", "marche", "ramen"], 12,
       lambda g: g["rep"] >= 15 and not g["patron"] and not g["akatsuki"],
       "« Hé hé ! Un ermite voyage toujours léger… et cherche des élèves. »", ["« Un bon ninja sait aussi écrire un bon roman, tu sais. »", "« Le chakra naturel est une affaire de patience. »"],
       "« Tu m'as l'air d'avoir du talent. Veux-tu devenir mon disciple ? »", "ermite"),
    _E("guy", "Naruto", "Might Guy", "💪", "Maître de taijutsu", "recruteur", 1.6, ["terrain", "academie"], 10,
       lambda g: not g["patron"] and not g["akatsuki"],
       "« La flamme de la jeunesse brûle en toi ! Cent tours du village sur les mains ! »", ["« Le travail acharné bat le talent ! »", "« Un vrai ninja n'abandonne jamais. »"],
       "« Deviens mon élève : ensemble, nous repousserons les limites ! »", "taijutsu"),
    _E("tsunade", "Naruto", "Tsunade", "💚", "Légende médicale", "recruteur", 1.7, ["marche", "academie"], 14,
       lambda g: g["intel"] >= 45 and not g["patron"] and not g["akatsuki"],
       "« Une apprentie… ou un apprenti ? Voyons si tu as les nerfs solides. »", ["« Soigner, c'est affronter la mort à mains nues. »"],
       "« Je cherche un élève pour apprendre la médecine ninja. Tu viens ? »", "medic"),
    _E("anbu_rec", "Naruto", "Homme masqué", "🎭", "Recruteur de l'ANBU", "recruteur", 1.8, ["porte", "foret"], 18,
       lambda g: g["cap"] >= 3 and "anbu" not in g["flags"] and not g["akatsuki"],
       "« Ton dossier est remarquable. L'ANBU t'observe depuis longtemps. »", ["« Les ombres servent le village sans jamais recevoir de gloire. »"],
       "« Acceptes-tu de passer l'épreuve du masque ? »", "anbu"),
    _E("itachi", "Naruto", "Itachi", "🌑", "Émissaire en manteau noir", "recruteur", 2.0, ["foret", "porte"], 16,
       lambda g: g["karma"] <= -20 and not g["akatsuki"],
       "« Ton regard a quelque chose de sombre. L'Akatsuki pourrait t'offrir un but. »", ["« Les liens ne sont que des chaînes. »", "« Le monde ne change que par la force. »"],
       "« Rejoins l'Akatsuki. Ton village ne te comprendra jamais comme nous. »", "akatsuki"),
    _E("lee", "Naruto", "Rock Lee", "🥋", "Prodige du travail", "rival", 1.1, ["terrain", "academie"], 8, lambda g: True,
       "« Je te défie ! Même sans talent, je te battrai à force de travail ! »", ["« Mon rêve : devenir un grand ninja sans jutsu ! »"]),
    _E("gaara", "Naruto", "Gaara", "🏜️", "Enfant du sable", "rival", 1.7, ["porte", "foret"], 14, lambda g: True,
       "« Tu me sembles fort. Prouve-le. »", ["« Je me bats pour exister. »"]),
    _E("choji", "Naruto", "Chōji", "🍖", "Gourmand fidèle", "ami", .8, ["ramen", "marche"], 8, lambda g: True,
       "« Hé ! Tu veux partager mes chips ? »", ["« Un vrai ami ne te laisse jamais tomber. »", "« On ne combat bien que le ventre plein ! »"]),
    _E("marchand_n", "Naruto", "Marchand ambulant", "🛒", "Vendeur de matériel ninja", "marchand", 1.0, ["marche", "porte", "ramen"], 8, lambda g: True,
       "« Kunai, parchemins, pilules ! Tout à prix d'ami ! »", ["« Mes affaires sont des affaires sûres. »"]),
    # ───── Kuroko ─────
    _E("akashi", "Kuroko", "Seijūrō Akashi", "🔴", "Capitaine de Rakuzan", "recruteur", 1.8, ["gymnase", "stade"], 13,
       lambda g: not g["recrue"], "« Je gagne toujours. Voyons si tu as de l'intérêt. »", ["« Tout ce que je fais est juste. »", "« Les faibles n'ont pas leur place sur le terrain. »"],
       "« Rejoins-moi à Rakuzan. Je t'ai trouvé… digne. »", "gm:Akashi"),
    _E("aomine", "Kuroko", "Daiki Aomine", "🔵", "As de Tōō", "recruteur", 1.7, ["rue", "gymnase"], 13,
       lambda g: not g["recrue"], "« Hé, toi ! Un 1 contre 1 ? Je m'ennuie… »", ["« Seul moi peux me battre. »", "« Le basket, c'est du talent pur. »"],
       "« Tu m'amuses. Viens à Tōō, on s'éclatera. »", "gm:Aomine"),
    _E("murasakibara", "Kuroko", "Atsushi Murasakibara", "🟣", "Géant de Yōsen", "recruteur", 1.6, ["konbini", "gymnase"], 13,
       lambda g: not g["recrue"], "« Mmh… t'as des snacks ? Sinon, c'est pénible de jouer. »", ["« J'aime pas trop le basket, mais je gagne. »"],
       "« Viens à Yōsen… si t'es pas trop ennuyeux. »", "gm:Murasakibara"),
    _E("midorima", "Kuroko", "Shintarō Midorima", "🟢", "Tireur de Shūtoku", "recruteur", 1.5, ["gymnase", "ecole"], 13,
       lambda g: not g["recrue"], "« Le Cancer est classé premier aujourd'hui. Mon objet porte-bonheur t'ignore pourtant. »", ["« Je fais toujours tout ce qu'il faut pour réussir. »"],
       "« Tu es utile. Shūtoku te prendrait. Ce n'est pas que je m'en soucie… »", "gm:Midorima"),
    _E("kise", "Kuroko", "Ryōta Kise", "🟡", "Mannequin-basketteur de Kaijō", "recruteur", 1.4, ["rue", "konbini", "gymnase"], 13,
       lambda g: not g["recrue"], "« Waouh ! J'ai envie de te copier tout de suite ! »", ["« Je peux imiter n'importe qui, même toi ! »", "« Hé, on fait une photo ? »"],
       "« Viens à Kaijō ! On va s'éclater. »", "gm:Kise"),
    _E("kagami", "Kuroko", "Taiga Kagami", "🔥", "Ace de Seirin", "rival", 1.5, ["rue", "gymnase"], 14, lambda g: True,
       "« Hé ! T'as un bon regard. Un 1 contre 1 ? »", ["« Je deviendrai le meilleur du Japon. »", "« Un seul panier, le dernier. »"]),
    _E("kuroko_t", "Kuroko", "Tetsuya Kuroko", "👻", "Sixième homme fantôme", "ami", 1.2, ["gymnase", "konbini"], 13, lambda g: True,
       "« …Je suis là depuis tout à l'heure. »", ["« Je suis l'ombre de mon équipe. »", "« Les passes sont un langage. »"]),
    _E("himuro", "Kuroko", "Tatsuya Himuro", "❄️", "Frère de cœur de Kagami", "rival", 1.5, ["rue", "stade"], 15, lambda g: True,
       "« On s'est déjà croisés ? Moi, je suis Himuro. Je joue à Yōsen. »", ["« Le talent ne sert à rien sans travail. »"]),
    _E("hanamiya", "Kuroko", "Makoto Hanamiya", "😈", "Capitaine de Kirisaki Daiichi", "rival", 1.3, ["stade", "rue"], 15, lambda g: True,
       "« Haha. Un joli petit joueur… qui pourrait se faire casser. »", ["« Gagner par n'importe quel moyen, c'est gagner. »"]),
    _E("riko", "Kuroko", "Riko Aida", "📋", "Coach de Seirin", "recruteur", 1.0, ["gymnase", "salle", "ecole"], 13,
       lambda g: not g["lycee"] and not g["recrue"], "« Ouvre les yeux : tu as des chiffres de joueur prometteur ! »", ["« Mange bien, dors bien, entraîne-toi bien. »"],
       "« Seirin cherche des joueurs. Tu veux faire partie de l'équipe ? »", "seirin"),
    _E("scout_nba", "Kuroko", "Alex Garcia", "🇺🇸", "Recruteuse américaine", "recruteur", 1.6, ["stade", "salle"], 18,
       lambda g: not g["pro"] and g["mait"] >= 55 and g["rep"] >= 25, "« Cute. J'ai vu ton jeu. L'Amérique t'attend. »", ["« Ici, tout est plus grand et plus dur. »"],
       "« Je t'invite à un camp de détection. Tu viens ? »", "nba"),
    _E("street_cap", "Kuroko", "Capitaine du Strky", "🏙️", "Équipe de street basket", "recruteur", 1.3, ["rue"], 14,
       lambda g: not g["patron"], "« Hé, toi ! Un street ball, ça te dit ? On cherche du monde. »", ["« Le basket de rue, c'est la vraie liberté. »"],
       "« Rejoins notre équipe de rue. On gagne les tournois. »", "street"),
    _E("marchand_k", "Kuroko", "Vendeur de matériel", "🛒", "Boutique de sport", "marchand", 1.0, ["konbini", "salle"], 8, lambda g: True,
       "« Chaussures, ballons, bandages : tout y est ! »", ["« Les bonnes chaussures changent un match. »"]),
    # ───── Tokyo Revengers ─────
    _E("mikey", "Tokyo Revengers", "Mikey", "🏍️", "Chef de la Toman", "recruteur", 1.9, ["temple", "vague", "shibuya"], 13,
       lambda g: not g["gang"], "« T'as du cran, toi. J'aime bien ça. »", ["« Un gang, c'est une famille. »", "« Je veux un monde où personne n'est seul. »"],
       "« Rejoins la Toman. Je te présenterai les gars. »", "gang:Toman"),
    _E("draken", "Tokyo Revengers", "Draken", "🐉", "Vice-capitaine de la Toman", "recruteur", 1.5, ["temple", "konbini", "shibuya"], 13,
       lambda g: not g["gang"], "« Tu cherches la bagarre ou un camp ? »", ["« Un homme ne fuit pas. »", "« La loyauté, c'est ce qui compte. »"],
       "« Si t'es sérieux, je te présente à Mikey. »", "gang:Toman"),
    _E("kakucho", "Tokyo Revengers", "Kakucho", "🦅", "Lieutenant de Tenjiku", "recruteur", 1.6, ["bar", "shibuya"], 15,
       lambda g: not g["gang"], "« Tenjiku accueille ceux qui ont du poids. As-tu du poids ? »", ["« La famille avant tout. »"],
       "« Rejoins Tenjiku. On a besoin de gens comme toi. »", "gang:Tenjiku"),
    _E("baji", "Tokyo Revengers", "Baji", "😼", "Combattant de Valhalla", "recruteur", 1.4, ["vague", "dojo", "shibuya"], 13,
       lambda g: not g["gang"], "« Hé ! T'as l'air d'un type qui aime la baston ! »", ["« Un coup de poing vaut mille mots. »"],
       "« Viens chez Valhalla. Ça va chauffer ! »", "gang:Valhalla"),
    _E("hanma", "Tokyo Revengers", "Hanma", "🎯", "Cadre des Kantō Manji", "recruteur", 1.6, ["bar", "shibuya"], 15,
       lambda g: not g["gang"], "« Ça sent le talent brut. Je me trompe rarement. »", ["« La vie est trop courte pour être sage. »"],
       "« Kantō Manji aurait besoin de toi. Intéressé ? »", "gang:Kantō Manji"),
    _E("takemichi", "Tokyo Revengers", "Takemichi", "😭", "Héros qui pleure", "ami", .9, ["temple", "konbini", "vague"], 12, lambda g: True,
       "« Euh… salut ! J'ai pas peur, hein ! (Il tremble.) »", ["« Je protégerai mes amis, quoi qu'il arrive ! »", "« Je suis nul, mais j'abandonne jamais ! »"]),
    _E("kisaki", "Tokyo Revengers", "Kisaki", "🕶️", "Stratège cynique", "rival", 1.4, ["bar", "shibuya"], 15, lambda g: True,
       "« Les gens sont des pions. Es-tu un pion ou un joueur ? »", ["« Tout est question de plan. »"]),
    _E("senpai_tr", "Tokyo Revengers", "Un ancien du quartier", "🚬", "Vétéran des bagarres", "recruteur", 1.3, ["bar", "vague", "dojo"], 12,
       lambda g: not g["patron"], "« Gamin, t'as des yeux de bagarreur. Viens là. »", ["« La rue enseigne ce que l'école ne sait pas. »"],
       "« Je te prends sous mon aile. Écoute-moi et tu iras loin. »", "senpai"),
    _E("yakuza", "Tokyo Revengers", "Un yakuza en costume", "🕴️", "Intermédiaire discret", "recruteur", 1.7, ["bar", "shibuya"], 16,
       lambda g: not g["patron"] and g["karma"] <= 10, "« Mon patron aime les jeunes qui ont de l'ambition. »", ["« L'argent règle tout. »"],
       "« Travaille pour nous : tu auras de l'argent et de la protection. »", "yakuza"),
    _E("marchand_t", "Tokyo Revengers", "Vendeur de rue", "🛒", "Étal sous les néons", "marchand", 1.0, ["konbini", "shibuya", "bar"], 8, lambda g: True,
       "« Pas cher, pas cher ! Du bon matos ! »", ["« Tout s'achète, mon ami. »"]),
]
ENC_BY_ID = {e["id"]: e for e in ENC}

# ═════════════ Événements propres à chaque univers (format EV) ═════════════
EV_EXTRA = [
    # Naruto
    ("Naruto", 13, 45, "🏴‍☠️ Des brigands attaquent une caravane marchande à la sortie du village.",
     [("Intervenir seul", .55, {"xp": 25, "rep": 8, "argent": 80}, "Tu mets les brigands en fuite.", {"sante": -18, "rep": -3}, "Tu es débordé et blessé."),
      ("Alerter la patrouille", .9, {"rep": 3, "xp": 8}, "Les renforts arrivent à temps.", {"rep": -1}, "Tu arrives trop tard."),
      ("Détourner le regard", 1, {"karma": -3}, "Tu fais comme si de rien n'était.", {}, "")]),
    ("Naruto", 15, 50, "🦠 Une épidémie se répand dans le village. Les médecins sont débordés.",
     [("Aider les médecins", .8, {"karma": 6, "rep": 5, "xp": 10}, "Ton aide sauve des vies.", {"sante": -15}, "Tu tombes malade à ton tour."),
      ("Préparer un remède", ("st", "intel", 60), {"rep": 8, "xp": 15, "intel": 2}, "Ton remède fait ses preuves !", {"bonheur": -4}, "Ton remède est inefficace."),
      ("T'isoler", 1, {"karma": -2}, "Tu te protèges avant tout.", {}, "")]),
    ("Naruto", 14, 40, "🏃 Un déserteur de ton village est repéré près de la frontière.",
     [("Le traquer", ("pw", 120), {"xp": 30, "rep": 10}, "Tu le ramènes enchaîné.", {"sante": -20, "rep": -3}, "Il te piège et s'enfuit."),
      ("Le laisser fuir", 1, {"karma": 4}, "Tu fermes les yeux, il disparaît dans la nuit.", {}, "")]),
    ("Naruto", 12, 35, "🏆 Un daimyō organise un tournoi de ninjas : la récompense est généreuse.",
     [("S'inscrire", ("pw", 90), {"argent": 300, "rep": 10, "xp": 30}, "Tu remportes le tournoi !", {"sante": -12, "rep": -2}, "Tu es éliminé en demi-finale."),
      ("Regarder", 1, {"intel": 2, "bonheur": 2}, "Tu observes les styles de combat.", {}, "")]),
    ("Naruto", 16, 50, "📜 Tu reçois une lettre d'un village étranger : une offre mystérieuse.",
     [("La montrer à ton Kage", .95, {"rep": 8, "karma": 4}, "Ton village apprécie ta loyauté.", {}, ""),
      ("La brûler", 1, {}, "Personne ne saura.", {}, "")]),
    ("Naruto", 18, 60, "🗿 Un sceau ancien se brise dans une grotte voisine : une aura inquiétante s'en échappe.",
     [("Enquêter", ("pw", 140), {"xp": 40, "rep": 10, "chakra": 4}, "Tu refermes le sceau à temps.", {"sante": -25}, "Une force te rejette violemment."),
      ("Prévenir les anciens", .95, {"rep": 5}, "Les anciens envoient une équipe.", {}, "")]),
    # Kuroko
    ("Kuroko", 13, 40, "🩹 Un coéquipier se blesse gravement à l'entraînement.",
     [("Rester à ses côtés", 1, {"karma": 4, "bonheur": -3}, "Tu l'accompagnes à l'hôpital.", {}, ""),
      ("Prendre sa place", .7, {"rep": 6, "mait": 3}, "Tu saisis ta chance de titulaire.", {"bonheur": -4}, "La pression te pèse.")]),
    ("Kuroko", 14, 40, "😬 On te propose de truquer un match en échange d'argent.",
     [("Refuser net", 1, {"karma": 6, "rep": 3}, "Tu gardes ton intégrité.", {}, ""),
      ("Accepter", .5, {"argent": 400, "karma": -15}, "Tu empoches l'argent en silence.", {"rep": -15, "karma": -15}, "Le scandale éclate : réputation en miettes.")]),
    ("Kuroko", 15, 40, "😔 Défaite humiliante en public : les gradins se moquent.",
     [("Redoubler d'efforts", .8, {"mait": 4, "force": 2}, "Tu en sors plus fort.", {"bonheur": -6}, "Tu doutes de toi."),
      ("Quitter le terrain", 1, {"bonheur": -4}, "Tu rentres seul.", {}, "")]),
    ("Kuroko", 15, 40, "🏫 Ton lycée menace de supprimer le club de basket faute de résultats.",
     [("Lancer une campagne", ("st", "rep", 50), {"rep": 8, "karma": 3}, "Tout le lycée te soutient !", {"rep": -3}, "Personne ne se mobilise."),
      ("Gagner un match amical", ("pw", 90), {"xp": 20, "rep": 6}, "Une victoire sauve le club.", {"bonheur": -5}, "Le club ferme.")]),
    ("Kuroko", 15, 19, "🇯🇵 La sélection nationale des moins de 19 ans organise un camp.",
     [("Y participer", ("pw", 100), {"xp": 35, "rep": 10, "mait": 4}, "Tu impressionnes les sélectionneurs.", {"bonheur": -3}, "Le niveau est trop élevé."),
      ("Passer son tour", 1, {}, "Tu préfères te reposer.", {}, "")]),
    # Tokyo Revengers
    ("Tokyo Revengers", 13, 40, "🚓 Un membre de ton gang se fait arrêter : la police pose des questions.",
     [("Payer sa caution (150)", 1, {"argent": -150, "karma": 3, "rep": 4}, "Il sort et te doit une fière chandelle.", {}, ""),
      ("Ne rien dire", 1, {"rep": -4}, "Il est abandonné à son sort.", {}, "")], "gang"),
    ("Tokyo Revengers", 14, 40, "🔥 Un incendie ravage le QG de ton gang.",
     [("Sauver les membres", .7, {"karma": 5, "rep": 6, "sante": -10}, "Tu sors tout le monde à temps.", {"sante": -25, "membres": -2}, "Tu es blessé et perds des hommes."),
      ("Sauver le butin", .6, {"argent": 200, "karma": -4}, "Tu sauves la caisse.", {"sante": -15, "rep": -4}, "Tu perds la caisse et ta réputation.")], "gang"),
    ("Tokyo Revengers", 14, 35, "🎪 Une bagarre éclate pendant un festival : des civils sont en danger.",
     [("Protéger les civils", .65, {"karma": 6, "rep": 8, "xp": 15}, "On t'acclame.", {"sante": -18, "rep": -2}, "Tu prends des coups pour rien."),
      ("Rester dans la bagarre", .6, {"xp": 20, "rep": 6, "karma": -4}, "Tu cognes sans compter.", {"sante": -20}, "Tu te fais cueillir.")]),
    ("Tokyo Revengers", 15, 40, "🕵️ Un journaliste enquête sur les gangs du quartier.",
     [("Le renseigner", .6, {"rep": 6, "argent": 100, "karma": -2}, "Tu deviens une source.", {"rep": -6}, "Il te dénonce."),
      ("Le menacer", .5, {"karma": -6, "rep": 3}, "Il abandonne son article.", {"rep": -8, "karma": -6}, "Il appelle la police.")]),
    ("Tokyo Revengers", 14, 40, "🕴️ Un yakuza réclame un tribut aux commerçants de ton quartier.",
     [("Protéger les commerçants", ("pw", 110), {"karma": 8, "rep": 10, "xp": 25}, "Le yakuza recule, sidéré.", {"sante": -22, "rep": -3}, "Les hommes du yakuza te corrigent."),
      ("Payer le tribut", 1, {"argent": -150, "karma": -2}, "Tu achètes la paix.", {}, "")]),
    ("Tokyo Revengers", 15, 40, "😡 Un membre ambitieux de ton gang conteste ton rang.",
     [("L'affronter", ("pw", 90), {"rep": 10, "xp": 25}, "Tu as réglé le problème.", {"sante": -15, "rep": -5}, "Tu perds la face."),
      ("Discuter", .7, {"karma": 3, "rep": 3}, "Vous trouvez un terrain d'entente.", {"bonheur": -3}, "Il garde rancune.")], "gang"),
]

# ═════════════ Arcs supplémentaires ═════════════
ARCS_EXTRA = [
    dict(id="akat_raid", nom="Attaque de l'Akatsuki sur {V}", u="Naruto", a=(16, 55), cond=lambda g: _nar_ok(g) and "akat_raid" not in _flags(g), p=.09, need=2,
         steps=[
             dict(t="🌑 Deux silhouettes en manteau noir à nuages rouges franchissent les défenses de {V}. Les cloches d'alarme résonnent.", ch=[
                 ("Alerter tout le village", ("st", "rep", 50), {"xp": 15, "rep": 6}, "Le village se mobilise grâce à toi.", {"rep": -2}, "Personne ne te croit à temps."),
                 ("Les intercepter à l'entrée", ("pw", 140), {"xp": 25, "rep": 8}, "Tu retardes leur avancée.", {"sante": -20}, "Ils te balayent d'un geste.")]),
             dict(t="Ils sont en quête d'un jinchūriki. Le combat gronde au cœur du village.", ch=[
                 ("Affronter le plus faible", ("pw", 160), {"xp": 35, "rep": 10}, "Tu le blesses : il recule.", {"sante": -28}, "Tu es gravement touché."),
                 ("Évacuer les civils", .75, {"karma": 6, "rep": 8}, "Tu sauves des dizaines de vies.", {"sante": -10}, "Tu ne peux pas tous les sauver.")]),
             dict(t="Les ninjas d'élite arrivent. L'ennemi bat en retraite, mais le village est ravagé.", ch=[
                 ("Organiser les secours", ("st", "intel", 65), {"rep": 8, "xp": 20}, "Tu coordonnes la reconstruction.", {"bonheur": -4}, "Le chaos règne."),
                 ("Poursuivre les agresseurs", ("pw", 170), {"xp": 40, "rep": 12}, "Tu les harcèles jusqu'à la frontière.", {"sante": -25}, "Tu tombes dans une embuscade.")]),
         ],
         fin=dict(eff={"xp": 100, "rep": 20, "flag": "akat_raid"}, txt="🛡️ Tu as repoussé l'Akatsuki : {V} te doit beaucoup.")),
    dict(id="raid_rival", nom="Attaque d'un village rival", u="Naruto", a=(14, 50), cond=lambda g: _nar_ok(g), p=.08, rep=True, need=2,
         steps=[
             dict(t="⚔️ Un village rival lance une attaque sur {V}. Des ninjas ennemis franchissent la frontière.", ch=[
                 ("Tenir la frontière", ("pw", 100), {"xp": 20, "rep": 6}, "Tu repousses la première vague.", {"sante": -15}, "Tu es repoussé."),
                 ("Tendre une embuscade", ("st", "intel", 60), {"xp": 18, "rep": 5}, "Ton piège décime leur avant-garde.", {"bonheur": -3}, "L'ennemi flaire le piège.")]),
             dict(t="Leur commandant avance avec une escouade d'élite.", ch=[
                 ("Le défier en combat singulier", ("pw", 130), {"xp": 30, "rep": 10}, "Tu le mets à terre.", {"sante": -25}, "Tu es sévèrement blessé."),
                 ("Attaquer son ravitaillement", .65, {"xp": 25, "rep": 6}, "Il doit battre en retraite.", {"sante": -12}, "Ton raid échoue.")]),
             dict(t="La bataille touche à sa fin. On te demande de négocier ou de poursuivre.", ch=[
                 ("Imposer un cessez-le-feu", ("st", "rep", 60), {"rep": 10, "alrel": 6}, "La paix est signée.", {"rep": -3}, "Le village rival refuse."),
                 ("Poursuivre l'offensive", ("pw", 140), {"xp": 35, "rep": 8, "karma": -3}, "Tu écrases leur arrière-garde.", {"sante": -22}, "Tu te fais piéger.")]),
         ],
         fin=dict(eff={"xp": 70, "rep": 15}, txt="🏆 Tu repousses le village rival : on chante ton nom.")),
    dict(id="brigands", nom="Raid de brigands sur {V}", u="Naruto", a=(12, 45), cond=lambda g: _nar_ok(g), p=.12, rep=True, need=2,
         steps=[
             dict(t="🏴‍☠️ Une bande de brigands attaque la lisière de {V}. Le village appelle les ninjas disponibles.", ch=[
                 ("Foncer sur les brigands", ("pw", 55), {"xp": 12, "rep": 3}, "Tu en renverses plusieurs.", {"sante": -10}, "Tu es bousculé."),
                 ("Défendre les civils", .8, {"karma": 4, "rep": 3}, "Les villageois te remercient.", {"sante": -8}, "Tu es blessé.")]),
             dict(t="Le chef des brigands te défie.", ch=[
                 ("Relever le défi", ("pw", 70), {"xp": 20, "rep": 6, "argent": 100}, "Tu le terrasses.", {"sante": -15}, "Il te fait mordre la poussière."),
                 ("Le piéger", ("st", "intel", 50), {"xp": 15, "rep": 4}, "Il tombe dans ton filet.", {"bonheur": -2}, "Il découvre ton piège.")]),
             dict(t="Il reste à débusquer leur repaire.", ch=[
                 ("Pister jusqu'à leur camp", ("pw", 65), {"xp": 15, "argent": 150}, "Tu libères les captifs.", {"sante": -10}, "Tu te perds en route."),
                 ("Envoyer un rapport", 1, {"rep": 2}, "Les anciens s'en occupent.", {}, "")]),
         ],
         fin=dict(eff={"xp": 40, "rep": 8, "argent": 150}, txt="🛡️ Les brigands sont chassés : {V} respire.")),
    dict(id="blessure", nom="Blessure grave", u="Kuroko", a=(14, 40), cond=lambda g: g["mait"] >= 20, p=.07, rep=True, need=2,
         steps=[
             dict(t="🩹 Pendant un match serré, ton genou craque. La douleur est aiguë.", ch=[
                 ("Sortir immédiatement", .9, {"sante": -8}, "Tu évites le pire.", {"sante": -15}, "La blessure s'aggrave quand même."),
                 ("Continuer à jouer", .35, {"rep": 5, "sante": -10}, "Tu termines le match en héros.", {"sante": -30, "bonheur": -6}, "Tu t'effondres sur le parquet.")]),
             dict(t="Le diagnostic tombe : plusieurs semaines de rééducation.", ch=[
                 ("Rééducation sérieuse", .85, {"sante": 10, "intel": 2}, "Tu progresses à chaque séance.", {"bonheur": -4}, "Tu stagnes."),
                 ("Accélérer le retour", .45, {"mait": 2, "sante": 5}, "Tu reviens plus vite que prévu.", {"sante": -15, "mait": -3}, "Tu aggraves la blessure.")]),
             dict(t="Tu reviens enfin sur le terrain, un peu hésitant.", ch=[
                 ("Reprendre en douceur", .9, {"mait": 2, "bonheur": 4}, "Tu retrouves tes sensations.", {"bonheur": -3}, "Tu doutes de toi."),
                 ("Tout donner dès le premier match", .5, {"rep": 6, "mait": 3}, "Tu prouves que tu es de retour !", {"sante": -12, "bonheur": -5}, "Tu te refais mal.")]),
         ],
         fin=dict(eff={"mait": 3, "bonheur": 6}, txt="💪 Tu reviens plus fort de cette blessure.")),
    dict(id="police", nom="Contrôle de police", u="Tokyo Revengers", a=(13, 40), cond=lambda g: bool(g["gang"]) and g["monde"] is not None, p=.18, rep=True, need=1,
         steps=[
             dict(t="🚓 Des gyrophares illuminent votre QG. Des agents bloquent les issues : contrôle de police.", ch=[
                 ("Fuir par la ruelle", ("pw", 70), {"xp": 10, "rep": 3}, "Tu files entre les mains des agents.", {"sante": -8, "rep": -4}, "Tu te fais rattraper."),
                 ("Négocier avec un agent", ("st", "rep", 45), {"rep": 4, "karma": 1}, "L'agent ferme les yeux.", {"argent": -100, "rep": -3}, "Il te met une amende salée."),
                 ("Faire diversion pour les autres", .65, {"karma": 5, "rep": 6}, "Ton gang s'échappe grâce à toi.", {"sante": -10, "rep": -2}, "Tu te fais arrêter à leur place.")]),
             dict(t="Au poste de police, un inspecteur t'interroge sur les activités du gang.", ch=[
                 ("Garder le silence", .75, {"rep": 6, "karma": 2}, "L'inspecteur finit par te relâcher.", {"rep": -4, "bonheur": -4}, "Il te garde une nuit en cellule."),
                 ("Nier en bloc", ("st", "intel", 50), {"rep": 3}, "Ton sang-froid désarme l'inspecteur.", {"rep": -6}, "Il décèle tes mensonges."),
                 ("Balancer un rival", .8, {"karma": -8, "rep": -3, "argent": 80}, "Tu te libères au prix d'un nom.", {"rep": -8, "karma": -8}, "Ton rival l'apprend.")]),
         ],
         fin=dict(eff={"rep": 3}, txt="🚓 Tu sors indemne de la descente de police.")),
    dict(id="tribut", nom="Guerre de territoire avec les yakuza", u="Tokyo Revengers", a=(16, 45), cond=lambda g: bool(g["gang"]) and nterr(g) >= 1, p=.1, rep=True, need=1,
         steps=[
             dict(t="🕴️ Un clan yakuza veut s'imposer dans ton quartier et exige que ton gang lui verse un tribut.", ch=[
                 ("Refuser avec fermeté", ("st", "rep", 55), {"rep": 8, "karma": 2}, "Les yakuza reculent, impressionnés.", {"rep": -4, "sante": -8}, "Ils t'envoient un message musclé."),
                 ("Négocier un compromis", .6, {"argent": -80, "rep": 3}, "Un arrangement boiteux est trouvé.", {"rep": -3}, "La négociation s'envenime.")]),
             dict(t="Les yakuza envoient leurs hommes de main. L'affrontement est inévitable.", ch=[
                 ("Tenir tête avec ton gang", ("pw", 140), {"xp": 40, "rep": 12, "gfor": 3}, "Ton gang tient le quartier !", {"sante": -25, "membres": -3}, "Tu perds du terrain."),
                 ("Appeler des alliés", .6, {"alrel": 6, "rep": 4}, "Un allié répond présent.", {"rep": -4}, "Personne ne répond.")]),
         ],
         fin=dict(eff={"xp": 60, "rep": 10}, txt="🕴️ Les yakuza lèvent le siège : ton gang a gagné le respect de la rue.")),
]
ARCS.extend(ARCS_EXTRA)
for _a in ARCS_EXTRA: ARC_BY_ID[_a["id"]] = _a

# ═════════════ Avatar (style BitLife) ═════════════
SKINS = ["#fde3cf", "#f5cba7", "#e0ac84", "#c68642", "#8d5524", "#5c3a21"]
SKIN_LBL = ["Très clair", "Clair", "Hâlé", "Mat", "Brun", "Foncé"]
HAIR_COL = {"Noir": "#1a1a1a", "Châtain": "#6b4423", "Roux": "#c2410c", "Blond": "#e8c35a", "Rouge": "#c1121f", "Bleu": "#2b59c3",
            "Vert": "#2e9e55", "Violet": "#7b3fc4", "Blanc": "#e8e8ee"}
HAIR_EMO = {"Noir": "⚫", "Châtain": "🟤", "Roux": "🟠", "Blond": "🟡", "Rouge": "🔴", "Bleu": "🔵", "Vert": "🟢", "Violet": "🟣", "Blanc": "⚪"}
EYE_COL = {"Marron": "#6b3e1e", "Noisette": "#b07a2a", "Vert": "#3a9a4a", "Bleu": "#3a78d8", "Gris": "#8a97a8", "Ambre": "#f0a30a",
           "Rouge": "#c1121f", "Violet": "#7b3fc4"}
EYE_EMO = {"Marron": "🟤", "Noisette": "🟠", "Vert": "🟢", "Bleu": "🔵", "Gris": "⚪", "Ambre": "🟡", "Rouge": "🔴", "Violet": "🟣"}
HAIR_STYLES = ["Courts", "Hérissés", "Mi-longs", "Longs", "Queue de cheval", "Chauve"]
BROWS = ["Fins", "Épais", "Froncés"]
BEARDS = ["Aucune", "Moustache", "Bouc", "Barbe"]
SHIRT = {"Naruto": "#3a4a8c", "Kuroko": "#e8590c", "Tokyo Revengers": "#1c1c24"}


def random_av():
    f = random.random() < .5
    return dict(genre="F" if f else "H", peau=random.choices(range(6), weights=[3, 4, 3, 2, 1, 1])[0],
                style=random.choice(HAIR_STYLES[:5] if not f else ["Mi-longs", "Longs", "Queue de cheval", "Courts"]),
                couleur=random.choices(list(HAIR_COL), weights=[6, 5, 2, 3, 1, 1, 1, 1, 0.3])[0],
                yeux=random.choices(list(EYE_COL), weights=[6, 3, 2, 2, 1, 1, .5, .5])[0],
                sourcils=random.choice(BROWS), barbe="Aucune" if f or random.random() < .7 else random.choice(BEARDS[1:]))


def mix_av(a, b=None):
    """Avatar d'un enfant : proche de celui du parent, avec quelques variations."""
    n = random_av(); n["peau"] = a["peau"]; n["genre"] = n["genre"]
    if random.random() < .7: n["couleur"] = a["couleur"]
    if random.random() < .7: n["yeux"] = a["yeux"]
    return n


def avatar_svg(av, age=20, u=None, size=96, accessoire=True):
    av = av or dict(genre="H", peau=1, style="Courts", couleur="Noir", yeux="Marron", sourcils="Fins", barbe="Aucune")
    skin = SKINS[av.get("peau", 1) % len(SKINS)]
    hc = HAIR_COL.get(av.get("couleur", "Noir"), "#1a1a1a")
    if age >= 60: hc = "#d8d8dd"
    ec = EYE_COL.get(av.get("yeux", "Marron"), "#6b3e1e")
    st_, f = av.get("style", "Courts"), av.get("genre") == "F"
    sc = .55 + .45 * min(age, 16) / 16
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 120" width="{size}" height="{int(size * 1.2)}" style="display:inline-block">',
         f'<g transform="translate(50,120) scale({sc:.2f}) translate(-50,-120)">']
    if st_ in ("Longs", "Mi-longs"):
        h = 100 if st_ == "Longs" else 78
        p.append(f'<path d="M20 50 Q18 {h} 26 {h + 4} L74 {h + 4} Q82 {h} 80 50 Z" fill="{hc}"/>')
    if st_ == "Queue de cheval":
        p.append(f'<ellipse cx="82" cy="66" rx="7" ry="16" fill="{hc}" transform="rotate(-18 82 66)"/>')
    p.append(f'<path d="M8 120 Q8 92 50 88 Q92 92 92 120 Z" fill="{SHIRT.get(u, "#556")}"/>')
    p.append(f'<rect x="42" y="78" width="16" height="14" fill="{skin}"/>')
    p.append(f'<circle cx="22" cy="56" r="5" fill="{skin}"/><circle cx="78" cy="56" r="5" fill="{skin}"/>')
    p.append(f'<ellipse cx="50" cy="52" rx="28" ry="32" fill="{skin}"/>')
    # cheveux (devant)
    if st_ == "Courts": p.append(f'<path d="M21 48 Q20 16 50 16 Q80 16 79 48 Q70 30 50 33 Q32 30 21 48 Z" fill="{hc}"/>')
    elif st_ == "Hérissés": p.append(f'<path d="M21 48 L22 22 L32 30 L38 12 L47 26 L56 10 L62 27 L72 14 L76 30 L79 48 Q70 32 50 34 Q32 32 21 48 Z" fill="{hc}"/>')
    elif st_ == "Mi-longs": p.append(f'<path d="M20 56 Q18 14 50 15 Q82 14 80 56 Q76 34 50 34 Q24 34 20 56 Z" fill="{hc}"/>')
    elif st_ == "Longs": p.append(f'<path d="M19 66 Q16 12 50 14 Q84 12 81 66 Q74 30 52 32 Q28 30 19 66 Z" fill="{hc}"/>')
    elif st_ == "Queue de cheval": p.append(f'<path d="M21 48 Q20 14 50 15 Q80 14 79 48 Q70 30 50 33 Q32 30 21 48 Z" fill="{hc}"/>')
    # accessoires selon l'univers
    if accessoire and u == "Naruto" and age >= 12:
        p.append('<rect x="21" y="30" width="58" height="9" fill="#2b3a67"/><rect x="38" y="28" width="24" height="13" rx="2" fill="#c3cad8" stroke="#6c7690" stroke-width="1"/><path d="M45 34 Q50 30 55 34" stroke="#4a5470" fill="none" stroke-width="1.5"/>')
    if accessoire and u == "Kuroko" and age >= 12:
        p.append('<rect x="24" y="32" width="52" height="4" rx="2" fill="#e8590c"/>')
    # yeux, sourcils
    for x in (38, 62):
        p.append(f'<ellipse cx="{x}" cy="53" rx="6.2" ry="4.4" fill="#fff"/><circle cx="{x}" cy="53" r="3.3" fill="{ec}"/><circle cx="{x}" cy="53" r="1.5" fill="#111"/>')
        if f: p.append(f'<path d="M{x - 7} 51 Q{x} 46 {x + 7} 51" stroke="#222" stroke-width="1.2" fill="none"/>')
    b = av.get("sourcils", "Fins")
    w = {"Fins": 1.5, "Épais": 3.2, "Froncés": 2.4}[b]
    if b == "Froncés": p.append(f'<path d="M30 45 L45 48 M70 45 L55 48" stroke="{hc}" stroke-width="{w}" stroke-linecap="round"/>')
    else: p.append(f'<path d="M31 46 Q38 43 45 46 M55 46 Q62 43 69 46" stroke="{hc}" stroke-width="{w}" fill="none" stroke-linecap="round"/>')
    p.append('<path d="M50 56 L47 66 Q50 68 53 66" stroke="#0003" fill="none" stroke-width="1.3"/>')
    p.append(f'<path d="M42 72 Q50 78 58 72" stroke="{"#b23a48" if f else "#7a3b3b"}" stroke-width="{2.2 if f else 1.8}" fill="none" stroke-linecap="round"/>')
    # pilosité
    br = av.get("barbe", "Aucune")
    if not f and age >= 14:
        if br == "Moustache": p.append(f'<path d="M40 68 Q50 63 60 68 Q50 70 40 68 Z" fill="{hc}"/>')
        elif br == "Bouc": p.append(f'<path d="M44 78 Q50 90 56 78 Q50 80 44 78 Z" fill="{hc}"/>')
        elif br == "Barbe": p.append(f'<path d="M22 58 Q24 86 50 88 Q76 86 78 58 Q72 74 50 74 Q28 74 22 58 Z" fill="{hc}" opacity=".9"/>')
    if age >= 60: p.append('<path d="M34 36 Q50 32 66 36 M30 62 Q34 66 38 64 M70 62 Q66 66 62 64" stroke="#0002" fill="none"/>')
    p.append('</g></svg>')
    return "".join(p)


# ═════════════ École : clubs, cliques ═════════════
CLUBS = {
    "Sport": ("⚽", "Entraînement collectif", dict(force=3, sante=2, bonheur=2)),
    "Sciences": ("🔬", "Expériences et lecture", dict(intel=4)),
    "Théâtre": ("🎭", "Monter sur scène", dict(beaute=3, bonheur=3)),
    "Musique": ("🎵", "Jouer en groupe", dict(bonheur=4, intel=1)),
    "Arts martiaux": ("🥋", "Discipline et combat", dict(force=2, mait=2)),
    "Cuisine": ("🍱", "Cuisiner pour les autres", dict(sante=3, bonheur=2)),
}
CLIQUES = {
    "Sportifs": ("🏅", dict(force=1, sante=1), 1),
    "Intellos": ("📚", dict(intel=2), 0),
    "Rebelles": ("😎", dict(rep=1, karma=-1), 0),
    "Populaires": ("🌟", dict(beaute=1, bonheur=1), 2),
    "Artistes": ("🎨", dict(bonheur=1, intel=1), 1),
}
PLATS = {"Naruto": ["Gazette du village", "Bingo Book", "Messagers itinérants"],
         "Kuroko": ["Instagram", "TikTok", "YouTube", "Twitch", "Twitter", "Facebook"],
         "Tokyo Revengers": ["Instagram", "TikTok", "YouTube", "Twitch", "Twitter", "Facebook"]}
PLAT_ICO = {"Instagram": "📸", "TikTok": "🎵", "YouTube": "▶️", "Twitch": "🎮", "Twitter": "🐦", "Facebook": "📘",
            "Gazette du village": "📰", "Bingo Book": "📜", "Messagers itinérants": "🕊️"}
MARQUES = {"Naruto": ["Marchands de Konoha", "Forge de Tetsu", "Maison de thé Ichiraku"],
           "Kuroko": ["Kibō Sneakers", "Tōkyō Sports", "Ramen Ichi"], "Tokyo Revengers": ["Néon Racing", "Shibuya Wear", "Moto Bōsō"]}

# ═════════════ Saisons (Kuroko : temps par trimestre) ═════════════
SAISONS = ["Printemps", "Été", "Automne", "Hiver"]
SAISON_ICO = ["🌸", "☀️", "🍂", "❄️"]
SAISON_MOIS = ["avril–juin", "juillet–septembre", "octobre–décembre", "janvier–mars"]
COMP["ete"] = ("Tournoi d'été inter-lycées", (15, 18), ["Premier tour", "Demi-finale", "Finale"], {"xp": 60, "rep": 8, "argent": 150})
COMP["printemps"] = ("Coupe de printemps", (13, 18), ["Premier tour", "Demi-finale", "Finale"], {"xp": 45, "rep": 6, "argent": 100})
COMP_Q = {"college": [0], "inter": [0], "ete": [1], "winter": [2], "printemps": [3], "nba": [0]}
for _id, _q in (("interhigh", [0]), ("wintercup", [2]), ("lastgame", [1]), ("nba", [0, 1]), ("lycee", [0])):
    ARC_BY_ID[_id]["q"] = _q

# ═════════════ Rivalités entre factions ═════════════
RIVALITES = {
    "Naruto": [("Konoha", "Iwa"), ("Suna", "Kumo"), ("Kiri", "Iwa"), ("Ame", "Konoha"), ("Taki", "Kumo")],
    "Tokyo Revengers": [("Toman", "Valhalla"), ("Toman", "Tenjiku"), ("Moebius", "Brahman"), ("Black Dragons", "Tenjiku"),
                        ("Rokuhara Tandai", "Kantō Manji"), ("Valhalla", "Kantō Manji")],
    "Kuroko": [("Lycée Seirin", "Lycée Kirisaki Daiichi"), ("Lycée Shūtoku", "Lycée Kaijō"), ("Lycée Tōō", "Lycée Yōsen"), ("Lycée Rakuzan", "Lycée Seirin")],
}

# ═════════════ Lycées : exigences, coach, coéquipiers, Miracle associé ═════════════
ECOLES = {
    "Lycée Seirin": dict(mait=20, coach="Riko Aida", membres=["Junpei Hyūga", "Shun Izuki", "Teppei Kiyoshi"], gm=None),
    "Lycée Kaijō": dict(mait=45, coach="Coach Takeuchi", membres=["Yukio Kasamatsu", "Yoshitaka Moriyama", "Mitsuhiro Hayakawa"], gm="Kise"),
    "Lycée Shūtoku": dict(mait=50, coach="Coach Nakatani", membres=["Kazunari Takao", "Taisuke Ōtsubo", "Kiyoshi Miyaji"], gm="Midorima"),
    "Lycée Tōō": dict(mait=50, coach="Coach Harasawa", membres=["Satsuki Momoi", "Kōsuke Wakamatsu", "Shōichi Imayoshi"], gm="Aomine"),
    "Lycée Yōsen": dict(mait=55, coach="Coach Araki", membres=["Tatsuya Himuro", "Kenichi Okamura", "Kensuke Fukui"], gm="Murasakibara"),
    "Lycée Rakuzan": dict(mait=65, coach="Coach Shirogane", membres=["Reo Mibuchi", "Eikichi Nebuya", "Kotarō Hayama"], gm="Akashi"),
}
for _n, _e in ECOLES.items():
    if _n == "Lycée Seirin": continue
    _id = "coach_" + _n.split()[-1].lower()
    ENC.append(_E(_id, "Kuroko", _e["coach"], "📋", f"Coach du {_n}", "recruteur", 1.1, ["gymnase", "salle", "ecole", "stade"], 13,
                  lambda g: not g["lycee"] and not g["recrue"], "« J'ai suivi tes matchs. Tu as un vrai potentiel. »",
                  ["« Chez nous, l'équipe passe avant l'individu. »", "« Travaille dur et tu auras ta place. »"],
                  f"« Rejoins le {_n} : nous avons une place pour toi. »", "lycee:" + _n))
for _e in ENC[-5:]: ENC_BY_ID[_e["id"]] = _e
ENC_BY_ID["riko"]["org"] = "lycee:Lycée Seirin"
ENC_BY_ID["riko"]["offre"] = "« Seirin cherche des joueurs. Tu veux faire partie de l'équipe ? »"

# ═════════════ Amitié avec la Génération des Miracles ═════════════
SCENES_GM = {
    "Akashi": [("Akashi t'invite à une partie de shogi : tu apprends à anticiper.", {"intel": 3}), ("Akashi t'observe en silence puis te donne un conseil précis.", {"mait": 3}),
               ("Vous parlez longuement de ce que signifie gagner.", {"bonheur": 3, "intel": 1})],
    "Aomine": [("Aomine te défie sur un terrain de rue : tu lui tiens tête quelques minutes.", {"mait": 4, "force": 1}), ("Vous mangez des glaces en riant de tout et de rien.", {"bonheur": 5}),
               ("Aomine t'avoue qu'il s'ennuyait. Tu le fais sourire.", {"bonheur": 3, "rep": 1})],
    "Murasakibara": [("Murasakibara partage ses snacks avec toi. C'est rare.", {"bonheur": 5}), ("Il te montre comment il protège le panier avec ses bras.", {"force": 3, "mait": 1}),
                     ("Vous jouez au 1 contre 1 de mauvaise grâce, puis vous riez.", {"mait": 2, "bonheur": 3})],
    "Midorima": [("Midorima te prête son objet porte-bonheur du jour.", {"bonheur": 4}), ("Tu regardes ses tirs à l'entraînement : une leçon de précision.", {"mait": 4}),
                 ("Il t'explique son horoscope avec un sérieux absolu.", {"bonheur": 3, "intel": 1})],
    "Kise": [("Kise t'entraîne à copier un mouvement. Il est ravi de ta réussite.", {"mait": 4}), ("Vous prenez une photo qui fait le tour du lycée.", {"rep": 3, "bonheur": 3}),
             ("Il te raconte ses séances de photo, hilare.", {"bonheur": 4})],
}

# ═════════════ Constructeurs d'arcs ═════════════
def C(l, p, eo, to="", ek=None, tk=""): return (l, p, eo, to, ek or {}, tk)
def S(t, *ch, ko=None):
    d = dict(t=t, ch=list(ch))
    if ko: d["ko"] = ko
    return d
def AR(id, nom, u, a, cond, p, steps, fin_eff, fin_txt, **kw):
    d = dict(id=id, nom=nom, u=u, a=a, cond=cond, p=p, steps=steps, fin=dict(eff=fin_eff, txt=fin_txt), rep=True)
    d.update(kw); return d
def SC(id, nom, u, a, cond, req, p, steps, fin_eff, fin_txt, **kw):
    eff = dict(fin_eff); eff["flag"] = f"s_{id}"
    cnd = lambda g, c=cond, i=id: f"s_{i}" not in g["flags"] and c(g)
    return AR(id, nom, u, a, cnd, p, steps, eff, fin_txt, man=True, scen=True, req=req, **kw)

def _ally_rel(g, r): return any(f["allie"] and f["rel"] >= r for f in g["fact"].values())
def _gang_rang(g, r): return bool(g["gang"]) and (g["gang"]["chef"] or g["gang"]["rang"] >= r)

ARCS_POL = [
    # ───────────── NARUTO : scénarios débloquables ─────────────
    SC("pacte_defense", "Pacte de défense avec {A}", "Naruto", (16, 60), lambda g: _ally_rel(g, 60) and g["cap"] >= 2 and _nar_ok(g),
       "Un village allié (relation ≥ 60) et le rang de Chūnin", .1,
       [S("Les émissaires de {A} proposent un pacte de défense mutuelle. Les termes restent à négocier.",
          C("Négocier fermement", ("st", "intel", 60), {"rep": 6}, "Tu obtiens des clauses avantageuses.", {"relx": ["A", -5]}, "Les négociations s'enlisent."),
          C("Faire des concessions", .85, {"relx": ["A", 8]}, "Votre confiance mutuelle grandit.", {"rep": -2}, "Tes concessions passent pour de la faiblesse.")),
        S("La cérémonie de signature réunit les deux Kage. Un saboteur rôde dans la salle.",
          C("Sécuriser la salle", ("pw", 180), {"xp": 25, "rep": 8}, "Le saboteur est neutralisé.", {"sante": -15}, "Le saboteur s'échappe."),
          C("Avancer la signature", .6, {"relx": ["A", 6]}, "Le pacte est scellé avant tout incident.", {"rep": -4}, "La précipitation vexe tes hôtes.")),
        S("Première opération commune : écraser un repaire de brigands à la frontière.",
          C("Mener l'assaut", ("pw", 200), {"xp": 40, "rep": 10}, "Les deux armées triomphent ensemble.", {"sante": -20}, "L'opération tourne mal."),
          C("Coordonner à distance", ("st", "intel", 70), {"xp": 30, "rep": 8}, "Ton plan est exécuté sans accroc.", {"bonheur": -3}, "Les transmissions sont coupées."))],
       {"alrel": 15, "rep": 12, "xp": 70}, "🤝 Le pacte est signé : {V} et {A} sont désormais liés.", need=2),
    SC("mission_conjointe", "Mission conjointe avec {A}", "Naruto", (14, 60), lambda g: bool(allies(g)) and _nar_ok(g), "Un village allié", .12,
       [S("Une escouade de {A} se joint à la tienne pour escorter un convoi sensible.",
          C("Prendre la tête", ("st", "rep", 50), {"rep": 4}, "Les deux escouades suivent ton commandement.", {"relx": ["A", -3]}, "Leurs ninjas contestent ton autorité."),
          C("Laisser leur chef décider", .85, {"relx": ["A", 5]}, "Ton humilité est remarquée.", {}, "")),
        S("Une embuscade de brigands vous attend dans les gorges.",
          C("Contre-attaquer", ("pw", 120), {"xp": 25, "rep": 6}, "Vous les balayez ensemble.", {"sante": -12}, "Vous subissez des pertes."),
          C("Contourner par la crête", ("st", "intel", 55), {"xp": 20}, "Vous les prenez à revers.", {"sante": -8}, "Vous arrivez trop tard.")),
        S("Au retour, les ninjas de {A} te proposent un combat amical.",
          C("Accepter", ("pw", 140), {"xp": 20, "relx": ["A", 6]}, "Un beau combat qui renforce vos liens.", {"sante": -10, "relx": ["A", 3]}, "Tu perds avec les honneurs."),
          C("Décliner poliment", 1, {}, "Tu préfères ménager tes forces.", {}, ""))],
       {"relx": ["A", 12], "xp": 50, "rep": 10}, "🛡️ Mission accomplie : {A} t'estime désormais bien plus.", need=2),
    SC("guerre_ennemi", "Guerre contre {E}", "Naruto", (18, 60), lambda g: bool(ennemis(g)) and g["cap"] >= 2 and _nar_ok(g),
       "Un village ennemi déclaré et le rang de Chūnin", .1,
       [S("Les hostilités avec {E} dégénèrent : leurs avant-gardes franchissent la frontière.",
          C("Tenir la frontière", ("pw", 150), {"xp": 30, "rep": 8}, "Tu stoppes l'avant-garde ennemie.", {"sante": -20}, "Tu es repoussé."),
          C("Frapper en premier", ("pw", 170), {"xp": 35, "rep": 6, "karma": -3}, "Ton raid désorganise leurs lignes.", {"sante": -25, "rep": -3}, "Ton raid tombe dans un piège.")),
        S("Un siège s'installe. Les vivres s'amenuisent.",
          C("Rationner et tenir", .7, {"xp": 20, "rep": 6}, "Le village tient bon.", {"bonheur": -6}, "Le moral s'effondre."),
          C("Briser le siège", ("pw", 190), {"xp": 40, "rep": 10}, "Tu ouvres une brèche !", {"sante": -30}, "Tu es gravement blessé.")),
        S("Le commandant de {E} te défie pour décider de l'issue.",
          C("Accepter le duel", ("pw", 210), {"xp": 60, "rep": 15}, "Tu l'emportes : {E} bat en retraite.", {"sante": -35}, "Tu t'inclines face à lui."),
          C("Proposer un armistice", ("st", "rep", 70), {"rep": 8, "karma": 3}, "Un armistice est signé.", {"rep": -4}, "Il refuse tout compromis."))],
       {"paix": "E", "xp": 100, "rep": 20}, "🕊️ {E} demande la paix : la guerre est terminée.", need=2),
    SC("coalition", "Coalition contre {E}", "Naruto", (22, 60), lambda g: len(allies(g)) >= 2 and bool(ennemis(g)) and _nar_ok(g),
       "Deux alliés et un ennemi déclaré", .08,
       [S("Tu réunis les Kage alliés autour d'une table de guerre.",
          C("Forger un plan commun", ("st", "intel", 75), {"alrel": 6, "rep": 8}, "Ta stratégie fait l'unanimité.", {"alrel": -3}, "Les rivalités paralysent la réunion."),
          C("Imposer ton leadership", ("st", "rep", 80), {"rep": 10}, "Les alliés se rallient à toi.", {"alrel": -5, "rep": -4}, "Ils refusent de t'obéir.")),
        S("La coalition marche sur {E}. L'affrontement est monstrueux.",
          C("Mener l'avant-garde", ("pw", 220), {"xp": 60, "rep": 15}, "Ta charge ouvre la voie.", {"sante": -35}, "Tu es submergé."),
          C("Diriger depuis l'arrière", ("st", "intel", 80), {"xp": 45, "rep": 10}, "Ton commandement est impeccable.", {"bonheur": -4}, "Ton plan est lu par l'ennemi."))],
       {"paix": "E", "alrel": 10, "xp": 90, "rep": 15}, "🌐 La coalition triomphe : {E} s'incline.", need=1),
    SC("operation_secrete", "Opération secrète chez {E}", "Naruto", (20, 60), lambda g: bool(ennemis(g)) and g["cap"] >= 3 and _nar_ok(g),
       "Un village ennemi et le rang de Jōnin", .08,
       [S("On t'envoie infiltrer {E} pour y récupérer des documents.",
          C("Infiltration furtive", ("st", "intel", 75), {"xp": 30}, "Tu passes inaperçu.", {"sante": -15}, "Tu es repéré."),
          C("Se déguiser en marchand", .6, {"xp": 25, "argent": 100}, "Ton déguisement est parfait.", {"rep": -4}, "Un garde te démasque.")),
        S("Les documents contiennent un secret explosif.",
          C("Les rapporter à ton Kage", .9, {"rep": 10, "xp": 30}, "Ton village est reconnaissant.", {}, ""),
          C("Les vendre au plus offrant", .6, {"argent": 600, "karma": -12}, "Tu empoches une fortune.", {"rep": -12, "karma": -10}, "Ta trahison est découverte."))],
       {"xp": 80, "rep": 10}, "🕵️ L'opération secrète est un succès.", need=2),
    SC("festival_amitie", "Festival de l'amitié avec {A}", "Naruto", (14, 60), lambda g: _ally_rel(g, 50), "Un village allié (relation ≥ 50)", .1,
       [S("{A} t'invite à son festival : lanternes, danses et combats amicaux.",
          C("Participer à la danse", .8, {"bonheur": 8, "relx": ["A", 6]}, "Tu t'amuses comme jamais.", {"bonheur": 2}, "Tu danses un peu maladroitement."),
          C("Défier un champion local", ("pw", 120), {"rep": 8, "relx": ["A", 4]}, "La foule t'ovationne.", {"sante": -8}, "Tu es battu avec le sourire.")),
        S("Une belle rencontre au détour des étals.",
          C("Faire connaissance", .7, {"bonheur": 6, "intel": 1}, "Une amitié sincère naît.", {"bonheur": -2}, "Tu restes en retrait."),
          C("Acheter un cadeau (80)", 1, {"argent": -80, "bonheur": 4, "relx": ["A", 3]}, "Un souvenir précieux.", {}, ""))],
       {"relx": ["A", 15], "bonheur": 10}, "🏮 Le festival renforce durablement votre amitié.", need=1),
    # ───────────── NARUTO : incidents diplomatiques et politiques ─────────────
    AR("inc_frontiere", "Incident diplomatique à la frontière", "Naruto", (16, 60), lambda g: bool(g["fact"]) and g["cap"] >= 1 and _nar_ok(g), .08,
       [S("Une patrouille de {E} est accusée d'avoir franchi la frontière de {V}. La tension monte.",
          C("S'excuser publiquement", .8, {"relx": ["E", 8], "rep": -3}, "L'incident est désamorcé.", {"rep": -4}, "Tes excuses sont prises pour de la faiblesse."),
          C("Défendre l'honneur de {V}", ("st", "rep", 55), {"rep": 8, "relx": ["E", -8]}, "Ton aplomb impressionne.", {"rep": -4}, "Ta fermeté tourne à l'esclandre."),
          C("Exiger réparation", ("pw", 140), {"xp": 20, "rep": 6, "relx": ["E", -10]}, "Ils paient pour l'incident.", {"sante": -12, "relx": ["E", -5]}, "Ils te rient au nez.")),
        S("Les Kage envoient des émissaires pour clore l'affaire.",
          C("Plaider la paix", ("st", "intel", 60), {"karma": 4, "relx": ["E", 8]}, "Un accord est trouvé.", {"rep": -2}, "Les émissaires repartent bredouilles."),
          C("Rester intransigeant", .6, {"rep": 6}, "Ton village te soutient.", {"relx": ["E", -6], "ennemi": "E"}, "L'affaire s'envenime : {E} devient hostile."))],
       {"rep": 4}, "🕊️ L'incident diplomatique est clos.", need=1),
    AR("emissaire", "Assassinat d'un émissaire de {A}", "Naruto", (20, 60), lambda g: bool(allies(g)) and g["cap"] >= 2 and _nar_ok(g), .06,
       [S("L'émissaire de {A} est retrouvé mort dans {V}. On soupçonne un complot.",
          C("Mener l'enquête", ("st", "intel", 65), {"xp": 20, "rep": 6}, "Tu remontes une piste sérieuse.", {"relx": ["A", -4]}, "L'enquête piétine."),
          C("Calmer {A}", ("st", "rep", 60), {"relx": ["A", 5]}, "Tes mots apaisent leurs émissaires.", {"relx": ["A", -6]}, "Ils t'accusent d'étouffer l'affaire.")),
        S("Les preuves désignent {E}. Il faut trancher.",
          C("Accuser {E} publiquement", .65, {"rep": 8, "ennemi": "E", "relx": ["A", 10]}, "{A} te remercie, {E} devient ton ennemi.", {"rep": -6, "relx": ["A", -5]}, "Les preuves s'avèrent fragiles."),
          C("Demander un jugement neutre", .85, {"karma": 5, "rep": 4}, "Un tribunal impartial est convoqué.", {}, ""))],
       {"xp": 40, "rep": 8}, "⚖️ L'affaire de l'émissaire est réglée.", need=1),
    AR("succession", "Querelle de succession à la tête de {V}", "Naruto", (25, 70), lambda g: g["cap"] >= 2 and _nar_ok(g), .06,
       [S("Le Kage de {V} est affaibli : deux factions se disputent sa succession au conseil.",
          C("Soutenir le candidat modéré", .7, {"rep": 6, "karma": 3}, "Tu gagnes le respect des sages.", {"rep": -5}, "Les radicaux t'en tiennent rigueur."),
          C("Soutenir le candidat radical", .7, {"rep": 6, "xp": 15, "karma": -3}, "Tu deviens un homme influent.", {"rep": -5}, "Les modérés t'isolent."),
          C("Rester neutre", 1, {"karma": 1}, "Tu ne prends pas parti.", {}, "")),
        S("La querelle tourne à l'affrontement dans les rues.",
          C("Interposer ton escouade", ("pw", 160), {"rep": 10, "xp": 25}, "Tu rétablis l'ordre.", {"sante": -15}, "Tu es pris entre deux feux."),
          C("Appeler une médiation extérieure", .6, {"rep": 6, "relx": ["A", 4]}, "Un médiateur apaise la crise.", {"rep": -3}, "Personne ne répond à ton appel."))],
       {"rep": 6}, "🏯 La crise de succession est passée.", need=1),
    AR("espion", "Un espion de {E} démasqué", "Naruto", (16, 60), lambda g: g["cap"] >= 1 and _nar_ok(g), .08,
       [S("Tu découvres qu'un marchand de {V} transmet des informations à {E}.",
          C("L'arrêter immédiatement", ("pw", 120), {"xp": 20, "rep": 6}, "L'espion est capturé.", {"sante": -10}, "Il t'échappe."),
          C("Le suivre pour remonter le réseau", ("st", "intel", 65), {"xp": 25, "rep": 8}, "Tu démantèles tout un réseau.", {"bonheur": -3}, "Il te sème en ville.")),
        S("Que faire de l'espion ?",
          C("Le livrer à ton Kage", .95, {"rep": 5, "relx": ["E", -6]}, "L'affaire fait grand bruit.", {}, ""),
          C("Le retourner contre {E}", ("st", "intel", 70), {"xp": 30, "rep": 8}, "Il devient ton agent double.", {"rep": -4}, "Il te trahit à nouveau."))],
       {"xp": 30}, "🕵️ Le réseau d'espionnage est neutralisé.", need=1),
    AR("embargo", "Embargo commercial de {E}", "Naruto", (18, 60), lambda g: g["cap"] >= 1 and _nar_ok(g), .06,
       [S("{E} décrète un embargo sur les marchandises de {V}. Les prix flambent.",
          C("Négocier des exceptions", ("st", "rep", 55), {"argent": 80, "rep": 5, "relx": ["E", 4]}, "Tu obtiens des dérogations.", {"argent": -60}, "Les négociations échouent."),
          C("Organiser la contrebande", .6, {"argent": 300, "karma": -6}, "Tu t'enrichis dans l'ombre.", {"rep": -6, "argent": -80}, "Les douaniers t'attrapent."),
          C("Aider les villageois", .9, {"karma": 6, "rep": 6, "argent": -80}, "Ton geste te fait aimer.", {}, ""))],
       {"rep": 2}, "📦 L'embargo est surmonté.", need=1),
    AR("traite_paix", "Offre de traité de paix de {E}", "Naruto", (16, 70), lambda g: bool(ennemis(g)) and _nar_ok(g), .12,
       [S("Des émissaires de {E} proposent un traité de paix à {V}.",
          C("Accepter", .9, {"paix": "E", "rep": 6, "karma": 3}, "La paix est signée.", {"rep": -2}, "Le traité est refusé par les anciens."),
          C("Exiger un tribut", .6, {"paix": "E", "argent": 300, "rep": 3}, "Ils paient pour la paix.", {"relx": ["E", -5], "rep": -3}, "Ils quittent la table."),
          C("Refuser", 1, {"rep": 3, "karma": -2}, "Tu poursuis les hostilités.", {}, ""))],
       {}, "", need=1),
    AR("complot", "Complot au conseil de {V}", "Naruto", (28, 70), lambda g: g["cap"] >= 3 and _nar_ok(g), .05,
       [S("Des rumeurs de complot parcourent le conseil de {V}.",
          C("Enquêter discrètement", ("st", "intel", 70), {"xp": 20, "rep": 6}, "Tu repères les conspirateurs.", {"bonheur": -3}, "Tu es suivi."),
          C("Alerter ton Kage", .9, {"rep": 5}, "Ton Kage te remercie.", {}, "")),
        S("Les conspirateurs passent à l'action.",
          C("Les arrêter en pleine séance", ("pw", 190), {"xp": 40, "rep": 12}, "Le complot est étouffé.", {"sante": -22}, "Certains s'enfuient."),
          C("Les piéger", ("st", "intel", 80), {"xp": 35, "rep": 10}, "Ils tombent dans ton piège.", {"rep": -4}, "Ils déjouent ton piège.")),
        S("Il faut décider du sort des coupables.",
          C("Les juger publiquement", .9, {"rep": 8, "karma": 4}, "Justice est rendue.", {}, ""),
          C("Les exiler discrètement", .85, {"rep": 5}, "La crise est étouffée.", {"rep": -3}, ""))],
       {"xp": 60, "rep": 10}, "🏯 Le complot est déjoué.", need=2),
    AR("extradition", "Demande d'extradition par {A}", "Naruto", (18, 60), lambda g: bool(allies(g)) and _nar_ok(g), .06,
       [S("{A} exige l'extradition d'un déserteur réfugié à {V}.",
          C("Le livrer à {A}", .9, {"relx": ["A", 10], "karma": -3}, "Votre alliance en sort renforcée.", {}, ""),
          C("Refuser au nom de l'asile", ("st", "rep", 55), {"karma": 6, "rep": 4, "relx": ["A", -6]}, "Tu protèges l'exilé.", {"relx": ["A", -10], "rep": -3}, "{A} te reproche ton refus."),
          C("Organiser son exil", ("st", "intel", 60), {"karma": 3, "relx": ["A", 2]}, "Il disparaît avec ton aide.", {"relx": ["A", -8]}, "Ton plan est découvert."))],
       {}, "", need=1),
    # ───────────── TOKYO REVENGERS : scénarios débloquables ─────────────
    SC("banquet_alliance", "Banquet d'alliance avec {A}", "Tokyo Revengers", (14, 50), lambda g: _ally_rel(g, 50) and bool(g["gang"]),
       "Un gang allié (relation ≥ 50) et ton propre gang", .1,
       [S("{A} t'invite à un banquet pour sceller votre alliance. Les chefs sont tous là.",
          C("Porter un toast", .8, {"rep": 4, "relx": ["A", 6]}, "Ton discours fait l'unanimité.", {"rep": -2}, "Ton toast tombe à plat."),
          C("Offrir un cadeau (100)", 1, {"argent": -100, "relx": ["A", 8]}, "Le cadeau est très apprécié.", {}, "")),
        S("Un rival du banquet provoque un esclandre.",
          C("Le calmer", ("st", "rep", 55), {"karma": 3, "rep": 5}, "L'incident est évité.", {"rep": -3}, "Le rival s'énerve davantage."),
          C("Le corriger", ("pw", 120), {"rep": 8, "xp": 20}, "Tu règles l'affaire en deux coups.", {"sante": -12, "relx": ["A", -3]}, "Tu perds la face devant tout le monde."))],
       {"relx": ["A", 15], "rep": 8}, "🍶 L'alliance avec {A} est scellée.", need=1),
    SC("guerre_gang", "Guerre ouverte contre {E}", "Tokyo Revengers", (15, 50), lambda g: bool(ennemis(g)) and _gang_rang(g, 2),
       "Un gang ennemi déclaré et le grade de capitaine", .1,
       [S("{E} attaque le quartier de ton gang. C'est la guerre.",
          C("Tenir la ligne", ("pw", 140), {"xp": 30, "rep": 8}, "Ton gang résiste.", {"sante": -18}, "Tu es débordé."),
          C("Contre-attaquer au QG ennemi", ("pw", 160), {"xp": 35, "rep": 8, "gfor": 3}, "Tu frappes au cœur.", {"sante": -25, "membres": -2}, "Ton raid échoue.")),
        S("Les affrontements se multiplient dans toute la ville.",
          C("Mobiliser tous les membres", .75, {"gfor": 4, "membres": 3, "xp": 20}, "Tous répondent présent.", {"membres": -3}, "Plusieurs désertent."),
          C("Chercher des alliés", ("st", "rep", 60), {"alrel": 6, "rep": 6}, "Un allié rejoint la bataille.", {"rep": -3}, "Personne ne répond.")),
        S("Le chef de {E} te défie en face à face.",
          C("Accepter le duel", ("pw", 180), {"xp": 55, "rep": 15}, "Tu le terrasses sous les yeux de tous !", {"sante": -30}, "Il te met à terre."),
          C("Tendre un piège", ("st", "intel", 70), {"xp": 45, "rep": 12}, "Ta ruse le piège.", {"rep": -4}, "Il déjoue ton piège."))],
       {"terr": 1, "gfor": 8, "xp": 90, "rep": 15}, "🔥 Tu écrases {E} et prends un nouveau territoire.", need=2),
    SC("conseil_chefs", "Conseil des chefs de gangs", "Tokyo Revengers", (16, 50), lambda g: len(allies(g)) >= 2 and nterr(g) >= 2,
       "Deux gangs alliés et deux territoires", .08,
       [S("Les chefs de gangs de la ville se réunissent pour redessiner la carte des territoires.",
          C("Réclamer plus de territoires", ("st", "rep", 70), {"rep": 8}, "Tu fais valoir ton poids.", {"alrel": -4}, "Tes exigences passent mal."),
          C("Proposer un partage équitable", ("st", "intel", 60), {"alrel": 6, "karma": 3}, "Les chefs applaudissent ta sagesse.", {"rep": -2}, "Personne n'est convaincu.")),
        S("Un chef ambitieux menace de quitter la table.",
          C("Le retenir", ("st", "rep", 65), {"alrel": 4, "rep": 5}, "Il reste, vexé.", {"rep": -3}, "Il claque la porte."),
          C("Laisser faire", 1, {"karma": -1}, "Le conseil se poursuit sans lui.", {}, "")),
        S("Il faut voter le nouvel ordre.",
          C("Voter pour la stabilité", .85, {"rep": 6}, "Un accord est trouvé.", {}, ""),
          C("Voter pour la conquête", .6, {"rep": 8, "gfor": 3}, "Ta ligne dure l'emporte.", {"alrel": -5}, "Tu es mis en minorité."))],
       {"terr": 1, "alrel": 8, "rep": 12}, "🗺️ Le conseil te cède un territoire.", need=2),
    SC("pacte_yakuza", "Pacte avec les yakuza", "Tokyo Revengers", (16, 50), lambda g: bool(g["gang"]) and g["rep"] >= 40 and g["karma"] <= 10,
       "Un gang, 40 de réputation et un karma ≤ 10", .08,
       [S("Un intermédiaire yakuza te propose une protection en échange d'un pourcentage de tes revenus.",
          C("Négocier les termes", ("st", "intel", 60), {"argent": 100, "rep": 4}, "Tu obtiens de bonnes conditions.", {"karma": -3}, "Ils imposent leurs termes."),
          C("Refuser poliment", .6, {"karma": 4, "rep": 3}, "Ils respectent ton choix.", {"sante": -10, "rep": -3}, "Ils te le font payer.")),
        S("Ils exigent une première faveur : intimider un commerçant.",
          C("Obéir", .8, {"argent": 300, "karma": -8}, "Tu empoches ta commission.", {"rep": -5, "karma": -5}, "Le commerçant te dénonce."),
          C("Détourner l'ordre", ("st", "intel", 65), {"karma": 2, "rep": 3}, "Personne n'y voit rien.", {"sante": -12, "rep": -4}, "Ils te démasquent."))],
       {"gfor": 10, "argent": 400, "karma": -10}, "🕴️ Ton gang gagne un puissant protecteur.", need=1),
    SC("operation_police", "Opération anti-gangs de la police", "Tokyo Revengers", (16, 50), lambda g: nterr(g) >= 4, "Contrôler au moins 4 territoires", .08,
       [S("La police lance une grande opération contre les gangs de la ville. Tes territoires sont visés.",
          C("Disperser tes membres", .8, {"membres": -2, "rep": 3}, "Peu de pertes dans tes rangs.", {"membres": -5}, "Plusieurs membres sont arrêtés."),
          C("Corrompre un officier (200)", .65, {"argent": -200, "rep": 5}, "L'opération est détournée.", {"rep": -8, "karma": -4}, "L'officier te dénonce.")),
        S("Les médias réclament des têtes.",
          C("Faire profil bas", .9, {"rep": -1}, "La tempête passe.", {}, ""),
          C("Donner une interview", ("st", "rep", 70), {"rep": 8}, "Tu retournes l'opinion publique.", {"rep": -6}, "Tes propos choquent."))],
       {"xp": 50, "rep": 8}, "🚓 L'opération est derrière toi.", need=1),
    SC("tournoi_gangs", "Tournoi des gangs de Shibuya", "Tokyo Revengers", (15, 50), lambda g: _gang_rang(g, 1), "Faire partie d'un gang", .1,
       [S("Les gangs de Shibuya organisent un tournoi de combat.",
          C("Combat de qualification", ("pw", 90), {"xp": 20, "rep": 4}, "Tu passes le premier tour.", {"sante": -10}, "Tu es éliminé d'entrée."),
          C("Parier sur toi (100)", .6, {"argent": 150, "xp": 15}, "Ton pari est payant.", {"argent": -100}, "Tu perds ta mise.")),
        S("Demi-finale contre un champion de sports de combat.",
          C("Attaquer fort", ("pw", 120), {"xp": 30, "rep": 8}, "Tu le fais plier.", {"sante": -15}, "Il te contre."),
          C("Jouer la défense", ("st", "intel", 55), {"xp": 25, "rep": 6}, "Tu l'épuises.", {"sante": -10}, "Il perce ta garde.")),
        S("La finale, devant la foule en délire.",
          C("Tout donner", ("pw", 150), {"xp": 40, "rep": 12}, "Tu remportes le tournoi !", {"sante": -20}, "Tu perds de justesse."),
          C("Utiliser ta technique de style", ("pw", 140), {"xp": 40, "rep": 12}, "Ta technique fait mouche.", {"sante": -15}, "Il l'avait anticipée."))],
       {"xp": 60, "rep": 15, "gfor": 4}, "🏆 Tu remportes le tournoi des gangs !", need=2),
    # ───────────── TOKYO REVENGERS : incidents ─────────────
    AR("querelle_chefs", "Querelle entre chefs de gangs", "Tokyo Revengers", (15, 50), lambda g: bool(g["gang"]) and bool(g["fact"]), .1,
       [S("Le chef de {E} insulte publiquement ton gang lors d'une réunion.",
          C("Répliquer sèchement", ("st", "rep", 55), {"rep": 6, "relx": ["E", -6]}, "Tu cloues le bec à son chef.", {"rep": -3}, "Ta réplique se retourne contre toi."),
          C("Laisser couler", .9, {"karma": 2, "rep": -2}, "Tu gardes ton sang-froid.", {}, ""),
          C("Le provoquer en duel", ("pw", 120), {"xp": 25, "rep": 8}, "Tu le corriges devant tous.", {"sante": -15, "rep": -3}, "Tu perds contre lui.")),
        S("Les deux gangs se rassemblent, prêts à s'affronter.",
          C("Proposer une médiation", ("st", "intel", 55), {"karma": 4, "relx": ["E", 8]}, "La querelle s'éteint.", {"rep": -2}, "Personne ne veut discuter."),
          C("Mobiliser ton gang", .7, {"gfor": 3, "rep": 5, "ennemi": "E"}, "Tes membres répondent à l'appel.", {"membres": -2}, "Peu de gens se présentent."))],
       {"rep": 3}, "🔥 La querelle est close.", need=1),
    AR("trefve_rompue", "Une trêve est rompue avec {A}", "Tokyo Revengers", (15, 50), lambda g: bool(allies(g)) and bool(g["gang"]), .06,
       [S("Un membre de {A} a frappé l'un des tiens : la trêve est en péril.",
          C("Exiger des excuses", ("st", "rep", 55), {"relx": ["A", 3], "rep": 5}, "Ils s'excusent platement.", {"relx": ["A", -8]}, "Ils refusent de s'excuser."),
          C("Passer l'éponge", .9, {"karma": 3, "relx": ["A", 4]}, "La paix tient.", {"rep": -3}, "On te juge faible."),
          C("Rendre le coup", ("pw", 120), {"rep": 6, "relx": ["A", -10]}, "Tu marques ton territoire.", {"sante": -12, "relx": ["A", -12]}, "Tu es battu."))],
       {}, "", need=1),
    AR("indic", "Un indic dans ton gang", "Tokyo Revengers", (14, 50), lambda g: bool(g["gang"]), .08,
       [S("La police semble toujours un pas d'avance : quelqu'un parle dans ton gang.",
          C("Surveiller tes proches", ("st", "intel", 60), {"xp": 15, "rep": 4}, "Tu repères l'indic.", {"bonheur": -4}, "Tu soupçonnes à tort."),
          C("Tendre un piège", .6, {"xp": 20, "rep": 6}, "L'indic tombe dans le piège.", {"rep": -4}, "Le piège échoue.")),
        S("Que faire de l'indic ?",
          C("L'exclure du gang", .9, {"rep": 5}, "Il disparaît du quartier.", {}, ""),
          C("Le retourner contre la police", ("st", "intel", 65), {"xp": 25, "rep": 8}, "Tu l'utilises pour intoxiquer la police.", {"rep": -4}, "Il double son jeu."))],
       {"xp": 20}, "🕵️ Le gang est assaini.", need=1),
    AR("politicien", "Un politicien veut acheter ton gang", "Tokyo Revengers", (16, 50), lambda g: bool(g["gang"]) and g["rep"] >= 30, .06,
       [S("Un candidat aux élections locales te propose de l'argent pour que ton gang « sécurise » ses meetings.",
          C("Accepter", .8, {"argent": 500, "karma": -6, "gfor": 3}, "Tu empoches la mise.", {"rep": -8, "karma": -6}, "Un journaliste t'a repéré."),
          C("Refuser", 1, {"karma": 5, "rep": 3}, "Tu gardes ton indépendance.", {}, ""),
          C("Le faire chanter", ("st", "intel", 70), {"argent": 800, "karma": -10}, "Tu as un joli levier.", {"rep": -10, "sante": -10}, "Le piège se retourne contre toi."))],
       {}, "", need=1),
    AR("election", "Soutien électoral à un candidat", "Tokyo Revengers", (18, 50), lambda g: nterr(g) >= 2, .05,
       [S("Plusieurs candidats sollicitent ton gang pour obtenir des voix dans tes quartiers.",
          C("Soutenir le candidat honnête", .8, {"karma": 5, "rep": 6}, "Il l'emporte et te remercie.", {"rep": -2}, "Il perd, déçu."),
          C("Soutenir celui qui paie", .8, {"argent": 400, "karma": -6}, "Il gagne et t'enrichit.", {"rep": -6}, "Il perd et te réclame ton argent."),
          C("Rester hors du jeu", 1, {}, "Tu laisses la ville voter.", {}, ""))],
       {}, "", need=1),
    AR("scandale", "Scandale médiatique autour des gangs", "Tokyo Revengers", (15, 50), lambda g: bool(g["gang"]), .08,
       [S("Un reportage révèle les activités des gangs de la ville : ton nom est cité.",
          C("Nier en bloc", ("st", "intel", 55), {"rep": 3}, "Personne ne peut le prouver.", {"rep": -8}, "Les preuves t'accablent."),
          C("Assumer publiquement", ("st", "rep", 60), {"rep": 8, "karma": 2}, "Ton franc-parler plaît.", {"rep": -6}, "Ton discours choque."),
          C("Faire profil bas", .9, {"rep": -2}, "L'affaire s'éteint.", {}, ""))],
       {}, "", need=1),
    AR("mediation", "Médiation entre deux gangs", "Tokyo Revengers", (16, 50), lambda g: bool(g["gang"]) and g["rep"] >= 45 and bool(g["fact"]), .06,
       [S("Deux gangs voisins se déchirent. Ils te sollicitent comme médiateur.",
          C("Accepter la médiation", ("st", "rep", 65), {"rep": 10, "karma": 4, "relx": ["A", 4]}, "Ton arbitrage est respecté.", {"rep": -4}, "Ta médiation échoue."),
          C("Profiter du conflit", .65, {"argent": 300, "karma": -5}, "Tu vends tes services au plus offrant.", {"rep": -6}, "On te traite d'opportuniste."),
          C("Refuser", 1, {}, "Ce n'est pas ton problème.", {}, ""))],
       {}, "", need=1),
    AR("paix_gangs", "Proposition de paix de {E}", "Tokyo Revengers", (15, 50), lambda g: bool(ennemis(g)) and bool(g["gang"]), .12,
       [S("{E} envoie un émissaire proposer la paix entre vos gangs.",
          C("Accepter la paix", .9, {"paix": "E", "rep": 5, "karma": 3}, "La guerre cesse.", {"rep": -2}, "Les tiens refusent la paix."),
          C("Exiger un tribut", .6, {"paix": "E", "argent": 300}, "Ils paient pour la paix.", {"relx": ["E", -5], "rep": -3}, "Ils quittent la table."),
          C("Refuser", 1, {"rep": 3, "karma": -2}, "Tu veux la guerre.", {}, ""))],
       {}, "", need=1),
    # ───────────── KUROKO : scénarios et incidents ─────────────
    SC("revanche", "Revanche contre {E}", "Kuroko", (15, 40), lambda g: bool(ennemis(g)) and g["mait"] >= 40, "Un lycée ennemi et 40 de maîtrise", .12,
       [S("Le {E} t'a humilié il y a peu : l'occasion d'un match de revanche se présente.",
          C("Préparer un plan défensif", ("st", "intel", 55), {"mait": 3}, "Ton plan est affûté.", {"bonheur": -2}, "Ton plan manque de finesse."),
          C("S'entraîner en solo", .85, {"mait": 4, "force": 2}, "Tu progresses nettement.", {"sante": -5}, "Tu te blesses légèrement.")),
        S("Premier quart-temps de la revanche : ils te marquent de près.",
          C("Jouer la vitesse", ("pw", 120), {"xp": 20}, "Tu les surprends.", {"bonheur": -3}, "Ils te contiennent."),
          C("Jouer la passe", ("pw", 115), {"xp": 20}, "Votre collectif fonctionne.", {"bonheur": -3}, "Les passes sont interceptées.")),
        S("Dernières secondes, tout se joue sur un tir.",
          C("Tenter le tir", ("pw", 140), {"xp": 40, "rep": 10}, "Le ballon traverse le filet !", {"bonheur": -6}, "Le tir touche l'arceau."),
          C("Servir ton coéquipier", ("pw", 135), {"xp": 40, "rep": 10}, "Il conclut pour la victoire.", {"bonheur": -5}, "La passe est mal dosée."))],
       {"paix": "E", "rep": 12, "xp": 60}, "🏀 Revanche réussie : {E} te respecte désormais.", need=2),
    SC("camp_commun", "Camp d'entraînement commun avec {A}", "Kuroko", (14, 40), lambda g: bool(allies(g)), "Un lycée allié", .12,
       [S("Le {A} t'invite à un camp d'entraînement commun en montagne.",
          C("Y aller avec enthousiasme", .9, {"mait": 4, "relx": ["A", 5]}, "Tu t'entraînes aux côtés des meilleurs.", {"sante": -5}, "Tu te fatigues trop."),
          C("Proposer un tournoi interne", ("st", "rep", 45), {"rep": 5, "relx": ["A", 4]}, "L'idée plaît beaucoup.", {}, "")),
        S("La dernière soirée, tout le monde se confie autour du feu.",
          C("Partager tes doutes", .8, {"bonheur": 6, "intel": 1}, "Tu repars l'esprit léger.", {"bonheur": -1}, "Tu te sens un peu exposé."),
          C("Raconter des blagues", .8, {"bonheur": 5, "rep": 2}, "Tu es la star de la soirée.", {"bonheur": 1}, "Personne ne rit."))],
       {"relx": ["A", 10], "mait": 3, "bonheur": 6}, "🏕️ Ce camp commun renforce votre amitié.", need=1),
    SC("match_gala", "Match de gala des Miracles", "Kuroko", (16, 40), lambda g: any(v >= 60 for v in g["amitie"].values()),
       "Être ami avec un joueur de la Génération des Miracles", .1,
       [S("Tes amis de la Génération des Miracles organisent un match de gala et t'invitent.",
          C("Accepter avec joie", .95, {"bonheur": 6, "rep": 4}, "L'ambiance est électrique.", {}, ""),
          C("Demander à jouer face à eux", ("pw", 160), {"rep": 8, "xp": 20}, "Tu relèves le défi.", {"sante": -8}, "Ils te surclassent.")),
        S("Le match est intense. Chacun veut prouver sa valeur.",
          C("Jouer en duo avec un ami", .8, {"mait": 4, "rep": 6}, "Votre synergie est remarquable.", {"bonheur": -2}, "Vous vous gênez."),
          C("Défier le plus fort", ("pw", 180), {"mait": 5, "rep": 10}, "Tu tiens tête à un Miracle !", {"sante": -12}, "Tu es dépassé."))],
       {"rep": 15, "amitie": ["auto", 10]}, "⭐ Ce match de gala devient légendaire.", need=1),
    AR("polemique", "Polémique entre lycées", "Kuroko", (15, 40), lambda g: bool(g["lycee"]) and bool(g["fact"]), .08,
       [S("Un article accuse ton lycée d'avoir triché face au {E}. Les esprits s'échauffent.",
          C("Défendre ton équipe", ("st", "rep", 50), {"rep": 5, "relx": ["E", -4]}, "Tu prends la défense de ton lycée.", {"rep": -3}, "On t'accuse de mauvaise foi."),
          C("Appeler au calme", .85, {"karma": 4, "relx": ["E", 5]}, "Tes mots apaisent le débat.", {}, ""))],
       {}, "", need=1),
    AR("fede", "Réunion de la fédération de basket", "Kuroko", (16, 40), lambda g: bool(g["lycee"]), .05,
       [S("La fédération organise une réunion sur le règlement des tournois. Les lycées s'opposent.",
          C("Défendre le jeu offensif", ("st", "intel", 55), {"rep": 5}, "Ton avis est entendu.", {}, ""),
          C("Défendre l'équité", .8, {"karma": 4, "rep": 3, "relx": ["E", 3]}, "Tu es applaudi.", {"rep": -2}, "Le débat te dépasse."))],
       {}, "", need=1),
]
ARCS.extend(ARCS_POL)
for _a in ARCS_POL: ARC_BY_ID[_a["id"]] = _a

# ═════════════ Banque d'événements supplémentaires ═════════════
# V(univers|None, âge min, âge max, texte, *choix, cond=None) — choix : C(libellé, p, eff_ok, txt_ok, eff_ko, txt_ko)
# cond : "flag:x", "noflag:x", "couple", "nocouple", "enfant", "riche", "pauvre", "celeb", "ecole", "ennemi", "gang", "pro"...
def V(u, a0, a1, t, *ch, cond=None):
    return (u, a0, a1, t, list(ch), cond)


EV_MORE = [
    # ───────────── Petite enfance (tous) ─────────────
    V(None, 1, 3, "🍼 Tu prononces enfin tes premiers mots. Toute la famille retient son souffle.",
      C("« Maman ! »", 1, {"bonheur": 4, "intel": 1}, "Ta mère fond en larmes de joie.", {}, ""),
      C("« Papa ! »", 1, {"bonheur": 4, "intel": 1}, "Ton père rayonne.", {}, ""),
      C("Un mot inventé", 1, {"intel": 2}, "Tout le monde éclate de rire.", {}, "")),
    V(None, 2, 5, "🛒 Tu te perds dans un marché bondé.",
      C("Appeler à pleins poumons", .8, {"bonheur": -2, "intel": 1}, "Un adulte te ramène vite à tes parents.", {"bonheur": -5}, "Tu pleures longtemps avant d'être retrouvé."),
      C("Attendre sans bouger", .9, {"intel": 2}, "Tes parents te retrouvent, rassurés.", {"bonheur": -2}, "Le temps te paraît interminable."),
      C("Suivre un inconnu", .3, {"bonheur": 3}, "Il t'offre des bonbons et te ramène.", {"sante": -5, "bonheur": -6}, "Tu t'enfonces dans des ruelles et tu as très peur.")),
    V(None, 3, 6, "🐱 Un chat errant te suit jusqu'à la maison.",
      C("L'adopter", .6, {"bonheur": 6, "karma": 2, "flag": "ev_chat"}, "Tes parents cèdent : tu as un compagnon !", {"bonheur": -2}, "Tes parents refusent, tu pleures."),
      C("Lui donner du lait", 1, {"bonheur": 3, "karma": 2}, "Le chat ronronne puis s'en va.", {}, ""),
      C("Le chasser", 1, {"karma": -2}, "Il s'enfuit, miaulant.", {}, "")),
    V(None, 2, 6, "🌙 Un cauchemar te réveille en pleine nuit.",
      C("Appeler tes parents", .95, {"bonheur": 3, "sante": 2}, "Ils te rassurent jusqu'à l'aube.", {}, ""),
      C("Affronter ta peur seul", .5, {"force": 1, "intel": 1}, "Tu te rendors fier de toi.", {"bonheur": -4}, "Tu ne dors plus de la nuit."),
      C("Te cacher sous la couette", 1, {"bonheur": 1}, "Ça fonctionne, plus ou moins.", {}, "")),
    V(None, 3, 6, "🖍️ Tu as dessiné sur le mur du salon.",
      C("Avouer", .8, {"karma": 3, "intel": 1}, "Tes parents apprécient ton honnêteté.", {"bonheur": -3}, "Tu es puni quand même."),
      C("Accuser le chat", .4, {"bonheur": 2}, "Personne ne te soupçonne.", {"karma": -3, "bonheur": -4}, "Personne n'est dupe : punition double."),
      C("Dire que c'est de l'art", .5, {"intel": 2, "bonheur": 3}, "Ta mère encadre le dessin !", {"bonheur": -2}, "Tu dois frotter le mur.")),
    V(None, 4, 7, "🧸 Un enfant du quartier te prend ton jouet préféré.",
      C("Te battre pour le récupérer", .5, {"force": 2, "rep": 1}, "Tu récupères ton jouet.", {"sante": -4, "bonheur": -3}, "Tu reçois quelques bleus."),
      C("Proposer d'échanger", .8, {"intel": 2, "karma": 2}, "Vous devenez amis.", {"bonheur": -2}, "Il refuse et file."),
      C("Appeler un adulte", .9, {"bonheur": 1}, "Le jouet te revient.", {}, "")),
    V(None, 1, 5, "🤒 Tu as une forte fièvre.",
      C("Rester au lit", .95, {"sante": 6, "bonheur": -1}, "Tu guéris vite.", {"sante": -3}, "La fièvre traîne un peu."),
      C("Boire la soupe de ta grand-mère", 1, {"sante": 4, "bonheur": 3}, "Un vrai remède de famille.", {}, ""),
      C("Désobéir et sortir jouer", .3, {"bonheur": 4}, "Tu t'en sors miraculeusement.", {"sante": -10}, "Tu rechutes lourdement.")),
    V(None, 5, 6, "🎂 Pour ton anniversaire, tes parents te laissent choisir.",
      C("Une grande fête", 1, {"bonheur": 6, "argent": -30}, "Une fête inoubliable !", {}, ""),
      C("Un cadeau unique", 1, {"intel": 2, "bonheur": 3}, "Un cadeau qui te suivra longtemps.", {}, ""),
      C("Une sortie en famille", 1, {"bonheur": 5, "karma": 1}, "Un beau souvenir partagé.", {}, "")),
    # ───────────── Enfance (tous) ─────────────
    V(None, 6, 11, "📚 Un camarade te demande de copier ton devoir.",
      C("Le laisser faire", .6, {"karma": -1, "popu": 4}, "Il t'en est reconnaissant.", {"karma": -2, "notes": -4}, "Le professeur vous surprend tous les deux."),
      C("Refuser gentiment", .9, {"karma": 2, "notes": 2}, "Il comprend.", {"popu": -3}, "Il boude."),
      C("Lui proposer de l'aider à comprendre", .8, {"karma": 4, "intel": 2, "popu": 3}, "Vous étudiez ensemble.", {"bonheur": -1}, "Il n'écoute pas.")),
    V(None, 6, 13, "👛 Tu trouves un portefeuille dans la rue.",
      C("Le rapporter à son propriétaire", .9, {"karma": 6, "argent": 30}, "Le propriétaire te récompense.", {"karma": 3}, "Personne ne te remercie vraiment."),
      C("Garder l'argent", .6, {"argent": 120, "karma": -6}, "Tu empoches la somme.", {"karma": -6, "rep": -3, "bonheur": -4}, "On t'a vu : tu es pris."),
      C("Le déposer au poste", 1, {"karma": 3}, "Tu fais ce qu'il faut.", {}, "")),
    V(None, 7, 12, "🥊 Une bagarre éclate dans la cour de récréation.",
      C("Intervenir pour séparer", .5, {"karma": 4, "rep": 3, "popu": 3}, "Tu calmes tout le monde.", {"sante": -5, "popu": -2}, "Tu reçois un coup perdu."),
      C("Y participer", .5, {"force": 2, "rep": 2, "karma": -2}, "Tu gagnes la bagarre.", {"sante": -8, "notes": -3}, "Tu perds et tu es puni."),
      C("Appeler un professeur", .9, {"notes": 2, "popu": -2}, "Les adultes prennent le relais.", {}, ""),
      C("Filmer… en pensée", 1, {}, "Tu regardes de loin, impassible.", {}, "")),
    V(None, 8, 14, "💬 Une rumeur étrange circule sur toi à l'école.",
      C("La démentir publiquement", ("st", "rep", 30), {"rep": 3, "popu": 4}, "Les gens te croient.", {"popu": -4}, "Personne ne te croit."),
      C("L'ignorer", .7, {"bonheur": 1}, "Elle finit par s'éteindre.", {"bonheur": -4, "popu": -3}, "Elle enfle au contraire."),
      C("Remonter à la source", ("st", "intel", 40), {"intel": 2, "karma": 1, "rep": 2}, "Tu démasques le coupable.", {"bonheur": -2}, "Tu accuses la mauvaise personne.")),
    V(None, 9, 14, "💘 Tu ressens un premier béguin pour quelqu'un de ta classe.",
      C("Lui écrire un mot", .5, {"bonheur": 6}, "La réponse est positive !", {"bonheur": -5}, "Le mot circule dans toute la classe…"),
      C("Rester discret(e)", 1, {"bonheur": 1}, "Ton secret reste intact.", {}, ""),
      C("Demander conseil à un ami", .8, {"bonheur": 3, "intel": 1}, "Il t'aide à te lancer.", {"bonheur": -2}, "Il raconte tout à tout le monde.")),
    V(None, 8, 13, "🎒 L'école organise un voyage scolaire.",
      C("Y aller avec enthousiasme", 1, {"bonheur": 5, "intel": 2, "argent": -30}, "Tu reviens avec des souvenirs plein la tête.", {}, ""),
      C("Rester et étudier", 1, {"notes": 3, "intel": 1}, "Tu progresses en classe.", {}, ""),
      C("Faire une bêtise pendant le voyage", .5, {"popu": 5, "bonheur": 4}, "Les anecdotes t'amusent encore.", {"notes": -4, "rep": -2}, "Tu es sermonné.")),
    V(None, 6, 12, "🎹 On te propose d'apprendre un instrument.",
      C("Le piano", 1, {"intel": 3, "bonheur": 2, "argent": -20}, "Tu fais de rapides progrès.", {}, ""),
      C("La guitare", 1, {"popu": 4, "bonheur": 3, "argent": -20}, "Tu deviens la vedette de la récré.", {}, ""),
      C("La flûte", 1, {"intel": 1, "bonheur": 2}, "Tes voisins en profitent aussi…", {}, ""),
      C("Refuser", 1, {}, "Tu préfères jouer dehors.", {}, "")),
    V(None, 7, 13, "👴 Un voisin âgé a du mal à porter ses courses.",
      C("L'aider avec le sourire", 1, {"karma": 5, "bonheur": 3, "argent": 10}, "Il te glisse une petite pièce.", {}, ""),
      C("Faire semblant de ne pas voir", 1, {"karma": -2}, "Tu files sans te retourner.", {}, ""),
      C("Lui proposer de revenir chaque semaine", .8, {"karma": 6, "rep": 2, "argent": 20, "flag": "ev_voisin"}, "Une belle habitude s'installe.", {"bonheur": -1}, "Tu abandonnes au bout de deux fois.")),
    V(None, 6, 11, "🐕 Tu supplies tes parents de t'offrir un animal de compagnie.",
      C("Promettre de t'en occuper", .6, {"bonheur": 6, "karma": 2}, "Tes parents cèdent !", {"bonheur": -3}, "Refusé, une fois de plus."),
      C("Faire une grève de la faim… de dessert", .4, {"bonheur": 4}, "Ça marche !", {"bonheur": -4, "sante": -1}, "Tes parents ne bronchent pas."),
      C("Te contenter d'un poisson rouge", 1, {"bonheur": 2, "argent": -10}, "Un compagnon discret.", {}, "")),
    V(None, 8, 13, "🏫 Ton professeur te remarque : il te propose un exercice plus avancé.",
      C("Relever le défi", ("st", "intel", 45), {"intel": 3, "notes": 5, "rep": 2}, "Tu brilles devant toute la classe.", {"notes": -3, "bonheur": -3}, "Tu sèches lamentablement."),
      C("Refuser par modestie", 1, {"bonheur": 1}, "Tu préfères rester discret.", {}, ""),
      C("Demander de l'aide à un camarade", .7, {"intel": 2, "popu": 3}, "Vous réussissez à deux.", {"popu": -2}, "Le professeur n'est pas dupe.")),
    V(None, 6, 12, "🧪 Tu fais une expérience « scientifique » dans la cuisine.",
      C("Mélanger tout ce que tu trouves", .4, {"intel": 3, "bonheur": 4}, "Un petit volcan magnifique !", {"sante": -5, "bonheur": -4, "argent": -15}, "Explosion : cuisine ravagée."),
      C("Suivre un livre", .95, {"intel": 3, "notes": 2}, "Tu réussis ton expérience.", {}, ""),
      C("Demander l'aide d'un adulte", 1, {"intel": 2, "karma": 1}, "Tu apprends en toute sécurité.", {}, "")),
    V(None, 9, 14, "🎉 Un camarade t'invite à sa fête d'anniversaire.",
      C("Y aller avec un cadeau (30)", 1, {"popu": 4, "bonheur": 4, "argent": -30}, "Tu passes un excellent moment.", {}, ""),
      C("Y aller sans cadeau", .7, {"popu": 2, "bonheur": 3}, "Personne ne le remarque.", {"popu": -3, "bonheur": -2}, "Son frère te lance un regard noir."),
      C("Décliner poliment", 1, {"bonheur": -1}, "Tu restes chez toi.", {}, "")),
    # ───────────── Adolescence (tous) ─────────────
    V(None, 12, 18, "🧾 Les examens approchent. La pression monte.",
      C("Réviser jour et nuit", .85, {"notes": 8, "intel": 3, "sante": -4}, "Tu décroches d'excellents résultats.", {"notes": 3, "sante": -6, "bonheur": -4}, "Tu t'épuises pour des résultats moyens."),
      C("Réviser en groupe", .8, {"notes": 5, "popu": 4, "intel": 2}, "Vous vous motivez mutuellement.", {"notes": 1}, "La séance dérive en bavardages."),
      C("Compter sur la chance", .3, {"bonheur": 3}, "Tu t'en sors miraculeusement.", {"notes": -8, "bonheur": -5}, "C'est la catastrophe."),
      C("Tricher", .5, {"notes": 5, "karma": -4}, "Personne ne s'en aperçoit.", {"notes": -8, "rep": -5, "karma": -4}, "Tu es pris : convocation chez le directeur.")),
    V(None, 14, 18, "💼 Un job d'été t'est proposé.",
      C("Serveur dans un restaurant", .9, {"argent": 200, "popu": 2, "sante": -2}, "Tu gagnes ton premier salaire !", {"argent": 80, "bonheur": -3}, "Le patron est odieux."),
      C("Livreur à vélo", .8, {"argent": 180, "force": 2, "sante": 1}, "Tu te muscles les jambes.", {"argent": 60, "sante": -5}, "Tu fais une chute."),
      C("Aider un artisan", .9, {"argent": 150, "intel": 2, "mait": 1}, "Tu apprends un métier.", {"argent": 50}, "Il n'a pas de quoi te payer."),
      C("Passer l'été à te reposer", 1, {"bonheur": 6, "sante": 3}, "Un été de rêve.", {}, "")),
    V(None, 13, 18, "🎶 Une soirée est organisée chez un camarade.",
      C("Y aller et profiter", .75, {"bonheur": 6, "popu": 5}, "Tu t'amuses énormément.", {"sante": -4, "bonheur": -2, "popu": -2}, "La soirée dégénère."),
      C("Y aller en restant raisonnable", .9, {"bonheur": 3, "popu": 3, "karma": 1}, "Une soirée agréable.", {}, ""),
      C("Rester réviser", 1, {"notes": 3, "intel": 1}, "Tu rates la soirée, mais pas ton examen.", {}, "")),
    V(None, 13, 17, "😠 Une dispute éclate avec ton meilleur ami.",
      C("Présenter des excuses", .8, {"karma": 3, "bonheur": 4}, "Vous vous réconciliez.", {"bonheur": -3}, "Il refuse tes excuses."),
      C("Attendre que ça passe", .5, {"bonheur": 2}, "Le temps arrange tout.", {"bonheur": -5}, "Il s'éloigne pour de bon."),
      C("Tenir bon sur ta position", .5, {"rep": 3}, "Il finit par admettre son tort.", {"bonheur": -4, "popu": -3}, "Vous ne vous parlez plus.")),
    V(None, 14, 19, "💔 Ta première relation amoureuse prend fin.",
      C("Pleurer avec tes amis", 1, {"bonheur": -2, "popu": 2}, "Tu es bien entouré.", {}, ""),
      C("Te plonger dans le travail", .8, {"intel": 3, "bonheur": -3}, "Tu canalises ta peine.", {"bonheur": -6}, "Tu t'enfermes dans ta peine."),
      C("Te lancer dans un nouveau défi", .7, {"mait": 3, "force": 2}, "Tu en ressors plus fort(e).", {"bonheur": -4}, "Tu te disperses.")),
    V(None, 15, 19, "🧭 Il faut choisir ton orientation pour les années à venir.",
      C("Suivre ta passion", .7, {"bonheur": 5, "mait": 3}, "Tu te sens enfin à ta place.", {"bonheur": -3, "argent": -50}, "Tes parents ne sont pas convaincus."),
      C("Choisir la voie sûre", .9, {"intel": 3, "argent": 50}, "Un avenir stable s'ouvre à toi.", {"bonheur": -2}, "Tu t'ennuies déjà."),
      C("Prendre une année sabbatique", .6, {"bonheur": 6, "intel": 1, "argent": -80}, "Tu voyages et tu grandis.", {"argent": -120, "bonheur": -2}, "Tu t'ennuies et dépenses.")),
    V(None, 13, 18, "🕵️ Tu découvres un secret de ta famille.",
      C("Interroger tes parents", .7, {"intel": 2, "bonheur": -2, "karma": 2}, "La vérité est difficile mais libératrice.", {"bonheur": -5}, "Ils refusent d'en parler."),
      C("Mener ta propre enquête", ("st", "intel", 50), {"intel": 3, "xp": 10}, "Tu reconstitues toute l'histoire.", {"bonheur": -3}, "Tu te perds en conjectures."),
      C("L'oublier", 1, {"bonheur": 1}, "Certains secrets valent mieux ignorés.", {}, "")),
    V(None, 12, 17, "😞 Un élève est harcelé devant toi.",
      C("Le défendre", .6, {"karma": 8, "rep": 4, "popu": 2}, "Le harceleur recule.", {"sante": -6, "popu": -3}, "Tu es pris à partie à ton tour."),
      C("Prévenir un adulte", .9, {"karma": 4, "notes": 1}, "L'école intervient.", {}, ""),
      C("Rester spectateur", 1, {"karma": -5, "bonheur": -3}, "Tu t'en veux longtemps.", {}, ""),
      C("Te joindre aux moqueries", .5, {"popu": 4, "karma": -10}, "Tu gagnes en popularité… et perds ton âme.", {"popu": -4, "karma": -10, "rep": -3}, "On t'en fait voir de toutes les couleurs.")),
    V(None, 14, 18, "💸 Tu hésites entre dépenser ou économiser ton argent de poche.",
      C("Tout dépenser (60)", 1, {"bonheur": 5, "argent": -60}, "Un plaisir immédiat.", {}, ""),
      C("Économiser", 1, {"argent": 40, "intel": 1}, "Une cagnotte qui grandit.", {}, ""),
      C("Investir dans du matériel", .8, {"mait": 2, "argent": -40}, "Un bon achat.", {"argent": -40, "bonheur": -2}, "Tu regrettes l'achat.")),
    V(None, 15, 19, "🛵 Un ami te propose de conduire sa moto sans permis.",
      C("Accepter", .5, {"bonheur": 6, "rep": 2}, "Une sensation de liberté inoubliable !", {"sante": -12, "bonheur": -3, "argent": -80}, "Tu tombes : égratignures et amende."),
      C("Refuser", 1, {"karma": 2, "intel": 1}, "Tu restes prudent(e).", {}, ""),
      C("Lui conseiller de ne pas le faire non plus", .7, {"karma": 4, "rep": 1}, "Il t'écoute.", {"popu": -2}, "Il se moque de toi.")),
    V(None, 13, 18, "🔥 Un ami te confie un lourd secret.",
      C("Le garder pour toi", 1, {"karma": 3, "bonheur": 1}, "Votre confiance se renforce.", {}, ""),
      C("Le répéter à quelqu'un de confiance", .5, {"karma": 1}, "Tu espères bien faire.", {"bonheur": -5, "karma": -3}, "Il apprend que tu as parlé."),
      C("T'en servir", .5, {"rep": 3, "karma": -8}, "Ça te sert, mais tu t'en veux.", {"rep": -6, "karma": -8, "bonheur": -4}, "Il te démasque.")),
    V(None, 16, 20, "🏆 Un concours local est ouvert à tous.",
      C("Participer", ("st", "mait", 40), {"rep": 5, "argent": 100, "xp": 20}, "Tu remportes un prix !", {"bonheur": -2}, "Tu fais une belle figuration."),
      C("Observer d'abord", 1, {"intel": 2}, "Tu apprends des meilleurs.", {}, ""),
      C("Aider à l'organisation", .9, {"karma": 3, "rep": 2, "argent": 30}, "Tu te fais des contacts.", {}, "")),
    # ───────────── Jeunes adultes (tous) ─────────────
    V(None, 18, 30, "🚚 Tu envisages de déménager.",
      C("Changer de ville", .7, {"bonheur": 4, "intel": 2, "argent": -80}, "Un nouveau départ prometteur.", {"bonheur": -4, "argent": -100}, "Tu regrettes ton ancien quartier."),
      C("Rester près de ta famille", 1, {"bonheur": 3, "karma": 1}, "Tu restes bien entouré.", {}, ""),
      C("Partir à l'étranger", .5, {"intel": 4, "xp": 25, "bonheur": 3, "argent": -200}, "Une expérience inoubliable.", {"bonheur": -5, "argent": -200}, "Le mal du pays te ronge.")),
    V(None, 20, 40, "💍 Ton partenaire te parle de mariage.",
      C("Dire oui", .8, {"bonheur": 10, "argent": -150}, "Une belle cérémonie !", {"bonheur": -4}, "Vous vous disputez sur les préparatifs.", ), 
      C("Demander du temps", .9, {"intel": 1}, "Votre relation respire.", {"bonheur": -3}, "Il/elle le prend mal."),
      C("Refuser", 1, {"bonheur": -6}, "Une conversation difficile.", {}, ""), cond="couple"),
    V(None, 18, 35, "💳 Tu t'endettes plus que prévu.",
      C("Négocier un échéancier", ("st", "intel", 55), {"argent": 30, "karma": 1}, "Le créancier accepte.", {"argent": -60, "bonheur": -3}, "Il refuse tout compromis."),
      C("Travailler plus", .85, {"argent": 100, "sante": -5}, "Tu rembourses vite.", {"sante": -8}, "Tu t'épuises."),
      C("Ignorer la dette", .3, {"bonheur": 2}, "Ça se tasse.", {"argent": -200, "rep": -5, "flag": "ev_dette"}, "La dette s'aggrave et te poursuit.")),
    V(None, 18, 40, "🤔 Une crise existentielle te frappe : que veux-tu vraiment faire de ta vie ?",
      C("Chercher un but", .7, {"bonheur": 4, "intel": 2, "xp": 15}, "Tu redéfinis tes priorités.", {"bonheur": -5}, "Tu tournes en rond."),
      C("Partir en voyage", .8, {"bonheur": 6, "argent": -120, "intel": 2}, "Le voyage te remet les idées en place.", {"argent": -120, "bonheur": -2}, "Tu reviens plus perdu."),
      C("Te noyer dans le travail", .8, {"xp": 20, "bonheur": -3}, "Tu avances, au moins.", {"sante": -6, "bonheur": -5}, "Tu craques.")),
    V(None, 18, 35, "💸 Un ami te propose un investissement « miracle ».",
      C("Investir (200)", .35, {"argent": 600, "rep": 2}, "Tu triples ta mise !", {"argent": -200, "bonheur": -5}, "Tu perds tout."),
      C("Demander à voir les comptes", ("st", "intel", 55), {"intel": 2, "karma": 1}, "Tu évites une arnaque.", {"bonheur": -1}, "Tu n'y comprends rien."),
      C("Refuser", 1, {}, "Tu restes prudent(e).", {}, "")),
    V(None, 20, 45, "👪 Un proche tombe gravement malade.",
      C("Passer du temps à ses côtés", .9, {"karma": 5, "bonheur": -3, "intel": 1}, "Votre lien en sort renforcé.", {"bonheur": -6}, "Tu t'effondres devant lui."),
      C("Payer ses soins (300)", 1, {"argent": -300, "karma": 6}, "Il est sauvé.", {}, ""),
      C("Prendre de la distance", 1, {"karma": -5, "bonheur": -3}, "Tu te sens coupable.", {}, "")),
    V(None, 20, 45, "🧳 Un ancien camarade réapparaît et te propose de monter un projet ensemble.",
      C("Accepter", .6, {"argent": 300, "xp": 25, "rep": 3}, "Le projet est un succès.", {"argent": -150, "bonheur": -4}, "Le projet tourne court."),
      C("Prendre le temps de réfléchir", .9, {"intel": 2}, "Tu poses les bonnes questions.", {}, ""),
      C("Refuser", 1, {}, "Chacun sa route.", {}, "")),
    V(None, 18, 45, "🎭 Tu es témoin d'un vol à l'étalage.",
      C("Intervenir", .5, {"karma": 5, "rep": 3}, "Le voleur est arrêté.", {"sante": -8, "rep": -1}, "Le voleur te pousse et s'enfuit."),
      C("Prévenir la sécurité", .9, {"karma": 2}, "L'affaire est réglée.", {}, ""),
      C("Détourner le regard", 1, {"karma": -2}, "Tu ne veux pas t'en mêler.", {}, "")),
    V(None, 22, 50, "🎓 On te propose de transmettre ton savoir à des jeunes.",
      C("Accepter avec joie", .9, {"karma": 5, "rep": 5, "bonheur": 4, "intel": 1}, "Tes élèves t'adorent.", {"bonheur": -2}, "L'enseignement s'avère épuisant."),
      C("Poser des conditions", ("st", "rep", 40), {"argent": 100, "rep": 3}, "Un bon arrangement.", {"rep": -1}, "L'organisateur renonce."),
      C("Décliner", 1, {}, "Tu n'as pas le temps.", {}, "")),
    V(None, 20, 50, "🕊️ Tu retrouves d'anciens amis d'enfance.",
      C("Organiser des retrouvailles", .85, {"bonheur": 8, "popu": 3}, "Une soirée magique.", {"bonheur": -3}, "Les retrouvailles sont gênantes."),
      C("Garder le contact par lettres", 1, {"bonheur": 3}, "Vous restez liés.", {}, ""),
      C("Les éviter", 1, {"bonheur": -2}, "Le passé reste le passé.", {}, "")),
    # ───────────── Âge adulte (tous) ─────────────
    V(None, 30, 55, "📈 Une promotion s'offre à toi.",
      C("Foncer", ("st", "rep", 45), {"argent": 250, "rep": 6, "xp": 25}, "Tu décroches le poste !", {"bonheur": -3}, "Un concurrent est préféré."),
      C("Négocier ton salaire", ("st", "intel", 50), {"argent": 350, "rep": 3}, "Tu obtiens bien plus.", {"rep": -2}, "La direction se braque."),
      C("Refuser pour garder ta liberté", 1, {"bonheur": 4}, "Tu préfères ta tranquillité.", {}, "")),
    V(None, 30, 55, "💢 Ta relation de couple traverse une crise.",
      C("En parler franchement", .7, {"bonheur": 6, "karma": 2}, "Vous vous retrouvez.", {"bonheur": -6}, "La discussion dégénère."),
      C("Proposer un voyage à deux (150)", .85, {"bonheur": 8, "argent": -150}, "Une parenthèse enchantée.", {"argent": -150, "bonheur": -2}, "Le voyage ne change rien."),
      C("Faire comme si de rien n'était", .4, {"bonheur": 1}, "La tempête passe.", {"bonheur": -8}, "Le silence vous éloigne."), cond="couple"),
    V(None, 30, 60, "😮‍💨 Tu frôles le burn-out.",
      C("Prendre des vacances", .95, {"sante": 8, "bonheur": 6, "argent": -100}, "Tu te ressources.", {"sante": 3}, "Tu pensais au travail tout le temps."),
      C("Consulter un spécialiste (100)", 1, {"sante": 6, "intel": 1, "argent": -100}, "Un bon accompagnement.", {}, ""),
      C("Continuer à travailler", .3, {"xp": 20, "argent": 120}, "Tu tiens bon.", {"sante": -20, "bonheur": -8}, "Tu t'effondres.")),
    V(None, 30, 55, "🏠 Tu envisages d'acheter une maison.",
      C("Acheter (400)", ("st", "rep", 30), {"argent": -400, "bonheur": 8, "karma": 1}, "Un vrai chez-soi.", {"argent": -150, "bonheur": -2}, "Le prêt est refusé."),
      C("Louer encore", 1, {"argent": 40}, "Tu gardes ta liberté.", {}, ""),
      C("Retaper une ruine", .5, {"argent": -250, "mait": 2, "bonheur": 6}, "Elle est magnifique !", {"argent": -350, "bonheur": -4}, "Un gouffre financier.")),
    V(None, 30, 60, "🪞 Tu croises un ancien rival devenu un ami… ou presque.",
      C("Lui tendre la main", .7, {"karma": 4, "bonheur": 5}, "Vous enterrez la hache de guerre.", {"bonheur": -2}, "Il t'ignore."),
      C("Défier ton ancien rival", ("pw", 120), {"rep": 5, "xp": 20}, "Tu confirmes ta supériorité.", {"rep": -3, "bonheur": -3}, "Il te surpasse encore."),
      C("L'éviter", 1, {}, "Certaines histoires restent closes.", {}, "")),
    V(None, 35, 60, "🎗️ Une association te demande de l'aide pour une cause.",
      C("Donner de l'argent (150)", 1, {"karma": 6, "argent": -150, "rep": 2}, "Ton geste est salué.", {}, ""),
      C("Donner du temps", .9, {"karma": 6, "bonheur": 4, "sante": -1}, "Tu te sens utile.", {}, ""),
      C("Décliner", 1, {}, "Pas cette fois.", {}, "")),
    V(None, 35, 60, "🩺 Un bilan de santé révèle un petit souci.",
      C("Suivre le traitement", .9, {"sante": 8}, "Tu te sens mieux.", {"sante": 2}, "Les effets tardent."),
      C("Changer de mode de vie", .7, {"sante": 6, "bonheur": 3, "force": 1}, "Tu retrouves la forme.", {"bonheur": -2}, "Tu abandonnes en route."),
      C("Ignorer l'avertissement", .4, {"bonheur": 1}, "Rien ne se passe.", {"sante": -12}, "Ça s'aggrave.")),
    V(None, 30, 55, "👶 L'un de tes enfants a du mal à l'école.",
      C("L'aider à réviser", .8, {"karma": 4, "bonheur": 4}, "Il remonte la pente.", {"bonheur": -2}, "Vous vous disputez."),
      C("Engager un répétiteur (100)", 1, {"argent": -100, "karma": 2}, "Les notes remontent.", {}, ""),
      C("Le laisser se débrouiller", .5, {"bonheur": 1}, "Il apprend l'autonomie.", {"bonheur": -4, "karma": -2}, "Ses résultats chutent."), cond="enfant"),
    # ───────────── Âge mûr / vieillesse (tous) ─────────────
    V(None, 50, 90, "📜 Tu songes à écrire tes mémoires.",
      C("Te mettre à l'écriture", .8, {"intel": 3, "rep": 4, "bonheur": 5}, "Ton récit touche beaucoup de monde.", {"bonheur": -2}, "Tu ne dépasses pas le premier chapitre."),
      C("Raconter à voix haute", 1, {"bonheur": 4, "karma": 1}, "Tes proches boivent tes paroles.", {}, ""),
      C("Garder tes souvenirs pour toi", 1, {"bonheur": 1}, "Certaines choses restent privées.", {}, "")),
    V(None, 50, 90, "🌅 Une vague de nostalgie te submerge.",
      C("Revisiter les lieux de ton enfance", .85, {"bonheur": 7, "intel": 1}, "Un pèlerinage touchant.", {"bonheur": -3}, "Tout a changé."),
      C("Feuilleter de vieilles photos", 1, {"bonheur": 4}, "Les souvenirs affluent.", {}, ""),
      C("Aller de l'avant", 1, {"xp": 10}, "Le passé est le passé.", {}, "")),
    V(None, 55, 95, "👨‍👩‍👧‍👦 Ta famille se réunit pour fêter tes dernières années.",
      C("Prononcer un discours", .8, {"bonheur": 8, "karma": 3}, "Un moment d'émotion.", {"bonheur": 2}, "Tu t'emmêles les mots, mais tout le monde rit."),
      C("Offrir un cadeau à chacun (200)", 1, {"argent": -200, "karma": 5, "bonheur": 6}, "Tout le monde est touché.", {}, ""),
      C("Rester en retrait", 1, {"bonheur": 2}, "Tu profites du moment.", {}, ""), cond="couple"),
    V(None, 55, 95, "🍵 Tu te découvres une passion tardive : le jardinage.",
      C("T'y consacrer", .9, {"bonheur": 6, "sante": 3}, "Ton jardin est magnifique.", {"bonheur": 1}, "Les mauvaises herbes ont gagné."),
      C("Partager tes récoltes", 1, {"karma": 4, "rep": 2, "bonheur": 4}, "Le voisinage t'adore.", {}, ""),
      C("Abandonner", 1, {}, "Ce n'était qu'une lubie.", {}, "")),
    V(None, 60, 95, "⚰️ Tu fais ton testament.",
      C("Tout léguer à ta famille", 1, {"karma": 4, "bonheur": 3}, "Un geste apaisant.", {}, ""),
      C("Faire un don à une cause", 1, {"karma": 8, "rep": 4}, "Ta mémoire sera honorée.", {}, ""),
      C("Garder tout jusqu'au bout", 1, {"bonheur": 1}, "Rien ne presse.", {}, "")),
    V(None, 60, 95, "🚶 Un jeune te demande conseil pour sa vie.",
      C("Lui raconter tes erreurs", 1, {"karma": 5, "bonheur": 4, "rep": 2}, "Il t'écoute avec attention.", {}, ""),
      C("Lui donner un conseil brutal", .6, {"rep": 3, "karma": 1}, "Il saura s'en souvenir.", {"bonheur": -2}, "Il ne revient jamais."),
      C("Esquiver la question", 1, {}, "Tu changes de sujet.", {}, "")),
    # ───────────── Suites d'événements (selon tes choix passés) ─────────────
    V(None, 8, 40, "🐱 Ton vieux chat te cherche partout : il est malade.",
      C("L'emmener chez le vétérinaire (60)", 1, {"argent": -60, "karma": 4, "bonheur": 3}, "Il se rétablit !", {}, ""),
      C("Le soigner toi-même", ("st", "intel", 40), {"bonheur": 4, "karma": 2}, "Tes soins le sauvent.", {"bonheur": -6}, "Tu arrives trop tard."), cond="flag:ev_chat"),
    V(None, 12, 60, "👴 Ton ancien voisin te fait un cadeau pour te remercier de ton aide.",
      C("Accepter", 1, {"argent": 100, "karma": 3, "bonheur": 4}, "Un geste qui te touche.", {}, ""),
      C("Refuser poliment", 1, {"karma": 5, "bonheur": 3}, "Il insiste pour t'offrir le thé.", {}, ""), cond="flag:ev_voisin"),
    V(None, 20, 60, "📞 Ton créancier te relance sérieusement.",
      C("Rembourser (250)", 1, {"argent": -250, "karma": 2, "bonheur": 3, "flag": "ev_dette_ok"}, "Tu es enfin libéré de cette dette.", {}, ""),
      C("Négocier", ("st", "rep", 40), {"argent": -100, "karma": 1}, "Un accord est trouvé.", {"argent": -300, "rep": -4}, "La dette double."),
      C("Fuir", .3, {"bonheur": 2}, "Tu t'en sors, pour l'instant.", {"rep": -8, "argent": -300, "sante": -5}, "Il te retrouve, furieux."), cond="flag:ev_dette"),
]

EV_MORE += [
    # ═══════════ NARUTO ═══════════
    V("Naruto", 6, 11, "🏫 À l'Académie, l'instructeur organise un exercice de lancer de kunai.",
      C("Viser la cible au centre", ("st", "mait", 12), {"mait": 3, "popu": 3, "xp": 5}, "Plein centre !", {"bonheur": -2}, "Ton kunai ricoche piteusement."),
      C("Tenter un lancer acrobatique", .4, {"mait": 4, "popu": 6, "xp": 8}, "Toute la classe applaudit.", {"sante": -4, "popu": -3}, "Tu t'écroules en riant."),
      C("Aider un camarade qui rate", .9, {"karma": 4, "popu": 2}, "Il te remercie.", {}, "")),
    V("Naruto", 7, 12, "🍥 Tu surprends un camarade en train de se faire disputer par un ninja plus âgé.",
      C("Intervenir", .5, {"karma": 5, "rep": 3, "xp": 8}, "Le plus âgé s'éloigne.", {"sante": -6, "rep": -1}, "Tu te fais malmener aussi."),
      C("Aller chercher ton instructeur", .9, {"karma": 2}, "L'instructeur règle la situation.", {}, ""),
      C("Passer ton chemin", 1, {"karma": -2}, "Tu files, honteux.", {}, "")),
    V("Naruto", 10, 16, "🎎 Le village célèbre un grand festival : stands, lanternes et défis.",
      C("Participer au concours de shuriken", ("st", "mait", 20), {"argent": 80, "rep": 3, "mait": 2}, "Tu repars avec un prix.", {"bonheur": -1}, "Tu n'as pas de chance."),
      C("Goûter à tous les stands", 1, {"bonheur": 6, "argent": -40, "sante": 1}, "Un vrai festin !", {}, ""),
      C("Inviter quelqu'un à danser", .6, {"bonheur": 6, "popu": 3}, "Une belle soirée.", {"bonheur": -3}, "Tu essuies un refus.")),
    V("Naruto", 12, 18, "📜 Ton escouade doit choisir sa prochaine mission.",
      C("Mission de rang D (sûre)", .95, {"xp": 8, "argent": 60}, "Un travail honnête.", {}, ""),
      C("Mission de rang C (risquée)", ("pw", 90), {"xp": 20, "argent": 150, "rep": 3}, "Vous brillez !", {"sante": -10, "rep": -1}, "La mission tourne court."),
      C("Mission de rang B (audacieuse)", ("pw", 150), {"xp": 40, "argent": 300, "rep": 6}, "Un exploit remarqué par le village.", {"sante": -20, "rep": -3}, "Vous échouez de justesse.")),
    V("Naruto", 12, 40, "🌲 Tu découvres un parchemin ancien dans les ruines d'un vieux sanctuaire.",
      C("Le déchiffrer", ("st", "intel", 55), {"intel": 3, "mait": 3, "xp": 20}, "Tu apprends une technique oubliée.", {"bonheur": -2}, "Les caractères restent hermétiques."),
      C("Le vendre au marché (250)", .8, {"argent": 250, "karma": -1}, "Tu fais un joli bénéfice.", {"argent": 60}, "L'acheteur te rogne le prix."),
      C("Le rapporter à ton Kage", 1, {"rep": 5, "karma": 4}, "Le village apprécie ton geste.", {}, "")),
    V("Naruto", 13, 40, "🥷 Un ninja d'un autre village propose de t'apprendre un jutsu en secret, contre service.",
      C("Accepter le marché", .55, {"mait": 4, "xp": 20, "karma": -3}, "Tu apprends un truc fabuleux.", {"rep": -5, "argent": -80}, "C'était un piège."),
      C("Refuser", 1, {"karma": 2}, "Tu restes loyal à ton village.", {}, ""),
      C("Le dénoncer", .8, {"rep": 6, "karma": 1}, "Ton village te félicite.", {"rep": -1}, "Il avait disparu.")),
    V("Naruto", 14, 45, "🧪 Un laboratoire clandestin t'offre de tester un nouveau renforçateur de chakra.",
      C("Accepter", .5, {"chakra": 10, "force": 3, "karma": -3}, "Tu ressens un pouvoir nouveau !", {"sante": -18, "chakra": -5}, "Effets secondaires terribles."),
      C("Refuser", 1, {"karma": 2}, "Tu gardes tes distances.", {}, ""),
      C("Alerter les autorités", .85, {"rep": 5, "karma": 3}, "Le laboratoire est fermé.", {}, "")),
    V("Naruto", 14, 50, "🦊 Un animal étrange blessé gît en bordure de forêt.",
      C("Le soigner", .8, {"karma": 5, "bonheur": 4, "flag": "ev_invocation"}, "Il te regarde avec gratitude.", {"sante": -4}, "Il te griffe et s'enfuit."),
      C("Le capturer", .4, {"argent": 200, "karma": -5}, "Un acheteur te le paie cher.", {"sante": -8}, "Il te mord et s'échappe."),
      C("Le laisser en paix", 1, {}, "Tu poursuis ton chemin.", {}, "")),
    V("Naruto", 14, 50, "💥 Un genjutsu piège t'empêche de distinguer le réel de l'illusion.",
      C("Dissiper l'illusion avec ton chakra", ("st", "chakra", 40), {"chakra": 3, "xp": 20, "mait": 2}, "Tu brises le piège !", {"sante": -10}, "Tu restes prisonnier un long moment."),
      C("Te blesser pour te réveiller", .7, {"sante": -6, "xp": 12}, "La douleur te libère.", {"sante": -12}, "Tu te blesses pour rien."),
      C("Attendre l'aide de ton équipe", .6, {"karma": 1, "xp": 8}, "Ton équipier te libère.", {"sante": -8}, "Ils arrivent trop tard.")),
    V("Naruto", 15, 50, "🏯 Les clans organisent un banquet pour renforcer leurs liens.",
      C("Faire un discours", ("st", "rep", 40), {"rep": 5, "popu": 3}, "Les chefs de clan acquiescent.", {"rep": -2}, "Ton discours tombe à plat."),
      C("Nouer des contacts", .85, {"rep": 3, "argent": 50}, "Tu te fais des alliés utiles.", {}, ""),
      C("Rester dans ton coin", 1, {"bonheur": 1}, "Tu observes de loin.", {}, "")),
    V("Naruto", 16, 50, "🛡️ Des orphelins de guerre errent à la lisière du village.",
      C("Les recueillir", .85, {"karma": 8, "bonheur": 5, "argent": -100, "flag": "ev_orphelins"}, "Ils trouvent un foyer grâce à toi.", {"bonheur": -2, "argent": -50}, "Le conseil refuse de les accueillir."),
      C("Leur donner de la nourriture (40)", 1, {"karma": 4, "argent": -40}, "Un petit geste qui compte.", {}, ""),
      C("Les ignorer", 1, {"karma": -4}, "Tu détournes les yeux.", {}, "")),
    V("Naruto", 18, 55, "🏹 Un contrat de chasse à la prime s'offre à toi (Bingo Book).",
      C("Traquer la cible", ("pw", 120), {"argent": 400, "xp": 30, "rep": 5, "karma": -2}, "Tu empoches la prime.", {"sante": -15, "rep": -2}, "La cible t'échappe."),
      C("Refuser les contrats sanglants", 1, {"karma": 3}, "Tu gardes ta conscience tranquille.", {}, ""),
      C("Le dénoncer au village", .8, {"rep": 4}, "On te remercie de ta vigilance.", {}, "")),
    V("Naruto", 18, 55, "🔥 Ton équipier s'entraîne seul jusqu'à l'épuisement.",
      C("L'arrêter", .8, {"karma": 3, "bonheur": 3}, "Il te remercie.", {"bonheur": -2}, "Il t'envoie promener."),
      C("T'entraîner avec lui", .85, {"mait": 3, "force": 2, "sante": -3}, "Vous progressez ensemble.", {"sante": -8}, "Vous vous blessez tous les deux."),
      C("Le laisser faire", 1, {}, "Chacun son rythme.", {}, "")),
    V("Naruto", 16, 50, "🗡️ Un ninja renégat menace un convoi de civils.",
      C("L'affronter seul", ("pw", 130), {"xp": 35, "rep": 8, "karma": 3}, "Tu protèges le convoi !", {"sante": -22, "rep": -2}, "Tu es blessé mais les civils s'enfuient."),
      C("Appeler des renforts", .8, {"xp": 12, "rep": 3}, "Les renforts arrivent à temps.", {"rep": -2}, "Ils arrivent trop tard."),
      C("Négocier", ("st", "rep", 50), {"rep": 6, "karma": 2}, "Il baisse les armes.", {"sante": -10}, "Il t'attaque par surprise.")),
    V("Naruto", 20, 60, "🏛️ Le conseil du village te demande un avis sur une décision politique.",
      C("Soutenir une politique de paix", .8, {"karma": 5, "rep": 4}, "Le conseil suit ton avis.", {"rep": -2}, "Tes arguments sont balayés."),
      C("Soutenir une politique de force", .8, {"xp": 10, "rep": 4, "karma": -2}, "Le conseil durcit sa position.", {"rep": -2}, "On t'accuse de bellicisme."),
      C("Garder le silence", 1, {}, "Tu laisses les autres trancher.", {}, "")),
    V("Naruto", 20, 60, "🌊 Un typhon menace le village.",
      C("Aider à consolider les digues", .85, {"karma": 5, "rep": 5, "force": 1}, "Le village est sauvé.", {"sante": -8}, "Tu es emporté par une vague."),
      C("Évacuer les civils", .9, {"karma": 6, "rep": 6}, "Tu sauves de nombreuses vies.", {"sante": -4}, "Tu perds du temps."),
      C("Te mettre à l'abri", 1, {"karma": -2}, "Tu préserves ta peau.", {}, "")),
    V("Naruto", 24, 60, "🧒 Les orphelins que tu as recueillis ont grandi : l'un d'eux veut devenir ninja.",
      C("Devenir son maître", .85, {"karma": 6, "rep": 5, "bonheur": 6}, "Tu formes un jeune prometteur.", {"bonheur": -2}, "Il n'est pas prêt."),
      C("Lui offrir ton ancien équipement (100)", 1, {"argent": -100, "karma": 4, "bonheur": 4}, "Il te remercie les larmes aux yeux.", {}, ""),
      C("Le décourager", 1, {"karma": -2}, "Il baisse la tête.", {}, ""), cond="flag:ev_orphelins"),
    V("Naruto", 16, 60, "🐸 L'animal que tu as soigné revient avec un cadeau : un parchemin d'invocation.",
      C("Signer le contrat", .8, {"mait": 5, "chakra": 5, "xp": 25}, "Tu peux désormais l'invoquer !", {"chakra": -3, "sante": -6}, "Le contrat te drainera à l'avenir."),
      C("Le remercier et refuser", 1, {"karma": 3}, "Il repart en gambadant.", {}, ""), cond="flag:ev_invocation"),
    # ═══════════ KUROKO ═══════════
    V("Kuroko", 8, 14, "🏀 Un terrain de basket de quartier est libre : des enfants cherchent un joueur.",
      C("Jouer avec eux", .9, {"mait": 3, "bonheur": 4, "popu": 3}, "Un match amusant !", {"bonheur": -1}, "Ils sont plus forts que toi."),
      C("T'exercer seul au lancer franc", ("st", "mait", 12), {"mait": 3, "intel": 1}, "Tu progresses.", {"bonheur": -1}, "Tu rates les trois quarts de tes tirs."),
      C("Regarder les autres jouer", 1, {"intel": 2}, "Tu repères leurs combinaisons.", {}, "")),
    V("Kuroko", 12, 18, "🌙 Tu t'entraînes seul(e) au tir en pleine nuit.",
      C("Continuer jusqu'à l'aube", .6, {"mait": 5, "sante": -5}, "Ton tir devient plus fluide.", {"sante": -10, "bonheur": -3}, "Tu t'épuises."),
      C("Rentrer dormir", 1, {"sante": 3}, "Tu es raisonnable.", {}, ""),
      C("Inviter un ami pour t'entraîner", .8, {"mait": 3, "bonheur": 4}, "Une belle séance à deux.", {}, "")),
    V("Kuroko", 13, 19, "🩹 Un coéquipier se foule la cheville pendant l'entraînement.",
      C("L'aider à se rendre à l'infirmerie", 1, {"karma": 4, "popu": 2}, "Il t'est très reconnaissant.", {}, ""),
      C("Le remplacer au pied levé", .6, {"mait": 3, "rep": 3}, "Tu saisis ta chance.", {"bonheur": -3}, "Tu te sens dépassé."),
      C("Poursuivre l'entraînement", 1, {"mait": 1}, "Le coach ordonne de continuer.", {}, "")),
    V("Kuroko", 13, 19, "🧢 Un fan t'attend à la sortie du gymnase pour un autographe.",
      C("Signer et discuter", 1, {"bonheur": 4, "rep": 2}, "Un moment sympa.", {}, ""),
      C("Passer rapidement", 1, {"rep": -1}, "Tu es pressé(e).", {}, ""),
      C("Lui proposer un 1 contre 1", .6, {"bonheur": 5, "mait": 2, "rep": 3}, "Il garde un souvenir inoubliable.", {"bonheur": -1}, "Il te met 11-2.")),
    V("Kuroko", 14, 19, "📰 Un journaliste sportif te propose une interview.",
      C("Accepter", .85, {"rep": 6, "bonheur": 3}, "Un bel article sur toi.", {"rep": -3}, "Tes propos sont déformés."),
      C("Refuser", 1, {"mait": 2}, "Tu préfères t'entraîner.", {}, ""),
      C("Parler uniquement de l'équipe", .9, {"rep": 4, "karma": 3}, "L'équipe est mise en avant.", {}, "")),
    V("Kuroko", 14, 19, "👟 Une marque de chaussures te propose un contrat de sponsoring.",
      C("Accepter (400)", ("st", "rep", 30), {"argent": 400, "rep": 3}, "Tu signes ton premier sponsor.", {"bonheur": -2}, "La marque se rétracte."),
      C("Négocier plus", ("st", "intel", 50), {"argent": 700, "rep": 4}, "Tu obtiens un bien meilleur contrat.", {"argent": 100}, "On te propose moins."),
      C("Refuser pour rester libre", 1, {"karma": 2, "bonheur": 2}, "Tu gardes ton indépendance.", {}, ""), cond="celeb"),
    V("Kuroko", 14, 18, "😤 Un joueur de ton équipe est jaloux de ton temps de jeu.",
      C("Lui parler franchement", .75, {"karma": 3, "mait": 1}, "Vous vous expliquez.", {"bonheur": -3}, "La discussion dégénère."),
      C("L'ignorer", .5, {"bonheur": 1}, "Il se calme.", {"bonheur": -4, "popu": -3}, "Il te mène la vie dure."),
      C("Le défier en match amical", ("pw", 80), {"rep": 4, "mait": 2}, "Tu gagnes le respect de tous.", {"rep": -3}, "Tu perds devant l'équipe.")),
    V("Kuroko", 14, 19, "🏋️ Le coach impose un entraînement physique très dur.",
      C("Tout donner", .7, {"force": 4, "sante": -5, "rep": 2}, "Tu repousses tes limites.", {"sante": -12, "bonheur": -4}, "Tu craques."),
      C("Doser tes efforts", .9, {"force": 2, "mait": 1}, "Tu progresses prudemment.", {}, ""),
      C("Chercher à t'esquiver", .4, {"bonheur": 3}, "Tu passes entre les mailles.", {"rep": -3, "karma": -2}, "Le coach te colle une punition.")),
    V("Kuroko", 15, 19, "🏀 Dernière seconde du match : on te donne la balle.",
      C("Tirer à trois points", ("st", "mait", 55), {"rep": 8, "mait": 3, "bonheur": 8}, "Le buzzer sonne : panier !", {"bonheur": -8, "rep": -2}, "Le ballon rebondit sur l'anneau."),
      C("Passer à un coéquipier", .7, {"karma": 3, "rep": 4, "popu": 3}, "Il marque : victoire collective.", {"bonheur": -3}, "Sa tentative échoue."),
      C("Aller au cercle", ("pw", 90), {"rep": 7, "mait": 3, "force": 1}, "Tu perces la défense !", {"sante": -5, "bonheur": -4}, "Tu te fais contrer.")),
    V("Kuroko", 14, 19, "😖 Tu rates deux lancers francs cruciaux.",
      C("Accepter ta défaite", 1, {"bonheur": -3, "karma": 2}, "Tu en tires une leçon.", {}, ""),
      C("T'entraîner jusqu'à les maîtriser", .8, {"mait": 4, "bonheur": 2}, "La prochaine fois sera la bonne.", {"sante": -3}, "Tu doutes encore."),
      C("Incriminer l'arbitre", .3, {"popu": 2}, "Quelques coéquipiers te soutiennent.", {"rep": -4, "karma": -3}, "Le coach est furieux.")),
    V("Kuroko", 15, 19, "🏙️ Un tournoi de street basket 3 contre 3 est organisé.",
      C("Monter une équipe", .7, {"rep": 5, "mait": 3, "argent": 100}, "Votre équipe finit sur le podium.", {"bonheur": -2}, "Vous perdez au premier tour."),
      C("Rejoindre une équipe existante", .9, {"mait": 2, "popu": 3}, "Tu apprends de nouveaux styles.", {}, ""),
      C("Regarder seulement", 1, {"intel": 2}, "Tu prends des notes mentales.", {}, "")),
    V("Kuroko", 15, 19, "🧑‍🏫 Ton coach te propose de devenir capitaine.",
      C("Accepter", ("st", "rep", 35), {"rep": 5, "karma": 3, "mait": 2}, "L'équipe te suit.", {"bonheur": -3}, "La pression est trop forte."),
      C("Refuser humblement", 1, {"karma": 2}, "Tu préfères jouer simplement.", {}, ""),
      C("Proposer un coéquipier", .8, {"karma": 4, "popu": 3}, "Ton ami est ravi.", {}, "")),
    V("Kuroko", 15, 20, "🇯🇵 Une sélection de joueurs prometteurs est organisée pour l'équipe nationale jeune.",
      C("Tenter ta chance", ("pw", 100), {"rep": 8, "mait": 3, "xp": 25}, "Tu es retenu(e) !", {"bonheur": -3}, "Tu n'es pas sélectionné(e)."),
      C("Observer d'abord", 1, {"intel": 2}, "Tu repères les meilleurs.", {}, ""),
      C("Décliner", 1, {}, "Tu préfères le lycée.", {}, "")),
    V("Kuroko", 14, 19, "😠 Un rival te provoque en ligne avant un grand match.",
      C("Répondre avec humour", .7, {"popu": 4, "rep": 2}, "Les internautes sont de ton côté.", {"rep": -2}, "Ça tombe à plat."),
      C("Répondre sur le terrain", ("pw", 90), {"rep": 5, "xp": 15}, "Tu lui fermes le clapet.", {"bonheur": -3}, "Il avait raison de se vanter."),
      C("Ne pas répondre", 1, {"karma": 2}, "Tu gardes la tête froide.", {}, "")),
    V("Kuroko", 16, 22, "🎓 Une université américaine t'envoie une lettre d'intérêt.",
      C("Répondre favorablement", .7, {"rep": 4, "xp": 15}, "Le dialogue s'engage.", {"bonheur": -2}, "La réponse ne vient jamais."),
      C("Demander une bourse complète", ("st", "mait", 60), {"argent": 300, "rep": 5}, "Une bourse t'est offerte.", {"rep": -1}, "L'offre est retirée."),
      C("Rester au Japon", 1, {"bonheur": 2}, "Tu préfères tes racines.", {}, "")),
    V("Kuroko", 13, 18, "🏆 Ton équipe est menée de 20 points à la mi-temps.",
      C("Mobiliser l'équipe", ("st", "rep", 35), {"rep": 5, "karma": 2}, "Vous remontez le score !", {"bonheur": -3}, "Rien n'y fait."),
      C("Changer de tactique", ("st", "intel", 45), {"intel": 2, "rep": 4}, "Votre nouvelle défense surprend l'adversaire.", {"bonheur": -2}, "La tactique tourne court."),
      C("Prendre plus de tirs", .4, {"mait": 3, "rep": 3}, "Tu ramènes l'équipe dans le match.", {"rep": -3}, "Tu forces et rates.")),
    # ═══════════ TOKYO REVENGERS ═══════════
    V("Tokyo Revengers", 12, 18, "🏍️ Une course de motos illégale se prépare sur l'autoroute.",
      C("Y participer", ("st", "mait", 45), {"rep": 6, "xp": 15, "argent": 100}, "Tu remportes la course !", {"sante": -15, "argent": -80}, "Tu te vautres et la moto est cassée."),
      C("Parier sur un pilote (80)", .5, {"argent": 200}, "Ton pilote gagne.", {"argent": -80}, "Tu perds ta mise."),
      C("Rester spectateur", 1, {"bonheur": 3, "intel": 1}, "L'ambiance est électrique.", {}, "")),
    V("Tokyo Revengers", 13, 25, "🧍 Un commerçant du quartier est menacé par des racketteurs.",
      C("Le protéger", ("pw", 80), {"karma": 6, "rep": 6, "xp": 15, "flag": "ev_commercant"}, "Les racketteurs détalent.", {"sante": -14, "rep": -2}, "Tu te fais malmener."),
      C("Prévenir la police", .8, {"karma": 2}, "La police intervient.", {}, ""),
      C("Prendre ta part du racket", .5, {"argent": 150, "karma": -8}, "Tu t'enrichis salement.", {"rep": -5, "karma": -8}, "Les racketteurs te rackettent aussi.")),
    V("Tokyo Revengers", 13, 40, "🚬 Un ancien te propose de te faire gagner de l'argent facilement.",
      C("Accepter", .5, {"argent": 250, "karma": -5}, "Un petit trafic discret.", {"sante": -10, "rep": -4, "karma": -5}, "Tu te retrouves dans de beaux draps."),
      C("Refuser", 1, {"karma": 3}, "Tu gardes les mains propres.", {}, ""),
      C("Le dénoncer", .7, {"rep": 4, "karma": 2}, "Le quartier te respecte plus.", {"sante": -6}, "Il te repère.")),
    V("Tokyo Revengers", 13, 40, "🥊 Un champion de boxe locale te lance un défi amical au dojo.",
      C("Relever le défi", ("pw", 90), {"rep": 5, "force": 2, "mait": 2}, "Beau combat, tu tiens bon !", {"sante": -10, "rep": -1}, "Tu es mis K.O. dès le troisième round."),
      C("Décliner", 1, {}, "Tu n'es pas prêt.", {}, ""),
      C("Demander à l'observer d'abord", .9, {"intel": 2, "mait": 1}, "Tu repères sa garde.", {}, "")),
    V("Tokyo Revengers", 14, 40, "🚓 Un policier bienveillant te met en garde.",
      C("L'écouter", .85, {"karma": 3, "intel": 1}, "Son conseil te servira.", {}, ""),
      C("Te moquer de lui", .5, {"rep": 3, "karma": -2}, "Tes amis rient.", {"rep": -3, "argent": -50}, "Il te colle une amende."),
      C("Nouer une relation avec lui", .6, {"karma": 2, "rep": 2, "flag": "ev_policier"}, "Un contact précieux.", {"bonheur": -1}, "Il reste méfiant.")),
    V("Tokyo Revengers", 14, 40, "🏚️ Un gang rival squatte ton terrain de jeu habituel.",
      C("Les chasser", ("pw", 90), {"rep": 7, "xp": 20}, "Tu récupères ton terrain.", {"sante": -15, "rep": -3}, "Ils te mettent dehors."),
      C("Négocier un partage", ("st", "rep", 40), {"rep": 3, "karma": 2}, "Un compromis est trouvé.", {"rep": -2}, "Ils refusent de céder."),
      C("Aller ailleurs", 1, {"bonheur": -1}, "Tu changes de terrain.", {}, "")),
    V("Tokyo Revengers", 13, 30, "🌃 Tu croises un type bizarre qui te dit venir du futur.",
      C("L'écouter avec curiosité", .7, {"intel": 3, "xp": 10}, "Il te donne de précieux conseils.", {"bonheur": -2}, "Tu es perplexe."),
      C("Lui rire au nez", 1, {"bonheur": 1}, "Il s'éloigne en grommelant.", {}, ""),
      C("Le suivre", .4, {"intel": 4, "xp": 20}, "Il te montre ce qui t'attend.", {"sante": -8, "bonheur": -3}, "Il disparaît dans la foule.")),
    V("Tokyo Revengers", 14, 40, "🍜 Une rencontre amicale avec les anciens du quartier au restaurant.",
      C("Écouter leurs histoires", 1, {"intel": 2, "karma": 1, "bonheur": 3}, "Tu en apprends beaucoup.", {}, ""),
      C("Les inviter (60)", 1, {"argent": -60, "rep": 3, "popu": 3}, "Ils te respectent davantage.", {}, ""),
      C("Les provoquer", .4, {"rep": 4}, "Ils rient de ton culot.", {"sante": -8, "rep": -3}, "Ils te remettent à ta place.")),
    V("Tokyo Revengers", 14, 40, "🔥 Un ami proche est battu par un gang rival.",
      C("Venger ton ami", ("pw", 100), {"rep": 8, "xp": 25, "karma": -2}, "Tu leur fais payer.", {"sante": -20, "rep": -2}, "Tu te fais écraser."),
      C("L'emmener à l'hôpital", 1, {"karma": 6, "bonheur": -2}, "Tu veilles sur lui.", {}, ""),
      C("Chercher les coupables avec ton gang", .6, {"rep": 5, "xp": 15}, "Ils sont démasqués.", {"rep": -2}, "Aucune piste."), cond="gang"),
    V("Tokyo Revengers", 14, 40, "😠 Un membre de ton gang désobéit ouvertement à tes ordres.",
      C("Le recadrer fermement", ("st", "rep", 45), {"rep": 4, "karma": 1}, "Il rentre dans le rang.", {"rep": -3}, "Il te défie devant tout le monde."),
      C("Le raisonner", .7, {"karma": 3, "intel": 1}, "Il comprend.", {"bonheur": -2}, "Il ne t'écoute pas."),
      C("L'exclure du gang", .8, {"rep": 3, "karma": -1}, "L'exemple est donné.", {"membres": -2, "rep": -2}, "Il part avec des amis."), cond="gang"),
    V("Tokyo Revengers", 15, 40, "💰 Un yakuza t'offre un job de surveillant dans un salon de jeux.",
      C("Accepter", .8, {"argent": 300, "karma": -4, "xp": 10}, "Un petit boulot bien payé.", {"rep": -4, "karma": -4}, "Une descente de police tourne mal."),
      C("Refuser", 1, {"karma": 2}, "Tu restes loin des yakuza.", {}, ""),
      C("Demander plus", ("st", "rep", 50), {"argent": 500, "rep": 2}, "Tu obtiens un meilleur contrat.", {"rep": -3}, "Il se vexe.")),
    V("Tokyo Revengers", 13, 40, "🌆 Un orphelin du quartier te demande de lui apprendre à se battre.",
      C("Accepter de l'entraîner", .85, {"karma": 6, "rep": 3, "bonheur": 4, "force": 1}, "Il progresse vite.", {"bonheur": -1}, "Il se décourage."),
      C("Lui donner quelques conseils", 1, {"karma": 2, "bonheur": 1}, "Il part content.", {}, ""),
      C("Le renvoyer", 1, {"karma": -2}, "Tu n'as pas le temps.", {}, "")),
    V("Tokyo Revengers", 16, 40, "💼 Un politicien local veut ton soutien dans son quartier.",
      C("Soutenir le politicien", .7, {"argent": 250, "rep": 3, "karma": -3}, "Il te revaudra ça.", {"rep": -4}, "Il t'oublie vite."),
      C("Le dénoncer pour corruption", ("st", "intel", 60), {"rep": 6, "karma": 4}, "Le scandale éclate.", {"rep": -3, "sante": -6}, "Tu manques de preuves."),
      C("Ne pas t'en mêler", 1, {}, "La politique, très peu pour toi.", {}, "")),
    V("Tokyo Revengers", 16, 40, "🎪 Les gangs défilent pour le festival d'été du quartier.",
      C("Défiler fièrement", .8, {"rep": 5, "popu": 4}, "Le public t'acclame.", {"rep": -1}, "Un incident gâche la fête."),
      C("Assurer la sécurité", .8, {"karma": 4, "rep": 3}, "Tout se passe calmement.", {"sante": -5}, "Une bagarre éclate."),
      C("Passer incognito", 1, {"bonheur": 3}, "Tu profites tranquillement.", {}, "")),
    V("Tokyo Revengers", 18, 45, "🧓 Le commerçant que tu as protégé te remercie en t'offrant un petit cadeau.",
      C("Accepter", 1, {"argent": 150, "karma": 3, "bonheur": 4}, "Il insiste pour te servir un repas.", {}, ""),
      C("Refuser et lui demander des informations", .8, {"intel": 2, "rep": 3}, "Il te raconte tout ce qu'il sait.", {}, ""), cond="flag:ev_commercant"),
    V("Tokyo Revengers", 18, 50, "🕴️ Le policier que tu connais te prévient d'une descente imminente.",
      C("Prévenir ton gang", .9, {"rep": 5, "karma": 1}, "Ton gang évite le pire.", {"rep": 1}, "Personne ne te croit."),
      C("Garder l'info pour toi", 1, {"karma": -2}, "Tu te protèges.", {}, ""),
      C("Le remercier avec un cadeau (100)", 1, {"argent": -100, "karma": 2, "rep": 1}, "Votre lien se renforce.", {}, ""), cond="flag:ev_policier"),
]

EV_MORE += [
    # ───────────── Petite enfance supplémentaire ─────────────
    V(None, 2, 5, "🎈 On te donne un ballon à la fête du quartier.",
      C("Le serrer fort", .8, {"bonheur": 4}, "Tu le gardes toute la journée.", {"bonheur": -3}, "Il s'envole et tu pleures."),
      C("Le lâcher volontairement", 1, {"bonheur": 2, "intel": 1}, "Tu le regardes grimper dans le ciel.", {}, ""),
      C("Le partager avec un autre enfant", .9, {"karma": 3, "popu": 2}, "Vous jouez ensemble.", {}, "")),
    V(None, 3, 6, "🍬 Tu trouves un paquet de bonbons caché dans la cuisine.",
      C("Tout manger", .5, {"bonheur": 5}, "Un festin clandestin !", {"sante": -4, "bonheur": -3}, "Tu as mal au ventre."),
      C("En manger un seul", 1, {"bonheur": 2, "karma": 1}, "Tu te montres raisonnable.", {}, ""),
      C("Les remettre à leur place", 1, {"karma": 2}, "Tes parents ne sauront jamais.", {}, "")),
    V(None, 4, 6, "🌧️ Il pleut et tu veux jouer dehors.",
      C("Sauter dans les flaques", .7, {"bonheur": 5}, "Une joie immense !", {"sante": -4, "bonheur": 1}, "Tu attrapes un petit rhume."),
      C("Rester dessiner à l'intérieur", 1, {"intel": 2, "bonheur": 2}, "Tu t'amuses autrement.", {}, ""),
      C("Faire un fort avec des coussins", .9, {"bonheur": 4, "intel": 1}, "Un château formidable.", {}, "")),
    # ───────────── 22-45 ans ─────────────
    V(None, 22, 45, "🎤 On t'invite à prendre la parole lors d'un événement public.",
      C("Accepter", ("st", "rep", 35), {"rep": 5, "popu": 3}, "Ton discours marque les esprits.", {"rep": -3, "bonheur": -3}, "Le trac te trahit."),
      C("Préparer longuement", ("st", "intel", 45), {"rep": 4, "intel": 2}, "Un discours très abouti.", {"bonheur": -1}, "Tu te perds dans tes notes."),
      C("Décliner", 1, {}, "Ce n'est pas pour toi.", {}, "")),
    V(None, 22, 45, "🏞️ Tu te perds en randonnée et tombes sur un lieu magnifique.",
      C("Planter ta tente", 1, {"bonheur": 6, "sante": 2}, "Une nuit sous les étoiles.", {}, ""),
      C("Chercher ton chemin", ("st", "intel", 40), {"intel": 2, "xp": 8}, "Tu retrouves la route.", {"sante": -4, "bonheur": -2}, "Tu marches des heures."),
      C("Photographier et repartir", 1, {"bonheur": 3, "rep": 1}, "Un souvenir à partager.", {}, "")),
    V(None, 25, 45, "🏷️ Un ami d'enfance te demande de lui servir de témoin à son mariage.",
      C("Accepter avec joie", 1, {"bonheur": 6, "karma": 2, "argent": -60}, "Une journée mémorable.", {}, ""),
      C("Préparer un discours drôle", .7, {"popu": 4, "bonheur": 5}, "La salle éclate de rire.", {"bonheur": -2}, "Ta blague tombe à plat."),
      C("Décliner", 1, {"bonheur": -3, "karma": -1}, "Il en est un peu peiné.", {}, "")),
    # ───────────── 50+ ans (tous) ─────────────
    V(None, 50, 95, "🧓 Un vieux compagnon de route frappe à ta porte.",
      C("L'accueillir à bras ouverts", 1, {"bonheur": 7, "karma": 2}, "Vous parlez jusqu'au matin.", {}, ""),
      C("Lui offrir un repas (40)", 1, {"bonheur": 4, "argent": -40, "karma": 3}, "Un repas chaleureux.", {}, ""),
      C("Lui fermer la porte", 1, {"karma": -4, "bonheur": -3}, "Tu le regrettes aussitôt.", {}, "")),
    V(None, 50, 95, "🩹 Tes articulations te font souffrir davantage chaque année.",
      C("Suivre une rééducation douce", .85, {"sante": 6, "bonheur": 2}, "Tu retrouves de la souplesse.", {"sante": 1}, "Peu d'effet."),
      C("Continuer à t'activer", .6, {"force": 1, "bonheur": 3}, "Tu restes alerte.", {"sante": -8}, "Tu te blesses."),
      C("Te résigner", 1, {"bonheur": -2}, "L'âge n'est pas tendre.", {}, "")),
    V(None, 50, 95, "🏡 Tes enfants te proposent de vivre chez eux.",
      C("Accepter", .8, {"bonheur": 5, "sante": 3, "karma": 1}, "Tu es bien entouré.", {"bonheur": -3}, "Tu te sens de trop."),
      C("Rester indépendant", .8, {"bonheur": 3, "force": 0}, "Tu gardes ta liberté.", {"sante": -3}, "La solitude se fait sentir."),
      C("Partir vivre à la campagne", .7, {"bonheur": 6, "sante": 4}, "Un cadre idéal.", {"bonheur": -2, "argent": -80}, "Le quotidien est difficile."), cond="enfant"),
    V(None, 50, 95, "🏅 La ville souhaite t'honorer pour ton parcours.",
      C("Accepter la cérémonie", .95, {"rep": 8, "bonheur": 6}, "Un moment inoubliable.", {"bonheur": 2}, "Tu es bien gêné."),
      C("Refuser par modestie", 1, {"karma": 3, "bonheur": 2}, "Tu préfères rester dans l'ombre.", {}, ""),
      C("Demander que ce soit pour les jeunes", 1, {"karma": 6, "rep": 5}, "Tu fais le bien autour de toi.", {}, ""), cond="celeb"),
    V(None, 55, 95, "🪑 Tu passes l'après-midi sur un banc à regarder passer le monde.",
      C("Engager la conversation", .8, {"bonheur": 5, "karma": 1}, "Tu fais une belle rencontre.", {"bonheur": 1}, "On te répond à peine."),
      C("Profiter du silence", 1, {"bonheur": 3, "sante": 2}, "Un moment de paix.", {}, ""),
      C("Nourrir les pigeons", 1, {"bonheur": 2, "karma": 1}, "Ils t'adorent.", {}, "")),
    V(None, 60, 95, "💭 Tu te demandes si tu as fait les bons choix dans ta vie.",
      C("Faire la paix avec le passé", .85, {"bonheur": 6, "karma": 3}, "Tu te sens apaisé.", {"bonheur": -2}, "Les regrets persistent."),
      C("Écrire à quelqu'un que tu as perdu de vue", .6, {"bonheur": 7, "karma": 3}, "Il te répond avec joie.", {"bonheur": -4}, "Aucune réponse ne vient."),
      C("Te lancer un dernier défi", .6, {"xp": 20, "bonheur": 4, "sante": -3}, "Tu te sens vivant.", {"sante": -8}, "Tu y laisses des forces.")),
    # ───────────── Anciens (par univers) ─────────────
    V("Naruto", 40, 80, "🧓 De jeunes ninjas viennent te demander de leur raconter tes exploits.",
      C("Tout leur raconter", 1, {"rep": 6, "bonheur": 5, "karma": 2}, "Ils t'écoutent, fascinés.", {}, ""),
      C("Leur donner une leçon pratique", ("pw", 100), {"rep": 7, "karma": 3, "mait": 1}, "Ils sont impressionnés.", {"sante": -5, "rep": 1}, "Ton dos te lâche, mais ils rient avec toi."),
      C("Leur dire d'aller s'entraîner", 1, {"karma": 1}, "Il n'y a pas de raccourci.", {}, "")),
    V("Naruto", 40, 80, "🏯 Le village te demande de siéger au conseil des sages.",
      C("Accepter", ("st", "rep", 55), {"rep": 8, "karma": 4, "bonheur": 3}, "Ta voix compte désormais.", {"rep": -2}, "Les jeunes te trouvent dépassé."),
      C("Décliner", 1, {"bonheur": 2}, "Tu préfères ta tranquillité.", {}, ""),
      C("Proposer un successeur", .85, {"karma": 5, "rep": 4}, "Tu transmets le flambeau.", {}, ""), cond="celeb"),
    V("Kuroko", 36, 80, "🏀 Une équipe de jeunes te demande de devenir leur entraîneur.",
      C("Accepter avec joie", .85, {"karma": 5, "rep": 5, "bonheur": 6}, "Tu retrouves le goût du jeu.", {"bonheur": -2}, "Les jeunes sont indisciplinés."),
      C("Donner une séance de démonstration", ("st", "mait", 50), {"rep": 4, "bonheur": 4}, "Tu leur montres comment faire.", {"sante": -5}, "Ton corps n'a plus vingt ans."),
      C("Décliner", 1, {}, "Tu laisses la place à d'autres.", {}, "")),
    V("Kuroko", 38, 80, "🏛️ On t'annonce ton intronisation au Temple de la renommée du basket.",
      C("Accepter avec émotion", 1, {"rep": 10, "bonheur": 10}, "Une consécration.", {}, ""),
      C("Remercier tous ceux qui t'ont aidé", 1, {"karma": 6, "rep": 8, "bonheur": 8}, "Un discours qui fait pleurer toute la salle.", {}, "")),
    V("Tokyo Revengers", 36, 80, "🕶️ Un jeune loup défie ta réputation d'ancien du quartier.",
      C("Le remettre à sa place", ("pw", 140), {"rep": 7, "xp": 15}, "Tu rappelles qui tu es.", {"sante": -10, "rep": -3}, "L'âge se fait sentir."),
      C("Lui offrir un thé et un conseil", .85, {"karma": 5, "rep": 4, "bonheur": 4}, "Il repart plus sage.", {"rep": -1}, "Il n'écoute pas."),
      C("Passer ton chemin", 1, {"bonheur": 1}, "Tu n'as plus rien à prouver.", {}, "")),
    V("Tokyo Revengers", 38, 80, "🍶 Tes anciens compagnons de gang se retrouvent dans un bar.",
      C("Trinquer aux souvenirs", 1, {"bonheur": 8, "rep": 2}, "La nostalgie coule à flots.", {}, ""),
      C("Évoquer les disparus", .9, {"bonheur": 4, "karma": 3}, "Un instant de silence.", {}, ""),
      C("Parler de tes regrets", .7, {"bonheur": 5, "karma": 2}, "Ils te comprennent.", {"bonheur": -3}, "Ça les met mal à l'aise.")),
]

EV_MORE += [
    # ───────────── 30-60 ans (tous) ─────────────
    V(None, 30, 60, "🏘️ Un conflit de voisinage éclate à propos d'une clôture.",
      C("Discuter calmement", ("st", "rep", 35), {"karma": 3, "bonheur": 2}, "Vous trouvez un arrangement.", {"bonheur": -3}, "La discussion s'envenime."),
      C("Passer par un médiateur (60)", .9, {"argent": -60, "karma": 2}, "Le médiateur règle l'affaire.", {}, ""),
      C("Construire un mur plus haut", 1, {"argent": -120, "bonheur": -2}, "Chacun reste de son côté.", {}, "")),
    V(None, 30, 60, "🍷 Un collègue te propose de monter une affaire ensemble.",
      C("Foncer", .5, {"argent": 400, "rep": 4, "xp": 20}, "L'affaire démarre très fort.", {"argent": -250, "bonheur": -4}, "La société fait faillite."),
      C("Demander un business plan", ("st", "intel", 55), {"argent": 250, "intel": 2}, "Tu évites les écueils.", {"bonheur": -1}, "Tu n'y comprends rien."),
      C("Refuser", 1, {}, "Tu préfères la sécurité.", {}, "")),
    V(None, 30, 60, "🎨 Tu te découvres une passion pour la peinture.",
      C("T'y consacrer le week-end", .9, {"bonheur": 6, "intel": 2}, "Tes toiles te ressemblent.", {"bonheur": 1}, "Le talent se fait attendre."),
      C("Exposer tes œuvres", .6, {"rep": 4, "argent": 80, "bonheur": 4}, "Une galerie t'accueille.", {"bonheur": -3}, "Personne ne vient."),
      C("Prendre des cours (80)", 1, {"mait": 2, "intel": 2, "argent": -80}, "Tu progresses vite.", {}, "")),
    V(None, 32, 60, "🚨 Un cambriolage a lieu chez toi.",
      C("Appeler la police", .8, {"karma": 1, "argent": 20}, "Une partie du butin est retrouvée.", {"argent": -150, "bonheur": -4}, "Rien n'est retrouvé."),
      C("Mener ta propre enquête", ("st", "intel", 55), {"xp": 15, "rep": 3, "argent": 80}, "Tu retrouves le coupable.", {"bonheur": -3}, "Aucune piste."),
      C("Installer une meilleure sécurité (100)", 1, {"argent": -100, "bonheur": 2}, "Plus de mauvaise surprise.", {}, "")),
    V(None, 32, 60, "📚 Un ancien professeur t'invite à donner une conférence.",
      C("Accepter", ("st", "rep", 35), {"rep": 5, "intel": 2, "bonheur": 4}, "Le public est conquis.", {"rep": -2}, "Tu peines à capter l'attention."),
      C("Refuser", 1, {}, "Tu laisses la place aux jeunes.", {}, ""),
      C("Proposer à un élève de le remplacer", .85, {"karma": 4, "rep": 2}, "Il fait un joli début.", {}, "")),
    V(None, 35, 60, "🌍 Tu reçois une invitation à un grand voyage à l'étranger.",
      C("Partir (250)", .85, {"bonheur": 8, "intel": 3, "argent": -250}, "Un voyage inoubliable.", {"bonheur": -2, "argent": -250}, "Tu tombes malade sur place."),
      C("Y aller en dormant à l'auberge (100)", .9, {"bonheur": 6, "intel": 2, "argent": -100}, "Tu rencontres des gens extraordinaires.", {}, ""),
      C("Rester chez toi", 1, {"bonheur": -1}, "Un autre voyage, peut-être.", {}, "")),
    V(None, 35, 60, "🏋️ Tu décides de remettre ton corps en forme.",
      C("T'inscrire à la salle (60)", .8, {"force": 3, "sante": 5, "argent": -60}, "Tu te sens revivre.", {"argent": -60, "bonheur": -2}, "Tu abandonnes après un mois."),
      C("Courir tous les matins", .75, {"sante": 6, "force": 1, "bonheur": 2}, "Tu prends goût à l'effort.", {"sante": -4}, "Tu te blesses au genou."),
      C("Attendre le mois prochain", 1, {}, "Demain, vraiment.", {}, "")),
    V(None, 38, 60, "💬 Une dispute familiale éclate lors d'un repas.",
      C("Calmer tout le monde", ("st", "rep", 40), {"karma": 4, "bonheur": 3}, "Tout rentre dans l'ordre.", {"bonheur": -4}, "Tu te fais houspiller à ton tour."),
      C("Prendre parti", .5, {"rep": 2}, "Tu soutiens ton camp.", {"bonheur": -5, "karma": -2}, "La famille se divise."),
      C("Quitter la table", 1, {"bonheur": -2}, "Tu sors prendre l'air.", {}, ""), cond="couple"),
    V(None, 40, 65, "👀 Un jeune collègue te propose de devenir son mentor.",
      C("Accepter", .9, {"karma": 5, "rep": 4, "bonheur": 4}, "Vous formez un bon duo.", {"bonheur": -1}, "Il n'écoute pas tes conseils."),
      C("Lui confier un projet", .7, {"rep": 3, "xp": 15}, "Il le mène à bien.", {"rep": -1}, "Il échoue."),
      C("Refuser", 1, {}, "Tu n'as pas la patience.", {}, "")),
    V(None, 40, 65, "💼 On te propose une retraite anticipée.",
      C("Accepter", 1, {"argent": 300, "bonheur": 5}, "Tu savoures ta liberté.", {}, ""),
      C("Refuser et continuer à travailler", .9, {"xp": 20, "rep": 3}, "Tu restes actif.", {"sante": -4}, "La fatigue se fait sentir."),
      C("Négocier une retraite progressive", ("st", "intel", 50), {"argent": 150, "bonheur": 4, "sante": 2}, "Un bel équilibre.", {"bonheur": -1}, "On te renvoie à tes habitudes.")),
    # ───────────── Carrière NBA (Kuroko) ─────────────
    V("Kuroko", 20, 42, "🇺🇸 Ta franchise te propose une prolongation de contrat.",
      C("Accepter (500)", .95, {"argent": 500, "rep": 3}, "Tu restes au club.", {"bonheur": -2}, "L'offre est finalement réduite."),
      C("Négocier à la hausse", ("st", "rep", 55), {"argent": 900, "rep": 4}, "Tu décroches un contrat record.", {"rep": -2, "argent": 100}, "La franchise se braque."),
      C("Tester le marché", .5, {"argent": 700, "xp": 20}, "Plusieurs franchises te courtisent.", {"bonheur": -3}, "Personne ne s'intéresse à toi."), cond="pro"),
    V("Kuroko", 20, 42, "🩹 Une blessure musculaire te prive de plusieurs matchs.",
      C("Revenir trop tôt", .35, {"rep": 3}, "Tu joues malgré la douleur.", {"sante": -18, "mait": -2}, "Tu aggraves ta blessure."),
      C("Suivre une rééducation sérieuse", .9, {"sante": 6, "intel": 1}, "Tu reviens en pleine forme.", {"sante": 1}, "La reprise est lente."),
      C("Consulter un spécialiste (300)", 1, {"sante": 8, "argent": -300}, "Tu retrouves vite tes jambes.", {}, "")),
    V("Kuroko", 20, 42, "👟 Une grande marque veut faire de toi son ambassadeur.",
      C("Signer (800)", .9, {"argent": 800, "rep": 5}, "Ton visage s'affiche partout.", {"rep": -2}, "Le contrat est annulé."),
      C("Exiger une ligne à ton nom", ("st", "rep", 65), {"argent": 1500, "rep": 8}, "Ta propre ligne de chaussures !", {"rep": -1}, "La marque ne cède pas."),
      C("Refuser pour rester libre", 1, {"karma": 2}, "Tu gardes ton indépendance.", {}, ""), cond="pro"),
    V("Kuroko", 21, 42, "🏆 Un jeune rookie japonais rejoint ta franchise.",
      C("Le prendre sous ton aile", .9, {"karma": 5, "rep": 4, "bonheur": 4}, "Il te considère comme un modèle.", {"bonheur": -1}, "Il est trop têtu."),
      C("Le tester à l'entraînement", ("pw", 140), {"rep": 4, "mait": 2}, "Tu lui montres qui commande.", {"rep": -2}, "Il te surprend."),
      C("L'ignorer", 1, {}, "Chacun sa route.", {}, ""), cond="pro"),
    V("Kuroko", 30, 45, "🎙️ Une chaîne sportive te propose de devenir consultant TV.",
      C("Accepter", .9, {"argent": 300, "rep": 4, "bonheur": 3}, "Tu deviens la voix du basket.", {"bonheur": -2}, "Tu es mal à l'aise devant les caméras."),
      C("Refuser", 1, {}, "Tu veux continuer à jouer.", {}, ""),
      C("Négocier des conditions", ("st", "rep", 55), {"argent": 500, "rep": 5}, "Un contrat sur mesure.", {}, ""), cond="pro"),
    # ───────────── 35-55 ans (univers) ─────────────
    V("Naruto", 35, 60, "🏯 Un village voisin propose un échange de formateurs.",
      C("Y envoyer tes élèves", .85, {"karma": 3, "rep": 4, "relx": ["A", 5]}, "Un lien précieux se noue.", {"rep": -1}, "Les élèves reviennent déçus."),
      C("Y aller toi-même", .8, {"xp": 20, "intel": 2, "relx": ["A", 6]}, "Tu apprends beaucoup.", {"sante": -4}, "Le voyage est épuisant."),
      C("Refuser", 1, {}, "Tu préfères rester au village.", {}, "")),
    V("Naruto", 35, 60, "⚔️ Une ancienne rivale vient te défier au nom du bon vieux temps.",
      C("Accepter", ("pw", 160), {"rep": 6, "xp": 20}, "Un combat magnifique !", {"sante": -12, "bonheur": -1}, "Tu es battu, mais c'était beau."),
      C("Lui offrir le thé", 1, {"bonheur": 5, "karma": 2}, "Vous parlez de vos souvenirs.", {}, ""),
      C("La renvoyer", 1, {"karma": -1}, "Tu n'as plus rien à prouver.", {}, "")),
    V("Kuroko", 35, 60, "🏀 Un match entre anciens est organisé au gymnase de ton lycée.",
      C("Jouer à fond", ("pw", 110), {"bonheur": 8, "rep": 3}, "Tu retrouves tes sensations d'antan.", {"sante": -8, "bonheur": 3}, "Tes muscles te le font payer."),
      C("Arbitrer", 1, {"bonheur": 4, "karma": 2}, "Tu n'as pas perdu ton œil.", {}, ""),
      C("Assister depuis les gradins", 1, {"bonheur": 3}, "Un moment de nostalgie.", {}, "")),
    V("Tokyo Revengers", 35, 60, "🚬 Un ancien rival du quartier te demande de l'aide pour sa famille.",
      C("L'aider", .9, {"karma": 5, "rep": 3, "argent": -80}, "Tu gagnes un allié inattendu.", {"bonheur": -1}, "Il disparaît avec l'argent."),
      C("Refuser", 1, {"karma": -2}, "Il te lance un regard noir.", {}, ""),
      C("Lui proposer un petit boulot", .85, {"karma": 4, "rep": 2}, "Il s'en sort peu à peu.", {}, "")),
    V("Tokyo Revengers", 35, 60, "🏍️ Tu retrouves ta vieille moto au fond d'un garage.",
      C("La remettre en état (100)", .9, {"bonheur": 8, "mait": 1, "argent": -100}, "Elle ronronne comme au premier jour.", {"argent": -150, "bonheur": -2}, "Elle ne démarre plus jamais."),
      C("La vendre", 1, {"argent": 250, "bonheur": -2}, "Un souvenir de moins.", {}, ""),
      C("La laisser telle quelle", 1, {"bonheur": 2}, "Un souvenir intact.", {}, "")),
]

# ═════════════ Nouvelles du monde ═════════════
NEWS_TPL = {
    "Naruto": [
        "🤝 {X} et {Y} signent un traité de commerce.", "⚔️ Escarmouche à la frontière entre {X} et {Y}.",
        "🌑 L'Akatsuki serait de nouveau actif près de {X}.", "👑 Un nouveau dirigeant est désigné à {X}.",
        "🥷 {X} ouvre les inscriptions de son examen Chūnin.", "📜 La prime d'un ninja renégat grimpe dans le Bingo Book.",
        "🦠 Une épidémie touche un village proche de {X}.", "🌧️ De fortes pluies ravagent les récoltes de {X}.",
        "🏮 {X} célèbre son grand festival annuel.", "🕵️ Des espions de {X} ont été démasqués à {Y}.",
        "🦊 Des rumeurs évoquent un nouveau jinchūriki à {X}.", "🐉 Un animal d'invocation colossal est aperçu près de {X}.",
        "💰 Le prix des parchemins explose à {X}.", "🏹 Des brigands attaquent des caravanes à la frontière de {X}.",
        "🧠 {X} ouvre une nouvelle école de médecine ninja.", "🛡️ {V} renforce ses patrouilles aux frontières.",
        "📣 Le conseil de {V} annonce une grande réforme.", "🎓 De jeunes ninjas de {X} sont promus Genin.",
        "🌊 Une tempête retarde les convois entre {X} et {Y}.", "🔥 Un incendie de forêt menace les environs de {X}.",
    ],
    "Kuroko": [
        "🏀 {X} bat {Y} lors d'un match d'entraînement très disputé.", "⭐ {GM} est élu meilleur joueur du mois.",
        "🩹 {GM} est absent quelques semaines à cause d'une blessure légère.", "📰 Des recruteurs américains observent les lycées japonais.",
        "🏆 Les inscriptions de la prochaine compétition sont ouvertes.", "👟 Une marque lance une chaussure en édition limitée signée {GM}.",
        "🎥 Un documentaire sur la Génération des Miracles fait le buzz.", "🧑‍🏫 {X} change d'entraîneur.",
        "🏟️ Le gymnase de {X} est entièrement rénové.", "🚀 Un joueur de {Y} impressionne les recruteurs.",
        "💬 {GM} déclare vouloir affronter les meilleurs lycées du pays.", "📈 {X} aligne sa 5e victoire consécutive.",
        "🔥 Un match amical entre {X} et {Y} attire toute la ville.", "🎙️ Un magazine sacre {GM} « joueur le plus prometteur ».",
        "🧊 Le moral de {Y} est au plus bas après une série de défaites.", "🌟 Un lycéen inconnu fait sensation lors d'un tournoi de rue.",
    ],
    "Tokyo Revengers": [
        "🚓 La police intensifie ses patrouilles à {T}.", "🏍️ Une course de motos illégale a lieu à {T}.",
        "🔥 Un affrontement éclate entre {X} et {Y}.", "🕴️ Les yakuza étendent leur influence à {T}.",
        "📰 Un journaliste enquête sur les gangs de {T}.", "🤝 Rumeur d'une alliance entre {X} et {Y}.",
        "💥 Un entrepôt prend feu à {T}.", "🥊 Un tournoi clandestin se prépare à {T}.",
        "🌃 Un festival nocturne attire des milliers de personnes à {T}.", "👑 {X} affiche sa force lors d'un grand rassemblement.",
        "😠 Des tensions montent entre {X} et {Y} à {T}.", "🏚️ Un squat est évacué par la police à {T}.",
        "🧥 Les vestes de {X} sont à la mode chez les lycéens de {T}.", "💬 Un chef de {Y} promet de « reprendre ce qui lui appartient ».",
    ],
    None: [
        "🌤️ Une belle semaine ensoleillée apaise les esprits.", "📈 L'économie locale se porte bien.", "🌧️ Une tempête approche.",
        "🍜 Un nouveau restaurant de ramen fait fureur.", "🎆 De grandes festivités se préparent pour la saison.",
        "🚧 Des travaux paralysent plusieurs rues.", "📚 Une nouvelle bibliothèque ouvre ses portes.",
    ],
}
NEWS_STATE = {
    "ennemi": {"Naruto": ["⚔️ {E} masse des troupes près de la frontière de {V}.", "😠 Un émissaire de {E} insulte publiquement ton village."],
               "Kuroko": ["😠 Les joueurs du {E} se disent prêts à t'écraser.", "🔥 Le {E} recrute pour se venger de toi."],
               "Tokyo Revengers": ["😠 {E} menace ouvertement ton gang.", "🔥 Des membres de {E} rôdent près de tes quartiers."]},
    "allie": {"Naruto": ["🤝 {A} propose de renforcer son alliance avec {V}.", "🎎 Une délégation de {A} est attendue en visite officielle."],
              "Kuroko": ["🤝 Le {A} t'invite à un match amical.", "👏 Les supporters du {A} saluent ton équipe."],
              "Tokyo Revengers": ["🤝 {A} te fait savoir qu'il compte sur toi.", "🍶 {A} organise un banquet pour ses alliés."]},
}

# ═════════════ Petits boulots (argent de poche) ═════════════
# id, icône, nom, âge min, (gain min, max), effets, texte
JOBS = [
    ("journaux", "📰", "Distribuer les journaux", 9, (20, 45), {"force": 1}, "Tu fais ta tournée matinale."),
    ("courses", "🛒", "Faire des courses pour les voisins", 8, (15, 35), {"karma": 1}, "Les voisins te donnent un petit pourboire."),
    ("babysit", "🍼", "Garder des enfants", 12, (30, 60), {"karma": 1, "intel": 1}, "La soirée est calme… pour une fois."),
    ("magasin", "🏪", "Aider dans un magasin", 13, (35, 70), {"intel": 1}, "Tu ranges les rayons et tiens la caisse."),
    ("plonge", "🍽️", "Faire la plonge au restaurant", 14, (45, 80), {"sante": -1}, "Une pile d'assiettes à n'en plus finir."),
    ("service", "🍜", "Servir en salle", 15, (55, 95), {"popu": 1}, "Les clients te laissent des pourboires."),
    ("demenage", "📦", "Aider à déménager", 15, (50, 90), {"force": 1, "sante": -1}, "Un canapé interminable à monter."),
    ("tuteur", "📚", "Donner des cours particuliers", 16, (60, 110), {"intel": 1, "karma": 1}, "Ton élève progresse enfin."),
    # Naruto
    ("bois", "🪵", "Couper du bois pour le village", 8, (25, 50), {"force": 1}, "Tes mains en gardent les ampoules.", "Naruto"),
    ("parchemins", "📜", "Livrer des parchemins", 10, (40, 75), {"mait": 1}, "Tu cours de toit en toit.", "Naruto"),
    ("forge", "⚒️", "Aider le forgeron", 12, (50, 90), {"force": 1, "mait": 1}, "Les étincelles volent.", "Naruto"),
    ("garde", "🏮", "Garder la porte de nuit", 14, (55, 100), {"intel": 1}, "Une nuit paisible sous les lanternes.", "Naruto"),
    ("herbes", "🌿", "Cueillir des herbes médicinales", 11, (35, 70), {"intel": 1, "sante": 1}, "Tu reconnais déjà chaque plante.", "Naruto"),
    # Kuroko
    ("ramasseur", "🏀", "Ramasseur de balles", 9, (20, 40), {"mait": 1}, "Tu observes les matchs de près.", "Kuroko"),
    ("arbitre", "🦓", "Arbitrer des matchs de quartier", 13, (40, 75), {"intel": 1, "rep": 1}, "Tu siffles sans trembler.", "Kuroko"),
    ("coach_enf", "🧒", "Entraîner des enfants", 15, (50, 95), {"mait": 1, "karma": 1}, "Ils t'appellent « coach ».", "Kuroko"),
    ("sport_shop", "👟", "Vendeur en magasin de sport", 15, (55, 100), {"intel": 1}, "Tu conseilles les meilleures baskets.", "Kuroko"),
    # Tokyo Revengers
    ("ramen_moto", "🛵", "Livrer des ramen en moto", 14, (45, 85), {"mait": 1}, "Tu files entre les voitures.", "Tokyo Revengers"),
    ("bar", "🍶", "Plonger dans un bar de nuit", 15, (60, 105), {"rep": 1}, "Tu entends des histoires étranges.", "Tokyo Revengers"),
    ("mecano", "🔧", "Mécanicien de motos", 13, (50, 95), {"mait": 1, "force": 1}, "Tu as les mains pleines de cambouis.", "Tokyo Revengers"),
    ("dojo_aide", "🥋", "Aider au dojo", 12, (30, 60), {"force": 1, "mait": 1}, "Tu essuies les tatamis et observes.", "Tokyo Revengers"),
]
JOBS_BY_ID = {j[0]: j for j in JOBS}
IMMEDIAT = {"cadeau", "revive", "nature", "biju"}

# ═════════════ Rencontres amoureuses ═════════════
def _R(id, u, nom, ico, titre, genre, lieux, intro, talk):
    e = _E(id, u, nom, ico, titre, "amour", .9, lieux, 14, lambda g: not g["couple"], intro, talk)
    e["genre"] = genre
    return e

ENC += [
    _R("hinata", "Naruto", "Hinata", "🌸", "Kunoichi timide du clan Hyūga", "F", ["marche", "ramen", "academie"], "« Oh… b-bonjour. Je ne t'avais pas vu(e)… »", ["« J'admire les gens qui ne renoncent jamais. »", "« Tu es plus courageux que tu ne le crois. »"]),
    _R("ino", "Naruto", "Ino", "💐", "Fleuriste et kunoichi", "F", ["marche", "porte"], "« Hé, toi ! Une fleur pour égayer ta journée ? »", ["« Une fleur et un sourire, ça règle tout ! »", "« Je suis très exigeante, tu sais. »"]),
    _R("tenten", "Naruto", "Tenten", "🗡️", "Experte en armes", "F", ["terrain", "marche"], "« Tu t'y connais en armes ? J'adore en discuter ! »", ["« Chaque kunai a son caractère. »", "« J'aime les gens qui travaillent dur. »"]),
    _R("temari", "Naruto", "Temari", "🌬️", "Kunoichi de Suna", "F", ["porte", "foret"], "« Tu me regardes comme ça pourquoi ? Réponds. »", ["« Je n'aime pas les hommes indécis. »", "« Le vent m'a toujours guidée. »"]),
    _R("shika", "Naruto", "Shikamaru", "☁️", "Stratège paresseux", "H", ["ramen", "marche"], "« Quelle galère… mais bon, assieds-toi. »", ["« Regarder les nuages, c'est un art. »", "« Les gens compliqués, ça fatigue. »"]),
    _R("kiba", "Naruto", "Kiba", "🐕", "Ninja au flair infaillible", "H", ["terrain", "porte"], "« Hé ! Akamaru dit que tu sens plutôt bon ! »", ["« On fait la course ? »", "« Un bon ami, c'est tout ce qu'il faut. »"]),
    _R("momoi", "Kuroko", "Satsuki Momoi", "🌷", "Manageuse de génie", "F", ["gymnase", "stade", "konbini"], "« Oh, un joueur intéressant ! Je peux regarder tes statistiques ? »", ["« Les données ne mentent jamais. »", "« J'aime les gens qui progressent. »"]),
    _R("misaki", "Kuroko", "Misaki", "📣", "Supportrice passionnée", "F", ["gymnase", "stade"], "« Je t'ai vu jouer : tu étais incroyable ! »", ["« Je ne rate jamais un match ! »", "« On pourrait aller manger après ? »"]),
    _R("yui", "Kuroko", "Yui", "📚", "Camarade studieuse", "F", ["ecole", "konbini"], "« Ah, c'est toi ! Tu as pris des notes en cours ? »", ["« J'aime lire en regardant les entraînements. »", "« Je n'aurais jamais cru parler à un joueur. »"]),
    _R("sota", "Kuroko", "Sōta", "🎽", "Coéquipier plein d'énergie", "H", ["gymnase", "konbini"], "« Hé ! Un 1 contre 1 ? Ou un jus ? »", ["« Le basket, c'est la vie ! »", "« Tu fais battre mon cœur plus vite que le ballon. »"]),
    _R("ren", "Kuroko", "Ren", "🎧", "Lycéen discret et musicien", "H", ["ecole", "konbini"], "« Tu écoutes quoi, d'habitude ? »", ["« La musique et le sport, même combat. »"]),
    _R("hinata_t", "Tokyo Revengers", "Hinata Tachibana", "🌻", "Lycéenne douce et courageuse", "F", ["konbini", "temple", "shibuya"], "« Excuse-moi… on s'est déjà vus quelque part ? »", ["« J'aime les gens qui protègent les autres. »", "« Le monde est trop violent, parfois. »"]),
    _R("emma", "Tokyo Revengers", "Emma Sano", "🌺", "Sœur au caractère de feu", "F", ["temple", "dojo", "bar"], "« Toi, tu as l'air costaud. T'as quelque chose à dire ? »", ["« Je n'ai peur de personne. »", "« J'aime les gens francs. »"]),
    _R("yuzuha", "Tokyo Revengers", "Yuzuha", "🕶️", "Combattante mystérieuse", "F", ["bar", "shibuya"], "« Tu me suis, ou c'est le hasard ? »", ["« Je ne fais confiance qu'à ceux qui se battent. »"]),
    _R("naoto", "Tokyo Revengers", "Naoto", "🧠", "Jeune homme sérieux et intelligent", "H", ["konbini", "temple"], "« Salut. Je cherche quelqu'un avec qui discuter. »", ["« La violence ne résout rien. »", "« J'aime les gens qui réfléchissent. »"]),
    _R("mitsuya", "Tokyo Revengers", "Mitsuya", "🧵", "Couturier talentueux", "H", ["konbini", "shibuya", "temple"], "« Tu portes bien cette veste. Je pourrais la retoucher ! »", ["« Un bon vêtement, c'est de l'armure. »"]),
]
ENC_BY_ID.update({_e["id"]: _e for _e in ENC})

# ═════════════ Événements de dirigeant (Naruto) ═════════════
EV_MORE += [
    V("Naruto", 28, 90, "🏛️ Le conseil de ton village réclame un bilan de ton action à la tête de la communauté.",
      C("Présenter un bilan honnête", .85, {"rep": 5, "karma": 4}, "Le conseil apprécie ta franchise.", {"rep": -2}, "Certains anciens t'accusent d'avoir échoué."),
      C("Enjoliver les chiffres", .5, {"rep": 6, "karma": -3}, "Personne n'y voit rien.", {"rep": -8, "karma": -4}, "La supercherie est démasquée."),
      C("Envoyer un conseiller à ta place", 1, {"rep": -1}, "Tu délègues cette corvée.", {}, ""), cond="flag:kage"),
    V("Naruto", 28, 90, "🕊️ Le chef d'un autre village te demande une entrevue privée.",
      C("L'accueillir en personne", .8, {"rep": 5, "relx": ["A", 8]}, "Votre rencontre est cordiale.", {"relx": ["A", -4]}, "Les débats tournent à la dispute."),
      C("Envoyer un émissaire", .9, {"relx": ["A", 3]}, "Le message est transmis.", {}, ""),
      C("Refuser", 1, {"relx": ["A", -8], "rep": -1}, "L'affront est noté.", {}, ""), cond="flag:kage"),
    V("Naruto", 28, 90, "😠 Un jeune ninja prometteur remet publiquement en cause ton autorité.",
      C("Le défier en duel", ("pw", 180), {"rep": 8, "xp": 20}, "Tu rappelles qui commande.", {"sante": -15, "rep": -5}, "Il t'humilie devant la foule."),
      C("L'écouter et le nommer à un poste", .8, {"karma": 5, "rep": 5}, "Tu transformes un rival en allié.", {"rep": -2}, "Il prend cela pour une faiblesse."),
      C("Le faire taire", .5, {"rep": 2, "karma": -6}, "Il se tait… pour l'instant.", {"rep": -6, "karma": -6}, "On t'accuse de tyrannie."), cond="flag:kage"),
    V("Naruto", 28, 90, "💰 Les daimyō exigent plus de missions pour moins de paie.",
      C("Négocier fermement", ("st", "rep", 60), {"argent": 300, "rep": 5}, "Tu obtiens de meilleurs tarifs.", {"rep": -3}, "Les daimyō menacent d'aller voir ailleurs."),
      C("Accepter pour le bien du village", 1, {"karma": 2, "argent": 80}, "Tes ninjas travaillent dur.", {}, ""),
      C("Refuser net", .6, {"rep": 4}, "Ton village te soutient.", {"argent": -200, "rep": -3}, "Les daimyō coupent les financements."), cond="flag:kage"),
]

EV.extend(EV_NEW)
EV.extend(EV_EXTRA)
EV.extend(EV_MORE)
BIJU_EV = [i for i, e in enumerate(EV) if e[0] == "SPECIAL" and e[5] == "pacte"][0]
GM_EV = [i for i, e in enumerate(EV) if e[0] == "SPECIAL" and e[5] == "gm"][0]
AKAT_EV = [i for i, e in enumerate(EV) if e[0] == "SPECIAL" and e[5] == "akat"][0]

DEFIS = [
    ("d1", "Atteindre 18 ans", lambda g: g["age"] >= 18, {"argent": 200}),
    ("d2", "Apprendre 3 techniques", lambda g: len(g["tech"]) >= 3, {"argent": 300, "xp": 30}),
    ("d3", "Gagner 5 duels", lambda g: g["wins"] >= 5, {"argent": 400, "xp": 40}),
    ("d4", "Avoir 1000 d'argent", lambda g: g["argent"] >= 1000, {"xp": 50}),
    ("d5", "Atteindre 80 de réputation", lambda g: g["rep"] >= 80, {"argent": 500}),
    ("d6", "Maîtriser une nature niveau 3", lambda g: max(list(g["nat"].values()) or [0]) >= 3, {"xp": 60}),
    ("d7", "Atteindre le 3e rang", lambda g: rang(g)[0] >= 2, {"argent": 600}),
    ("d8", "Débloquer une nature rare", lambda g: any(n in g["nat"] for n in ("Glace", "Bois")), {"xp": 100}),
    ("d9", "Être en couple", lambda g: bool(g["couple"]), {"bonheur": 20, "argent": 200}),
    ("d10", "Survivre jusqu'à 40 ans", lambda g: g["age"] >= 40, {"xp": 150}),
    ("d11", "Devenir porteur d'un bijū", lambda g: bool(g["biju"]), {"xp": 80}),
    ("d13", "Devenir un héros (karma ≥ 60)", lambda g: g["karma"] >= 60, {"rep": 10, "argent": 300}),
    ("d14", "Rejoindre l'Akatsuki", lambda g: g["akatsuki"], {"xp": 100}),
    ("d15", "Voler 2 pupilles", lambda g: len(g["pupilles"]) >= 2, {"xp": 200, "argent": 500}),
    ("d12", "Atteindre 60 de lien avec ton bijū", lambda g: bool(g["biju"]) and g["biju"]["lien"] >= 60, {"xp": 200, "argent": 500}),
]
# ───────────────────────── LOGIQUE ─────────────────────────
ICON = {k: lab.split()[0] for k, lab in STATS}
ICON.update(argent="💴", xp="✨", karma="☯️", lien="🔗")


def _delta(k, v):
    try: st.session_state.setdefault("dl", []).append((k, v))
    except Exception: pass


def L(g, txt):
    g["log"].append([g["age"], txt] + ([g.get("trim", 0)] if g.get("u") == "Kuroko" else []))
    try:
        if txt.startswith(WIN_PREFIX): st.session_state["fx"] = "win"
        elif txt.startswith(LOSE_PREFIX): st.session_state.setdefault("fx", "lose")
    except Exception: pass


def clamp(x, a, b): return max(a, min(b, x))


def stage(g):
    a = g["age"]
    return "Bébé" if a < 3 else "Petit enfant" if a < 6 else "Enfant" if a < 13 else "Adolescent" if a < 18 else "Adulte" if a < 60 else "Senior"


def nom_complet(g):
    f = (g.get("fam") or {}).get("nom")
    return f"{g['nom']} {f}" if f else g["nom"]


def fmt(g, s):
    v = g.get("village")
    k = VILL.get(v, {}).get("kage", "Kage")
    s = s.replace("{K}", k).replace("{V}", v or "ton village")
    if "kage" in g.get("flags", []):
        s = s.replace("ton Kage", "ton conseil").replace("invité comme conseiller", "convié en tant que dirigeant")
    if "{A}" in s or "{E}" in s:
        ae = g.get("_ae")
        if not ae:
            e = g.get("event")
            ae = (e.get("A"), e.get("E")) if isinstance(e, dict) else (None, None)
        s = s.replace("{A}", ae[0] or (allies(g) or ["un allié"])[0]).replace("{E}", ae[1] or (ennemis(g) or ["un rival"])[0])
    return s


def karma_label(k):
    return "Héros" if k >= 60 else "Bon" if k >= 20 else "Neutre" if k > -20 else "Louche" if k > -60 else "Sombre"


def depenser(g):
    if g["pa"] <= 0: return False
    g["pa"] -= 1
    return True


def ajouter_flag(g, f):
    if f not in g["flags"]: g["flags"].append(f)


# ───────── Naissance ─────────
def tirer_fam(u): return random.choices(FAM[u], weights=[f[4] for f in FAM[u]])[0]


def deux_nat(inn):
    base = [n for n in inn if n in BASE_NAT]
    if len(base) == 1 and random.random() < .12:
        inn.append(random.choice([n for n in BASE_NAT if n not in inn]))


def init_naruto(g, perks, ch, her):
    c = v = None
    if her:
        c, v = her["clan"], her["village"]
    elif perks.get("talent_choix") and ch.get("clan"):
        c = None if ch["clan"] == "Sans clan" else ch["clan"]
        v = CLANS[c]["v"] if c else random.choice(list(VILL))
    elif perks.get("prestige"):
        c = random.choice(PRESTIGE); v = CLANS[c]["v"]
    else:
        v = random.choices(list(VILL), weights=[VILL[x]["w"] for x in VILL])[0]
        pool = [k for k, d in CLANS.items() if d["v"] == v]
        if pool and random.random() < .5:
            c = random.choices(pool, weights=[CLANS[k]["w"] for k in pool])[0]
    cd = CLANS.get(c, {})
    g["clan"], g["village"] = c, v
    sn = (her or {}).get("fam") or c or random.choice(SURN)
    g["fam"] = dict(nom=sn, type=f"Clan {c}" if c else "Famille de villageois", d=cd.get("d", "Une famille ordinaire de ton village."))
    if her and her.get("nat"): inn = list(her["nat"])
    elif perks.get("nat_choix") and ch.get("nat"): inn = [ch["nat"]]
    elif cd.get("nat"): inn = list(cd["nat"])
    else: inn = [random.choices(VILL[v]["nat"], weights=[5, 4, 3, 2, 1])[0]]
    if perks.get("don") and not her:
        extra = [n for n in BASE_NAT if n not in inn]
        if len([x for x in inn if x in BASE_NAT]) < 2 and extra: inn.append(random.choice(extra))
    elif not her:
        deux_nat(inn)
    g["nat_innee"] = inn
    if cd.get("eye"): g["oeil"] = [cd["eye"], cd["eage"]]
    ap(g, cd.get("bonus", {}))
    g["fact"] = {n: dict(rel=random.randint(10, 40), allie=False) for n in UNIV["Naruto"]["fact"] if n != v}
    L(g, f"{VILL[v]['ico']} Tu naîs à {v}" + (f", dans le clan {cd['ico']} {c}." if c else ", dans une famille sans clan."))
    ch_b = 1.0 if perks.get("biju") else cd.get("biju", .03)
    if not her and random.random() < ch_b:
        get_biju(g); L(g, "😱 Un bijū a été scellé en toi dès la naissance !")


def init_kuroko(g, perks, ch, her):
    f = tirer_fam("Kuroko")
    g["fam"] = dict(nom=(her or {}).get("fam") or random.choice(SURN), type=f[0], d=f[1])
    g["riche"] = f[3]; ap(g, f[2])
    if her and her.get("talent"): k = her["talent"]
    elif perks.get("talent_choix") and ch.get("talent"): k = ch["talent"]
    elif perks.get("prestige"): k = random.choice(["freestyle", "empereur", "belial"])
    else: k = random.choices(list(TALENTS), weights=[t[5] for t in TALENTS.values()])[0]
    g["talent"] = dict(k=k, lvl=1)
    ap(g, TALENTS[k][3])
    g["zpot"] = 1.25 if perks.get("don") else (her or {}).get("zpot") or random.choices([.8, 1.0, 1.25], weights=[3, 5, 2])[0]
    g["fact"] = {n: dict(rel=random.randint(10, 40), allie=False) for n in UNIV["Kuroko"]["fact"]}
    L(g, f"🏠 {f[0]} : {f[1]}")
    L(g, f"✨ Tu naîs avec un talent inné : {TALENTS[k][1]} {TALENTS[k][0]} !")
    L(g, f"⚡ Potentiel de Zone : {ZPOT_LBL[g['zpot']]}.")


def init_tr(g, perks, ch, her):
    if perks.get("prestige"): f = [x for x in FAM["Tokyo Revengers"] if x[0] == "Famille de yakuza"][0]
    elif perks.get("talent_choix") and ch.get("origine"): f = [x for x in FAM["Tokyo Revengers"] if x[0] == ch["origine"]][0]
    else: f = tirer_fam("Tokyo Revengers")
    g["fam"] = dict(nom=(her or {}).get("fam") or random.choice(SURN), type=f[0], d=f[1])
    g["riche"] = f[3]; ap(g, f[2])
    g["style"] = random.choice(["Karatéka", "Karatéka", "Boxeur"] if f[0] == "Famille de dojo" else STYLES)
    L(g, f"🥋 Ton style de combat : {g['style']}.")
    if perks.get("don") and not her: ap(g, {"force": 20})
    if her and her.get("monde"):
        g["monde"], g["libres"] = her["monde"], her["libres"]
    else:
        monde_init(g)
    g["fact"] = {n: dict(rel=random.randint(10, 40), allie=False) for n in UNIV["Tokyo Revengers"]["fact"] if n in g["monde"]}
    L(g, f"🏠 {f[0]} : {f[1]}")


ZPOT_LBL = {.8: "faible", 1.0: "moyen", 1.25: "élevé"}


def new_game(nom, u, perks=None, her=None, ch=None, av=None):
    perks, ch = perks or {}, ch or {}
    g = dict(v=SAVE_V, nom=nom, u=u, age=0, sante=random.randint(70, 95), bonheur=random.randint(60, 80),
             intel=random.randint(10, 40), force=random.randint(5, 20), mait=random.randint(0, 5),
             chakra=random.randint(5, 25) if u == "Naruto" else 0, rep=0, argent=0, xp=0, pa=PA, cadeau=0, revive=0, wins=0,
             couple="", riche=random.randint(1, 3), nat={}, tech=[], defis_ok=[], dead=False, cause="",
             event=None, biju=None, log=[], pnj=[], karma=0, akatsuki=False, pupilles=[], zone=0, zxp=0, sports={}, talent=None,
             recrue="", gm={n: 0 for n in GM}, match=None, cup=None, cal={}, fact={}, beaute=random.randint(25, 70),
             fam=None, clan=None, village=None, nat_innee=[], oeil=None, enfants=[], arcs_done=[], flags=[],
             cap=1 if u == "Naruto" else 5, gang=None, monde=None, libres=[], pro=None, titres={}, lycee="", zpot=1.0,
             cool={}, lignee=(her or {}).get("lignee", 1), ancetres=(her or {}).get("anc", []), achats=[], captures=0, her_gang=None, _who=None, enc=None, bat=None, patron=None, style="",
             av=av or random_av(), notes=random.randint(40, 65), popu=random.randint(30, 55), clique="", clubs=[], social={}, offres={}, trim=0, amitie={}, file=[], vus=[], news=[], palmares=[], inv={}, metiers={}, vol_bonus=0, vol_echecs=0)
    g["pref"] = "F" if g["av"].get("genre") == "H" else "H"
    L(g, f"🌱 {nom} naît. {UNIV[u]['intro']}")
    if perks.get("beaute"): g["beaute"] = 95
    if perks.get("beaute_choix"): g["beaute"] = BEAUTES.get(ch.get("beaute"), g["beaute"])
    if perks.get("esprit"): g["intel"] = min(100, g["intel"] + 20); g["mait"] += 10
    if perks.get("fer"): g["sante"] = 100; g["force"] += 15
    if perks.get("fortune"): g["riche"] = 5; g["argent"] += 500
    if perks.get("second"): g["revive"] += 1
    {"Naruto": init_naruto, "Kuroko": init_kuroko, "Tokyo Revengers": init_tr}[u](g, perks, ch, her)
    sn = g["fam"]["nom"]
    if her:
        g["pnj"].append(dict(nom=f"{her['parent2']} (parent)" if her.get("parent2") else f"{random.choice(PF)} (mère)", role="famille", aff=70, niv=1, trait="bienveillant"))
        g["argent"] += her.get("argent", 0); g["rep"] = clamp(her.get("rep", 0), 0, 100)
        L(g, f"🕯️ Tu es l'héritier(e) de {her['anc'][-1]}. La lignée continue.")
    else:
        for nm, r in (("mère", random.choice(PF)), ("père", random.choice(PM))):
            g["pnj"].append(dict(nom=f"{r} ({nm})", role="famille", aff=random.randint(50, 85), niv=1, trait=random.choice(TRAITS)))
        for _ in range(random.choice([0, 0, 1, 1, 2])):
            s = random.choice(["f", "m"])
            g["pnj"].append(dict(nom=f"{random.choice(KF if s == 'f' else KM)} ({'sœur' if s == 'f' else 'frère'})", role="famille", aff=random.randint(40, 80), niv=1, trait=random.choice(TRAITS)))
    if g["beaute"] >= 85: L(g, "💄 Tu es d'une beauté remarquable.")
    faire_nouvelles(g, 2)
    return g


def monde_init(g):
    ts = TERRS[:]; random.shuffle(ts)
    m = {}
    for i, (n, f) in enumerate(GFORCE.items()):
        fo = f + random.randint(-8, 8)
        m[n] = dict(force=fo, membres=int(fo * 1.5), terr=[ts[i]])
    g["monde"], g["libres"] = m, ts[len(GFORCE):]


PNJ_TXT = {"ami": "devient ton ami(e)", "rival": "devient ton rival(e)", "amour": "te fait battre le cœur",
           "mentor": "devient ton mentor", "equipier": "devient ton équipier(ère)"}


def ajouter_pnj(g, role):
    pool = [n for n in UNIV[g["u"]]["pnj"] if n not in [p["nom"] for p in g["pnj"]]]
    if pool:
        p = dict(nom=random.choice(pool), role=role, aff=random.randint(25, 50), niv=round(random.uniform(.7, 1.3), 2), trait=random.choice(TRAITS))
        if role == "mentor": p["aff"] = random.randint(35, 55); p["niv"] = 2.0; p["trait"] = random.choice(["loyal", "bienveillant", "courageux"])
        g["pnj"].append(p)
        L(g, f"👥 {p['nom']} {PNJ_TXT[role]}.")


def get_biju(g):
    if g["biju"]:
        return
    i = random.randrange(9)
    g["biju"] = dict(nom=f"{BIJU[i][0]} ({i + 1} queue{'s' if i else ''})", ico=BIJU[i][1], lien=10)
    ap(g, {"chakra": 20, "force": 8})
    ajouter_flag(g, "biju")
    L(g, f"{BIJU[i][1]} {BIJU[i][0]} est maintenant scellé en toi !")


# ───────── Effets spéciaux ─────────
def recruter(g, nom=None):
    if g["recrue"] or g["u"] != "Kuroko":
        return
    nom = nom or max(g["gm"], key=lambda n: (g["gm"][n], random.random()))
    g["recrue"] = nom
    lyc = GM[nom][0]
    rejoindre_lycee(g, lyc, silent=True)
    ajouter_amitie(g, nom, 25)
    ap(g, {"xp": 60, "rep": 10})
    L(g, f"🌟 {nom} te recrute dans le {lyc} !")


def donner_pupille(g, n):
    if n not in g["pupilles"]:
        g["pupilles"].append(n)
        L(g, f"✨ Pupille éveillée : {PUP[n][0]} {n} !")


def allier_auto(g):
    c = [n for n, f in g["fact"].items() if not f["allie"] and n != (g["gang"] or {}).get("nom")]
    if c and sum(f["allie"] for f in g["fact"].values()) < 3:
        faire_alliance(g, random.choice(c))


def gagner_titre(g, k):
    g["titres"][k] = g["titres"].get(k, 0) + 1
    if k == "nba" and g["pro"]: g["pro"]["titres"] += 1


def signer_pro(g, team):
    if g["pro"]: return
    if team == "auto" or team not in NBA: team = random.choice(list(NBA))
    g["pro"] = dict(team=team, saisons=0, titres=0, ppg=0.0, retraite=False)
    ajouter_flag(g, "pro")
    L(g, f"🇺🇸 Tu signes aux {team} : te voilà joueur NBA !")


def rejoindre_gang(g, nom):
    m = g["monde"]
    if m is None or g["gang"]: return
    if nom not in m:
        c = sorted(m, key=lambda n: m[n]["force"])[:3]
        nom = random.choice(c)
    g["gang"] = dict(nom=nom, rang=0, gxp=0, chef=False)
    L(g, f"🏍️ Tu rejoins {nom}. Ta nouvelle vie commence.")


def mon_monde(g):
    gg = g.get("gang")
    return g["monde"].get(gg["nom"]) if gg and g.get("monde") else None


def nterr(g):
    m = mon_monde(g)
    return len(m["terr"]) if m else 0


def dissoudre_si_vide(g, src):
    d = g["monde"].get(src)
    m = mon_monde(g)
    if d is not None and not d["terr"] and m is not None and src != g["gang"]["nom"]:
        m["force"] += d["force"] // 2; m["membres"] += d["membres"] // 2
        del g["monde"][src]; g["fact"].pop(src, None)
        L(g, f"🏴 {src} est dissous ! Ses membres rejoignent ton gang.")


def gagner_terr(g, n=1):
    m = mon_monde(g)
    if not m: return
    for _ in range(n):
        src = None
        if g["libres"]:
            t = g["libres"].pop(random.randrange(len(g["libres"])))
        else:
            autres = [k for k, v in g["monde"].items() if k != g["gang"]["nom"] and v["terr"]]
            if not autres: break
            src = random.choice(autres)
            t = g["monde"][src]["terr"].pop(random.randrange(len(g["monde"][src]["terr"])))
        m["terr"].append(t)
        L(g, f"🗺️ Ton gang prend {t}" + (f" à {src}." if src else "."))
        if src: dissoudre_si_vide(g, src)


def perdre_terr(g, n=1):
    m = mon_monde(g)
    for _ in range(n):
        if m and m["terr"]:
            t = m["terr"].pop(random.randrange(len(m["terr"])))
            g["libres"].append(t)
            L(g, f"🚩 Ton gang perd le contrôle de {t}.")


def who(g):
    w = g.get("_who")
    return next((p for p in g["pnj"] if p["nom"] == w), None) if w else None


def ap(g, eff):
    for k, v in eff.items():
        _delta(k, v)
        if k == "alrel":
            for f in g["fact"].values():
                if f["allie"]: f["rel"] = clamp(f["rel"] + v, 0, 100)
        elif k == "argent": g[k] = max(0, g[k] + v)
        elif k in ("xp", "pa", "cadeau", "revive"): g[k] += v
        elif k == "win": g["wins"] += v
        elif k == "nature": eveiller(g)
        elif k == "biju": get_biju(g)
        elif k == "recrue": recruter(g)
        elif k == "karma": g[k] = clamp(g[k] + v, -100, 100)
        elif k == "akatsuki":
            g["akatsuki"] = True
            L(g, "🌑 Tu rejoins l'Akatsuki. Ton village te considère désormais comme un traître.")
        elif k == "lien":
            if g["biju"]: g["biju"]["lien"] = clamp(g["biju"]["lien"] + v, 0, 100)
        elif k == "aff":
            p = who(g)
            if p: p["aff"] = clamp(p["aff"] + v, 0, 100)
        elif k == "ruptpnj":
            p = who(g)
            if p:
                g["pnj"].remove(p)
                if g["couple"] == p["nom"]: g["couple"] = ""
                L(g, f"👋 {p['nom']} quitte définitivement ta vie.")
        elif k == "flag": ajouter_flag(g, v)
        elif k == "cap": g["cap"] = max(g["cap"], v)
        elif k == "xpmin": g["xp"] = max(g["xp"], v)
        elif k == "titre": gagner_titre(g, v)
        elif k == "pro": signer_pro(g, v)
        elif k == "lycee": rejoindre_lycee(g, v)
        elif k == "gang": rejoindre_gang(g, v)
        elif k == "terr":
            (gagner_terr if v > 0 else perdre_terr)(g, abs(v))
        elif k == "membres":
            m = mon_monde(g)
            if m: m["membres"] = max(0, m["membres"] + v)
        elif k == "gfor":
            m = mon_monde(g)
            if m: m["force"] = max(0, m["force"] + v)
        elif k == "pupille": donner_pupille(g, v)
        elif k == "allie": allier_auto(g)
        elif k == "rompre":
            n_ = _res(g, v); f = g["fact"].get(n_)
            if f and f["allie"]:
                f["allie"] = False; f["rel"] = 0
                L(g, f"💔 L'alliance avec {n_} est rompue.")
        elif k == "ennemi": devenir_ennemi(g, _res(g, v))
        elif k == "paix": conclure_paix(g, _res(g, v))
        elif k == "relx":
            f = g["fact"].get(_res(g, v[0]))
            if f: f["rel"] = clamp(f["rel"] + v[1], 0, 100)
        elif k == "amitie":
            n_ = v[0] if v[0] in GM else (max(GM, key=lambda x: g["amitie"].get(x, 0)) if v[0] == "auto" else None)
            if n_: ajouter_amitie(g, n_, v[1])
        else: g[k] = clamp(g[k] + v, 0, 100)


def revele_nat(g):
    if not g["nat_innee"] and not g["nat"]:
        g["nat_innee"] = [random.choice(BASE_NAT)]
    for n in g["nat_innee"]:
        if n not in g["nat"]:
            g["nat"][n] = 1
            L(g, f"🔮 Le papier de chakra réagit : nature {NAT[n]} {n} !")


def eveiller(g):
    base = [n for n in g["nat"] if n in BASE_NAT]
    dispo = [n for n in BASE_NAT if n not in g["nat"]]
    if len(base) >= 2 or not dispo:
        L(g, "🔮 Ton corps ne supporte pas une nature de base supplémentaire.")
    elif random.random() < .6:
        n = random.choice(dispo); g["nat"][n] = 1
        L(g, f"🔮 Seconde nature de chakra éveillée : {NAT[n]} {n} !")
    else:
        ap(g, {"sante": -10})
        L(g, "🔮 Le parchemin se consume sans éveiller de nouvelle nature.")


def debloquer_rares(g):
    n = g["nat"]
    for new, (a, b), ico in (("Glace", ("Eau", "Vent"), "❄️"), ("Bois", ("Terre", "Eau"), "🌳"), ("Lave", ("Feu", "Terre"), "🌋")):
        if new not in n and n.get(a, 0) >= 3 and n.get(b, 0) >= 3 and g["age"] >= 15:
            n[new] = 1; L(g, f"{ico} Fusion {a} + {b} : nature rare {new.upper()} débloquée !")


# ───────── État du personnage ─────────
def rang(g):
    a = g["age"]
    ix = max(i for i, t in enumerate(RANK_TH) if g["xp"] >= t)
    ia = max(i for i, t in enumerate(RANK_AGE) if a >= t)
    i = min(ix, ia)
    if g["u"] == "Naruto": i = min(i, g["cap"])
    if g["u"] == "Tokyo Revengers":
        gg = g.get("gang")
        if gg and gg["chef"]: i = 5
        elif gg: i = min(i, gg["rang"])
        elif a >= 12: return 0, "Sans gang"
    if a < 6: return 0, "Petit enfant"
    if a < 12: return 0, UNIV[g["u"]]["pre"]
    if g["akatsuki"]: return i, "Membre de l'Akatsuki"
    return i, UNIV[g["u"]]["ranks"][i]


def puissance(g):
    p = g["force"] * .5 + g["mait"] * .6 + (g["chakra"] * .4 if g["u"] == "Naruto" else 0) + sum(g["nat"].values()) * 3 + g["intel"] * .1
    p += sum(TECH[t]["pw"] for t in g["tech"] if t in TECH)
    p += sum(PUP[n][2] for n in g["pupilles"])
    p += 7 * sum(f["allie"] for f in g["fact"].values()) + g["zone"] * 8 + sum(g["sports"].values()) * 3
    if sum(1 for v in g["sports"].values() if v >= 2) >= 3: p += 10
    if g["talent"]: p += TALENTS[g["talent"]["k"]][4] * g["talent"]["lvl"]
    if g["recrue"]: p += 12
    if g["clan"]: p += CLANS[g["clan"]].get("pw", 0)
    if g["pro"]: p += 20
    if g.get("patron"): p += ORGS.get(g["patron"]["org"], {}).get("pw", 0)
    p += 4 * sum(1 for v in g.get("amitie", {}).values() if v >= 60)
    p += 4 * len([f for f in ("chunin", "jonin", "anbu", "kage") if f in g["flags"]])
    m = mon_monde(g)
    if m: p += m["membres"] * .15 + len(m["terr"]) * 2 + g["gang"]["rang"] * 3
    if g["biju"]:
        p += 15 + g["biju"]["lien"] * .4 + (25 if g["biju"]["lien"] >= 60 else 0)
    return p


def proba(g, p):
    if isinstance(p, (list, tuple)):
        if p[0] == "pw":
            return clamp(.5 + (puissance(g) - p[1]) / p[1] * .5, .08, .92)
        if p[0] == "st":
            return clamp(.15 + .77 * min(1, g[p[1]] / p[2]), .1, .92)
    return p


def mort(g, cause, vieux=False):
    if g["revive"] > 0:
        g["revive"] -= 1
        g["sante"] = 50
        L(g, "⏳ L'amulette Time Leap s'active : tu reviens à la vie !")
        return
    g["dead"] = True
    g["cause"] = cause
    g["event"] = None
    if vieux: ajouter_flag(g, "vieillesse")


def score(g):
    s = int(g["xp"] + g["rep"] * 5 + sum(g["nat"].values()) * 50 + len(g["tech"]) * 100 + g["age"] * 10 + len(g["pupilles"]) * 80 + g["karma"] // 2
            + (g["biju"]["lien"] * 3 if g["biju"] else 0))
    s += sum(g["titres"].values()) * 150 + nterr(g) * 100 + len(g["enfants"]) * 50
    if g["pro"]: s += 200 + g["pro"]["saisons"] * 20
    if "ultime" in g["flags"]: s += 500
    return s


def verifie_objectifs(g):
    f = g["flags"]
    if g["u"] == "Naruto":
        if "elite" not in f and rang(g)[0] >= 3 and not g["akatsuki"]:
            ajouter_flag(g, "elite"); L(g, "🎖️ Tu es devenu un ninja d'élite : l'objectif de ta vie est accompli !")
        if "kage" in f and "ultime" not in f:
            ajouter_flag(g, "ultime")
    elif g["u"] == "Kuroko":
        if "lycee_champion" not in f and g["titres"].get("inter", 0) + g["titres"].get("winter", 0) >= 1:
            ajouter_flag(g, "lycee_champion"); L(g, "🏆 Tu as fait gagner ton lycée : un rêve d'adolescent accompli !")
        if "ultime" not in f and g["titres"].get("nba", 0) >= 1:
            ajouter_flag(g, "ultime"); L(g, "👑 Champion NBA : tu as dépassé la Génération des Miracles !")
    else:
        if "ultime" not in f and nterr(g) >= DOMINATION:
            ajouter_flag(g, "ultime"); L(g, "👑 Tu domines le Japon : tous les gangs te reconnaissent !")


# ───────── Événements ─────────
def ev_ok(g, e):
    if e[0] not in (None, g["u"]) or not (e[1] <= g["age"] <= e[2]):
        return False
    c = e[5] if len(e) > 5 else None
    if not c: return True
    if c == "biju": return bool(g["biju"])
    if c == "ally": return any(f["allie"] for f in g["fact"].values())
    if c == "gang": return bool(g["gang"])
    if c == "nogang": return not g["gang"]
    if c == "pro": return bool(g["pro"])
    if c == "couple": return bool(g["couple"])
    if c == "nocouple": return not g["couple"]
    if c == "enfant": return bool(g["enfants"])
    if c == "riche": return g["argent"] >= 800
    if c == "pauvre": return g["argent"] < 100
    if c == "celeb": return g["rep"] >= 50
    if c == "ecole": return en_ecole(g)
    if c == "ennemi": return bool(ennemis(g))
    if c.startswith("flag:"): return c[5:] in g["flags"]
    if c.startswith("noflag:"): return c[7:] not in g["flags"]
    return True


def arc_dispo(g):
    return [a for a in ARCS if a["u"] == g["u"] and a["a"][0] <= g["age"] <= a["a"][1] and (a.get("rep") or a["id"] not in g["arcs_done"])
            and g["cool"].get(a["id"], 0) <= g["age"] and (g["u"] != "Kuroko" or not a.get("q") or g.get("trim", 0) in a["q"]) and a["cond"](g)]


def lancer_arc(g, aid):
    al = allies(g)
    A = random.choice(al) if al else (random.choice(list(g["fact"])) if g["fact"] else "")
    pool = ennemis(g) or [n for n in g["fact"] if n not in al and n != A]
    E = random.choice(pool) if pool else A
    g["event"] = dict(arc=aid, step=0, ok=0, A=A, E=E)


def ev_courant(g):
    e = g["event"]
    if isinstance(e, int):
        ev = EV[e]
        return ev[3], ev[4], "ev"
    if "arc" in e:
        arc = ARC_BY_ID[e["arc"]]
        s = arc["steps"][e["step"]]
        return f"**{fmt(g, arc['nom'])}** — étape {e['step'] + 1}/{len(arc['steps'])}\n\n{fmt(g, s['t'])}", s["ch"], "arc"
    t_ = e["t"]
    if e.get("titre"): t_ = f"**{e['titre']}**\n\n{t_}"
    return t_, e["ch"], "dyn"


def pnjs(g, *roles): return [p for p in g["pnj"] if p["role"] in roles]


def ev_dyn(g):
    a, u = g["age"], g["u"]
    o = []
    for p in pnjs(g, "rival"):
        if a >= 8:
            seuil = (5 + a * 1.5 + rang(g)[0] * 15) * p["niv"]
            o.append((3, dict(who=p["nom"], t=f"😤 {p['nom']}, ton rival, te provoque devant tout le monde : un duel ?", ch=[
                ["Relever le défi", ["pw", seuil], {"xp": 15, "rep": 6, "aff": 5, "win": 1}, "Tu l'emportes sous les regards !", {"sante": -12, "rep": -3, "aff": 3}, "Il t'humilie, mais tu respectes sa force."],
                ["Ignorer la provocation", 1, {"karma": 1}, "Tu gardes ton sang-froid.", {}, ""]])))
    for p in pnjs(g, "ami", "equipier"):
        if a >= 6:
            o.append((2, dict(who=p["nom"], t=f"🤝 {p['nom']} te propose de vous entraîner ensemble.", ch=[
                ["Accepter", .9, {"mait": 3, "force": 2, "aff": 8, "bonheur": 3}, "Vous progressez tous les deux.", {"sante": -6, "aff": 2}, "Vous vous blessez en forçant."],
                ["Refuser", 1, {"aff": -5}, "Il est un peu déçu.", {}, ""]])))
        if a >= 12:
            o.append((1, dict(who=p["nom"], t=f"💸 {p['nom']} a des difficultés d'argent et te demande 80.", ch=[
                ["Lui prêter", .85, {"argent": -80, "aff": 15, "karma": 3}, "Il te remboursera, tu le sais.", {"argent": -80, "aff": -6}, "Il disparaît avec l'argent."],
                ["Refuser", 1, {"aff": -8}, "Il s'éloigne, blessé.", {}, ""]])))
    for p in pnjs(g, "amour"):
        if a >= 13 and g["couple"] != p["nom"]:
            o.append((2, dict(who=p["nom"], t=f"💗 {p['nom']} te propose une sortie ce week-end.", ch=[
                ["Accepter avec plaisir", .8, {"bonheur": 8, "aff": 10}, "Un moment merveilleux.", {"bonheur": -3, "aff": -3}, "Le rendez-vous tourne à la gêne."],
                ["Décliner", 1, {"aff": -6}, "Tu laisses passer l'occasion.", {}, ""]])))
    for p in pnjs(g, "famille"):
        if a >= 8:
            o.append((1, dict(who=p["nom"], t=f"🏥 {p['nom']} tombe malade et a besoin de soins coûteux (150).", ch=[
                ["Payer les soins", 1, {"argent": -150, "aff": 12, "karma": 4}, "Il/elle se rétablit, reconnaissant(e).", {}, ""],
                ["Ne pas payer", 1, {"aff": -15, "karma": -4}, "La famille t'en veut.", {}, ""]])))
    for p in pnjs(g, "mentor"):
        if a >= 10:
            o.append((2, dict(who=p["nom"], t=f"🎓 {p['nom']}, ton mentor, te propose une mission plus difficile que d'habitude.", ch=[
                ["Accepter", ["pw", 25 + a * 2.5], {"xp": 25, "mait": 4, "aff": 8, "rep": 4}, "Tu relèves le défi avec brio.", {"sante": -15, "aff": 2}, "Tu échoues, mais il t'encourage."],
                ["Reporter", 1, {"aff": -3}, "Il hausse les épaules.", {}, ""]])))
    for p in [q for q in pnjs(g, "ami", "equipier") if q["trait"] in ("ambitieux", "rusé", "jaloux") and q["aff"] < 55 and a >= 12]:
        t = {"Naruto": f"🗡️ {p['nom']} vendait des informations à un village rival !", "Kuroko": f"🗡️ {p['nom']} a transmis tes tactiques à l'équipe adverse.",
             "Tokyo Revengers": f"🗡️ {p['nom']} a vendu tes plans à un gang rival !"}[u]
        o.append((3, dict(who=p["nom"], t="Trahison ! " + t, ch=[
            ["Le confronter", .6, {"rep": 8, "xp": 15, "ruptpnj": 1}, "Tu le démasques devant tous.", {"sante": -12, "rep": -3, "ruptpnj": 1}, "Il s'enfuit en te blessant."],
            ["Lui laisser une chance", .5, {"karma": 6, "aff": 10}, "Il te remercie, repentant.", {"bonheur": -6, "rep": -4, "aff": -10}, "Il recommence dans ton dos."],
            ["Le dénoncer", .85, {"rep": 4, "karma": 1, "ruptpnj": 1}, "Il est écarté.", {"rep": -2, "ruptpnj": 1}, "On te reproche ta dureté."]])))
    for n, f in g["fact"].items():
        if f["allie"] and f["rel"] < 45:
            o.append((3, dict(who=None, t=f"🗡️ {n}, ton allié, te tourne le dos et se range du côté de tes ennemis !", ch=[
                ["Riposter", ["pw", 60 + a], {"xp": 20, "rep": 6, "rompre": n}, "Tu leur fais payer leur trahison.", {"sante": -15, "rep": -3, "rompre": n}, "Ils t'écrasent."],
                ["Négocier", .5, {"rep": 3, "alrel": 4}, "L'alliance tient bon.", {"rompre": n, "rep": -2}, "Les négociations échouent."]])))
    m = mon_monde(g)
    if m and m["terr"] and a >= 14:
        riv = [k for k in g["monde"] if k != g["gang"]["nom"]]
        if riv:
            att = random.choice(riv)
            o.append((3, dict(who=None, t=f"🚨 {att} attaque l'un de tes territoires !", ch=[
                ["Défendre en première ligne", ["pw", g["monde"][att]["force"] * .9], {"xp": 20, "rep": 8}, "Tu repousses l'assaut.", {"sante": -15, "terr": -1}, "Tu perds le quartier."],
                ["Envoyer des renforts", .6, {"gfor": 2, "rep": 3}, "Tes hommes tiennent la ligne.", {"membres": -2, "terr": -1}, "Tes hommes sont débordés."],
                ["Abandonner le quartier", 1, {"terr": -1, "rep": -6}, "Tu cèdes sans combattre.", {}, ""]])))
    if u == "Naruto" and a >= 13:
        o.append((1, dict(who=None, t="🌍 Un ninja d'un autre pays te défie : il veut mesurer sa force à celle de ton village.", ch=[
            ["Relever le défi", ["pw", 20 + a * 2.2], {"xp": 25, "rep": 8, "win": 1}, "Tu honores ton village !", {"sante": -15, "rep": -3}, "Tu es battu."],
            ["Décliner", 1, {}, "Tu évites le conflit.", {}, ""]])))
    for p in pnjs(g, "ami", "equipier"):
        if u == "Kuroko" and a >= 13:
            o.append((2, dict(who=p["nom"], t=f"🩹 {p['nom']} se blesse gravement lors d'un match : il sera absent des semaines.", ch=[
                ["Lui rendre visite chaque jour", 1, {"aff": 15, "karma": 3, "bonheur": -2}, "Votre amitié en sort renforcée.", {}, ""],
                ["Prendre sa place de titulaire", .7, {"mait": 3, "rep": 5, "aff": -8}, "Tu saisis ta chance, mais il t'en veut un peu.", {"bonheur": -4}, "La pression est trop forte."],
                ["Payer ses soins (150)", 1, {"argent": -150, "aff": 20, "karma": 5}, "Il n'oubliera jamais ce geste.", {}, ""]])))
        if u == "Tokyo Revengers" and a >= 13:
            o.append((2, dict(who=p["nom"], t=f"🚓 {p['nom']} se fait arrêter par la police après une bagarre.", ch=[
                ["Payer sa caution (150)", 1, {"argent": -150, "aff": 15, "karma": 2}, "Il sort et te remercie.", {}, ""],
                ["Aller témoigner pour lui", .6, {"aff": 12, "rep": 3}, "Ton témoignage le sauve.", {"rep": -4, "aff": 3}, "Tu es suspecté à ton tour."],
                ["Ne rien faire", 1, {"aff": -12}, "Il se sent abandonné.", {}, ""]])))
        if u == "Naruto" and a >= 12:
            o.append((2, dict(who=p["nom"], t=f"🩸 {p['nom']} est gravement blessé pendant une mission.", ch=[
                ["Le ramener au village", ["pw", 60 + a * 2], {"aff": 18, "karma": 5, "xp": 15}, "Tu le sauves de justesse.", {"sante": -15, "aff": 8}, "Tu arrives épuisé, mais il est vivant."],
                ["Le soigner sur place", ("st", "intel", 55), {"aff": 15, "karma": 4}, "Tes soins le stabilisent.", {"aff": 3}, "Tes soins sont insuffisants."],
                ["Poursuivre la mission", .8, {"xp": 20, "aff": -15, "karma": -4}, "Tu termines sans lui.", {"aff": -15, "rep": -3}, "La mission échoue."]])))
    o += ev_dyn2(g)
    if not o: return None
    return random.choices([x[1] for x in o], weights=[x[0] for x in o])[0]


def resoudre(g, ci):
    e = g["event"]
    g["_ae"] = (e.get("A"), e.get("E")) if isinstance(e, dict) and "A" in e else None
    try: _resoudre_core(g, ci)
    finally: g["_ae"] = None
    if g["dead"]: g["file"] = []
    elif g["event"] is None and g["file"]: g["event"] = g["file"].pop(0)


def _resoudre_core(g, ci):
    e = g["event"]
    txt, chs, kind = ev_courant(g)
    lab, p, eo, to, ek, tk = chs[ci]
    g["_who"] = e.get("who") if isinstance(e, dict) else None
    ok = random.random() < proba(g, p)
    lab, to, tk = fmt(g, lab), fmt(g, to), fmt(g, tk)
    if ok:
        ap(g, eo); L(g, f"✅ {lab}" + (f" → {to}" if to else ""))
    else:
        ap(g, ek); L(g, f"❌ {lab}" + (f" → {tk}" if tk else ""))
    g["_who"] = None
    if isinstance(e, dict) and "arc" in e:
        arc = ARC_BY_ID[e["arc"]]
        stp = arc["steps"][e["step"]]
        if ok: e["ok"] += 1
        fini = echec = False
        if not ok and stp.get("ko") == "end": fini = echec = True
        elif e["step"] + 1 >= len(arc["steps"]):
            fini = True; echec = e["ok"] < arc.get("need", len(arc["steps"]))
        else:
            e["step"] += 1
        if fini:
            g["event"] = None
            if not echec:
                if arc["fin"]["eff"]: ap(g, arc["fin"]["eff"])
                if arc["fin"]["txt"]: L(g, fmt(g, arc["fin"]["txt"]))
                if not arc.get("rep"): g["arcs_done"].append(arc["id"])
            else:
                L(g, f"🚫 {fmt(g, arc['nom'])} : " + fmt(g, arc.get("ko_txt", "Tu n'obtiens pas la gloire espérée.")))
                if not arc.get("rep"): g["arcs_done"].append(arc["id"])
                else: g["cool"][arc["id"]] = g["age"] + 2
    else:
        g["event"] = None
    if g["sante"] <= 0 and not g["dead"]:
        mort(g, "Tué par les événements de la vie.")
    verifie_objectifs(g)


# ───────── Les années passent ─────────
PNJ_AGE = [(4, "ami"), (7, "ami"), (9, "rival"), (12, "mentor"), (12, "equipier"), (13, "amour"), (13, "equipier"), (15, "rival")]


def saison_pro(g):
    p = g["pro"]
    if p["retraite"]: return
    p["saisons"] += 1
    ppg = round(max(4, 8 + g["mait"] * .25 + g["force"] * .1 + random.uniform(-3, 5) - max(0, g["age"] - 33) * .8), 1)
    p["ppg"] = ppg
    sal = 500 + int(g["mait"] * 6)
    g["argent"] += sal
    ap(g, {"xp": 20, "rep": 3 if ppg > 18 else 1})
    L(g, f"🇺🇸 Saison NBA {p['saisons']} avec les {p['team']} : {ppg} pts/match, salaire +{sal}.")
    if g["age"] >= 41:
        p["retraite"] = True
        L(g, "🏁 Tu prends ta retraite sportive, couvert de gloire.")


def gang_annuel(g):
    m = mon_monde(g)
    if not m: return
    gg = g["gang"]
    rev = 25 * len(m["terr"]) + (0 if gg["chef"] else 10 * gg["rang"])
    if rev:
        ap(g, {"argent": rev}); L(g, f"💴 Revenus du gang : +{rev}.")
    gg["gxp"] += 5
    for k, v in g["monde"].items():
        if k != gg["nom"]: v["force"] += random.randint(0, 2)
    if gg["chef"]: m["membres"] += random.randint(0, 3)
    for k, v in list(g["monde"].items()):
        if k != gg["nom"] and v["terr"] and random.random() < .25 and g["age"] >= 12:
            tgt = [x for x in g["monde"] if x != k and g["monde"][x]["terr"] and x != gg["nom"]]
            if tgt:
                b = random.choice(tgt)
                if v["force"] * random.uniform(.8, 1.2) > g["monde"][b]["force"] * random.uniform(.8, 1.2):
                    t = g["monde"][b]["terr"].pop()
                    v["terr"].append(t)
                    L(g, f"📰 {k} prend {t} à {b}."); news(g, f"📰 {k} prend {t} à {b}.")
                    if not g["monde"][b]["terr"] and b != gg["nom"]:
                        del g["monde"][b]; g["fact"].pop(b, None)
                        L(g, f"📰 {b} est anéanti."); news(g, f"📰 {b} est anéanti.")
                break


def vieillir(g, quiet=False):
    g["age"] += 1
    g["pa"] = pa_max(g)
    a = g["age"]
    g["match"] = None
    g["cup"] = None
    if g["u"] == "Kuroko":
        g["trim"] = 0
        g["cal"] = calendrier(g)
    L(g, f"🎂 Anniversaire : {a} an{'s' if a > 1 else ''} ({stage(g)}).")
    if g["u"] == "Kuroko" and g["cal"]:
        noms = [COMP[k][0] for k in g["cal"] if k in COMP]
        if noms: L(g, "📅 Cette année, tu peux participer à : " + ", ".join(noms) + ".")
    m = UNIV[g["u"]]["mile"].get(a)
    if m: L(g, f"🏫 {m}")
    if g["talent"] and a == 12 and g["talent"]["lvl"] < 5:
        g["talent"]["lvl"] += 1
        L(g, f"✨ Ton talent « {TALENTS[g['talent']['k']][0]} » s'éveille pleinement !")
    ap(g, {"intel": random.randint(0, 2) if a >= 3 else 1, "force": random.randint(0, 2) if a < 30 else -1})
    if a >= 45: ap(g, {"sante": -random.randint(1, 4)})
    else: ap(g, {"sante": 3})
    if 6 <= a < UNIV[g["u"]]["jobage"]:
        s = 10 * g["riche"]; g["argent"] += s
        L(g, f"👛 Argent de poche : +{s} {UNIV[g['u']]['monnaie']}.")
    elif a >= UNIV[g["u"]]["jobage"]:
        s = (20 + 15 * rang(g)[0]) * random.randint(1, 3); g["argent"] += s
        L(g, f"💴 Revenus de l'année : +{s} {UNIV[g['u']]['monnaie']}.")
    if g["karma"] >= 50: ap(g, {"rep": 2})
    elif g["karma"] <= -50 and not g["akatsuki"]: ap(g, {"rep": -2})
    if g["recrue"]: ap(g, {"xp": 10, "rep": 2})
    if g.get("patron") and not quiet:
        o_ = ORGS.get(g["patron"]["org"], {})
        ap(g, {k_: o_[k_] for k_ in ("xp", "rep", "mait", "force", "sante", "argent", "karma") if k_ in o_})
        L(g, f"🎓 {g['patron']['nom']} t'enseigne cette année ({o_.get('nom', '')}).")
    if 6 <= a <= 18:
        g["notes"] = clamp(g["notes"] + int((g["intel"] - 50) / 25) + random.randint(-4, 4), 0, 100)
        g["popu"] = clamp(g["popu"] + random.randint(-3, 3), 0, 100)
        if g["clique"] and not quiet: ap(g, CLIQUES[g["clique"]][1])
    if g["social"] and not quiet:
        inc = sum(g["social"].values()) // 40
        if inc: ap(g, {"argent": inc}); L(g, f"📱 Revenus de tes réseaux : +{inc}.")
    if a == 6 and g["u"] == "Naruto": revele_nat(g)
    if g.get("oeil") and a >= g["oeil"][1]: donner_pupille(g, g["oeil"][0])
    for age_p, role in PNJ_AGE:
        if a == age_p: ajouter_pnj(g, role)
    for p in g["pnj"]:
        p["aff"] = max(0, p["aff"] - random.randint(0, 4))
    for n, f in g["fact"].items():
        if f["allie"]:
            ap(g, {"xp": 5, "rep": 1, "argent": 15})
            f["rel"] = min(100, f["rel"] + random.randint(0, 3) - (6 if g["karma"] <= -40 else 0))
            if f["rel"] < 20:
                f["allie"] = False; L(g, f"💔 {n} rompt l'alliance.")
        else:
            f["rel"] = max(0, f["rel"] - random.randint(0, 2))
    if g.get("her_gang") and a >= 14 and not g["gang"]:
        g["gang"], g["her_gang"] = g["her_gang"], None
        L(g, f"👑 Tu hérites de la direction de {g['gang']['nom']} !")
    if quiet: return
    if a >= 10 and g.get("enc") is None and random.random() < .08:
        e_ = rencontre(g, None, "recruteur")
        if e_:
            e_["line"] = "« Je te cherchais. » " + e_["line"]; g["enc"] = e_
            L(g, f"👀 {e_['nom']} ({e_['titre']}) vient à ta rencontre.")
    if g["u"] == "Tokyo Revengers": gang_annuel(g)
    if g["pro"]: saison_pro(g)
    if g["biju"] and g["biju"]["lien"] < 25 and random.random() < .15:
        ap(g, {"sante": -20, "rep": -10, "bonheur": -8})
        L(g, f"👹 {g['biju']['nom']} prend le contrôle ! Tu causes des dégâts autour de toi...")
    faire_nouvelles(g, 2 if g["u"] == "Kuroko" else 3)
    if g["u"] == "Kuroko": news_resultats(g, 3, a - 1)
    if len(g["log"]) > 500: g["log"] = g["log"][-400:]
    verifie_objectifs(g)
    if g["sante"] <= 0:
        mort(g, "Épuisement et blessures."); return
    if a > 60 and random.random() < (a - 60) / 100:
        mort(g, "Mort de vieillesse, entouré de souvenirs.", vieux=True); return
    tirer_evenement(g)

# ───────── Duels, matchs, compétitions ─────────
def duel(g, niv, nom):
    mine = puissance(g) * random.uniform(.8, 1.2)
    foe = (5 + g["age"] * 1.5 + rang(g)[0] * 15) * niv * random.uniform(.8, 1.2)
    if mine >= foe:
        g["wins"] += 1
        ap(g, {"xp": int(10 * niv) + 5, "rep": 3, "argent": 30})
        L(g, f"⚔️ Tu bats {nom} ! (puissance {int(mine)} vs {int(foe)})")
        return True
    else:
        ap(g, {"sante": -random.randint(8, 20), "bonheur": -3})
        L(g, f"💥 {nom} te bat... (puissance {int(mine)} vs {int(foe)})")
        if g["sante"] <= 0:
            mort(g, f"Tué lors d'un duel contre {nom}.")
        return False


def choisir(g, ch, nom):
    lab, p, eo, to, ek, tk = ch
    ok = random.random() < p
    eff = dict(eo if ok else ek)
    d = eff.pop("gmi", 0)
    g["gm"][nom] = max(0, min(100, g["gm"][nom] + d))
    ap(g, eff)
    L(g, f"{'💬' if ok else '😬'} {nom} — {lab} : {to if ok else tk}")


def opp_niv(g, opp):
    if opp in NBA: return NBA[opp]
    f = list(g["fact"])
    return .9 + .5 * f.index(opp) / max(1, len(f) - 1) if opp in f else 1.0


def adversaires(g):
    if g.get("pro"): return [t for t in NBA if t != g["pro"]["team"]]
    own = set()
    if g["recrue"]: own.add(GM[g["recrue"]][0])
    if g["lycee"]: own.add(g["lycee"])
    return [n for n in g["fact"] if n not in own]


def demarrer_match(g, opp, cup=False):
    g["match"] = dict(opp=opp, q=1, me=0, en=0, talent=0, zone=False, cup=cup, lines=[], fini=False)


def talent_usages(g):
    return 2 if g["talent"] and g["talent"]["lvl"] >= 3 else 1


def jouer_quart(g, tac):
    m = g["match"]
    allies = sum(f["allie"] for f in g["fact"].values())
    a = 12 + puissance(g) * .18 + 3 * allies
    b = (12 + g["age"] * .4 + rang(g)[0] * 4) * opp_niv(g, m["opp"])
    tag = ""
    if m["zone"]:
        a += 5 * g["zone"]; tag += " ⚡Zone"
    if tac == "def":
        a *= .9; b *= .75; tag += " 🛡️Défense"
    elif tac == "duo" and duo_partner(g):
        pr_ = duo_partner(g); a += 12 if pr_ == g["recrue"] else 8
        g["gm"][pr_] = min(100, g["gm"][pr_] + 2); ajouter_amitie(g, pr_, 1); tag += f" 🌟Duo avec {pr_}"
    elif tac == "talent" and g["talent"] and m["talent"] < talent_usages(g):
        t = g["talent"]; mm, ad, ma = TALENT_FX[t["k"]]; f = .6 + .1 * t["lvl"]
        a = a * (1 + (mm - 1) * f * 2) + ad * f * 2
        b *= 1 - (1 - ma) * f * 1.5
        m["talent"] += 1; tag += f" {TALENTS[t['k']][1]}{TALENTS[t['k']][0]}"
    qa = int(a * random.uniform(.8, 1.2))
    qb = int(b * random.uniform(.8, 1.2))
    m["me"] += qa; m["en"] += qb
    m["lines"].append(f"Q{m['q']} : {qa}-{qb}{tag}")
    m["q"] += 1
    if m["q"] > 4:
        finir_match(g)


def finir_match(g):
    m = g["match"]
    me, en = m["me"], m["en"]
    if m["zone"]:
        ap(g, {"sante": -6 * g["zone"]})
    if me == en:
        me += random.choice([-2, 2])
    win = me > en
    k = 1.5 if m["cup"] else 1
    if win:
        ap(g, {"xp": int(25 * k), "rep": int(6 * k), "argent": int(80 * k), "bonheur": 4, "win": 1})
        L(g, f"🏀 Victoire {me}-{en} contre {m['opp']} !")
    else:
        ap(g, {"xp": 5, "bonheur": -5})
        L(g, f"😞 Défaite {me}-{en} contre {m['opp']}.")
    m["fini"] = True
    m["res"] = [win, me, en]
    if m["cup"] and g["cup"]:
        c = g["cup"]
        if win:
            c["i"] += 1
            if c["i"] >= len(c["opps"]):
                ap(g, c["rew"])
                L(g, f"🏆 Tu remportes la {c['nom']} !")
                g["palmares"].append([g["age"], g.get("trim", 0), c["key"]])
                news(g, f"🏆 {g['lycee'] or g['nom']} remporte la compétition « {c['nom']} » !")
                if c["key"] in ("college", "inter", "winter", "nba"): gagner_titre(g, c["key"])
                if c["key"] == "perso":
                    for n, (lyc, _, _) in GM.items():
                        if lyc in c["opps"] or lyc in c.get("equipes", []): g["gm"][n] = min(100, g["gm"][n] + 8)
                g["cup"] = None
        else:
            L(g, f"❌ Tu es éliminé de la {c['nom']} en {c['rounds'][c['i']].lower()}.")
            g["cup"] = None
    verifie_objectifs(g)
    if g["sante"] <= 0:
        mort(g, "Épuisé par l'effort de la Zone.")


def _nouvelle_cup(g, key, nom, rounds, opps, rew, aide=None, equipes=None):
    g["cup"] = dict(key=key, nom=nom, rounds=rounds, opps=opps, i=0, rew=rew, aide=aide or [], equipes=equipes or [])
    L(g, f"📣 Tu t'inscris à la {nom} !")
    demarrer_match(g, opps[0], True)


def demarrer_cup(g, key):
    nom, _, rounds, rew = COMP[key]
    g["cal"][key] = False
    pool = adversaires(g)
    opps = sorted(random.sample(pool, min(len(rounds), len(pool))), key=lambda n: opp_niv(g, n))
    _nouvelle_cup(g, key, nom, rounds[:len(opps)], opps, rew)


def organiser_tournoi(g, equipes):
    n = len(equipes)
    if n not in (3, 7): return "Choisis 3 ou 7 équipes."
    cout = 100 * (n + 1)
    if g["age"] < 15 or g["rep"] < 15: return "Il faut avoir 15 ans et 15 de réputation."
    if g["argent"] < cout: return f"Il faut {cout} pour l'organisation."
    if not depenser(g): return "Plus d'actions cette année."
    g["argent"] -= cout
    o = equipes[:]; random.shuffle(o)
    aide = []

    def ia(x, y):
        sx, sy = opp_niv(g, x) * random.uniform(.8, 1.2), opp_niv(g, y) * random.uniform(.8, 1.2)
        w, l = (x, y) if sx >= sy else (y, x)
        aide.append(f"{w} bat {l} {random.randint(65, 95)}-{random.randint(50, 64)}")
        return w
    opps = [o[0]]
    if n == 3:
        opps.append(ia(o[1], o[2])); rounds = ["Demi-finale", "Finale"]
    else:
        w2 = ia(o[1], o[2]); w3 = ia(o[3], o[4]); w4 = ia(o[5], o[6]); wb = ia(w3, w4)
        opps += [w2, wb]; rounds = ["Quart de finale", "Demi-finale", "Finale"]
    rew = {"xp": 40 + 10 * n, "rep": 8 + n, "argent": cout + 100 * n}
    _nouvelle_cup(g, "perso", f"Tournoi de {g['nom']}", rounds, opps, rew, aide, equipes)
    return None


# ───────── Gang (Tokyo Revengers) ─────────
def mission_gang(g):
    m = mon_monde(g)
    if not m or not depenser(g): return "Plus d'actions !"
    gg = g["gang"]
    if random.random() < clamp(.55 + (puissance(g) - 30 - gg["rang"] * 25) / 200, .3, .9):
        gx = 10 + 5 * gg["rang"]
        gg["gxp"] += gx; ap(g, {"xp": 12, "rep": 3, "argent": 40})
        L(g, f"🏍️ Mission de gang réussie : +{gx} points de gang.")
    else:
        ap(g, {"sante": -10, "bonheur": -2}); L(g, "💥 La mission de gang tourne mal.")
        if g["sante"] <= 0: mort(g, "Tué lors d'une mission de gang.")
    return None


def recruter_membres(g):
    m = mon_monde(g)
    if not m or not (g["gang"]["chef"] or g["gang"]["rang"] >= 2): return "Il faut être commandant ou chef."
    if g["argent"] < 80: return "Il faut 80."
    if not depenser(g): return "Plus d'actions !"
    g["argent"] -= 80; n = random.randint(3, 6); m["membres"] += n
    L(g, f"📣 {n} nouveaux membres rejoignent {g['gang']['nom']}.")
    return None


def entrainer_gang(g):
    m = mon_monde(g)
    if not m: return "Pas de gang."
    if g["argent"] < 60: return "Il faut 60."
    if not depenser(g): return "Plus d'actions !"
    g["argent"] -= 60; n = random.randint(2, 4); m["force"] += n
    L(g, f"🥊 Entraînement de la troupe : force du gang +{n}.")
    return None


def promotion(g):
    gg = g["gang"]
    if not gg or gg["chef"] or gg["rang"] >= 4: return "Plus de promotion possible ici."
    nx = gg["rang"] + 1
    if gg["gxp"] < GRANG_TH[nx] or g["rep"] < GRANG_REP[nx]:
        return f"Il faut {GRANG_TH[nx]} points de gang et {GRANG_REP[nx]} de réputation."
    gg["rang"] = nx
    ap(g, {"rep": 4})
    L(g, f"🎖️ Promotion dans {gg['nom']} : {UNIV['Tokyo Revengers']['ranks'][nx]} !")
    return None


def defier_chef(g):
    gg = g["gang"]; m = mon_monde(g)
    if not gg or gg["chef"] or gg["rang"] < 4: return "Il faut être Bras droit."
    if not depenser(g): return "Plus d'actions !"
    if puissance(g) * random.uniform(.8, 1.2) >= m["force"] * 1.1 * random.uniform(.8, 1.2):
        gg["chef"], gg["rang"] = True, 5
        ajouter_flag(g, "chef"); ap(g, {"rep": 15, "xp": 60})
        L(g, f"👑 Tu terrasses l'ancien chef : tu diriges désormais {gg['nom']} !")
    else:
        ap(g, {"sante": -20, "rep": -5}); L(g, "💥 Le chef te bat. Il te laisse une dernière chance.")
        if g["sante"] <= 0: mort(g, "Tué par le chef de son gang.")
    return None


def fonder_gang(g, nom):
    nom = nom.strip()
    if g["gang"] or g["monde"] is None: return "Tu es déjà dans un gang."
    if not nom or nom in g["monde"]: return "Choisis un nom unique."
    if g["age"] < 14 or g["rep"] < 20: return "Il faut 14 ans et 20 de réputation."
    if g["argent"] < 300: return "Il faut 300."
    g["argent"] -= 300
    t = None
    if g["libres"]: t = g["libres"].pop()
    else:
        faible = min((k for k in g["monde"] if len(g["monde"][k]["terr"]) > 0), key=lambda k: g["monde"][k]["force"])
        t = g["monde"][faible]["terr"].pop()
    g["monde"][nom] = dict(force=15, membres=3, terr=[t])
    g["gang"] = dict(nom=nom, rang=5, gxp=0, chef=True)
    ajouter_flag(g, "chef"); ap(g, {"rep": 8})
    L(g, f"🏍️ Tu fondes {nom} et prends {t} comme premier territoire !")
    for k in list(g["monde"]):
        if k != nom and not g["monde"][k]["terr"]:
            del g["monde"][k]; g["fact"].pop(k, None)
    return None


def quitter_gang(g):
    if not g["gang"]: return
    L(g, f"🚪 Tu quittes {g['gang']['nom']}.")
    ap(g, {"rep": -5})
    g["gang"] = None


def attaquer_terr(g, owner, terr=None):
    """Retourne (message d'erreur | None, résultat | None)."""
    m = mon_monde(g)
    if not m: return "Il faut un gang.", None
    gg = g["gang"]
    if not (gg["chef"] or gg["rang"] >= 2) or g["age"] < 14: return "Il faut être capitaine (14 ans minimum).", None
    if owner != "libre" and g["fact"].get(owner, {}).get("allie"): return "Tu ne peux pas attaquer un allié.", None
    if not depenser(g): return "Plus d'actions !", None
    mine = (puissance(g) + m["force"] * .5 + m["membres"] * .3) * random.uniform(.8, 1.2)
    if owner == "libre": foe = random.uniform(70, 110)
    else:
        d = g["monde"][owner]
        foe = (d["force"] + d["membres"] * .3) * (1.5 + .1 * len(d["terr"])) * random.uniform(.8, 1.2)
    win = mine >= foe
    if win:
        src = g["libres"] if owner == "libre" else g["monde"][owner]["terr"]
        t = terr if terr in src else random.choice(src)
        src.remove(t)
        m["terr"].append(t)
        ap(g, {"xp": 25, "rep": 6, "win": 1, "karma": -2 if owner != "libre" else 0})
        L(g, f"🗺️ Ton gang prend {t}" + (f" à {owner}." if owner != "libre" else "."))
        if owner != "libre": dissoudre_si_vide(g, owner)
        m["membres"] = max(1, m["membres"] - random.randint(0, 2))
    else:
        ap(g, {"sante": -12, "bonheur": -3}); m["membres"] = max(1, m["membres"] - random.randint(1, 4))
        L(g, f"💥 L'assaut échoue ({int(mine)} vs {int(foe)}).")
        if g["sante"] <= 0: mort(g, "Tué en tentant de conquérir un territoire.")
    verifie_objectifs(g)
    return None, (win, int(mine), int(foe))


# ───────── Famille ─────────
def avoir_enfant(g):
    if not g["couple"] or not (18 <= g["age"] <= 45): return "Il faut être en couple et avoir entre 18 et 45 ans."
    if len(g["enfants"]) >= 4: return "Ta famille est déjà nombreuse."
    if not depenser(g): return "Plus d'actions !"
    if random.random() >= .65:
        L(g, "💞 Vous essayez de fonder une famille, sans succès cette année.")
        return None
    s = random.choice(["f", "m"])
    e = dict(nom=random.choice(KF if s == "f" else KM), sexe=s, nai=g["age"])
    if g["u"] == "Kuroko" and g["talent"]:
        e["talent"] = g["talent"]["k"] if random.random() < .6 else random.choices(list(TALENTS), weights=[t[5] for t in TALENTS.values()])[0]
    if g["u"] == "Naruto":
        e["clan"] = g["clan"] if (g["clan"] and random.random() < .7) else (random.choice(list(CLANS)) if random.random() < .3 else None)
        if g["nat_innee"]: e["nat"] = random.sample(g["nat_innee"], 1)
    g["enfants"].append(e)
    g["pnj"].append(dict(nom=f"{e['nom']} (enfant)", role="enfant", aff=90, niv=1, trait=random.choice(TRAITS)))
    ap(g, {"bonheur": 12, "karma": 2})
    L(g, f"👶 {e['nom']} vient au monde ! Ta famille s'agrandit.")
    return None


def heriter(p, e):
    age = max(0, p["age"] - e["nai"])
    gg = p["gang"]
    her = dict(fam=p["fam"]["nom"], clan=e.get("clan") if p["u"] == "Naruto" else None, village=p["village"], talent=e.get("talent"),
               zpot=p["zpot"], nat=e.get("nat") or [], monde=p["monde"], libres=p["libres"], parent2=p["couple"], lignee=p["lignee"] + 1,
               argent=p["argent"] // 2, rep=p["rep"] // 3, anc=p["ancetres"] + [nom_complet(p)])
    g = new_game(e["nom"], p["u"], her=her, av=mix_av(p["av"]))
    if p["u"] == "Naruto" and her["clan"] is None: g["fam"] = dict(nom=p["fam"]["nom"], type="Famille de villageois", d="Une famille ordinaire de ton village.")
    if gg and gg["chef"]:
        g["her_gang"] = dict(nom=gg["nom"], rang=5, gxp=0, chef=True)
    for _ in range(age): vieillir(g, quiet=True)
    if g["u"] == "Naruto": g["cap"] = 1 if age < 14 else 2 if age < 22 else 3
    g["xp"] = max(g["xp"], age * 6 + (RANK_TH[g["cap"]] if g["u"] == "Naruto" and age >= 12 else 0))
    if g["u"] == "Kuroko" and age >= 15 and not g["lycee"]:
        g["lycee"] = random.choice(list(LYCEES_SEL))
    g["log"] = [[age, f"🕯️ Tu reprends le flambeau de {her['anc'][-1]}, à {age} ans. L'héritage de ta famille te précède."]]
    g["pa"] = pa_max(g)
    return g


# ───────── Profil, records, cimetière, sauvegarde ─────────
def new_profile(): return dict(v=SAVE_V, gems=0, inv={}, rec={}, defis=[], cim=[])


def maj_rec(prof, g):
    r = prof["rec"]
    for k, v in (("age", g["age"]), ("wins", g["wins"]), ("rep", g["rep"]), ("argent", g["argent"]), ("rang", rang(g)[0]), ("tech", len(g["tech"])),
                 ("enfants", len(g["enfants"])), ("gen", g["lignee"] - 1), ("terr", nterr(g)), ("zone", g["zone"]),
                 ("titres_l", g["titres"].get("inter", 0) + g["titres"].get("winter", 0)), ("karma_abs", abs(g["karma"]))):
        r[k] = max(r.get(k, 0), v)
    fl = r.setdefault("flags", [])
    for f in g["flags"]:
        if f not in fl and not f.startswith(("ev_", "s_")): fl.append(f)


def epitaphe(f):
    if "ultime" in f: return "Une légende dont on parlera pendant des générations."
    if "kage" in f: return "Il/elle a guidé son village jusqu'à la fin."
    if "elite" in f: return "Un(e) ninja d'élite respecté(e)."
    if "pro" in f: return "Un(e) joueur(se) qui a fait vibrer les parquets."
    if "chef" in f: return "Chef de gang : la rue se souvient de son nom."
    if "vieillesse" in f: return "Une longue vie, paisible dans sa chute."
    return "Une vie comme une autre, mais la sienne."


def enterrer(prof, g):
    if g.get("enterre"): return
    g["enterre"] = True
    maj_rec(prof, g)
    u = prof["rec"].setdefault("univs", [])
    if g["u"] not in u: u.append(g["u"])
    prof["cim"].append(dict(nom=nom_complet(g), u=g["u"], age=g["age"], cause=g["cause"], score=score(g), rang=rang(g)[1], gen=g["lignee"],
                            clan=g["clan"], village=g["village"], enfants=[e["nom"] for e in g["enfants"]], titres=g["titres"], flags=g["flags"],
                            couple=g["couple"], pro=g["pro"]["team"] if g["pro"] else "", terr=nterr(g), tech=len(g["tech"]),
                            ep=epitaphe(g["flags"]), log=g["log"][-25:]))
    prof["cim"] = prof["cim"][-80:]


DEFAULTS = dict(fam=None, clan=None, village=None, nat_innee=[], oeil=None, enfants=[], arcs_done=[], flags=[], gang=None, monde=None, libres=[],
                pro=None, titres={}, lycee="", zpot=1.0, cool={}, lignee=1, ancetres=[], achats=[], captures=0, her_gang=None, match=None, cup=None, cal={}, enc=None, bat=None, patron=None, style="",
                notes=50, popu=40, clique="", clubs=[], social={}, offres={}, trim=0, amitie={}, file=[], vus=[], news=[], palmares=[], inv={}, metiers={}, vol_bonus=0, vol_echecs=0)


def migrer(g):
    import copy
    for k, v in DEFAULTS.items(): g.setdefault(k, copy.deepcopy(v))
    g.setdefault("beaute", random.randint(25, 70))
    if not g.get("av"): g["av"] = random_av()
    if not g.get("pref"): g["pref"] = "F" if g["av"].get("genre") == "H" else "H"
    g.setdefault("cap", 5)
    g["v"] = SAVE_V
    for p in g["pnj"]: p.setdefault("trait", random.choice(TRAITS))
    if g["u"] == "Naruto":
        if not g["village"]: g["village"] = random.choice(list(VILL))
        for n in UNIV["Naruto"]["fact"]:
            if n != g["village"]: g["fact"].setdefault(n, dict(rel=random.randint(10, 40), allie=False))
    if g["u"] == "Kuroko":
        for n in UNIV["Kuroko"]["fact"]: g["fact"].setdefault(n, dict(rel=random.randint(10, 40), allie=False))
    if g["u"] == "Tokyo Revengers":
        if g["monde"] is None: monde_init(g)
        for n in UNIV["Tokyo Revengers"]["fact"]:
            if n in g["monde"]: g["fact"].setdefault(n, dict(rel=random.randint(10, 40), allie=False))
    if g["u"] == "Tokyo Revengers" and not g.get("style"): g["style"] = random.choice(STYLES)
    if not g["fam"]: g["fam"] = dict(nom=random.choice(SURN), type="Famille", d="")
    return g


def sauvegarde(prof, g):
    return json.dumps({"v": SAVE_V, "profile": prof, "g": g}, ensure_ascii=False)


def charger(data):
    """Retourne (profil, vie) ou lève ValueError."""
    if "profile" in data:
        prof = data["profile"]
        for k, v in new_profile().items(): prof.setdefault(k, v)
        g = data.get("g")
        return prof, (migrer(g) if g else None)
    if "u" in data and "nom" in data and data.get("v") in (5, 6, 7):
        return None, migrer(data)
    raise ValueError("Format de sauvegarde inconnu.")


def defis_dispo(prof):
    return [(i, t, c, r) for i, t, c, r in META_DEFIS if i not in prof["defis"]]


# ═════════════ Techniques : cohérence avec ta voie ═════════════
def req_ok(g, r):
    t = r[0]
    if t == "nat": return g["nat"].get(r[1], 0) >= r[2], f"{NAT[r[1]]} {r[1]} niv. {r[2]}"
    if t == "pup": return r[1] in g["pupilles"], f"pupille {r[1]}"
    if t == "clan": return g.get("clan") == r[1], f"clan {r[1]}"
    if t == "talent": return bool(g["talent"] and g["talent"]["k"] == r[1]), f"talent {TALENTS[r[1]][0]}"
    if t == "flag": return r[1] in g["flags"], "porteur de bijū" if r[1] == "biju" else r[1]
    if t == "any":
        res = [req_ok(g, x) for x in r[1]]
        return any(o for o, _ in res), " ou ".join(x for _, x in res)
    return g.get(t, 0) >= r[1], f"{t} ≥ {r[1]}"


def tech_info(g, t):
    """Retourne (apprenable, texte des prérequis, dans_ta_voie)."""
    r = t["req"]
    base, txt = req_ok(g, r)
    ok, voie = base, True
    if r[0] in ("pup", "clan", "talent", "any", "flag"): voie = base
    elif r[0] == "nat": voie = r[1] in g["nat"]
    if t.get("mait_min"):
        txt += f" + maîtrise ≥ {t['mait_min']}"; ok = ok and g["mait"] >= t["mait_min"]
    if t.get("tal"):
        tk = g["talent"]["k"] if g["talent"] else None
        tok = tk in t["tal"]
        txt += " + talent : " + ", ".join(TALENTS[x][0] for x in t["tal"]); ok = ok and tok; voie = voie and tok
    if t.get("sty"):
        sok = g.get("style") in t["sty"]
        txt += " + style : " + ", ".join(t["sty"]); ok = ok and sok; voie = voie and sok
    return ok, txt, voie


def apprendre(g, k):
    t = TECH[k]
    ok, _, _ = tech_info(g, t)
    if k in g["tech"]: return "Déjà apprise."
    if not ok: return "Cette technique n'est pas dans ta voie."
    if g["age"] < t["a"]: return f"Il faut avoir {t['a']} ans."
    if g["argent"] < t["p"]: return "Pas assez d'argent."
    g["argent"] -= t["p"]; g["tech"].append(k)
    L(g, f"📖 Technique apprise : {t['n']} !")
    return None


# ═════════════ Rencontres (carte / dialogues) ═════════════
def rencontre(g, lieu=None, kind=None):
    pool = [t for t in ENC if t["u"] == g["u"] and g["age"] >= t["amin"] and t["cond"](g) and (lieu is None or lieu in t["lieux"]) and (kind is None or t["kind"] == kind)
            and (t["kind"] != "amour" or _pref_ok(g, t.get("genre"))) and not (t["kind"] == "recruteur" and "kage" in g["flags"])]
    if not pool: return None
    w = [3 if t["kind"] in ("recruteur", "rival", "ami", "amour") else 2 for t in pool]
    t = random.choices(pool, weights=w)[0]
    return dict(tid=t["id"], nom=t["nom"], ico=t["ico"], titre=t["titre"], kind=t["kind"], niv=t["niv"], org=t["org"], aff=random.randint(10, 30),
                talks=0, fights=0, won=False, offered=False, recrute=False, lieu=lieu, line=t["intro"], step="menu", achats=[])


def explorer(g, lieu):
    """Dépense une action. Retourne un texte de narration (ou None si plus d'actions)."""
    if not depenser(g): return None
    r = random.random()
    if g["age"] >= 14 and not g["couple"] and random.random() < .12:
        e = rencontre(g, lieu, "amour") or rencontre(g, None, "amour")
        if e:
            g["enc"] = e; L(g, f"💘 Tu croises {e['nom']} ({e['titre']}).")
            return f"Tu croises {e['nom']} !"
    if r < .68 or (g["patron"] is None and g["age"] >= 12 and r < .74):
        e = rencontre(g, lieu)
        if e:
            g["enc"] = e
            L(g, f"🗺️ Tu croises {e['nom']} ({e['titre']}).")
            return f"Tu croises {e['nom']} !"
    if r < .9:
        txt, eff = random.choice(TROUVAILLES)
        ap(g, eff); L(g, "🗺️ " + txt)
        return txt
    L(g, "🗺️ Rien de spécial cette fois, mais la promenade te détend.")
    ap(g, {"bonheur": 2})
    return "Rien de spécial, mais la promenade te détend."


def _offer_check(g):
    e = g["enc"]
    if e["kind"] == "recruteur" and not e["offered"] and e["aff"] >= 60:
        e["offered"] = True; e["step"] = "offer"
        e["line"] = ENC_BY_ID[e["tid"]]["offre"]


def enc_parler(g):
    e = g["enc"]; t = ENC_BY_ID[e["tid"]]
    if e["talks"] >= 3:
        e["line"] = "« On a assez parlé pour aujourd'hui. »"; return
    e["talks"] += 1
    gain = random.randint(4, 10) + int((g["beaute"] - 50) / 25)
    if g["karma"] >= 20 and e["kind"] != "rival": gain += 3
    if t["id"] == "itachi" and g["karma"] <= -20: gain += 8
    e["aff"] = clamp(e["aff"] + gain, 0, 100)
    e["line"] = random.choice(t["talk"])
    ap(g, {"bonheur": 1})
    _offer_check(g)


def enc_cadeau(g):
    e = g["enc"]
    if g["cadeau"] <= 0: return "Achète un cadeau en boutique."
    g["cadeau"] -= 1; e["aff"] = clamp(e["aff"] + 15, 0, 100)
    e["line"] = "« Oh… merci, c'est gentil ! »"
    _offer_check(g)
    return None


def enc_demander(g):
    e = g["enc"]
    if e["kind"] != "recruteur" or not e["org"]:
        e["line"] = "« Je n'ai rien à te proposer, mais ravi de te connaître. »"
    elif e["aff"] >= 60:
        e["offered"] = True; e["step"] = "offer"; e["line"] = ENC_BY_ID[e["tid"]]["offre"]
    else:
        e["line"] = "« Prouve-moi d'abord ta valeur. Parlons… ou battons-nous. »"


def enc_battre(g):
    e = g["enc"]
    if e.get("fights", 0) >= 1:
        e["line"] = "« Assez pour aujourd'hui. Reviens me voir une autre fois. »"
        return
    e["fights"] = e.get("fights", 0) + 1
    bat_init(g, e["nom"], e["ico"], e["niv"], {"enc": True})


def recruter_pnj(g, e):
    org = e["org"]
    if org.startswith("gang:"):
        if g["gang"] or g["monde"] is None: return False, "Tu as déjà un gang."
        rejoindre_gang(g, org[5:])
        if not g["gang"]: return False, "Ce gang n'existe plus."
        ap(g, {"rep": 5, "xp": 15}); return True, f"{e['nom']} t'accueille dans {g['gang']['nom']} !"
    if org.startswith("gm:"):
        if g["recrue"]: return False, "Tu as déjà été recruté."
        recruter(g, org[3:]); return True, f"{e['nom']} te recrute !"
    if org.startswith("lycee:"):
        n = org[6:]
        if g["lycee"] or g["recrue"]: return False, "Tu as déjà un lycée."
        if g["mait"] < ECOLES[n]["mait"]: return False, f"Ton niveau est insuffisant pour le {n} (maîtrise ≥ {ECOLES[n]['mait']})."
        rejoindre_lycee(g, n); return True, f"Le {n} t'ouvre ses portes."
    if org == "seirin":
        if g["lycee"]: return False, "Tu as déjà un lycée."
        ap(g, {"lycee": "Lycée Seirin", "xp": 15, "rep": 3}); return True, "Riko t'accueille dans l'équipe de Seirin."
    if org in ("nba", "anbu"):
        a = ARC_BY_ID[org]
        if a not in arc_dispo(g): return False, "Tu n'es pas encore prêt(e) pour cette opportunité."
        lancer_arc(g, org); return True, f"{e['nom']} t'ouvre la porte de l'épreuve."
    if org == "akatsuki":
        if g["akatsuki"]: return False, "Tu es déjà membre."
        ap(g, {"akatsuki": 1, "karma": -10, "rep": -30}); return True, "Tu rejoins l'Akatsuki."
    if g["patron"]: return False, "Tu as déjà un maître : quitte-le d'abord (onglet Carte)."
    g["patron"] = dict(nom=e["nom"], ico=e["ico"], org=org, titre=e["titre"])
    ap(g, {"rep": 3, "xp": 10})
    return True, f"{e['nom']} fait de toi son protégé ({ORGS[org]['nom']}) !"


def enc_accepter(g):
    e = g["enc"]
    ok, msg = recruter_pnj(g, e)
    L(g, f"🤝 {msg}" if ok else f"🙅 {msg}")
    e["line"] = "« Excellent. » " + msg if ok else "« Dommage… » " + msg
    e["recrute"] = ok; e["step"] = "menu"
    if ok and g["event"] is not None: g["enc"] = None  # un arc vient de démarrer
    return ok


def enc_refuser(g):
    e = g["enc"]; e["aff"] = max(0, e["aff"] - 5); e["step"] = "menu"; e["line"] = "« Réfléchis-y. Je serai là. »"


def enc_acheter(g, key):
    err = acheter(g, key, .7)
    if not err: g["enc"]["achats"].append(key)
    return err


def enc_partir(g):
    e = g["enc"]
    if e["aff"] >= 40 and e["kind"] != "marchand" and e["nom"] not in [p["nom"] for p in g["pnj"]]:
        role = {"recruteur": "mentor", "rival": "rival", "ami": "ami", "amour": "amour"}[e["kind"]]
        g["pnj"].append(dict(nom=e["nom"], role=role, aff=e["aff"], niv=e["niv"], trait=random.choice(TRAITS)))
        L(g, f"👥 {e['nom']} fait désormais partie de tes contacts.")
    L(g, f"👋 Tu quittes {e['nom']}.")
    g["enc"] = None


def quitter_patron(g):
    if g["patron"]:
        L(g, f"👋 Tu quittes {g['patron']['nom']}."); g["patron"] = None


# ═════════════ Combat au tour par tour ═════════════
ATK_TXT = {"Naruto": ["lance une volée de kunai", "frappe en taijutsu", "enchaîne un coup de pied retourné"],
           "Kuroko": ["perce la défense d'un dribble", "plante un tir à mi-distance", "dunk puissant"],
           "Tokyo Revengers": ["envoie un direct", "place un coup de pied", "écrase un crochet"]}
SPEC_LBL = {"Naruto": "🌀 Chakra / Bijū", "Kuroko": "⚡ Zone / Talent", "Tokyo Revengers": "💢 Coup de grâce"}


def bat_init(g, nom, ico, niv, ctx=None):
    pw = puissance(g)
    fpw = (5 + g["age"] * 1.5 + rang(g)[0] * 15) * niv * random.uniform(.9, 1.1)
    mm = int((70 + pw * .6) * (.5 + g["sante"] / 200))
    fm = int(70 + fpw * .6)
    g["bat"] = dict(foe=nom, ico=ico, niv=niv, fpw=round(fpw, 1), fhp=fm, fmax=fm, mhp=mm, mmax=mm, guard=False, pp={}, boost=0,
                    spec=False, log=[f"{ico} {nom} te défie !"], over=None, ctx=ctx or {}, tours=0)


def _dmg(base): return max(1, int(base * random.uniform(.8, 1.2)))


def bat_move(g, mv, arg=None):
    b = g["bat"]
    if not b or b["over"]: return
    pw = puissance(g)
    lg = []
    dmg = 0
    if mv == "atk":
        dmg = _dmg(pw * .22); lg.append(f"Tu {random.choice(ATK_TXT[g['u']])} : {dmg} dégâts.")
    elif mv == "tech":
        t = TECH[arg]; left = b["pp"].get(arg, 2)
        if left <= 0: return
        b["pp"][arg] = left - 1
        dmg = _dmg(pw * .18 + t["pw"] * 1.1); lg.append(f"💥 {t['n']} ! {dmg} dégâts.")
    elif mv == "spec":
        if b["spec"]: return
        b["spec"] = True
        if g["u"] == "Naruto":
            if g["biju"] and g["biju"]["lien"] >= 25:
                dmg = _dmg(pw * .5 + 8); b["mhp"] -= 8
                lg.append(f"{g['biju']['ico']} Le chakra du bijū déferle : {dmg} dégâts (tu te blesses : -8 PV).")
            else:
                ap(g, {"chakra": -6}); dmg = _dmg(pw * .4)
                lg.append(f"🌀 Explosion de chakra : {dmg} dégâts.")
        elif g["u"] == "Kuroko":
            if g["zone"] >= 1:
                b["boost"] = 2; lg.append("⚡ Tu entres dans la Zone ! Tes deux prochaines actions sont renforcées.")
            elif g["talent"]:
                b["boost"] = 1; lg.append(f"{TALENTS[g['talent']['k']][1]} Ton talent « {TALENTS[g['talent']['k']][0]} » s'active !")
            else:
                b["boost"] = 1; lg.append("🔥 Tu te concentres à fond.")
        else:
            mult = 2.2 if b["fhp"] < b["fmax"] * .4 else 1.1
            dmg = _dmg(pw * .3 * mult); lg.append(f"💢 Coup de grâce ! {dmg} dégâts" + (" (critique)" if mult > 2 else "") + ".")
    elif mv == "def":
        b["guard"] = True; heal = int(b["mmax"] * .06); b["mhp"] = min(b["mmax"], b["mhp"] + heal)
        lg.append(f"🛡️ Tu te mets en garde (+{heal} PV).")
    elif mv == "item":
        if g["argent"] < 50: return
        g["argent"] -= 50; heal = int(b["mmax"] * .3); b["mhp"] = min(b["mmax"], b["mhp"] + heal)
        lg.append(f"🧪 Tu te soignes (+{heal} PV, -50).")
    elif mv == "fuite":
        if random.random() < .5:
            b["over"] = "fuite"; lg.append("🏃 Tu prends la fuite."); ap(g, {"rep": -2}); b["log"] += lg
            return
        lg.append("🏃 Impossible de fuir !")
    if dmg and b["boost"] > 0 and mv in ("atk", "tech"):
        dmg = int(dmg * 1.5); b["boost"] -= 1; lg[-1] += f" (renforcé : {dmg})"
    b["fhp"] -= dmg
    if b["fhp"] <= 0:
        b["log"] += lg; bat_fin_combat(g, True); return
    r = random.random(); fp = b["fpw"]
    if r < .65:
        d = _dmg(fp * .22); lg.append(f"{b['ico']} {b['foe']} attaque : {d} dégâts.")
    elif r < .87:
        d = _dmg(fp * .22 * 1.5); lg.append(f"{b['ico']} {b['foe']} lance sa technique : {d} dégâts !")
    else:
        d = 0; h = int(b["fmax"] * .05); b["fhp"] = min(b["fmax"], b["fhp"] + h); lg.append(f"{b['ico']} {b['foe']} se couvre (+{h} PV).")
    if d and b["guard"]: d = int(d * .4); lg[-1] += f" (garde : {d})"
    b["guard"] = False
    b["mhp"] -= d; b["tours"] += 1
    b["log"] += lg; b["log"] = b["log"][-14:]
    if b["mhp"] <= 0: bat_fin_combat(g, False)


def bat_fin_combat(g, win):
    b = g["bat"]; ctx = b["ctx"]
    b["over"] = "win" if win else "lose"
    if win:
        ap(g, {"xp": int(10 * b["niv"]) + 8, "rep": 3, "argent": 30, "win": 1})
        L(g, f"⚔️ Tu bats {b['foe']} en combat singulier !")
        b["log"].append(f"🏆 Tu as vaincu {b['foe']} !")
        if ctx.get("enc") and g["enc"]:
            g["enc"]["aff"] = clamp(g["enc"]["aff"] + 25, 0, 100); g["enc"]["won"] = True
            g["enc"]["line"] = "« Bien joué… j'ai du respect pour toi. »"
        if ctx.get("pnj"):
            p = next((q for q in g["pnj"] if q["nom"] == ctx["pnj"]), None)
            if p: p["aff"] = clamp(p["aff"] + 10, 0, 100)
    else:
        ap(g, {"sante": -random.randint(5, 15), "bonheur": -3})
        L(g, f"💥 {b['foe']} te bat en combat singulier.")
        b["log"].append(f"💀 {b['foe']} l'emporte.")
        if ctx.get("enc") and g["enc"]:
            g["enc"]["aff"] = clamp(g["enc"]["aff"] + 5, 0, 100); g["enc"]["line"] = "« Pas mal, mais tu dois t'améliorer. »"
        if ctx.get("pnj"):
            p = next((q for q in g["pnj"] if q["nom"] == ctx["pnj"]), None)
            if p: p["aff"] = clamp(p["aff"] + 3, 0, 100)
    verifie_objectifs(g)
    if g["sante"] <= 0 and not g["dead"]:
        mort(g, f"Tué lors d'un combat contre {b['foe']}.")


def bat_fin(g):
    if g["enc"] and g["bat"] and g["bat"]["ctx"].get("enc"):
        _offer_check(g)
    g["bat"] = None


# ═════════════ École (style BitLife) ═════════════
def en_ecole(g):
    return 6 <= g["age"] <= (12 if g["u"] == "Naruto" else 18) or (g["u"] == "Naruto" and g["age"] <= 12)


def ecole_etudier(g):
    if not depenser(g): return "Plus d'actions !"
    ap(g, {"intel": 2, "xp": 3, "bonheur": -1}); g["notes"] = clamp(g["notes"] + 6, 0, 100)
    L(g, "📚 Tu étudies davantage : tes notes s'améliorent."); return None


def ecole_secher(g):
    if not depenser(g): return "Plus d'actions !"
    if random.random() < .3:
        ap(g, {"rep": -4, "karma": -2, "bonheur": -2}); g["notes"] = clamp(g["notes"] - 4, 0, 100)
        L(g, "😬 Tu sèches les cours mais tu te fais prendre : retenue !")
    else:
        ap(g, {"bonheur": 6, "karma": -1}); g["notes"] = clamp(g["notes"] - 3, 0, 100)
        L(g, "🤫 Tu sèches les cours, personne ne remarque rien.")
    return None


def ecole_infirmerie(g):
    if not depenser(g): return "Plus d'actions !"
    ap(g, {"sante": 15}); L(g, "🩺 Tu passes à l'infirmerie : tu te sens mieux."); return None


def ecole_club(g, nom):
    if nom in g["clubs"]: return "Tu es déjà inscrit."
    if not depenser(g): return "Plus d'actions !"
    g["clubs"].append(nom); ap(g, CLUBS[nom][2]); g["popu"] = clamp(g["popu"] + 3, 0, 100)
    L(g, f"{CLUBS[nom][0]} Tu rejoins le club « {nom} »."); return None


def ecole_clique(g, nom):
    if g["clique"] == nom: return "Tu fais déjà partie de cette clique."
    if not depenser(g): return "Plus d'actions !"
    need = CLIQUES[nom][2]
    if g["popu"] < need * 25 and random.random() < .6:
        L(g, f"🚪 La clique des {nom} te refuse l'entrée."); ap(g, {"bonheur": -3}); return None
    g["clique"] = nom; L(g, f"{CLIQUES[nom][0]} Tu rejoins la clique des {nom}."); return None


def ecole_classe(g, act):
    if not depenser(g): return "Plus d'actions !"
    if act == "amis":
        if random.random() < .7: g["popu"] = clamp(g["popu"] + 6, 0, 100); ap(g, {"bonheur": 4}); L(g, "🧑‍🤝‍🧑 Tu te fais de nouveaux amis en classe.")
        else: ap(g, {"bonheur": -2}); L(g, "😕 Personne ne te prête attention aujourd'hui.")
    elif act == "pitre":
        if random.random() < .55: g["popu"] = clamp(g["popu"] + 8, 0, 100); L(g, "🤡 Tu fais le pitre : toute la classe rit !")
        else: g["popu"] = clamp(g["popu"] - 4, 0, 100); ap(g, {"rep": -2}); L(g, "😳 Ta blague tombe à plat.")
    elif act == "aider":
        ap(g, {"karma": 4, "bonheur": 2}); g["popu"] = clamp(g["popu"] + 3, 0, 100); L(g, "🤝 Tu aides un camarade en difficulté.")
    elif act == "brimer":
        ap(g, {"karma": -6, "rep": 1}); g["popu"] = clamp(g["popu"] + random.choice([-6, 4]), 0, 100); L(g, "😈 Tu t'en prends à un camarade.")
    return None


def ecole_prof(g, act):
    if not depenser(g): return "Plus d'actions !"
    if act == "aide":
        g["notes"] = clamp(g["notes"] + 5, 0, 100); ap(g, {"intel": 1}); L(g, "🧑‍🏫 Ton professeur t'explique patiemment la leçon.")
    elif act == "flatter":
        if random.random() < .6: g["notes"] = clamp(g["notes"] + 4, 0, 100); L(g, "🍎 Ta flatterie fonctionne : ton prof t'apprécie.")
        else: g["popu"] = clamp(g["popu"] - 5, 0, 100); L(g, "😒 On te traite de fayot.")
    elif act == "insolent":
        ap(g, {"rep": 2, "karma": -2}); g["notes"] = clamp(g["notes"] - 5, 0, 100); g["popu"] = clamp(g["popu"] + 3, 0, 100)
        L(g, "😤 Tu réponds insolemment à ton professeur.")
    return None


# ═════════════ Notoriété (offres à accepter / refuser) ═════════════
def lancer_offre(g, kind):
    if g["rep"] < 40: return "Il faut 40 de réputation pour être célèbre."
    if g["offres"].get(kind) == g["age"]: return "Tu as déjà sollicité cela cette année."
    if not depenser(g): return "Plus d'actions !"
    g["offres"][kind] = g["age"]
    k = 1 + g["rep"] / 60
    marque = random.choice(MARQUES[g["u"]])
    if kind == "pub":
        gain = int(random.uniform(200, 450) * k)
        ev = dict(titre="Célébrité — Publicité", t=f"« {marque} » vous propose de vous payer pour apparaître dans une publicité.\n\nOffre : {gain}",
                  ch=[["Accepter", .9, {"argent": gain, "rep": 2}, "Le tournage se passe à merveille.", {"rep": -3, "bonheur": -2}, "Le tournage est un fiasco."],
                      ["Refuser", 1, {}, "Tu déclines poliment.", {}, ""]])
    elif kind == "livre":
        gain = int((150 + g["intel"] * 8) * k)
        ev = dict(titre="Célébrité — Livre", t=f"Un éditeur vous propose d'écrire votre autobiographie.\n\nAvance : {gain}",
                  ch=[["Accepter", ["st", "intel", 50], {"argent": gain, "rep": 4, "intel": 1}, "Ton livre rencontre son public !", {"argent": gain // 3, "bonheur": -3}, "Tu abandonnes le manuscrit à mi-chemin."],
                      ["Refuser", 1, {}, "Tu préfères rester discret.", {}, ""]])
    elif kind == "photo":
        gain = int((120 + g["beaute"] * 4) * k)
        ev = dict(titre="Célébrité — Séance photo", t=f"« {marque} » vous propose une séance photo pour un magazine.\n\nCachet : {gain}",
                  ch=[["Accepter", min(.95, .5 + g["beaute"] / 150), {"argent": gain, "rep": 3, "bonheur": 3}, "Les clichés sont magnifiques.", {"bonheur": -3}, "La séance est un calvaire."],
                      ["Refuser", 1, {}, "Pas pour toi.", {}, ""]])
    else:
        ev = dict(titre="Célébrité — Talk-show", t="Une émission de talk-show vous invite en plateau.\n\nCachet : 100",
                  ch=[["Accepter", ["st", "rep", 70], {"rep": 6, "argent": 100, "bonheur": 4}, "Le public t'adore !", {"rep": -3, "bonheur": -3}, "Tu bafouilles devant les caméras."],
                      ["Refuser", 1, {}, "Tu laisses passer.", {}, ""]])
    g["event"] = ev
    return None


# ═════════════ Réseaux sociaux ═════════════
def social_inscrire(g, p):
    if g["age"] < 12: return "Il faut avoir 12 ans."
    if p in g["social"]: return "Déjà inscrit."
    g["social"][p] = 10 + random.randint(0, 20)
    L(g, f"{PLAT_ICO.get(p, '📱')} Tu t'inscris sur {p}."); return None


def social_poster(g, p):
    if p not in g["social"]: return "Inscris-toi d'abord."
    if not depenser(g): return "Plus d'actions !"
    f = g["social"][p]
    gain = int((g["rep"] * .8 + g["beaute"] * .4 + 5) * random.uniform(.4, 1.6) * (1 + f / 3000))
    if random.random() < .08:
        gain *= 5; ap(g, {"bonheur": 5}); L(g, f"🔥 Ton post sur {p} devient viral !")
    elif random.random() < .1:
        gain = max(0, gain // 3); ap(g, {"rep": -2, "bonheur": -3}); L(g, f"😡 Des internautes te critiquent sur {p}.")
    else:
        L(g, f"{PLAT_ICO.get(p, '📱')} Tu publies sur {p} : +{gain} abonnés.")
    g["social"][p] = f + gain
    if g["social"][p] >= 500 and g["event"] is None and random.random() < .2:
        marque = random.choice(MARQUES[g["u"]]); gain2 = int(g["social"][p] * .3)
        g["event"] = dict(titre=f"Sponsoring — {p}", t=f"« {marque} » vous propose un partenariat rémunéré.\n\nOffre : {gain2}",
                          ch=[["Accepter", .9, {"argent": gain2, "rep": 1}, "Le partenariat est un succès.", {"rep": -2}, "Tes abonnés crient à la pub déguisée."],
                              ["Refuser", 1, {"karma": 1}, "Tu restes authentique.", {}, ""]])
    return None


# ═════════════ Temps par trimestre (Kuroko) ═════════════
PA_SAISON = 4  # actions par trimestre (Kuroko)


def pa_max(g): return PA_SAISON if g["u"] == "Kuroko" else PA


def calendrier(g):
    a, q = g["age"], g.get("trim", 0)
    cal = {k: True for k, c in COMP.items() if c[1][0] <= a <= c[1][1] and q in COMP_Q.get(k, [0, 1, 2, 3]) and (k != "nba" or g["pro"])}
    if a >= 13 and q == 1: cal["camp"] = True
    return cal


def trimestre(g):
    if g["trim"] >= 3:
        vieillir(g); return
    prev = g["trim"]
    g["trim"] += 1; q = g["trim"]
    g["pa"] = pa_max(g)
    if g["cup"]: L(g, f"🏳️ La {g['cup']['nom']} s'arrête avec la fin du trimestre.")
    g["match"] = None; g["cup"] = None
    g["cal"] = calendrier(g)
    L(g, f"{SAISON_ICO[q]} {SAISONS[q]} ({SAISON_MOIS[q]}).")
    noms = [COMP[k][0] for k in g["cal"] if k in COMP]
    if noms: L(g, "📅 Ce trimestre : " + ", ".join(noms) + ".")
    news_resultats(g, prev, g["age"]); faire_nouvelles(g, 1)
    ap(g, {"xp": 3 + (3 if g["recrue"] else 0)})
    for p in g["pnj"]: p["aff"] = max(0, p["aff"] - random.randint(0, 1))
    if g["sante"] <= 0:
        mort(g, "Épuisement et blessures."); return
    tirer_evenement(g, intense=False)


def avancer(g):
    (trimestre if g["u"] == "Kuroko" else vieillir)(g)


def _vu(g, i):
    g["vus"].append(i); g["vus"] = g["vus"][-70:]


def _ev_libre(g):
    """Un événement aléatoire éligible, pas vu récemment (None s'il n'y en a pas)."""
    elig = [i for i, e in enumerate(EV) if ev_ok(g, e) and i not in g["vus"]]
    if not elig and g["vus"]:
        g["vus"] = g["vus"][-12:]
        elig = [i for i, e in enumerate(EV) if ev_ok(g, e) and i not in g["vus"]]
    return random.choice(elig) if elig else None


def tirer_evenement(g, intense=True):
    _tirer_core(g, intense)
    if intense and 6 <= g["age"] <= 45 and g["event"] is not None and not g["dead"] and random.random() < .45:
        j = _ev_libre(g)
        if j is not None and j != g["event"]:
            g["file"].append(j); _vu(g, j)


def _tirer_core(g, intense=True):
    a = g["age"]; f = 1.0 if intense else .5
    if not intense and (a < 8 or a > 38): return
    if g["u"] == "Kuroko" and not g["lycee"] and not g["recrue"] and 13 <= a <= 14 and random.random() < (.5 if intense else .35):
        ev = offre_lycee(g)
        if ev: g["event"] = ev; return
    if g["u"] == "Kuroko" and g["talent"] and not g["recrue"] and 13 <= a <= 18 and g["mait"] >= 45 and random.random() < .3 * f:
        g["event"] = GM_EV; return
    if g["u"] == "Naruto" and not g["akatsuki"] and a >= 16 and g["karma"] <= -40 and random.random() < .5:
        g["event"] = AKAT_EV; return
    if g["u"] == "Naruto" and not g["biju"] and a >= 3 and random.random() < .025:
        g["event"] = BIJU_EV; return
    arcs = [x for x in arc_dispo(g) if random.random() < x["p"] * (1 if intense else .8)]
    if arcs:
        lancer_arc(g, random.choice(arcs)["id"]); return
    if a >= 6 and random.random() < (.22 if intense else .1):
        d = ev_dyn(g)
        if d: g["event"] = d; return
    i = _ev_libre(g)
    if i is not None and random.random() < (.9 if intense else .2):
        g["event"] = i; _vu(g, i)


# ═════════════ Factions : alliances, ennemis, diplomatie ═════════════
def _own(g): return (g.get("gang") or {}).get("nom")
def allies(g): return [n for n, f in g["fact"].items() if f["allie"] and n != _own(g)]
def ennemis(g): return [n for n, f in g["fact"].items() if f.get("ennemi") and n != _own(g)]


def rivaux(g, n):
    return [b if a == n else a for a, b in RIVALITES.get(g["u"], []) if n in (a, b)]


def _res(g, v):
    ae = g.get("_ae") or (None, None)
    if v == "A": return ae[0] or (allies(g) or [None])[0]
    if v == "E": return ae[1] or (ennemis(g) or [None])[0]
    return v


def devenir_ennemi(g, n):
    f = g["fact"].get(n)
    if not f or f.get("ennemi") or n == _own(g): return
    f["ennemi"] = True; f["allie"] = False; f["rel"] = min(f["rel"], 10)
    L(g, f"⚔️ {n} devient ton ennemi déclaré !")


def conclure_paix(g, n):
    f = g["fact"].get(n)
    if f and f.get("ennemi"):
        f["ennemi"] = False; f["rel"] = max(f["rel"], 35)
        L(g, f"🕊️ La paix est conclue avec {n}.")


def faire_alliance(g, n):
    f = g["fact"][n]
    f["allie"] = True; f["ennemi"] = False; f["rel"] = max(f["rel"], 60)
    L(g, f"🤝 Alliance conclue avec {n} !")
    for r in rivaux(g, n):
        fr = g["fact"].get(r)
        if fr and not fr["allie"] and r != _own(g):
            fr["rel"] = max(0, fr["rel"] - 12)
            L(g, f"🔥 {r} voit cette alliance d'un mauvais œil.")
            if fr["rel"] <= 15 and not fr.get("ennemi") and random.random() < .4:
                devenir_ennemi(g, r)


def proposer_alliance(g, n):
    f = g["fact"][n]
    nal = len(allies(g))
    if g["age"] < 12 or nal >= 3: return "Il faut 12 ans et moins de 3 alliances."
    if f.get("ennemi"): return "Il faut d'abord faire la paix."
    cout = 100 * (nal + 1)
    if g["argent"] < cout: return f"Il faut {cout} d'argent."
    if not depenser(g): return "Plus d'actions !"
    g["argent"] -= cout
    if random.random() < min(.9, f["rel"] / 100 * .8 + g["rep"] / 250):
        faire_alliance(g, n); ap(g, {"rep": 5})
    else:
        f["rel"] = max(0, f["rel"] - 5); L(g, f"🙅 {n} refuse ton alliance.")
    return None


def declarer_hostilite(g, n):
    f = g["fact"][n]
    if g["age"] < 12: return "Trop jeune."
    ap(g, {"karma": -3, "rep": 2}); f["allie"] = False; devenir_ennemi(g, n)
    return None


def proposer_paix(g, n):
    f = g["fact"][n]
    if not depenser(g): return "Plus d'actions !"
    if random.random() < clamp(.3 + g["rep"] / 200 + f["rel"] / 200, .15, .85):
        conclure_paix(g, n); ap(g, {"rep": 3, "karma": 2})
    else:
        f["rel"] = max(0, f["rel"] - 3); L(g, f"🙅 {n} refuse tes avances de paix.")
    return None


def trahir_allie(g, n):
    f = g["fact"][n]
    f["allie"] = False; f["rel"] = 0
    ap(g, {"karma": -20, "argent": 200, "rep": -10})
    L(g, f"🗡️ Tu trahis {n} et pille leurs ressources.")
    if random.random() < .6: devenir_ennemi(g, n)


def tribut(g, n):
    if g["age"] < 10: return "Trop jeune."
    if g["argent"] < 80 or g["pa"] <= 0: return "Il faut 80 d'argent et une action."
    g["argent"] -= 80; g["pa"] -= 1
    f = g["fact"][n]; f["rel"] = min(100, f["rel"] + 12)
    L(g, f"🎁 {n} apprécie ton tribut."); return None


def ev_dyn2(g):
    a, u = g["age"], g["u"]
    o = []
    for n in ennemis(g):
        if a < 10: continue
        t = {"Naruto": f"⚔️ Des ninjas de {n} tendent une embuscade à ta patrouille près de la frontière.",
             "Kuroko": f"😠 Des joueurs du {n} te cherchent des noises à la sortie du gymnase.",
             "Tokyo Revengers": f"🔥 Des membres de {n} te tombent dessus dans une ruelle."}[u]
        o.append((4, dict(who=None, t=t, ch=[
            ["Résister", ["pw", 50 + a * 2.2], {"xp": 20, "rep": 6}, "Tu leur tiens tête !", {"sante": -15, "rep": -3}, "Ils te laissent à terre."],
            ["Négocier une trêve", ["st", "rep", 55], {"paix": n, "rep": 4}, "Une trêve est conclue.", {"rep": -2}, "Ils crachent sur ta main tendue."],
            ["Fuir", .8, {"rep": -2}, "Tu t'éclipses.", {"sante": -10, "rep": -3}, "Ils te rattrapent."]])))
    for n in allies(g):
        e = (ennemis(g) or rivaux(g, n) or ["des bandits"])[0]
        t = {"Naruto": f"🤝 {n} te demande de l'aide : {e} menace sa frontière.",
             "Kuroko": f"🤝 Le {n} te demande de l'aide : il affronte {e} et manque de joueurs.",
             "Tokyo Revengers": f"🤝 {n} te demande du renfort contre {e}."}[u]
        o.append((2, dict(who=None, t=t, ch=[
            ["Les aider", ["pw", 55 + a * 2], {"relx": [n, 10], "rep": 6, "xp": 20}, "Ton aide est décisive.", {"sante": -15, "relx": [n, 3]}, "Tu es débordé, mais ils apprécient le geste."],
            ["Envoyer de l'aide (100)", 1, {"argent": -100, "relx": [n, 6]}, "Ton soutien matériel est apprécié.", {}, ""],
            ["Refuser", 1, {"relx": [n, -12], "rep": -3}, "Ton allié te le reprochera.", {}, ""]])))
    if u == "Kuroko" and a >= 13:
        for nm, v in g["amitie"].items():
            if v >= 30:
                o.append((2, dict(who=None, t=f"🏀 {nm} t'invite à jouer un 1 contre 1 amical.", ch=[
                    ["Relever le défi", ["pw", 30 + GM[nm][1] * 45], {"mait": 4, "xp": 15, "amitie": [nm, 6]}, "Un très beau duel entre amis.", {"amitie": [nm, 3], "bonheur": -2}, "Tu perds, mais il te félicite."],
                    ["Décliner", 1, {"amitie": [nm, -3]}, "Il hausse les épaules.", {}, ""]])))
    return o


# ═════════════ Kuroko : lycées, amitié avec les Miracles ═════════════
def rejoindre_lycee(g, nom, silent=False):
    e = ECOLES.get(nom)
    g["lycee"] = nom
    if not e:
        if not silent: L(g, f"🏫 Tu intègres le {nom}.")
        return
    if g["fact"].get(nom) and not g["fact"][nom]["allie"] and len(allies(g)) < 3: faire_alliance(g, nom)
    names = [p["nom"] for p in g["pnj"]]
    for m in e["membres"][:3]:
        if m not in names:
            g["pnj"].append(dict(nom=m, role="equipier", aff=random.randint(25, 45), niv=round(random.uniform(.9, 1.4), 2), trait=random.choice(TRAITS)))
    if e["gm"]: ajouter_amitie(g, e["gm"], 10)
    if not silent:
        ap(g, {"xp": 20, "rep": 4}); L(g, f"🏫 Tu intègres le {nom} (coach : {e['coach']}) et rencontres tes coéquipiers.")


def offre_lycee(g):
    ok = sorted([n for n, e in ECOLES.items() if g["mait"] >= e["mait"] - 10 and n != g["lycee"]], key=lambda n: -ECOLES[n]["mait"])[:4]
    if not ok: return None
    ch = [[f"Accepter l'offre du {n.replace('Lycée ', '')}", ["st", "mait", ECOLES[n]["mait"]], {"lycee": n}, f"{ECOLES[n]['coach']} t'ouvre les portes du lycée.",
           {"bonheur": -3}, "Au dernier moment, le lycée te refuse : ton niveau est jugé insuffisant."] for n in ok]
    ch.append(["Attendre d'autres offres", 1, {"intel": 1}, "Tu prends ton temps.", {}, ""])
    return dict(titre="Recrutement", t="Plusieurs lycées s'intéressent à ton profil. Des coachs t'observent depuis les gradins.", who=None, ch=ch)


def ajouter_amitie(g, n, d):
    old = g["amitie"].get(n, 0); new = clamp(old + d, 0, 100)
    g["amitie"][n] = new
    if d > 0: g["gm"][n] = clamp(g["gm"][n] + d // 2, 0, 100)
    for seuil, lab in ((30, "une connaissance"), (60, "un ami"), (90, "un meilleur ami")):
        if old < seuil <= new: L(g, f"💞 {n} devient {lab} !")
    if new >= 60 and n not in [p["nom"] for p in g["pnj"]]:
        g["pnj"].append(dict(nom=n, role="ami", aff=new, niv=GM[n][1], trait="loyal"))
    for p in g["pnj"]:
        if p["nom"] == n: p["aff"] = max(p["aff"], new)


def temps_avec_gm(g, n):
    if g["age"] < 8: return "Trop jeune."
    if not depenser(g): return "Plus d'actions !"
    sc = random.choice(SCENES_GM[n])
    ap(g, sc[1]); ajouter_amitie(g, n, random.randint(8, 14))
    L(g, f"🤝 {sc[0]}")
    return None


def duo_partner(g):
    if g["recrue"]: return g["recrue"]
    best = max(g["amitie"], key=lambda n: g["amitie"][n], default=None)
    return best if best and g["amitie"][best] >= 60 else None


# ═════════════ Scénarios débloquables ═════════════
def scenarios(g):
    out = []
    for a in ARCS:
        if a.get("scen") and a["u"] == g["u"]:
            done = f"s_{a['id']}" in g["flags"]
            ok = (a["a"][0] <= g["age"] <= a["a"][1]) and a["cond"](g) and (g["u"] != "Kuroko" or not a.get("q") or g["trim"] in a["q"])
            out.append((a, ok, done))
    return out


def lancer_scenario(g, aid):
    a = ARC_BY_ID[aid]
    if (a, True, False) not in [(x, o, d) for x, o, d in scenarios(g) if x["id"] == aid and o and not d]: return "Ce scénario n'est pas débloqué."
    if not depenser(g): return "Plus d'actions !"
    lancer_arc(g, aid); L(g, f"📖 Tu t'engages dans le scénario : {fmt(g, a['nom'])}.")
    return None


# ═════════════ Nouvelles du monde & situation en cours ═════════════
def news(g, txt, tpl=None):
    g["news"].append([g["age"], txt, g.get("trim", 0), tpl])
    g["news"] = g["news"][-40:]


def _noms_monde(g):
    if g["u"] == "Naruto": return list(VILL) + ["Ame", "Taki"]
    if g["u"] == "Kuroko": return list(ECOLES) + ["Lycée Kirisaki Daiichi", "Lycée Fukuda Sōgō"]
    return list(g["monde"] or GFORCE)


def _fill(g, tpl):
    base = _noms_monde(g)
    base = base if len(base) >= 2 else base + [n for n in GFORCE if n not in base]
    x, y = random.sample(base, 2)
    if g["u"] == "Naruto" and g["village"] and random.random() < .4: x = g["village"] if y != g["village"] else x
    al, en = allies(g), ennemis(g)
    out = tpl
    rep = {"{X}": x, "{Y}": y, "{V}": g["village"] or "ton village", "{A}": random.choice(al) if al else random.choice(base),
           "{E}": random.choice(en) if en else random.choice(base), "{GM}": random.choice(list(GM)), "{T}": random.choice(TERRS),
           "{N}": random.choice(UNIV[g["u"]]["pnj"])}
    for k, v in rep.items(): out = out.replace(k, v)
    return out


def faire_nouvelles(g, n=3):
    pool = NEWS_TPL[g["u"]] + NEWS_TPL[None]
    state = []
    if ennemis(g): state += NEWS_STATE["ennemi"][g["u"]]
    if allies(g): state += NEWS_STATE["allie"][g["u"]]
    if g["u"] == "Tokyo Revengers" and g.get("monde"):
        top = max(g["monde"], key=lambda k: len(g["monde"][k]["terr"]))
        state.append(f"👑 {top} domine la carte avec {len(g['monde'][top]['terr'])} territoire(s) sur {len(TERRS)}.")
        if g.get("gang"): state.append(f"🏴 Les voisins de {g['gang']['nom']} s'inquiètent de son essor.")
    if g["u"] == "Kuroko" and g.get("pro"): state += [f"🇺🇸 Les {g['pro']['team']} font parler d'eux cette saison.", "🇺🇸 La ligue américaine annonce un calendrier chargé."]
    récents = [e[3] if len(e) > 3 else e[1] for e in g["news"][-14:]]
    for _ in range(n):
        for _try in range(8):
            tpl = random.choice(state) if state and random.random() < .4 else random.choice(pool)
            if tpl not in récents: break
        news(g, _fill(g, tpl), tpl); récents.append(tpl)


def news_resultats(g, q, age):
    """Résultats mondiaux des compétitions du trimestre q (Kuroko)."""
    if g["u"] != "Kuroko" or age < 12: return
    ecoles = [n for n in g["fact"]] or list(ECOLES)
    for k in ("college", "inter", "ete", "winter", "printemps"):
        if q in COMP_Q.get(k, []) and k in COMP and not any(p[0] == age and p[2] == k for p in g["palmares"]):
            w = random.choices(ecoles, weights=[1 + opp_niv(g, e) * 2 for e in ecoles])[0]
            news(g, f"🏆 Le {w} remporte la compétition « {COMP[k][0]} ».")
    if q in COMP_Q["nba"] and g["pro"] and not any(p[0] == age and p[2] == "nba" for p in g["palmares"]):
        w = random.choices(list(NBA), weights=[NBA[t] for t in NBA])[0]
        news(g, f"🇺🇸 Les {w} sont sacrés champions NBA.")


def en_cours(g):
    """Situation actuelle du personnage : liste de lignes markdown."""
    L_ = []
    if g["u"] == "Kuroko":
        q = g.get("trim", 0); nm = [COMP[k][0] for k in g["cal"] if k in COMP]
        L_.append(f"{SAISON_ICO[q]} **{SAISONS[q]}** ({SAISON_MOIS[q]}) : " + (", ".join(nm) if nm else "aucune compétition ce trimestre"))
    ops = [a for a in arc_dispo(g) if a.get("man") and not a.get("scen")]
    if ops: L_.append("📜 Opportunités : " + ", ".join(fmt(g, a["nom"]) for a in ops))
    sc = [a for a, ok, done in scenarios(g) if ok and not done]
    if sc: L_.append("📖 Scénarios débloqués : " + ", ".join(fmt(g, a["nom"]) for a in sc))
    if allies(g): L_.append("🤝 Alliés : " + ", ".join(allies(g)))
    if ennemis(g): L_.append("⚔️ Ennemis : " + ", ".join(ennemis(g)))
    if g.get("patron"): L_.append(f"🎓 Maître : {g['patron']['nom']} ({ORGS[g['patron']['org']]['nom']})")
    if g.get("gang"): L_.append(f"🏍️ Gang : {g['gang']['nom']} • {nterr(g)}/{DOMINATION} territoires pour dominer le Japon")
    if g.get("recrue"): L_.append(f"🌟 Recruté par {g['recrue']}")
    if g["lycee"]: L_.append(f"🏫 Lycée : {g['lycee']}")
    if g["pro"]: L_.append(f"🇺🇸 NBA : {g['pro']['team']} (saison {g['pro']['saisons']})")
    for e in g["enfants"]: L_.append(f"👶 {e['nom']} a {max(0, g['age'] - e['nai'])} ans")
    nxt = [(a, t) for a, t in sorted(UNIV[g["u"]]["mile"].items()) if a > g["age"]]
    if nxt: L_.append(f"🎯 Dans {nxt[0][0] - g['age']} an(s) : {nxt[0][1]}")
    return L_


# ═════════════ Petits boulots ═════════════
def jobs_dispo(g):
    return [j for j in JOBS if len(j) < 8 or j[7] == g["u"]]


def petit_boulot(g, jid):
    j = JOBS_BY_ID[jid]
    if len(j) > 7 and j[7] != g["u"]: return "Ce métier n'existe pas ici."
    if g["age"] < j[3]: return f"Il faut avoir {j[3]} ans."
    if not depenser(g): return "Plus d'actions !"
    n = g["metiers"].get(jid, 0)
    pay = int(random.randint(*j[4]) * (1 + min(.6, n * .06)))
    r = random.random()
    if r < .1:
        pay //= 2; ap(g, {"bonheur": -3}); extra = " (patron désagréable : paie réduite)"
    elif r > .9:
        pay += pay // 2; extra = " (gros pourboire !)"
    else: extra = ""
    g["argent"] += pay; ap(g, j[5]); g["metiers"][jid] = n + 1
    L(g, f"{j[1]} {j[2]} : +{pay} {UNIV[g['u']]['monnaie']}{extra}. {j[6]}")
    return None


# ═════════════ Inventaire & achats ═════════════
def acheter(g, k, remise=1.0):
    nm, pr, ds, eff, uu, ag = SHOP[k]
    prix = int(pr * remise)
    if g["age"] < ag: return "Trop jeune pour cet achat."
    if k in ONCE_SHOP and k in g["achats"]: return "Déjà possédé."
    if g["argent"] < prix: return "Pas assez d'argent."
    g["argent"] -= prix
    if k in ONCE_SHOP:
        g["achats"].append(k); ap(g, eff); L(g, f"🛍️ Achat : {nm} (équipé).")
    elif set(eff) & IMMEDIAT:
        ap(g, eff); L(g, f"🛍️ Achat : {nm}.")
    else:
        g["inv"][k] = g["inv"].get(k, 0) + 1; L(g, f"🛍️ Achat : {nm} (rangé dans ton inventaire).")
    return None


def utiliser(g, k):
    if g["inv"].get(k, 0) <= 0: return "Tu n'en as plus."
    g["inv"][k] -= 1
    if g["inv"][k] <= 0: del g["inv"][k]
    ap(g, SHOP[k][3]); L(g, f"🎒 Tu utilises : {SHOP[k][0]}.")
    return None


# ═════════════ Akatsuki : pupilles ═════════════
def chance_vol(g, n):
    base = puissance(g) / PUP[n][1] * .6
    if n == "Mangekyō Sharingan" and "Sharingan" not in g["pupilles"]: base *= .6
    return clamp(base + g.get("vol_bonus", 0) + g.get("vol_echecs", 0) * .08, .25, .92)


def reperer_porteur(g):
    if not depenser(g): return "Plus d'actions !"
    g["vol_bonus"] = min(.4, g.get("vol_bonus", 0) + .2)
    L(g, "🔍 Tu épies un porteur de pupille : ses habitudes n'ont plus de secrets pour toi (+20 % de chances)."); return None


def voler_pupille(g, n):
    if n in g["pupilles"]: return "Tu possèdes déjà cette pupille."
    if g["sante"] < 25: return "Tu es trop faible : soigne-toi d'abord."
    if not depenser(g): return "Plus d'actions !"
    if random.random() < chance_vol(g, n):
        g["pupilles"].append(n); g["vol_bonus"] = 0; g["vol_echecs"] = 0
        ap(g, {"karma": -15, "xp": 40, "rep": -3}); L(g, f"👁️ Tu voles le {n} ! Ta puissance grandit.")
    else:
        g["vol_echecs"] = g.get("vol_echecs", 0) + 1; g["vol_bonus"] = 0
        ap(g, {"sante": -15, "karma": -5}); L(g, f"💢 Ta cible t'échappe : tu rates le vol du {n}. (+8 % pour la prochaine tentative)")
        if g["sante"] <= 0: mort(g, "Tué en tentant de voler une pupille.")
    return None


def chercher_akatsuki(g):
    if g["akatsuki"] or g["age"] < 16: return "Impossible pour l'instant."
    if not depenser(g): return "Plus d'actions !"
    if g["karma"] <= -10:
        ap(g, {"akatsuki": 1, "karma": -10, "rep": -30, "xp": 30}); L(g, "🌑 Tu retrouves la trace de l'organisation : elle t'accepte dans ses rangs.")
    else:
        L(g, "🌑 Ta réputation est trop propre : l'Akatsuki ne veut pas de toi. Fais parler ton côté sombre (karma ≤ -10).")
    return None


# ═════════════ Romance ═════════════
def _pref_ok(g, genre):
    p = g.get("pref", "B")
    return p == "B" or genre == p


def chercher_amour(g):
    if g["age"] < 14: return "Il faut avoir 14 ans."
    if g["couple"]: return "Tu es déjà en couple."
    if not depenser(g): return "Plus d'actions !"
    e = rencontre(g, None, "amour")
    if not e: L(g, "💘 Tu ne croises personne d'intéressant."); return None
    g["enc"] = e; L(g, f"💘 Tu croises {e['nom']} ({e['titre']}).")
    return None


def enc_sortir(g):
    e = g["enc"]
    if g["couple"]:
        e["line"] = "« Tu es déjà avec quelqu'un… »"; return
    if e["aff"] < 45:
        e["line"] = "« On se connaît à peine… discutons encore un peu. »"; return
    if random.random() < clamp(e["aff"] / 100 + (g["beaute"] - 50) / 300, .15, .92):
        g["couple"] = e["nom"]
        if e["nom"] not in [p["nom"] for p in g["pnj"]]:
            g["pnj"].append(dict(nom=e["nom"], role="amour", aff=e["aff"], niv=e["niv"], trait=random.choice(TRAITS)))
        ap(g, {"bonheur": 12, "karma": 1}); L(g, f"💞 {e['nom']} accepte ! Vous êtes désormais en couple.")
        e["line"] = "« Avec plaisir… j'attendais que tu me le demandes. »"; e["recrute"] = True
    else:
        e["aff"] = max(0, e["aff"] - 10); ap(g, {"bonheur": -4}); L(g, f"💔 {e['nom']} décline ton invitation.")
        e["line"] = "« Désolé(e)… je ne suis pas prêt(e). »"


# ───────────────────────── INTERFACE ─────────────────────────
def action(g, eff, txt):
    if g["pa"] <= 0:
        st.toast("Plus d'actions cette année ! Fais vieillir ton personnage.", icon="⏳"); return
    g["pa"] -= 1
    ap(g, eff)
    L(g, txt)
    st.rerun()


def html_txt(s):
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s).replace("\n", "<br>")


def anim(frames, delay=.35):
    ph = st.empty()
    for f in frames:
        ph.markdown(f'<div class="pop" style="text-align:center;font-size:36px">{f}</div>', unsafe_allow_html=True)
        time.sleep(delay)
    ph.empty()


def parler(g, p, ch):
    lab, pr, eo, to, ek, tk = ch
    g["_who"] = p["nom"]
    ok = random.random() < pr
    ap(g, eo if ok else ek)
    g["_who"] = None
    L(g, f"{'💬' if ok else '😬'} {p['nom']} — {lab} : {to if ok else tk}")


def fxbg(u):
    em = UNIV[u]["fx"]
    sp = "".join(f'<span style="left:{6 + i * 15}%;animation-delay:{i * 1.7}s;animation-duration:{10 + (i % 3) * 3}s">{em[i % len(em)]}</span>' for i in range(6))
    st.markdown(f'<div class="fxbg">{sp}</div>', unsafe_allow_html=True)


def tab_defis_site(prof):
    st.subheader("🏅 Défis du site")
    st.caption("Accomplis ces défis au fil de tes vies pour gagner des 💎 gemmes, à dépenser dans la Boutique de l'âme. Les records sont cumulés sur toutes tes vies.")
    r = prof["rec"]
    done_n = len(prof["defis"])
    st.progress(done_n / len(META_DEFIS), text=f"{done_n}/{len(META_DEFIS)} défis réclamés")
    for did, txt, chk, rew in META_DEFIS:
        done = did in prof["defis"]
        c1, c2 = st.columns([3, 1])
        c1.write(("✅ " if done else "🎯 ") + f"{txt} — **{rew} 💎**")
        if not done and chk(r) and c2.button("Réclamer", key=f"md{did}"):
            prof["defis"].append(did); prof["gems"] += rew
            st.toast(f"+{rew} 💎", icon="💎"); st.rerun()


def tab_boutique_ame(prof):
    st.subheader("💎 Boutique de l'âme")
    st.markdown(f'Tes gemmes : <span class="gem">💎</span> **{prof["gems"]}**', unsafe_allow_html=True)
    st.caption("Ces avantages se choisissent à la naissance d'un nouveau personnage et sont consommés à ce moment-là.")
    for k, (nom, prix, desc, uu) in PERKS.items():
        c1, c2 = st.columns([3, 1])
        n = prof["inv"].get(k, 0)
        c1.write(f"**{nom}**" + (f" *({uu} uniquement)*" if uu else "") + f" — {desc}" + (f"  ·  possédé : **{n}**" if n else ""))
        if c2.button(f"{prix} 💎", key=f"pk{k}", disabled=prof["gems"] < prix):
            prof["gems"] -= prix; prof["inv"][k] = n + 1
            st.toast(f"Acheté : {nom}", icon="💎"); st.rerun()


def tab_cimetiere(prof):
    st.subheader("⚰️ Cimetière")
    cim = prof["cim"]
    if not cim:
        st.info("Aucune vie terminée pour l'instant. Tes personnages défunts reposeront ici.")
        return
    st.caption(f"{len(cim)} vie(s) terminée(s)")
    for i, f in enumerate(reversed(cim)):
        U_ = UNIV[f["u"]]
        with st.expander(f"{U_['icon']} {f['nom']} — {f['age']} ans — {f['rang']} — score {f['score']}"):
            st.markdown(f'<div class="grave">🪦 <i>{f.get("ep", "")}</i><br>Cause : {f["cause"] or "inconnue"}</div>', unsafe_allow_html=True)
            infos = [f"Génération {f['gen']}"]
            if f.get("village"): infos.append(f"{VILL_ICO.get(f['village'], '')} {f['village']}")
            if f.get("clan"): infos.append(f"clan {f['clan']}")
            if f.get("pro"): infos.append(f"🇺🇸 NBA : {f['pro']}")
            if f.get("terr"): infos.append(f"🗺️ {f['terr']} territoire(s)")
            if f.get("titres"): infos.append("🏆 " + ", ".join(f"{k} ×{v}" for k, v in f["titres"].items()))
            if f.get("couple"): infos.append(f"💞 {f['couple']}")
            if f.get("enfants"): infos.append("👶 " + ", ".join(f["enfants"]))
            st.write(" • ".join(infos))
            if st.checkbox("Voir les derniers événements", key=f"cg{i}"):
                for ent in f.get("log", []):
                    st.write(f"**{ent[0]}** — {ent[1]}")


def bloc_sauvegarde(prof, g, key):
    st.download_button("💾 Télécharger ma sauvegarde (.json)", sauvegarde(prof, g), file_name=f"shinobi_life_{(g or {}).get('nom', 'profil')}.json",
                       mime="application/json", key=f"dl{key}")
    st.caption("La sauvegarde contient ton profil (gemmes, défis, cimetière) **et** ta vie en cours. Sur Streamlit Cloud, rien n'est conservé entre les sessions : télécharge-la pour ne rien perdre.")
    up = st.file_uploader("📂 Charger une sauvegarde", type="json", key=f"up{key}")
    if up is not None and st.button("📂 Charger", key=f"ld{key}"):
        try:
            p, gg = charger(json.load(up))
            if p is not None: st.session_state.profile = p
            st.session_state.g = gg
            st.session_state["dl"] = []
            st.rerun()
        except Exception as ex:
            st.error(f"Sauvegarde illisible : {ex}")


def ecran_accueil(prof):
    st.title("🍥🏀🏍️ Shinobi Life")
    st.caption("Un jeu narratif et interactif : vis des vies entières dans les univers de Naruto, Kuroko no Basket et Tokyo Revengers.")
    st.markdown(f'💎 **{prof["gems"]}** gemmes · ⚰️ {len(prof["cim"])} vie(s) au cimetière · 🏅 {len(prof["defis"])}/{len(META_DEFIS)} défis', unsafe_allow_html=True)
    tabs = st.tabs(["🌱 Nouvelle vie", "⚰️ Cimetière", "💎 Boutique de l'âme", "🏅 Défis du site", "📂 Sauvegarde"])
    with tabs[0]:
        nom = st.text_input("Prénom de ton personnage", "Kenji")
        u = st.selectbox("Choisis ton univers", list(UNIV), format_func=lambda x: f"{UNIV[x]['icon']} {x}")
        st.markdown("#### 🎨 Apparence")
        if "av_draft" not in st.session_state: st.session_state["av_draft"] = random_av()
        av = st.session_state["av_draft"]
        ph = st.empty()
        if st.button("🎲 Aléatoire", key="av_rand"):
            st.session_state["av_draft"] = random_av()
            for k_ in [k_ for k_ in st.session_state if str(k_).startswith("av_w_")]: del st.session_state[k_]
            st.rerun()
        t_g, t_p, t_c, t_y, t_s, t_b = st.tabs(["Genre", "Peau", "Cheveux", "Yeux", "Sourcils", "Pilosité"])
        with t_g: av["genre"] = {"Homme": "H", "Femme": "F"}[st.radio("Genre", ["Homme", "Femme"], index=0 if av["genre"] == "H" else 1, horizontal=True, key="av_w_genre")]
        with t_p: av["peau"] = SKIN_LBL.index(st.radio("Peau", SKIN_LBL, index=av["peau"], horizontal=True, key="av_w_peau"))
        with t_c:
            av["style"] = st.selectbox("Coiffure", HAIR_STYLES, index=HAIR_STYLES.index(av["style"]), key="av_w_style")
            av["couleur"] = st.radio("Couleur", list(HAIR_COL), index=list(HAIR_COL).index(av["couleur"]), horizontal=True, format_func=lambda c: f"{HAIR_EMO[c]}", key="av_w_cc", help="Noir, châtain, roux, blond, rouge, bleu, vert, violet, blanc")
        with t_y: av["yeux"] = st.radio("Yeux", list(EYE_COL), index=list(EYE_COL).index(av["yeux"]), horizontal=True, format_func=lambda c: f"{EYE_EMO[c]} {c}", key="av_w_yeux")
        with t_s: av["sourcils"] = st.radio("Sourcils", BROWS, index=BROWS.index(av["sourcils"]), horizontal=True, key="av_w_sourcils")
        with t_b: av["barbe"] = st.radio("Pilosité faciale", BEARDS, index=BEARDS.index(av["barbe"]), horizontal=True, key="av_w_barbe", disabled=av["genre"] == "F")
        ph.markdown(f'<div style="text-align:center">{avatar_svg(av, 20, u, 150)}</div>', unsafe_allow_html=True)
        st.info(f"🎯 Objectif : {UNIV[u]['goal']}")
        owned = {k: n for k, n in prof["inv"].items() if n > 0 and k in PERKS and PERKS[k][3] in (None, u)}
        use, ch = {}, {}
        if owned:
            st.markdown("**💎 Avantages de naissance** (consommés à la naissance)")
            for k, n in owned.items():
                use[k] = st.checkbox(f"{PERKS[k][0]} ×{n} — {PERKS[k][2]}", key=f"use{k}")
            if use.get("beaute_choix"): ch["beaute"] = st.selectbox("Beauté", list(BEAUTES))
            if use.get("talent_choix"):
                if u == "Naruto": ch["clan"] = st.selectbox("Clan", ["Sans clan"] + list(CLANS), format_func=lambda c: c if c == "Sans clan" else f"{CLANS[c]['ico']} {c} ({CLANS[c]['v']})")
                elif u == "Kuroko": ch["talent"] = st.selectbox("Talent", list(TALENTS), format_func=lambda x: f"{TALENTS[x][1]} {TALENTS[x][0]}")
                else: ch["origine"] = st.selectbox("Origine", [f[0] for f in FAM["Tokyo Revengers"]])
            if use.get("nat_choix"): ch["nat"] = st.selectbox("Nature de chakra", BASE_NAT, format_func=lambda x: f"{NAT[x]} {x}")
        else:
            st.caption("Aucun avantage possédé : accomplis des défis du site pour gagner des 💎 et en acheter.")
        if st.button("🌱 Naître", use_container_width=True, type="primary"):
            perks = {k: 1 for k, v in use.items() if v}
            for k in perks: prof["inv"][k] -= 1
            st.session_state.g = new_game(nom or "Anonyme", u, perks=perks, ch=ch, av=dict(st.session_state["av_draft"]))
            st.session_state["page"] = "📖 Vie"; st.session_state["hist"] = []
            st.session_state["dl"] = []
            st.rerun()
    with tabs[1]: tab_cimetiere(prof)
    with tabs[2]: tab_boutique_ame(prof)
    with tabs[3]: tab_defis_site(prof)
    with tabs[4]: bloc_sauvegarde(prof, None, "home")


if "profile" not in st.session_state: st.session_state.profile = new_profile()
if "g" not in st.session_state: st.session_state.g = None
prof = st.session_state.profile
g = st.session_state.g

if g is None:
    ecran_accueil(prof)
    st.stop()

fxn = st.session_state.pop("fx", None)
if fxn == "win": st.balloons()
agg = {}
for k, v in st.session_state.pop("dl", []):
    if k in ICON and isinstance(v, int): agg[k] = agg.get(k, 0) + v
msg = " · ".join(f"{ICON[k]} {v:+d}" for k, v in agg.items() if v)
if msg: st.toast(msg)
if fxn == "lose": st.markdown('<div class="shake" style="text-align:center;font-size:38px">💥</div>', unsafe_allow_html=True)

verifie_objectifs(g)
maj_rec(prof, g)
U = UNIV[g["u"]]
ri, rn = rang(g)
fxbg(g["u"])
PAGE = st.session_state.get("page", "📖 Vie")


def go(p, reset=False):
    h = st.session_state.setdefault("hist", [])
    if reset: h.clear()
    elif st.session_state.get("page", "📖 Vie") != p: h.append(st.session_state.get("page", "📖 Vie"))
    st.session_state["page"] = p
    st.rerun()


def topbar(g, menu=True):
    c1, c2, c3 = st.columns([1, 4, 2])
    if menu and c1.button("☰", key="hamb"): go("☰ Menu")
    c2.markdown('<div class="bl-logo">SHINOBI LIFE</div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="bl-gems">💎 {prof["gems"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="bl-prof">{avatar_svg(g.get("av"), g["age"], g["u"], 52)}<div class="bl-name"><b>{nom_complet(g)}</b> 🇯🇵 {U["icon"]}'
                f'<br><small>{g["age"]} an{"s" if g["age"] > 1 else ""} • {rn}{(" • " + SAISON_ICO[g.get("trim", 0)] + " " + SAISONS[g.get("trim", 0)]) if g["u"] == "Kuroko" else ""}</small></div>'
                f'<div class="bl-bank"><b>{g["argent"]} {U["monnaie"]}</b><br><small>Solde bancaire • ⚡ {g["pa"]}/{pa_max(g)}</small></div></div>', unsafe_allow_html=True)


bj = ""
if g["village"]: bj += f" • {VILL_ICO.get(g['village'], '')} {g['village']}"
if g["clan"]: bj += f" • {CLANS[g['clan']]['ico']} Clan {g['clan']}"
if g["biju"]: bj += f" • {g['biju']['ico']} Jinchūriki"
if g["akatsuki"]: bj += " • 🌑 Akatsuki"
if g["talent"]: bj += f" • {TALENTS[g['talent']['k']][1]} {TALENTS[g['talent']['k']][0]}"
if g["recrue"]: bj += f" • 🌟 Recruté par {g['recrue']}"
if g["lycee"]: bj += f" • 🏫 {g['lycee']}"
if g["pro"]: bj += f" • 🇺🇸 {g['pro']['team']}"
if g["gang"]: bj += f" • 🏍️ {g['gang']['nom']}"
if g.get("style"): bj += f" • 🥋 {g['style']}"
if g.get("patron"): bj += f" • 🎓 {g['patron']['nom']}"
if g["lignee"] > 1: bj += f" • 🕯️ Génération {g['lignee']}"
topbar(g, menu=not (g["dead"] or g["event"] is not None or g["bat"] or g["enc"]))

if g["dead"]:
    enterrer(prof, g)
    if not g.get("fx_dead"):
        st.snow(); g["fx_dead"] = True
    st.error(f"💀 {nom_complet(g)} est mort à {g['age']} ans. {g['cause']}")
    st.markdown(f'<div class="grave">🪦 <i>{epitaphe(g["flags"])}</i> — {g["u"]} • {rn}</div>', unsafe_allow_html=True)
    st.metric("Score final", score(g))
    if g["enfants"]:
        st.markdown("### 👶 Ta lignée continue")
        st.caption("Reprends le flambeau : ton enfant hérite de ton nom, d'une partie de ta fortune et de ta réputation.")
        for i, e in enumerate(g["enfants"]):
            age_e = max(0, g["age"] - e["nai"])
            extra = ""
            if e.get("talent"): extra += f" • {TALENTS[e['talent']][1]} {TALENTS[e['talent']][0]}"
            if e.get("clan"): extra += f" • clan {e['clan']}"
            if st.button(f"👶 Continuer avec {e['nom']} ({age_e} ans){extra}", key=f"her{i}", use_container_width=True):
                st.session_state.g = heriter(g, e)
                st.session_state["dl"] = []
                st.rerun()
    with st.expander("Journal de vie", expanded=False):
        cur = None
        for ent in reversed(g["log"][-60:]):
            a, t = ent[0], ent[1]
            if a != cur:
                st.markdown(f"**Âge {a}**"); cur = a
            st.write(t)
    if st.button("🔄 Nouveau personnage", use_container_width=True):
        st.session_state.g = None
        st.rerun()
    bloc_sauvegarde(prof, g, "mort")
    st.stop()

if g["event"] is not None:
    txt, chs, kind = ev_courant(g)
    st.markdown(f'<div class="{"arc-card" if kind == "arc" else "ev-card"}">📣 {"<b>Arc narratif</b> — " if kind == "arc" else "<b>Événement</b> — "}{html_txt(fmt(g, txt))}</div>', unsafe_allow_html=True)
    for i, c in enumerate(chs):
        if st.button(fmt(g, c[0]), key=f"ev{i}", use_container_width=True):
            resoudre(g, i)
            st.rerun()
    st.stop()


# ───────── Écrans plein cadre : combat et rencontre (style RPG) ─────────
def hpbar(cur, mx):
    pct = max(0, min(100, int(100 * cur / max(1, mx))))
    c = "#4caf50" if pct > 50 else "#ffc107" if pct > 20 else "#f44336"
    return f'<div class="hp"><div class="hpf" style="width:{pct}%;background:{c}"></div></div><small>{max(0, int(cur))}/{mx} PV</small>'


def dlg(ico, nom, titre, txt):
    st.markdown(f'<div class="dlg"><div class="dlg-ico">{ico}</div><div class="dlg-body"><div class="dlg-name">{nom} <span>{titre}</span></div>'
                f'<div class="dlg-txt">{txt}</div></div></div>', unsafe_allow_html=True)


def ecran_bataille(g):
    b = g["bat"]
    st.markdown(f"### ⚔️ Combat : {g['nom']} contre {b['foe']}")
    c1, c2 = st.columns(2)
    c1.markdown(f'<div class="duel-card"><div class="sprite-big foe">{b["ico"]}</div><b>{b["foe"]}</b>{hpbar(b["fhp"], b["fmax"])}</div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="duel-card"><div class="sprite-big me">{avatar_svg(g.get("av"), g["age"], g["u"], 84)}</div><b>{g["nom"]}</b>{hpbar(b["mhp"], b["mmax"])}</div>', unsafe_allow_html=True)
    st.markdown('<div class="dlg"><div class="dlg-body"><div class="dlg-txt">' + "<br>".join(b["log"][-5:]) + "</div></div></div>", unsafe_allow_html=True)
    if b["boost"] > 0: st.caption(f"⚡ Bonus actif ({b['boost']} action(s) renforcée(s))")
    if b["over"]:
        if b["over"] == "win": st.success("🏆 Victoire !")
        elif b["over"] == "lose": st.error("💀 Défaite…")
        else: st.info("🏃 Tu as pris la fuite.")
        if st.button("Continuer", key="bt_cont", use_container_width=True, type="primary"):
            bat_fin(g); st.rerun()
        return
    r1 = st.columns(2)
    mv = arg = None
    if r1[0].button("⚔️ Attaque", key="bt_atk", use_container_width=True): mv = "atk"
    if r1[1].button("🛡️ Défense", key="bt_def", use_container_width=True): mv = "def"
    r2 = st.columns(2)
    if r2[0].button(SPEC_LBL[g["u"]], key="bt_spec", use_container_width=True, disabled=b["spec"]): mv = "spec"
    if r2[1].button("🧪 Soin (50 💴)", key="bt_item", use_container_width=True, disabled=g["argent"] < 50): mv = "item"
    techs = [t for t in g["tech"] if t in TECH]
    if techs:
        sel = st.selectbox("Technique", techs, format_func=lambda t: f"{TECH[t]['n']} — PP {b['pp'].get(t, 2)}/2", key="bt_sel")
        if st.button("💥 Utiliser la technique", key="bt_tech", use_container_width=True, disabled=b["pp"].get(sel, 2) <= 0): mv, arg = "tech", sel
    else:
        st.caption("Apprends des techniques (onglet Techniques) pour les utiliser ici.")
    if st.button("🏃 Fuir", key="bt_fuite", use_container_width=True): mv = "fuite"
    if mv:
        if mv in ("atk", "tech", "spec"): anim(["💥"], .25)
        bat_move(g, mv, arg)
        st.rerun()


def ecran_rencontre(g):
    e = g["enc"]; t = ENC_BY_ID[e["tid"]]
    lieu = next((f"{ic} {nm}" for i, ic, nm in LIEUX[g["u"]] if i == e["lieu"]), "En chemin")
    st.markdown(f"### 🗺️ {lieu}")
    dlg(e["ico"], e["nom"], e["titre"], e["line"])
    lab = {"recruteur": "🤝 Intérêt", "rival": "😤 Respect", "ami": "💞 Affinité", "marchand": "💰 Confiance", "amour": "💘 Attirance"}[e["kind"]]
    st.progress(e["aff"] / 100, text=f"{lab} : {e['aff']}/100")
    if e["step"] == "offer":
        st.markdown(f"**{e['nom']} te propose de rejoindre : {ORGS[t['org']]['nom'] if t['org'] in ORGS else t['org'].split(':')[-1]}**")
        c1, c2 = st.columns(2)
        if c1.button("✅ Accepter", key="en_ok", use_container_width=True, type="primary"):
            enc_accepter(g); st.rerun()
        if c2.button("❌ Refuser", key="en_no", use_container_width=True):
            enc_refuser(g); st.rerun()
        return
    if e["kind"] == "marchand":
        st.caption("Tout est à -30 % chez lui.")
        for k, (nm, pr, ds, eff, uu, ag) in [x for x in SHOP.items() if (not x[1][4] or x[1][4] == g["u"]) and g["age"] >= x[1][5]][:6]:
            deja = k in ONCE_SHOP and k in g["achats"]
            c1, c2 = st.columns([3, 1])
            c1.write(f"**{nm}** — {ds}")
            if c2.button(f"{int(pr * .7)} 💴", key=f"en_b{k}", disabled=deja or g["argent"] < int(pr * .7)):
                err = enc_acheter(g, k)
                if err: st.toast(err, icon="⚠️")
                st.rerun()
        if st.button("👋 Partir", key="en_out", use_container_width=True):
            enc_partir(g); st.rerun()
        return
    b = st.columns(2)
    if b[0].button(f"💬 Parler ({3 - e['talks']} restantes)", key="en_talk", use_container_width=True, disabled=e["talks"] >= 3):
        enc_parler(g); st.rerun()
    if b[1].button("🎁 Offrir un cadeau", key="en_gift", use_container_width=True):
        err = enc_cadeau(g)
        if err: st.toast(err, icon="🛒")
        st.rerun()
    deja_ = e.get("fights", 0) >= 1
    if b[0].button("⚔️ Combat terminé" if deja_ else "⚔️ Le défier au combat", key="en_fight", use_container_width=True, disabled=g["age"] < 7 or deja_):
        enc_battre(g); st.rerun()
    if e["kind"] == "amour":
        if b[1].button("💘 Inviter à sortir", key="en_date", use_container_width=True, disabled=bool(g["couple"])):
            enc_sortir(g); st.rerun()
    if e["kind"] == "recruteur" and e["org"]:
        if b[1].button("🤝 Demander à rejoindre", key="en_ask", use_container_width=True):
            enc_demander(g); st.rerun()
    if st.button("👋 Partir", key="en_out", use_container_width=True):
        enc_partir(g); st.rerun()


def bloc_nouvelle_vie(g, key):
    with st.expander("⚠️ Zone dangereuse : recommencer une nouvelle vie"):
        st.warning("Cette vie sera abandonnée et rejoindra le cimetière. Tape NOUVELLE VIE pour confirmer.")
        t = st.text_input("Confirmation", key=f"nvt{key}")
        if st.button("🗑️ Abandonner cette vie", key=f"nvy{key}", disabled=t.strip().upper() != "NOUVELLE VIE"):
            g["dead"] = True; g["cause"] = "A abandonné cette vie."
            if not g["enfants"]:
                enterrer(prof, g); st.session_state.g = None
            st.rerun()


if g["bat"]:
    ecran_bataille(g)
    st.stop()
if g["enc"]:
    ecran_rencontre(g)
    st.stop()


# ═════════════ Navigation façon BitLife ═════════════
NBA_CUP = bool(g["cup"] and g["cup"]["key"] == "nba")


def row(ico, titre, sous, target, key, locked=False):
    lab = f"{ico}  {titre}" + (f"  —  {sous}" if sous else "") + "   ›"
    if st.button(lab, key="row_" + key, use_container_width=True, disabled=locked):
        go(target)


def row_act(ico, titre, sous, key, locked=False):
    """Ligne qui déclenche directement une action. Retourne True si cliquée."""
    return st.button(f"{ico}  {titre}" + (f"  —  {sous}" if sous else "") + "   •••", key="row_" + key, use_container_width=True, disabled=locked)


def resultat(err):
    if err: st.toast(err, icon="⚠️")
    else: st.rerun()


def statbar(lab, ico, val, col="#2e9d3e"):
    v = max(0, min(100, int(val)))
    return (f'<div class="bl-stat"><span class="lab">{lab}</span><span class="ico">{ico}</span>'
            f'<div class="bar"><div style="width:{v}%;background:{col}"></div><b>{v}%</b></div></div>')


def barre_simple(lab, val):
    v = max(0, min(100, int(val)))
    return f'<div class="bl-mini">{lab}<div class="mb"><div style="width:{v}%"></div></div></div>'


if PAGE != "📖 Vie":
    c1_, c2_ = st.columns([1, 5])
    if c1_.button("⬅️", key="back"):
        h_ = st.session_state.get("hist", [])
        st.session_state["page"] = h_.pop() if h_ else "📖 Vie"
        st.rerun()
    c2_.markdown(f'<div class="bl-head">{PAGE.split(" ", 1)[1].upper()}</div>', unsafe_allow_html=True)

if PAGE == "📖 Vie":
    if bj: st.caption(bj.lstrip(" •"))
    if g["u"] == "Kuroko":
        q_ = g["trim"]; nm_ = [COMP[k][0] for k in g["cal"] if k in COMP]
        st.info(f"{SAISON_ICO[q_]} **{SAISONS[q_]}** ({SAISON_MOIS[q_]}) — " + (", ".join(nm_) if nm_ else "pas de compétition ce trimestre") + f" • ⚡ {g['pa']}/{pa_max(g)} actions")
    t_j, t_n, t_c = st.tabs(["📖 Journal", "📰 Nouvelles du monde", "📌 En cours"])
    with t_n:
        nws = g["news"][::-1][:10]
        if not nws: st.caption("Le monde est calme pour l'instant…")
        out_n = []
        for ent in nws:
            sn = (SAISON_ICO[ent[2]] + " ") if len(ent) > 2 and g["u"] == "Kuroko" else ""
            out_n.append(f'<div class="bl-line"><span class="news">{sn}Âge {ent[0]} •</span> {ent[1]}</div>')
        st.markdown("".join(out_n), unsafe_allow_html=True)
    with t_c:
        for l_ in en_cours(g): st.markdown(l_)
        row("📜", "Opportunités & objectifs", "", "🎯 Objectif", "vc1")
        row("📖", "Scénarios", "", "📖 Scénarios", "vc2")
        row("🤝", "Alliances & ennemis", "", "🤝 Alliances", "vc3")
    with t_j, st.container(height=340):
        cur = None; out = []
        for ent in reversed(g["log"][-80:]):
            a, t = ent[0], ent[1]
            sn = (SAISON_ICO[ent[2]] + " ") if len(ent) > 2 and g["u"] == "Kuroko" else ""
            if a != cur:
                out.append(f'<div class="bl-age">Âge : {a} an{"s" if a > 1 else ""}</div>'); cur = a
            out.append(f'<div class="bl-line">{sn}{t}</div>')
        st.markdown("".join(out), unsafe_allow_html=True)
    ex = {"Naruto": ("🌀", "Maîtrise"), "Kuroko": ("🏀", "Excellence"), "Tokyo Revengers": ("🥋", "Combat")}[g["u"]]
    bars = (statbar("Bonheur", "😆", g["bonheur"]) + statbar("Santé", "❤️", g["sante"]) + statbar("Intelligence", "💡", g["intel"])
            + statbar("Apparence", "☀️", g["beaute"]) + statbar(ex[1], ex[0], g["mait"], "#f0b840")
            + (statbar("Chakra", "🌀", g["chakra"], "#3a78d8") if g["u"] == "Naruto" else "")
            + statbar("Réputation", "⭐", g["rep"], "#b36bd8") + statbar("Karma", "☯️", (g["karma"] + 100) / 2, "#6c7a89"))
    st.markdown(bars, unsafe_allow_html=True)

# ───────── Menus ─────────
if PAGE == "💼 Travail":
    row("🧰", "Petits boulots", "argent de poche", "🧰 Petits boulots", "tj", locked=g["age"] < 8)
    if g["u"] == "Naruto":
        row("🥷", "Missions", "missions de rang pour ton village", "🏯 Village & clan", "t1")
        row("📜", "Examens & carrière", "Chūnin, Jōnin, ANBU, Kage", "🎯 Objectif", "t2")
        row("📖", "Scénarios", "alliances, ennemis, politique", "📖 Scénarios", "t6")
        row("🏯", "Village & clan", f"{g['village']}" + (f" • clan {g['clan']}" if g["clan"] else ""), "🏯 Village & clan", "t3")
        if g["biju"]: row("🦊", "Bijū", g["biju"]["nom"], "🦊 Bijū", "t4")
        if g["akatsuki"]: row("🌑", "Akatsuki", "missions de l'organisation", "🌑 Akatsuki", "t5")
        elif g["age"] >= 16:
            if row_act("🌑", "Chercher l'Akatsuki", "pour voler des pupilles (karma ≤ -10)", "t7"): resultat(chercher_akatsuki(g))
    elif g["u"] == "Kuroko":
        row("🏟️", "Matchs & compétitions", "Inter-High, Winter Cup, tournois", "🏟️ Matchs", "t1")
        row("⭐", "Génération des Miracles", "rivalités et recrutements", "⭐ Miracles", "t2")
        if g["pro"]: row("🇺🇸", "NBA", g["pro"]["team"], "🇺🇸 NBA", "t3")
        row("📜", "Opportunités", "Inter-High, Winter Cup, NBA", "🎯 Objectif", "t4")
        row("📖", "Scénarios", "alliances, rivalités, amitiés", "📖 Scénarios", "t6")
    else:
        row("🏍️", "Gang & territoires", g["gang"]["nom"] if g["gang"] else "rejoins ou fonde un gang", "🏍️ Gang", "t1")
        row("🥊", "Dojo", "sports de combat", "🥊 Dojo", "t2")
        row("📜", "Opportunités", "arcs de gangs", "🎯 Objectif", "t3")
        row("📖", "Scénarios", "alliances, ennemis, politique", "📖 Scénarios", "t6")

if PAGE == "💰 Capital":
    st.markdown(f'<div class="bl-prof"><div class="bl-bank" style="margin:0 auto;text-align:center"><b>{g["argent"]} {U["monnaie"]}</b><br><small>Solde bancaire</small></div></div>', unsafe_allow_html=True)
    row("🛒", "Boutique", "objets de ton univers", "🛒 Boutique", "c1")
    row("🎒", "Inventaire", f"{sum(g['inv'].values())} objet(s) • {g['cadeau']} cadeau(x)", "🎒 Inventaire", "c5")
    row("🌀", "Techniques", "apprendre contre de l'argent", "🌀 Techniques", "c2")
    row("🤝", "Alliances", "tributs et accords", "🤝 Alliances", "c3")
    row("💎", "Boutique de l'âme", f"{prof['gems']} gemmes", "🏅 Site", "c4")

if PAGE == "❤️ Relations":
    row("👥", "Amis, rivaux & amours", f"{len(g['pnj'])} contact(s)", "👥 Liens", "r1")
    row("👪", "Famille", f"{len(g['enfants'])} enfant(s)", "👪 Famille", "r2")
    row("🗺️", "Explorer & rencontres", "recruteurs, rivaux, marchands", "🗺️ Carte", "r3")
    row("🤝", "Alliances & ennemis", f"{len(allies(g))} allié(s) • {len(ennemis(g))} ennemi(s)", "🤝 Alliances", "r4")
    if row_act("💘", "Rencontrer quelqu'un", "1 action • amour", "r5", locked=g["age"] < 14 or bool(g["couple"])): resultat(chercher_amour(g))

if PAGE == "⚽ Activités":
    row("🏋️", "S'entraîner", "progresser", "🏋️ Actions", "a1")
    if en_ecole(g): row("🏫", "École", "notes, clubs, cliques, professeurs", "🏫 École", "a2")
    row("🗺️", "Explorer", "carte du monde", "🗺️ Carte", "a3")
    if g["u"] == "Tokyo Revengers": row("🥊", "Dojo", "sports de combat", "🥊 Dojo", "a4")
    row("🌟", "Notoriété", "livre, pub, séance photo, talk-show", "🌟 Notoriété", "a5")
    row("📱", "Réseaux sociaux" if g["u"] != "Naruto" else "Gazette & Bingo Book", "", "📱 Réseaux", "a6")
    row("🎯", "Objectif & défis de vie", "", "🎯 Objectif", "a7")

if PAGE == "☰ Menu":
    row("🎒", "Inventaire", "objets, cadeaux, compétences", "🎒 Inventaire", "m6")
    row("🎯", "Objectif de vie", U["goal"], "🎯 Objectif", "m1")
    row("📖", "Scénarios", "histoires débloquables", "📖 Scénarios", "m0")
    row("⚰️", "Cimetière", f"{len(prof['cim'])} vie(s)", "⚰️ Cimetière", "m2")
    row("🏅", "Défis du site & boutique de l'âme", f"💎 {prof['gems']}", "🏅 Site", "m3")
    row("💾", "Sauvegarde", "télécharger / charger", "💾 Sauver", "m4")
    row("⚙️", "Paramètres", "", "⚙️ Paramètres", "m5")

if PAGE == "⚙️ Paramètres":
    st.caption("Réglages de la partie.")
    st.write(f"Personnage : **{nom_complet(g)}** — génération {g['lignee']} — univers {g['u']}")
    pm_ = {"F": "Femmes", "H": "Hommes", "B": "Les deux"}
    nv_ = st.radio("Tu cherches (rencontres amoureuses)", list(pm_), format_func=lambda k: pm_[k], index=list(pm_).index(g.get("pref", "B")), horizontal=True, key="pref_radio")
    g["pref"] = nv_
    bloc_nouvelle_vie(g, "par")

# ───────── École (style BitLife) ─────────
if PAGE == "🏫 École":
    etab = {"Naruto": "Académie ninja", "Kuroko": "Lycée" if g["age"] >= 15 else "École", "Tokyo Revengers": "Lycée" if g["age"] >= 15 else "Collège"}[g["u"]]
    st.markdown(f'<div class="bl-rowinfo"><b>🏫 {etab}</b>{barre_simple("Notes", g["notes"])}</div>', unsafe_allow_html=True)
    cible = {"Naruto": "🏯 Village & clan", "Kuroko": "🏟️ Matchs", "Tokyo Revengers": "🏍️ Gang"}[g["u"]]
    row("🏅", {"Naruto": "Escouade", "Kuroko": "Équipe de basket", "Tokyo Revengers": "Gang"}[g["u"]], "", cible, "e1")
    row("🎭", "Activités", "rejoindre un club", "🎭 Clubs", "e2")
    st.markdown(f'<div class="bl-rowinfo"><b>✏️ Classe</b>{barre_simple("Popularité", g["popu"])}</div>', unsafe_allow_html=True)
    row("🍎", "Classe", "amis, pitre, entraide", "🍎 Classe", "e3")
    row("😎", "Cliques", g["clique"] or "rejoindre une clique", "👥 Cliques", "e4")
    row("🧑‍🏫", "Professeurs", "interagir avec tes professeurs", "🧑‍🏫 Professeurs", "e5")
    if row_act("🩺", "Infirmerie", "aller voir l'infirmière", "e6"): resultat(ecole_infirmerie(g))
    if row_act("🤫", "Sécher les cours", "faire l'école buissonnière", "e7"): resultat(ecole_secher(g))
    if row_act("📚", "Étudier davantage", "faire des efforts", "e8"): resultat(ecole_etudier(g))

if PAGE == "🎭 Clubs":
    for nm, (ic, ds, eff) in CLUBS.items():
        if row_act(ic, f"Club {nm}", ds + (" ✅" if nm in g["clubs"] else ""), "cl" + nm, locked=nm in g["clubs"]): resultat(ecole_club(g, nm))

if PAGE == "🍎 Classe":
    for act, ic, nm, ds in (("amis", "🧑‍🤝‍🧑", "Se faire des amis", "popularité"), ("pitre", "🤡", "Faire le pitre", "risqué mais drôle"),
                            ("aider", "🤝", "Aider un camarade", "karma"), ("brimer", "😈", "Embêter un camarade", "mauvaise idée")):
        if row_act(ic, nm, ds, "cs" + act): resultat(ecole_classe(g, act))

if PAGE == "👥 Cliques":
    for nm, (ic, eff, need) in CLIQUES.items():
        if row_act(ic, f"Les {nm}", "✅ ta clique" if g["clique"] == nm else "rejoindre", "cq" + nm, locked=g["clique"] == nm): resultat(ecole_clique(g, nm))

if PAGE == "🧑‍🏫 Professeurs":
    mn = next((p["nom"] for p in g["pnj"] if p["role"] == "mentor"), "ton professeur")
    st.caption(f"Interlocuteur : {mn}")
    for act, ic, nm, ds in (("aide", "🧑‍🏫", "Demander de l'aide", "notes"), ("flatter", "🍎", "Flatter", "peut mal tourner"), ("insolent", "😤", "Répondre insolemment", "réputation")):
        if row_act(ic, nm, ds, "pr" + act): resultat(ecole_prof(g, act))

# ───────── Notoriété ─────────
if PAGE == "🌟 Notoriété":
    if g["rep"] < 40: st.warning(f"Il faut 40 de réputation pour être célèbre (actuel : {g['rep']}).")
    for kind, ic, nm, ds in (("livre", "📖", "Livre", "écrire un livre"), ("pub", "🎬", "Publicité", "tourner une publicité"),
                             ("photo", "📸", "Séance photo", "poser pour un magazine"), ("talk", "📺", "Talk-show", "passer dans une émission")):
        if row_act(ic, nm, ds, "no" + kind, locked=g["rep"] < 40): resultat(lancer_offre(g, kind))

# ───────── Réseaux sociaux ─────────
if PAGE == "📱 Réseaux":
    if g["age"] < 12: st.info("Il faut avoir 12 ans.")
    for p_ in PLATS[g["u"]]:
        ic = PLAT_ICO.get(p_, "📱")
        if p_ not in g["social"]:
            if row_act(ic, p_, "s'inscrire", "sn" + p_, locked=g["age"] < 12): resultat(social_inscrire(g, p_))
        else:
            if row_act(ic, p_, f"{g['social'][p_]} abonnés • publier", "sp" + p_): resultat(social_poster(g, p_))


# ───────── Alliances, ennemis, scénarios ─────────
if PAGE == "🤝 Alliances":
    al_, en_ = allies(g), ennemis(g)
    st.subheader(f"🤝 Alliances ({len(al_)}/3) • ⚔️ Ennemis : {len(en_)}")
    st.caption("Un allié donne +7 puissance, XP, réputation et argent chaque année. S'allier à un camp irrite ses rivaux. Les relations débloquent des scénarios.")
    row("📖", "Scénarios", "histoires débloquées par tes relations", "📖 Scénarios", "al_sc")
    for n, f in g["fact"].items():
        if n == _own(g): continue
        etat = "allié" if f["allie"] else "ennemi" if f.get("ennemi") else "neutre"
        riv = rivaux(g, n)
        with st.expander(f"{'🤝' if f['allie'] else '⚔️' if f.get('ennemi') else '⚪'} {n} — {etat} — relation {f['rel']}"):
            st.progress(f["rel"] / 100)
            if riv: st.caption("Rivaux : " + ", ".join(riv))
            c1, c2 = st.columns(2)
            if c1.button("🎁 Offrir un tribut (80)", key=f"tr{n}", disabled=g["age"] < 10): resultat(tribut(g, n))
            if f["allie"]:
                if c2.button("🗡️ Trahir cet allié", key=f"bt{n}"):
                    trahir_allie(g, n); st.rerun()
            elif f.get("ennemi"):
                if c2.button("🕊️ Proposer la paix", key=f"pe{n}"): resultat(proposer_paix(g, n))
            else:
                cout = 100 * (len(al_) + 1); pa_ = int(100 * min(.9, f["rel"] / 100 * .8 + g["rep"] / 250))
                c2.caption(f"Coût {cout} • chances {pa_}%")
                if c2.button("📜 Proposer une alliance", key=f"al{n}", disabled=g["age"] < 12 or len(al_) >= 3): resultat(proposer_alliance(g, n))
                if st.button("⚔️ Déclarer l'hostilité", key=f"ho{n}", disabled=g["age"] < 12): resultat(declarer_hostilite(g, n))

if PAGE == "📖 Scénarios":
    st.caption("Des histoires en plusieurs étapes, débloquées par tes alliances, tes ennemis, ton rang et ta réputation. Les lancer coûte 1 action. Ils peuvent aussi survenir d'eux-mêmes.")
    row("🤝", "Alliances & ennemis", f"{len(allies(g))} allié(s) • {len(ennemis(g))} ennemi(s)", "🤝 Alliances", "sc_al")
    for a_, ok_, done_ in scenarios(g):
        sub = "✅ accompli" if done_ else ("▶️ disponible" if ok_ else "🔒 " + a_["req"])
        if row_act("📖", fmt(g, a_["nom"]), sub, "sc" + a_["id"], locked=(not ok_) or done_): resultat(lancer_scenario(g, a_["id"]))

# ───────── Petits boulots ─────────
if PAGE == "🧰 Petits boulots":
    st.caption("Chaque petit boulot coûte 1 action et rapporte de l'argent de poche. Plus tu le refais, mieux tu es payé (jusqu'à +60 %).")
    for j_ in jobs_dispo(g):
        n_ = g["metiers"].get(j_[0], 0)
        sub = f"{j_[4][0]}–{j_[4][1]} {U['monnaie']}" + (f" • {n_} fois {'⭐' * min(5, n_ // 3)}" if n_ else "") + (f" • dès {j_[3]} ans" if g["age"] < j_[3] else "")
        if row_act(j_[1], j_[2], sub, "jb" + j_[0], locked=g["age"] < j_[3]): resultat(petit_boulot(g, j_[0]))

# ───────── Inventaire ─────────
if PAGE == "🎒 Inventaire":
    st.markdown(f'<div class="bl-prof"><div class="bl-bank" style="margin:0 auto;text-align:center"><b>{g["argent"]} {U["monnaie"]}</b><br><small>Solde bancaire</small></div></div>', unsafe_allow_html=True)
    st.subheader("🎒 Objets")
    objs = [(k, n) for k, n in g["inv"].items() if n > 0 and k in SHOP]
    if not objs: st.caption("Ton sac est vide : achète des objets dans la Boutique.")
    for k_, n_ in objs:
        nm_, pr_, ds_, eff_, uu_, ag_ = SHOP[k_]
        if row_act("🎒", f"{nm_} ×{n_}", ds_, "iv" + k_): resultat(utiliser(g, k_))
    st.subheader("🎁 Objets spéciaux")
    st.write(f"🎁 Cadeaux : **{g['cadeau']}** (à offrir dans 👥 Liens ou lors d'une rencontre)")
    st.write(f"⏳ Time Leap : **{g['revive']}** (te ramène à la vie automatiquement à ta mort)")
    st.subheader("🏆 Possessions")
    poss = [SHOP[k][0] for k in g["achats"] if k in SHOP]
    st.write(", ".join(poss) if poss else "Aucun objet équipé.")
    st.subheader("📚 Compétences")
    st.write(", ".join(TECH[t]["n"] for t in g["tech"] if t in TECH) or "Aucune technique apprise.")
    if g["pupilles"]: st.write("👁️ Pupilles : " + ", ".join(f"{PUP[p][0]} {p}" for p in g["pupilles"]))
    if g["nat"]: st.write("🔮 Natures : " + ", ".join(f"{NAT[n]} {n} (niv. {l})" for n, l in g["nat"].items()))
    if g["u"] == "Kuroko" and g["talent"]: st.write(f"{TALENTS[g['talent']['k']][1]} Talent : {TALENTS[g['talent']['k']][0]}")
def ecran_match(g):
    m = g["match"]
    st.markdown(f"### 🏀 Toi vs {m['opp']}" + (" — 🏆 compétition" if m["cup"] else ""))
    c1, c2 = st.columns(2)
    c1.metric("Toi", m["me"])
    c2.metric(m["opp"], m["en"])
    st.progress(min(1.0, (m["q"] - 1) / 4), text=f"Quart-temps {min(m['q'], 4)}/4")
    for l in m["lines"]:
        st.write(l)
    if m["fini"]:
        win, me, en = m["res"]
        (st.success if win else st.error)(f"{'🏆 Victoire' if win else '😞 Défaite'} {me}-{en}")
        if st.button("Continuer", use_container_width=True):
            g["match"] = None
            st.rerun()
        return
    if g["zone"] >= 1 and not m["zone"] and m["q"] >= 2:
        if st.button(f"⚡ Entrer dans la Zone (coûte {6 * g['zone']} santé en fin de match)", use_container_width=True):
            m["zone"] = True
            st.rerun()
    if m["zone"]:
        st.info("⚡ Tu es dans la Zone : bonus à chaque quart-temps.")
    st.caption("Choisis ta tactique pour ce quart-temps :")
    b = st.columns(2)
    tac = None
    if b[0].button("⚔️ Attaquer", use_container_width=True): tac = "att"
    if b[1].button("🛡️ Défendre", use_container_width=True): tac = "def"
    if g["talent"]:
        td = TALENTS[g["talent"]["k"]]
        reste = talent_usages(g) - m["talent"]
        if b[0].button(f"{td[1]} Talent : {td[0]} ({reste})", use_container_width=True, disabled=reste <= 0): tac = "talent"
    pt_ = duo_partner(g)
    if pt_:
        if b[1].button(f"🌟 Duo avec {pt_}", use_container_width=True): tac = "duo"
    if tac:
        jouer_quart(g, tac)
        st.rerun()

def tournoi(g):
    ph = st.empty()
    for nom, niv in (("Quart de finale", .8), ("Demi-finale", 1.1), ("Finale", 1.4)):
        ph.info(f"🥊 {nom} : le combat commence !")
        time.sleep(.9)
        if not duel(g, niv, nom) or g["dead"]:
            ph.error(f"💥 Éliminé en {nom.lower()}.")
            return
        ph.success(f"✅ {nom} remportée !")
        time.sleep(.7)
    ap(g, {"argent": 300, "rep": 15, "xp": 60})
    L(g, "🏆 Tu remportes le tournoi de combat clandestin !")
    ph.success("🏆 Champion du tournoi clandestin !")


# ───────── Onglets ─────────
if PAGE == "🎯 Objectif":
    st.subheader(f"🎯 {U['goal']}")
    f_ = g["flags"]
    chk = lambda ok, txt: st.write(("✅ " if ok else "⬜ ") + txt)
    if g["u"] == "Naruto":
        st.progress(min(1, ri / 3), text=f"Rang actuel : {rn} → objectif : Jōnin")
        chk(g["cap"] >= 2, "Réussir l'examen Chūnin")
        chk(g["cap"] >= 3, "Réussir l'examen de Jōnin → ninja d'élite")
        chk("anbu" in f_, "Entrer dans l'ANBU (optionnel)")
        chk("kage" in f_, f"Devenir {VILL[g['village']]['kage']} de {g['village']} (ultime)")
        if g["akatsuki"]: st.warning("Membre de l'Akatsuki : ton village ne te promouvra plus.")
    elif g["u"] == "Kuroko":
        tl = g["titres"]
        chk(bool(g["lycee"]), f"Intégrer un lycée {('(' + g['lycee'] + ')') if g['lycee'] else ''}")
        chk(tl.get("inter", 0) >= 1, f"Remporter l'Inter-High (×{tl.get('inter', 0)})")
        chk(tl.get("winter", 0) >= 1, f"Remporter la Winter Cup (×{tl.get('winter', 0)})")
        chk(g["zone"] >= 1, f"Entrer dans la Zone (niveau {ZONES[g['zone']]})")
        chk(bool(g["pro"]), "Signer en NBA")
        chk(tl.get("nba", 0) >= 1, f"Devenir champion NBA (×{tl.get('nba', 0)}) (ultime)")
    else:
        n_t = nterr(g)
        st.progress(min(1, n_t / DOMINATION), text=f"Territoires contrôlés : {n_t}/{DOMINATION} pour dominer le Japon")
        chk(bool(g["gang"]), "Rejoindre un gang")
        chk("chef" in f_, "Devenir chef de gang")
        chk(n_t >= 3, "Contrôler 3 territoires")
        chk(n_t >= DOMINATION, "Dominer le Japon (ultime)")
    if "ultime" in f_: st.success("👑 Tu as accompli l'objectif ultime de cet univers !")
    st.markdown("### 📣 Opportunités")
    ops = [a for a in arc_dispo(g) if a.get("man") and not a.get("scen")]
    if not ops: st.caption("Aucune opportunité pour l'instant. Progresse (rang, réputation, maîtrise) : elles apparaissent aussi toutes seules au fil des années.")
    for a in ops:
        c1, c2 = st.columns([3, 1])
        c1.write(f"**{fmt(g, a['nom'])}** — {len(a['steps'])} étape(s)")
        if c2.button("Se lancer", key=f"op{a['id']}"):
            if depenser(g):
                lancer_arc(g, a["id"]); L(g, f"📣 Tu te lances : {fmt(g, a['nom'])}."); st.rerun()
            else:
                st.toast("Plus d'actions !", icon="⏳")
    st.divider()
    st.markdown("### 📋 Défis de cette vie")
    for did, txt, chk_, rew in DEFIS:
        if g["u"] != "Naruto" and did in ("d6", "d8", "d11", "d12", "d14", "d15"): continue
        done = did in g["defis_ok"]
        c1, c2 = st.columns([3, 1])
        c1.write(("✅ " if done else "🎯 ") + txt + f"  *(récompense : {rew})*")
        if not done and chk_(g) and c2.button("Réclamer", key=f"df{did}"):
            g["defis_ok"].append(did); ap(g, rew); L(g, f"🏆 Défi réussi : {txt}"); st.rerun()

if PAGE == "🏋️ Actions":
    st.subheader("Actions de l'année")
    acts = [
        ("🧸 Jouer", 0, {"bonheur": 4}, "🧸 Tu joues et tu t'amuses."),
        ("📚 Étudier", 5, {"intel": 4, "bonheur": -1}, "📚 Tu étudies sérieusement."),
        ("💪 Entraînement physique", 6, {"force": 4, "sante": -1}, "💪 Séance intense."),
        (f"🎯 Travailler le {U['mait'].lower()}", 6, {"mait": 4, "sante": -1}, f"🎯 Tu progresses en {U['mait'].lower()}."),
        ("🧘 Méditer (chakra)", 6, {"chakra": 4}, "🧘 Ton chakra se renforce."),
        ("😴 Se reposer", 0, {"sante": 6, "bonheur": 3}, "😴 Repos bien mérité."),
    ]
    acts = [x for x in acts if g["u"] == "Naruto" or "chakra" not in x[2]]
    cc = st.columns(2)
    for i, (lab, mn, eff, txt) in enumerate(acts):
        ok = g["age"] >= mn
        if cc[i % 2].button(lab if ok else f"🔒 {lab} (dès {mn} ans)", key=f"a{i}", disabled=not ok, use_container_width=True):
            action(g, eff, txt)
    ja = U["jobage"]
    if cc[0].button(f"💼 {U['job']}" if g["age"] >= ja else f"🔒 {U['job']} (dès {ja} ans)", disabled=g["age"] < ja, use_container_width=True):
        gain = random.randint(30, 80) * (1 + ri)
        action(g, {"argent": gain, "xp": 5}, f"💼 {U['job']} : +{gain} {U['monnaie']}.")
    st.markdown("**☯️ Actions morales**")
    k1, k2 = st.columns(2)
    if k1.button("🤲 Aider un inconnu" if g["age"] >= 8 else "🔒 Aider (dès 8 ans)", disabled=g["age"] < 8, use_container_width=True):
        action(g, {"karma": 5, "bonheur": 2}, "🤲 Tu aides un inconnu, ça fait du bien.")
    if k2.button("🎗️ Faire un don (50)" if g["age"] >= 10 else "🔒 Don (dès 10 ans)", disabled=g["age"] < 10, use_container_width=True):
        if g["argent"] >= 50:
            action(g, {"argent": -50, "karma": 6, "bonheur": 3}, "🎗️ Tu fais un don à un orphelinat.")
        else:
            st.toast("Pas assez d'argent.", icon="💴")
    if k1.button("😈 Intimider un camarade" if g["age"] >= 8 else "🔒 Intimider (dès 8 ans)", disabled=g["age"] < 8, use_container_width=True):
        action(g, {"karma": -6, "rep": 2, "bonheur": -1}, "😈 Tu intimides un camarade.")
    if k2.button("🗡️ Voler un marchand" if g["age"] >= 10 else "🔒 Voler (dès 10 ans)", disabled=g["age"] < 10, use_container_width=True):
        if random.random() < .65:
            gain = random.randint(40, 120)
            action(g, {"argent": gain, "karma": -8}, f"🗡️ Tu voles un marchand : +{gain}.")
        else:
            action(g, {"rep": -10, "bonheur": -5, "karma": -3}, "🚨 Tu te fais prendre en train de voler !")
    st.divider()
    if g["nat"]:
        st.subheader("Entraîner une nature de chakra")
        n = st.selectbox("Nature", list(g["nat"]), format_func=lambda x: f"{NAT[x]} {x} (niv. {g['nat'][x]})")
        if st.button("✨ S'entraîner", use_container_width=True):
            lvl = g["nat"][n]
            if g["pa"] <= 0:
                st.toast("Plus d'actions !", icon="⏳")
            elif lvl >= 5:
                st.toast("Niveau maximum atteint.", icon="🏆")
            else:
                g["pa"] -= 1
                if random.random() < max(.2, .75 - .12 * lvl + g["chakra"] / 300):
                    g["nat"][n] += 1
                    L(g, f"✨ {NAT[n]} {n} passe niveau {g['nat'][n]} !")
                    debloquer_rares(g)
                else:
                    L(g, f"😓 L'entraînement de {n} n'a pas porté ses fruits.")
                    ap(g, {"sante": -2})
                st.rerun()
    elif g["u"] == "Naruto":
        st.info("Ton chakra s'éveillera à 6 ans.")


if PAGE == "👥 Liens":
    st.subheader("Relations")
    if g["couple"]: st.success(f"💞 En couple avec {g['couple']}")
    for i, p in enumerate(g["pnj"]):
        ico = ROLE_ICO.get(p["role"], "👤")
        with st.expander(f"{ico} {p['nom']} — affinité {p['aff']} • {p.get('trait', '')}"):
            st.progress(p["aff"] / 100)
            tp = TALK_GEN.get(p["role"], TALK_GEN["famille"])
            j = st.selectbox("De quoi lui parler ?", list(range(len(tp))), format_func=lambda j, tp=tp: tp[j][0], key=f"tp{i}")
            c1, c2 = st.columns(2)
            if c1.button("💬 Discuter", key=f"d{i}"):
                if depenser(g):
                    parler(g, p, tp[j]); st.rerun()
                else: st.toast("Plus d'actions !", icon="⏳")
            if c2.button("🎁 Offrir un cadeau", key=f"g{i}"):
                if g["cadeau"] > 0:
                    g["cadeau"] -= 1; p["aff"] = min(100, p["aff"] + 15)
                    L(g, f"🎁 {p['nom']} adore ton cadeau !"); st.rerun()
                else: st.toast("Achète un cadeau en boutique.", icon="🛒")
            if p["role"] in ("ami", "rival", "equipier", "mentor"):
                if c1.button("⚔️ Défier en duel" if g["age"] >= 7 else "🔒 Duel (dès 7 ans)", key=f"x{i}", disabled=g["age"] < 7):
                    if depenser(g):
                        bat_init(g, p["nom"], ROLE_ICO.get(p["role"], "😤"), p["niv"], {"pnj": p["nom"]}); st.rerun()
                    else: st.toast("Plus d'actions !", icon="⏳")
            if p["role"] == "famille" and g["age"] >= 6:
                if c1.button("💰 Argent de poche", key=f"m{i}"):
                    if depenser(g):
                        if random.random() < p["aff"] / 100:
                            s = random.randint(10, 30) * g["riche"]; g["argent"] += s
                            L(g, f"💰 {p['nom']} te donne {s} {U['monnaie']}.")
                        else: L(g, f"🙅 {p['nom']} refuse de te donner de l'argent.")
                        st.rerun()
            if p["role"] == "amour" and not g["couple"] and g["age"] >= 13:
                if c2.button("💍 Se déclarer", key=f"l{i}"):
                    if random.random() < min(.95, p["aff"] / 100 + (g["beaute"] - 50) / 400):
                        g["couple"] = p["nom"]; ap(g, {"bonheur": 15})
                        L(g, f"💞 {p['nom']} accepte ! Vous êtes en couple.")
                    else:
                        ap(g, {"bonheur": -8}); L(g, f"💔 {p['nom']} refuse tes sentiments.")
                    st.rerun()

if PAGE == "👪 Famille":
    fm = g["fam"]
    st.subheader(f"👪 Famille {fm['nom']}")
    st.caption(f"{fm['type']} — {fm['d']}")
    if g["ancetres"]: st.write("🕯️ Lignée : " + " → ".join(g["ancetres"]) + f" → **{g['nom']}**")
    for p in pnjs(g, "famille"): st.write(f"👪 {p['nom']} — affinité {p['aff']}")
    if g["couple"]: st.write(f"💞 Conjoint(e) : {g['couple']}")
    st.markdown("### 👶 Enfants")
    if not g["enfants"]: st.caption("Aucun enfant. Il faut être en couple et avoir entre 18 et 45 ans.")
    for e in g["enfants"]:
        ex = f" • {TALENTS[e['talent']][1]} {TALENTS[e['talent']][0]}" if e.get("talent") else ""
        ex += f" • clan {e['clan']}" if e.get("clan") else ""
        st.write(f"{'👧' if e['sexe'] == 'f' else '👦'} **{e['nom']}** — {max(0, g['age'] - e['nai'])} ans{ex}")
    if g["enfants"]: st.info("À ta mort, tu pourras reprendre la vie d'un de tes enfants.")
    if st.button("👶 Fonder une famille / avoir un enfant", use_container_width=True):
        err = avoir_enfant(g)
        if err: st.toast(err, icon="⚠️")
        else: st.rerun()


if PAGE == "🌀 Techniques":
    if g["u"] == "Naruto":
        st.subheader("🌀 Natures de chakra")
        if g["nat"]:
            for n, l in g["nat"].items(): st.write(f"{NAT[n]} **{n}** — niveau {l}/5")
        else: st.write("Aucune nature éveillée pour l'instant (éveil à 6 ans).")
        if g["oeil"]: st.write(f"👁️ Pupille héréditaire : {PUP[g['oeil'][0]][0]} {g['oeil'][0]} (éveil à {g['oeil'][1]} ans)")
        st.caption("Tu ne peux apprendre que les techniques de ta voie : ta nature, ton clan, tes pupilles. Fusion à 15 ans : Eau+Vent → Glace, Terre+Eau → Bois, Feu+Terre → Lave (niv. 3 chacune).")
    elif g["u"] == "Kuroko":
        if g["talent"]:
            td_ = TALENTS[g["talent"]["k"]]
            st.write(f"{td_[1]} Talent de naissance : **{td_[0]}**")
        st.caption("Tes techniques doivent correspondre à ton talent de naissance : les autres sont verrouillées.")
    else:
        st.write(f"🥋 Style de combat : **{g.get('style') or 'inconnu'}**")
        st.caption("Tes techniques de combat dépendent de ton style : les autres sont verrouillées.")
    st.subheader("⚔️ Techniques")
    hors = []
    for k, t in TECH.items():
        if t["u"] != g["u"]: continue
        ok, req_txt, voie = tech_info(g, t)
        if k in g["tech"]:
            st.success(f"✅ {t['n']} (puissance +{t['pw']})")
        elif not voie:
            hors.append((t, req_txt))
        else:
            c1, c2 = st.columns([3, 1])
            c1.write(f"**{t['n']}** — +{t['pw']} puissance — dès {t['a']} ans — requis : {req_txt} — {t['p']} 💴")
            if c2.button("Apprendre", key=f"t{k}", disabled=not ok or g["age"] < t["a"]):
                err = apprendre(g, k)
                if err: st.toast(err, icon="⚠️")
                else: st.rerun()
    if hors:
        with st.expander(f"🔒 Hors de ta voie ({len(hors)})"):
            for t, rt in hors: st.write(f"{t['n']} — requis : {rt}")
    st.metric("Puissance totale", int(puissance(g)))

if PAGE == "🏯 Village & clan":
    if PAGE == "🏯 Village & clan":
        v = g["village"]; vd = VILL[v]
        st.subheader(f"{vd['ico']} {v} — village du {vd['kage']}")
        if g["clan"]:
            cd = CLANS[g["clan"]]
            st.markdown(f"### {cd['ico']} Clan {g['clan']}")
            st.write(cd["d"])
            if cd.get("eye"): st.write(f"👁️ Pupille héréditaire : **{cd['eye']}**" + (" ✅ éveillée" if cd["eye"] in g["pupilles"] else f" (éveil à {cd['eage']} ans)"))
        else:
            st.write("Tu n'appartiens à aucun clan : ta force viendra de ton travail.")
        st.write("🔮 Natures innées : " + (", ".join(f"{NAT[n]} {n}" for n in g["nat_innee"]) or "inconnues"))
        st.markdown("### 🎖️ Parcours shinobi")
        for fl, lab in (("rangC", "Mission de rang C héroïque"), ("chunin", "Chūnin"), ("invasion", "Défenseur du village"), ("jonin", "Jōnin"),
                        ("anbu", "ANBU"), ("guerre", "Vétéran de la Grande Guerre"), ("kage", f"{vd['kage']}")):
            st.write(("✅ " if fl in g["flags"] else "⬜ ") + lab)
        letter = "DCBAS"[min(4, ri)]
        st.markdown(f"### 📜 Mission de rang {letter}")
        seuil = 18 + ri * 38
        st.caption(f"Chances estimées : {int(proba(g, ['pw', seuil]) * 100)} %")
        if st.button(f"📜 Accepter une mission de rang {letter}", use_container_width=True, disabled=g["age"] < 12 or g["akatsuki"]):
            if depenser(g):
                anim(["🥷", "💨", "⚔️"])
                if random.random() < proba(g, ["pw", seuil]):
                    ap(g, {"xp": 12 + 8 * ri, "rep": 2 + ri, "argent": 60 + 50 * ri}); L(g, f"📜 Mission de rang {letter} réussie pour {v}.")
                else:
                    ap(g, {"sante": -8 - 4 * ri, "rep": -2}); L(g, f"💥 Mission de rang {letter} échouée.")
                    if g["sante"] <= 0: mort(g, "Tué en mission.")
                st.rerun()
            else: st.toast("Plus d'actions !", icon="⏳")


if PAGE == "🗺️ Carte":
    st.subheader("🗺️ Explorer")
    st.caption("Chaque sortie coûte 1 action. Tu peux croiser des amis, des rivaux, des marchands… ou des recruteurs qui t'offriront de rejoindre leur équipe, leur gang ou leur école.")
    if "flash" in st.session_state: st.info(st.session_state.pop("flash"))
    if g["patron"]:
        pt = g["patron"]; o_ = ORGS[pt["org"]]
        st.success(f"{pt['ico']} **{pt['nom']}** — {pt['titre']} • {o_['nom']} : +{o_['pw']} puissance, bonus chaque année")
        if st.button("👋 Quitter ce maître", key="qpatron"):
            quitter_patron(g); st.rerun()
    cols_ = st.columns(3)
    for i, (lid, ico, nm) in enumerate(LIEUX[g["u"]]):
        if cols_[i % 3].button(f"{ico} {nm}", key=f"lieu{lid}", use_container_width=True, disabled=g["age"] < 6):
            if g["pa"] <= 0:
                st.toast("Plus d'actions cette année !", icon="⏳")
            else:
                anim(["🚶", "🚶💨", "❓"], .3)
                st.session_state["flash"] = explorer(g, lid) or ""
                st.rerun()
    if g["age"] < 6: st.caption("🔒 Tu pourras explorer à partir de 6 ans.")
    st.markdown("### 📇 Contacts")
    for p in g["pnj"]:
        if p["role"] in ("mentor", "rival", "ami", "equipier") :
            st.write(f"{ROLE_ICO.get(p['role'], '👤')} {p['nom']} — affinité {p['aff']} ({p['role']})")
if PAGE == "🦊 Bijū":
    if PAGE == "🦊 Bijū":
        b = g["biju"]
        if not b:
            st.info("Tu n'abrites aucun bijū. Un événement rare peut survenir au fil des années (plus fréquent dans l'univers Naruto) : une bête à queues peut choisir de se sceller en toi.")
        else:
            st.subheader(f"{b['ico']} {b['nom']}")
            st.progress(b["lien"] / 100, text=f"Lien avec le bijū : {b['lien']}/100")
            st.caption("Sous 25, le bijū risque de prendre le contrôle. À 60, tu débloques le Mode Bijū (gros bonus de puissance).")
            if b["lien"] >= 60:
                st.success("🔥 Mode Bijū débloqué !")
            c1, c2 = st.columns(2)
            if c1.button("🗣️ Dialoguer avec lui", use_container_width=True):
                action(g, {"lien": 6, "bonheur": 2}, "🗣️ Tu discutes avec ton bijū, la confiance grandit.")
            if c2.button("🧘 Méditer dans ton esprit", use_container_width=True):
                action(g, {"lien": 4, "chakra": 3}, "🧘 Tu rencontres ton bijū dans ton monde intérieur.")
            if st.button("🔥 Puiser dans sa puissance", use_container_width=True):
                if g["pa"] <= 0:
                    st.toast("Plus d'actions !", icon="⏳")
                else:
                    g["pa"] -= 1
                    if random.random() < .3 + b["lien"] / 150:
                        ap(g, {"xp": 30, "chakra": 8, "rep": 3, "lien": -2})
                        L(g, "🔥 Tu maîtrises la puissance du bijū !")
                    else:
                        ap(g, {"sante": -25, "lien": -6})
                        L(g, "💢 La puissance du bijū te dépasse, tu es blessé.")
                        if g["sante"] <= 0:
                            mort(g, "Consumé par la puissance de son bijū.")
                    st.rerun()

if PAGE == "🌑 Akatsuki":
    if PAGE == "🌑 Akatsuki":
        st.subheader("🌑 Akatsuki")
        st.caption("Tu es un déserteur : ton village te traque, mais l'organisation t'offre des missions sombres.")
        if g["pupilles"]:
            st.write("👁️ Pupilles volées : " + ", ".join(f"{PUP[n][0]} {n}" for n in g["pupilles"]))
        restantes = [n for n in PUP if n not in g["pupilles"]]
        if restantes:
            cible = st.selectbox("Pupille à voler", restantes, format_func=lambda n: f"{PUP[n][0]} {n} (difficulté {PUP[n][1]})")
            pch = int(100 * chance_vol(g, cible))
            st.caption(f"Chances de succès : {pch} %" + (f" • repérage : +{int(g.get('vol_bonus', 0) * 100)} %" if g.get("vol_bonus") else "") + (f" • persévérance : +{g.get('vol_echecs', 0) * 8} %" if g.get("vol_echecs") else ""))
            if cible == "Mangekyō Sharingan" and "Sharingan" not in g["pupilles"]: st.caption("⚠️ Vole d'abord un Sharingan : sans lui, le Mangekyō est bien plus difficile.")
            vb1, vb2 = st.columns(2)
            if vb1.button("🔍 Repérer un porteur (+20 %)", key="rep_pup", use_container_width=True): resultat(reperer_porteur(g))
            if vb2.button("👁️ Voler la pupille", key="vol_pup", use_container_width=True): resultat(voler_pupille(g, cible))
        else:
            st.success("Tu possèdes toutes les pupilles légendaires.")
if PAGE == "⭐ Miracles":
    if PAGE == "⭐ Miracles":
        tl = g["talent"]
        td = TALENTS[tl["k"]]
        st.subheader(f"{td[1]} Talent inné : {td[0]}")
        st.caption(td[2])
        st.progress(tl["lvl"] / 5, text=f"Niveau du talent : {tl['lvl']}/5 (+{td[4] * tl['lvl']} puissance)")
        if st.button("🔥 Entraîner mon talent", use_container_width=True, disabled=g["age"] < 6 or tl["lvl"] >= 5):
            if g["pa"] <= 0:
                st.toast("Plus d'actions !", icon="⏳")
            else:
                g["pa"] -= 1
                if random.random() < max(.2, .75 - .12 * tl["lvl"]):
                    tl["lvl"] += 1
                    ap(g, {"mait": 2})
                    L(g, f"✨ Ton talent « {td[0]} » passe niveau {tl['lvl']} !")
                else:
                    L(g, "😓 Ton talent refuse de progresser cette année.")
                st.rerun()
        if g["age"] < 6:
            st.caption("🔒 Entraînement du talent dès 6 ans.")
        st.divider()
        st.subheader("⭐ Génération des Miracles")
        if g["recrue"]:
            r = g["recrue"]
            st.success(f"🌟 Tu es recruté par {r} ({GM[r][0]}) : +12 puissance, +10 XP et +2 réputation par an.")
            st.markdown(f"**🤝 Équipe de {r}**")
            b1, b2, b3 = st.columns(3)
            if b1.button("🏋️ Duo d'entraînement", use_container_width=True):
                g["gm"][r] = min(100, g["gm"][r] + 5)
                action(g, {"mait": 6, "force": 3, "sante": -3}, f"🏋️ Entraînement intensif avec {r}.")
            if b2.button("🎯 Perfectionner mon talent", use_container_width=True):
                if g["pa"] <= 0:
                    st.toast("Plus d'actions !", icon="⏳")
                else:
                    g["pa"] -= 1
                    if tl["lvl"] < 5 and random.random() < .6:
                        tl["lvl"] += 1
                        L(g, f"✨ {r} t'aide à faire progresser ton talent (niveau {tl['lvl']}) !")
                    else:
                        ap(g, {"mait": 3})
                        L(g, f"🎯 {r} te donne des conseils précieux.")
                    st.rerun()
            if b3.button("🍜 Sortir manger", use_container_width=True):
                action(g, {"bonheur": 6, "rep": 2}, f"🍜 Tu passes la soirée avec {r}.")
        else:
            st.caption("Impressionne-les en 1 contre 1. À 60 d'intérêt, 30 de réputation et 50 de maîtrise, tu peux demander à les rejoindre. Ils peuvent aussi te repérer par eux-mêmes (13-18 ans).")
        use_t = st.checkbox(f"{td[1]} Activer mon talent pendant les 1 contre 1 (−3 santé)")
        for n, (lyc, niv, tal) in GM.items():
            it = g["gm"][n]
            with st.expander(f"{n} — {lyc} — intérêt {it}" + (" 🌟" if n == g["recrue"] else "")):
                st.caption(f"Talent : {tal}")
                st.progress(it / 100)
                am = g["amitie"].get(n, 0)
                st.caption(f"💞 Amitié : {am}/100 — " + ("meilleur ami" if am >= 90 else "ami" if am >= 60 else "connaissance" if am >= 30 else "inconnu") + " (un ami ≥ 60 permet le duo en match)")
                st.progress(am / 100)
                if st.button("🤝 Passer du temps ensemble", key=f"am{n}", disabled=g["age"] < 8, use_container_width=True):
                    err_ = temps_avec_gm(g, n)
                    if err_: st.toast(err_, icon="⚠️")
                    else: st.rerun()
                i = st.selectbox("Que lui dire ?", list(range(len(TALK[n]))), format_func=lambda j, n=n: TALK[n][j][0], key=f"tk{n}")
                if st.button("💬 Lui parler", key=f"tb{n}", disabled=g["age"] < 8, use_container_width=True):
                    if g["pa"] <= 0:
                        st.toast("Plus d'actions !", icon="⏳")
                    else:
                        g["pa"] -= 1
                        choisir(g, TALK[n][i], n)
                        st.rerun()
                c1, c2 = st.columns(2)
                if c1.button("🏀 Défier en 1 contre 1", key=f"gm{n}", disabled=g["age"] < 13):
                    if g["pa"] <= 0:
                        st.toast("Plus d'actions !", icon="⏳")
                    else:
                        g["pa"] -= 1
                        mine = puissance(g) * random.uniform(.8, 1.2)
                        if use_t:
                            mine *= 1 + .08 * tl["lvl"]
                            ap(g, {"sante": -3})
                        foe = (30 + niv * 35) * random.uniform(.85, 1.15)
                        if mine >= foe:
                            g["gm"][n] = min(100, it + 18)
                            ap(g, {"rep": 8, "xp": 25})
                            L(g, f"🏀 Victoire en 1 contre 1 contre {n} ! Il te remarque." + (f" ({td[1]} talent activé)" if use_t else ""))
                        else:
                            g["gm"][n] = min(100, it + 6)
                            ap(g, {"sante": -5, "bonheur": -3})
                            L(g, f"😞 {n} te bat en 1 contre 1, mais apprécie ta combativité.")
                        st.rerun()
                if not g["recrue"] and c2.button("🤝 Demander à rejoindre", key=f"gr{n}", disabled=g["age"] < 14):
                    if it < 60 or g["rep"] < 30 or g["mait"] < 50:
                        st.toast("Il faut intérêt ≥ 60, réputation ≥ 30 et maîtrise ≥ 50.", icon="🔒")
                    elif random.random() < min(.9, .6 + it / 300):
                        recruter(g, n)
                        st.rerun()
                    else:
                        g["gm"][n] = max(0, it - 10)
                        L(g, f"🙅 {n} refuse pour l'instant ta demande.")
                        st.rerun()

if PAGE == "🏟️ Matchs":
    if PAGE == "🏟️ Matchs":
        if NBA_CUP:
            st.info("🇺🇸 Playoffs NBA en cours : rends-toi dans l'onglet NBA.")
        elif g["match"]:
            ecran_match(g)
        else:
            if g["cup"]:
                c = g["cup"]
                st.info(f"🏆 {c['nom']} en cours — {c['rounds'][c['i']]} contre {c['opps'][c['i']]} ({c['i'] + 1}/{len(c['opps'])})")
                if c.get("aide"):
                    with st.expander("📰 Autres résultats du tournoi"):
                        for l_ in c["aide"]: st.write(l_)
                if st.button("▶️ Lancer le match", use_container_width=True):
                    demarrer_match(g, c["opps"][c["i"]], True)
                    st.rerun()
                if st.button("🏳️ Abandonner la compétition", use_container_width=True):
                    L(g, f"🏳️ Tu abandonnes la {c['nom']}.")
                    g["cup"] = None
                    st.rerun()
            else:
                st.subheader(f"📅 Calendrier — {SAISON_ICO[g['trim']]} {SAISONS[g['trim']]} ({SAISON_MOIS[g['trim']]})")
                shown = False
                for key, (nom, (a0, a1), rounds, rew) in COMP.items():
                    if key == "nba": continue
                    if g["age"] < a0:
                        st.write(f"🔒 {nom} — dès {a0} ans")
                    elif g["age"] <= a1:
                        shown = True
                        dispo = g["cal"].get(key)
                        c1, c2 = st.columns([3, 1])
                        c1.write(f"{'🟢' if dispo else '⏳'} **{nom}** — {len(rounds)} tours — {'ce trimestre' if dispo else 'prochain : ' + SAISONS[COMP_Q.get(key, [0])[0]]} — récompense : {rew}")
                        if c2.button("S'inscrire", key=f"cp{key}", disabled=not dispo):
                            if g["pa"] <= 0:
                                st.toast("Plus d'actions !", icon="⏳")
                            else:
                                g["pa"] -= 1
                                demarrer_cup(g, key)
                                st.rerun()
                if g["age"] > 18:
                    st.caption("Plus de compétitions lycéennes à ton âge.")
                if g["age"] >= 13:
                    c1, c2 = st.columns([3, 1])
                    c1.write(f"{'🟢' if g['cal'].get('camp') else '✅'} **🏕️ Camp d'entraînement d'été** — +6 maîtrise, +4 force (150)")
                    if c2.button("Y aller", key="camp", disabled=not g["cal"].get("camp")):
                        if g["argent"] < 150:
                            st.toast("Pas assez d'argent.", icon="💴")
                        else:
                            g["argent"] -= 150
                            g["cal"]["camp"] = False
                            action(g, {"mait": 6, "force": 4, "sante": -4}, "🏕️ Tu passes une semaine intense au camp d'été.")
                st.divider()
                st.subheader("🏆 Organiser un tournoi entre équipes")
                ad = adversaires(g)
                st.caption("Invite 3 équipes (4 au total) ou 7 équipes (8 au total) : tu joues les matchs de ton parcours, les autres sont simulés. Coût : 100 par équipe. Il faut 15 ans et 15 de réputation.")
                inv = st.multiselect("Équipes invitées", ad, key="tour_eq")
                if st.button("📣 Lancer le tournoi", use_container_width=True, disabled=len(inv) not in (3, 7)):
                    err = organiser_tournoi(g, inv)
                    if err: st.toast(err, icon="⚠️")
                    else: st.rerun()
                st.divider()
                st.subheader("⚡ La Zone")
                st.progress(g["zone"] / 3, text=f"Niveau de Zone : {ZONES[g['zone']]}")
                if g["zone"] < 3:
                    r = ZONE_REQ[g["zone"] + 1]
                    st.caption(f"Prochain niveau ({ZONES[g['zone'] + 1]}) : {g['zxp']}/{r[0]} entraînements, maîtrise ≥ {r[1]}, âge ≥ {r[2]}.")
                st.caption(f"Potentiel de Zone : {ZPOT_LBL.get(g['zpot'], 'moyen')}. Tu actives la Zone pendant un match, à partir du 2e quart-temps.")
                if st.button("🧘 S'entraîner à entrer dans la Zone", use_container_width=True, disabled=g["age"] < 14 or g["zone"] >= 3):
                    if g["pa"] <= 0:
                        st.toast("Plus d'actions !", icon="⏳")
                    elif g["mait"] < 40:
                        L(g, "🧘 Ta maîtrise est trop faible pour approcher la Zone.")
                        g["pa"] -= 1; st.rerun()
                    else:
                        g["pa"] -= 1
                        if random.random() < min(.95, (.6 + g["intel"] / 300) * g["zpot"]):
                            g["zxp"] += 1
                            r = ZONE_REQ[g["zone"] + 1]
                            if g["zxp"] >= r[0] and g["mait"] >= r[1] and g["age"] >= r[2]:
                                g["zone"] += 1
                                ap(g, {"mait": 5})
                                L(g, f"✨ Tu atteins le niveau : {ZONES[g['zone']]} !")
                            else:
                                L(g, "🧘 Tu approches de la Zone...")
                        else:
                            L(g, "😓 Impossible de te concentrer aujourd'hui.")
                        st.rerun()
                if g["age"] < 14:
                    st.caption("🔒 Entraînement de la Zone dès 14 ans.")
                st.divider()
                st.subheader("🏀 Match amical")
                opps = adversaires(g)
                if g["recrue"]:
                    st.caption(f"Tu ne peux pas affronter {GM[g['recrue']][0]} : c'est ton équipe.")
                opp = st.selectbox("Adversaire", opps)
                if st.button("▶️ Jouer le match" if g["age"] >= 12 else "🔒 Matchs dès 12 ans", use_container_width=True, disabled=g["age"] < 12):
                    if g["pa"] <= 0:
                        st.toast("Plus d'actions !", icon="⏳")
                    else:
                        g["pa"] -= 1
                        demarrer_match(g, opp)
                        st.rerun()

if PAGE == "🥊 Dojo":
    if PAGE == "🥊 Dojo":
        st.subheader("🥊 Dojo — sports de combat")
        st.caption("Chaque niveau : +3 puissance. Trois sports niveau 2 ou plus : bonus « Polyvalent » (+10). Dès 8 ans.")
        for n, ico in SPORTS.items():
            lvl = g["sports"].get(n, 0)
            cost = 40 * (lvl + 1)
            c1, c2 = st.columns([3, 1])
            c1.progress(lvl / 5, text=f"{ico} {n} — niveau {lvl}/5")
            if c2.button(f"{cost} 💴", key=f"sp{n}", disabled=g["age"] < 8 or lvl >= 5):
                if g["pa"] <= 0:
                    st.toast("Plus d'actions !", icon="⏳")
                elif g["argent"] < cost:
                    st.toast("Pas assez d'argent.", icon="💴")
                else:
                    g["pa"] -= 1; g["argent"] -= cost
                    if random.random() < max(.25, .85 - .12 * lvl):
                        g["sports"][n] = lvl + 1
                        ap(g, {"force": 2, "mait": 2})
                        L(g, f"{ico} Tu progresses en {n} (niveau {lvl + 1}) !")
                    else:
                        ap(g, {"sante": -2})
                        L(g, f"😓 Séance de {n} sans progrès.")
                    st.rerun()
        st.divider()
        if st.button("🏆 Tournoi clandestin (dès 14 ans)", use_container_width=True, disabled=g["age"] < 14):
            if g["pa"] <= 0:
                st.toast("Plus d'actions !", icon="⏳")
            else:
                g["pa"] -= 1
                tournoi(g)


if PAGE == "🏍️ Gang":
    if PAGE == "🏍️ Gang":
        gg = g["gang"]; m = mon_monde(g)
        if not gg:
            st.subheader("🏍️ Pas de gang")
            st.info("Rejoins un gang pour grimper les échelons, ou fonde le tien (14 ans, 20 de réputation, 300 💴).")
            for n, d in sorted(g["monde"].items(), key=lambda x: x[1]["force"]):
                c1, c2 = st.columns([3, 1])
                c1.write(f"**{n}** — force {d['force']} • {d['membres']} membres • {len(d['terr'])} territoire(s)")
                if c2.button("Rejoindre", key=f"gj{n}", disabled=g["age"] < 12):
                    if depenser(g):
                        anim(["🏍️", "🏍️💨", "🔥"])
                        if random.random() < proba(g, ["pw", d["force"] * .6]): rejoindre_gang(g, n)
                        else:
                            ap(g, {"sante": -8, "bonheur": -3}); L(g, f"💥 {n} te met à l'épreuve et te renvoie chez toi.")
                        st.rerun()
                    else: st.toast("Plus d'actions !", icon="⏳")
            st.divider()
            nm = st.text_input("Nom de ton futur gang", "Nouvelle Ère")
            if st.button("🏴 Fonder mon gang", use_container_width=True):
                err = fonder_gang(g, nm)
                if err: st.toast(err, icon="⚠️")
                else: st.rerun()
        else:
            ranks = UNIV["Tokyo Revengers"]["ranks"]
            st.subheader(f"🏍️ {gg['nom']} — {ranks[gg['rang']]}")
            c1, c2, c3 = st.columns(3)
            c1.metric("Force", m["force"]); c2.metric("Membres", m["membres"]); c3.metric("Territoires", len(m["terr"]))
            if not gg["chef"] and gg["rang"] < 4:
                nx = gg["rang"] + 1
                st.progress(min(1, gg["gxp"] / GRANG_TH[nx]), text=f"Points de gang : {gg['gxp']}/{GRANG_TH[nx]} • réputation requise : {GRANG_REP[nx]}")
            b = st.columns(2)
            if b[0].button("🛡️ Mission de gang", use_container_width=True):
                anim(["🏍️", "👊", "💨"]); err = mission_gang(g)
                if err: st.toast(err, icon="⏳")
                else: st.rerun()
            if b[1].button("🥊 Entraîner la troupe (60)", use_container_width=True):
                err = entrainer_gang(g)
                if err: st.toast(err, icon="⚠️")
                else: st.rerun()
            if b[0].button("📣 Recruter (80)", use_container_width=True):
                err = recruter_membres(g)
                if err: st.toast(err, icon="⚠️")
                else: st.rerun()
            if not gg["chef"]:
                if b[1].button("🎖️ Demander une promotion", use_container_width=True):
                    err = promotion(g)
                    if err: st.toast(err, icon="⚠️")
                    else: st.rerun()
                if gg["rang"] >= 4 and st.button("👑 Défier le chef pour prendre sa place", use_container_width=True):
                    anim(["👑", "⚔️", "💥"]); err = defier_chef(g)
                    if err: st.toast(err, icon="⚠️")
                    else: st.rerun()
            if st.button("🚪 Quitter le gang"):
                quitter_gang(g); st.rerun()
            st.divider()
            st.subheader("🗺️ Carte des territoires")
            own = {t: n for n, d in g["monde"].items() for t in d["terr"]}
            for t in g["libres"]: own[t] = "libre"
            st.caption("Prends des territoires (capitaine minimum, 14 ans). Les gangs sans territoire sont absorbés par le tien. Attaquer un allié est impossible.")
            for t in TERRS:
                o = own.get(t, "libre")
                c1, c2 = st.columns([3, 1])
                if o == gg["nom"]:
                    c1.write(f"✅ **{t}** — à toi")
                else:
                    c1.write(f"{'⬜' if o == 'libre' else '🚩'} **{t}** — {'libre' if o == 'libre' else o}")
                    allie = o != "libre" and g["fact"].get(o, {}).get("allie")
                    if c2.button("⚔️ Attaquer", key=f"at{t}", disabled=allie or (not gg["chef"] and gg["rang"] < 2) or g["age"] < 14):
                        anim(["🏍️💨", "👊💥", "🔥"])
                        err, res = attaquer_terr(g, o, t)
                        if err: st.toast(err, icon="⚠️")
                        else: st.rerun()

if PAGE == "🇺🇸 NBA":
    if PAGE == "🇺🇸 NBA":
        p = g["pro"]
        st.subheader(f"🇺🇸 {p['team']}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Saisons", p["saisons"]); c2.metric("Pts/match", p["ppg"]); c3.metric("Titres NBA", p["titres"])
        if p["retraite"]: st.info("🏁 Tu es à la retraite sportive.")
        if NBA_CUP:
            c = g["cup"]
            if g["match"]:
                ecran_match(g)
            else:
                st.info(f"🏆 {c['nom']} — {c['rounds'][c['i']]} contre les {c['opps'][c['i']]} ({c['i'] + 1}/{len(c['opps'])})")
                if st.button("▶️ Lancer le match", key="nba_go", use_container_width=True):
                    demarrer_match(g, c["opps"][c["i"]], True); st.rerun()
        else:
            if g["cal"].get("nba") and not p["retraite"]:
                if st.button("🏆 Jouer les playoffs NBA", use_container_width=True, type="primary"):
                    if depenser(g):
                        demarrer_cup(g, "nba"); st.rerun()
                    else: st.toast("Plus d'actions !", icon="⏳")
            else:
                st.caption("Les playoffs de l'année sont terminés (ou tu n'es plus en activité).")
            if st.button("🏋️ Camp d'entraînement privé (300)", key="nba_camp", use_container_width=True):
                if g["argent"] >= 300 and g["pa"] > 0:
                    g["argent"] -= 300; action(g, {"mait": 5, "force": 3, "sante": -3}, "🏋️ Camp d'entraînement privé : tu repousses tes limites.")
                else: st.toast("Il faut 300 💴 et une action.", icon="⚠️")
            if st.button("🤝 Négocier un meilleur contrat", key="nba_nego", use_container_width=True):
                if g["pa"] > 0:
                    g["pa"] -= 1
                    if random.random() < min(.85, .2 + g["rep"] / 150):
                        ap(g, {"argent": 800, "rep": 2}); L(g, "🤝 Ton agent obtient une prime de 800.")
                    else: L(g, "🙅 La franchise refuse de renégocier.")
                    st.rerun()
                else: st.toast("Plus d'actions !", icon="⏳")

if PAGE == "🛒 Boutique":
    st.subheader("🛒 Boutique")
    for k, (nm, pr, ds, eff, uu, ag) in SHOP.items():
        if uu and uu != g["u"]: continue
        c1, c2 = st.columns([3, 1])
        deja = k in ONCE_SHOP and k in g["achats"]
        c1.write(f"**{nm}** — {ds} *(dès {ag} ans)*" + (" ✅ possédé" if deja else ""))
        if c2.button(f"{pr} 💴", key=f"s{k}", disabled=g["age"] < ag or deja):
            resultat(acheter(g, k))
    st.caption(f"🎁 Cadeaux : {g['cadeau']} • ⏳ Time Leap : {g['revive']} • Les objets achetés vont dans ton 🎒 Inventaire.")

if PAGE == "⚰️ Cimetière":
    tab_cimetiere(prof)

if PAGE == "🏅 Site":
    s1, s2 = st.tabs(["🏅 Défis du site", "💎 Boutique de l'âme"])
    with s1: tab_defis_site(prof)
    with s2: tab_boutique_ame(prof)

if PAGE == "💾 Sauver":
    bloc_sauvegarde(prof, g, "jeu")


# ───────── Barre de navigation fixe (style BitLife) ─────────
st.markdown('<div style="height:130px"></div>', unsafe_allow_html=True)
with st.container(key="navbar"):
    nc = st.columns([1, 1, 1.25, 1, 1])
    for c_, (lab_, pg_, k_) in zip((nc[0], nc[1], nc[3], nc[4]), (("💼 Travail", "💼 Travail", "nav_w"), ("💰 Capital", "💰 Capital", "nav_c"),
                                                                ("❤️ Relations", "❤️ Relations", "nav_r"), ("⚽ Activités", "⚽ Activités", "nav_a"))):
        if c_.button(lab_, key=k_, use_container_width=True): go(pg_, reset=True)
    if nc[2].button("➕ Âge" if g["u"] != "Kuroko" else "➕ Trim.", key="nav_age", use_container_width=True):
        avancer(g)
        st.session_state["page"] = "📖 Vie"; st.session_state["hist"] = []
        st.rerun()
