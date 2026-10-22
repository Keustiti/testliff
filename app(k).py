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

EV.extend(EV_NEW)
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
    g["log"].append([g["age"], txt])
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
    return s.replace("{K}", k).replace("{V}", v or "ton village")


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
    if perks.get("don") and not her: ap(g, {"force": 20})
    if her and her.get("monde"):
        g["monde"], g["libres"] = her["monde"], her["libres"]
    else:
        monde_init(g)
    g["fact"] = {n: dict(rel=random.randint(10, 40), allie=False) for n in UNIV["Tokyo Revengers"]["fact"] if n in g["monde"]}
    L(g, f"🏠 {f[0]} : {f[1]}")


ZPOT_LBL = {.8: "faible", 1.0: "moyen", 1.25: "élevé"}


def new_game(nom, u, perks=None, her=None, ch=None):
    perks, ch = perks or {}, ch or {}
    g = dict(v=SAVE_V, nom=nom, u=u, age=0, sante=random.randint(70, 95), bonheur=random.randint(60, 80),
             intel=random.randint(10, 40), force=random.randint(5, 20), mait=random.randint(0, 5),
             chakra=random.randint(5, 25) if u == "Naruto" else 0, rep=0, argent=0, xp=0, pa=PA, cadeau=0, revive=0, wins=0,
             couple="", riche=random.randint(1, 3), nat={}, tech=[], defis_ok=[], dead=False, cause="",
             event=None, biju=None, log=[], pnj=[], karma=0, akatsuki=False, pupilles=[], zone=0, zxp=0, sports={}, talent=None,
             recrue="", gm={n: 0 for n in GM}, match=None, cup=None, cal={}, fact={}, beaute=random.randint(25, 70),
             fam=None, clan=None, village=None, nat_innee=[], oeil=None, enfants=[], arcs_done=[], flags=[],
             cap=1 if u == "Naruto" else 5, gang=None, monde=None, libres=[], pro=None, titres={}, lycee="", zpot=1.0,
             cool={}, lignee=(her or {}).get("lignee", 1), ancetres=(her or {}).get("anc", []), achats=[], captures=0, her_gang=None, _who=None)
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
    g["lycee"] = lyc
    f = g["fact"].get(lyc)
    if f and not f["allie"] and sum(x["allie"] for x in g["fact"].values()) < 3:
        f["allie"] = True
        f["rel"] = max(f["rel"], 60)
    ap(g, {"xp": 60, "rep": 10})
    L(g, f"🌟 {nom} te recrute dans le {lyc} !")


def donner_pupille(g, n):
    if n not in g["pupilles"]:
        g["pupilles"].append(n)
        L(g, f"✨ Pupille éveillée : {PUP[n][0]} {n} !")


def allier_auto(g):
    c = [n for n, f in g["fact"].items() if not f["allie"] and n != (g["gang"] or {}).get("nom")]
    if c and sum(f["allie"] for f in g["fact"].values()) < 3:
        n = random.choice(c)
        g["fact"][n]["allie"] = True; g["fact"][n]["rel"] = max(60, g["fact"][n]["rel"])
        L(g, f"🤝 Alliance conclue avec {n} !")


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
        elif k == "lycee":
            g["lycee"] = v; L(g, f"🏫 Tu intègres le {v}.")
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
            f = g["fact"].get(v)
            if f and f["allie"]:
                f["allie"] = False; f["rel"] = 0
                L(g, f"💔 L'alliance avec {v} est rompue.")
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
    if c == "biju": return bool(g["biju"])
    if c == "ally": return any(f["allie"] for f in g["fact"].values())
    return True


def arc_dispo(g):
    return [a for a in ARCS if a["u"] == g["u"] and a["a"][0] <= g["age"] <= a["a"][1] and (a.get("rep") or a["id"] not in g["arcs_done"])
            and g["cool"].get(a["id"], 0) <= g["age"] and a["cond"](g)]


def lancer_arc(g, aid):
    g["event"] = dict(arc=aid, step=0, ok=0)


def ev_courant(g):
    e = g["event"]
    if isinstance(e, int):
        ev = EV[e]
        return ev[3], ev[4], "ev"
    if "arc" in e:
        arc = ARC_BY_ID[e["arc"]]
        s = arc["steps"][e["step"]]
        return f"**{fmt(g, arc['nom'])}** — étape {e['step'] + 1}/{len(arc['steps'])}\n\n{fmt(g, s['t'])}", s["ch"], "arc"
    return e["t"], e["ch"], "dyn"


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
    if not o: return None
    return random.choices([x[1] for x in o], weights=[x[0] for x in o])[0]


def resoudre(g, ci):
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
                    L(g, f"📰 {k} prend {t} à {b}.")
                    if not g["monde"][b]["terr"] and b != gg["nom"]:
                        del g["monde"][b]; g["fact"].pop(b, None)
                        L(g, f"📰 {b} est anéanti.")
                break


def vieillir(g, quiet=False):
    g["age"] += 1
    g["pa"] = PA
    a = g["age"]
    g["match"] = None
    g["cup"] = None
    if g["u"] == "Kuroko":
        g["cal"] = {k: True for k, c in COMP.items() if c[1][0] <= a <= c[1][1] and (k != "nba" or g["pro"])}
        if a >= 13: g["cal"]["camp"] = True
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
    if g["u"] == "Tokyo Revengers": gang_annuel(g)
    if g["pro"]: saison_pro(g)
    if g["biju"] and g["biju"]["lien"] < 25 and random.random() < .15:
        ap(g, {"sante": -20, "rep": -10, "bonheur": -8})
        L(g, f"👹 {g['biju']['nom']} prend le contrôle ! Tu causes des dégâts autour de toi...")
    if len(g["log"]) > 500: g["log"] = g["log"][-400:]
    verifie_objectifs(g)
    if g["sante"] <= 0:
        mort(g, "Épuisement et blessures."); return
    if a > 60 and random.random() < (a - 60) / 100:
        mort(g, "Mort de vieillesse, entouré de souvenirs.", vieux=True); return
    if g["u"] == "Kuroko" and g["talent"] and not g["recrue"] and 13 <= a <= 18 and g["mait"] >= 45 and random.random() < .3:
        g["event"] = GM_EV; return
    if g["u"] == "Naruto" and not g["akatsuki"] and a >= 16 and g["karma"] <= -40 and random.random() < .5:
        g["event"] = AKAT_EV; return
    if g["u"] == "Naruto" and not g["biju"] and a >= 3 and random.random() < .025:
        g["event"] = BIJU_EV; return
    arcs = [x for x in arc_dispo(g) if random.random() < x["p"]]
    if arcs:
        lancer_arc(g, random.choice(arcs)["id"]); return
    if a >= 6 and random.random() < .22:
        d = ev_dyn(g)
        if d: g["event"] = d; return
    elig = [i for i, e in enumerate(EV) if ev_ok(g, e)]
    if elig and random.random() < .85:
        g["event"] = random.choice(elig)


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
    elif tac == "duo" and g["recrue"]:
        a += 12; g["gm"][g["recrue"]] = min(100, g["gm"][g["recrue"]] + 2); tag += f" 🌟Duo avec {g['recrue']}"
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
    g = new_game(e["nom"], p["u"], her=her)
    if p["u"] == "Naruto" and her["clan"] is None: g["fam"] = dict(nom=p["fam"]["nom"], type="Famille de villageois", d="Une famille ordinaire de ton village.")
    if gg and gg["chef"]:
        g["her_gang"] = dict(nom=gg["nom"], rang=5, gxp=0, chef=True)
    for _ in range(age): vieillir(g, quiet=True)
    if g["u"] == "Naruto": g["cap"] = 1 if age < 14 else 2 if age < 22 else 3
    g["xp"] = max(g["xp"], age * 6 + (RANK_TH[g["cap"]] if g["u"] == "Naruto" and age >= 12 else 0))
    if g["u"] == "Kuroko" and age >= 15 and not g["lycee"]:
        g["lycee"] = random.choice(list(LYCEES_SEL))
    g["log"] = [[age, f"🕯️ Tu reprends le flambeau de {her['anc'][-1]}, à {age} ans. L'héritage de ta famille te précède."]]
    g["pa"] = PA
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
        if f not in fl: fl.append(f)


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
                pro=None, titres={}, lycee="", zpot=1.0, cool={}, lignee=1, ancetres=[], achats=[], captures=0, her_gang=None, match=None, cup=None, cal={})


def migrer(g):
    import copy
    for k, v in DEFAULTS.items(): g.setdefault(k, copy.deepcopy(v))
    g.setdefault("beaute", random.randint(25, 70))
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
                for a, t in f.get("log", []):
                    st.write(f"**{a}** — {t}")


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
            st.session_state.g = new_game(nom or "Anonyme", u, perks=perks, ch=ch)
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
st.title(f"{U['icon']} {nom_complet(g)} — {g['age']} an{'s' if g['age'] > 1 else ''}")
st.markdown(f'<div class="scene"><span class="sprite s-{U["cls"]}">{U["icon"]}</span></div>', unsafe_allow_html=True)
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
if g["lignee"] > 1: bj += f" • 🕯️ Génération {g['lignee']}"
st.caption(f"{stage(g)} • {g['u']} • **{rn}**{bj} • 💴 {g['argent']} {U['monnaie']} • XP {g['xp']} • Actions : {g['pa']}/{PA} • 💎 {prof['gems']}")
cols = st.columns(2)
for i, (k, lab) in enumerate([x for x in STATS if x[0] != "chakra" or g["u"] == "Naruto"]):
    cols[i % 2].progress(g[k] / 100, text=f"{lab} : {g[k]}")
st.progress((g["karma"] + 100) / 200, text=f"☯️ Karma : {g['karma']} ({karma_label(g['karma'])})")

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
        for a, t in reversed(g["log"][-60:]):
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
    if g["recrue"]:
        if b[1].button(f"🌟 Duo avec {g['recrue']}", use_container_width=True): tac = "duo"
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
NBA_CUP = bool(g["cup"] and g["cup"]["key"] == "nba")
names = (["📖 Vie", "🎯 Objectif", "🏋️ Actions", "👥 Liens", "👪 Famille", "🌀 Techniques"]
         + (["🏯 Village & clan", "🦊 Bijū"] if g["u"] == "Naruto" else []) + (["🌑 Akatsuki"] if g["akatsuki"] else [])
         + (["🏟️ Matchs", "⭐ Miracles"] if g["u"] == "Kuroko" else []) + (["🇺🇸 NBA"] if g["pro"] else [])
         + (["🏍️ Gang", "🥊 Dojo"] if g["u"] == "Tokyo Revengers" else [])
         + ["🤝 Alliances", "🛒 Boutique", "⚰️ Cimetière", "🏅 Site", "💾 Sauver"])
T = dict(zip(names, st.tabs(names)))

with T["📖 Vie"]:
    if st.button("⏩ Vieillir d'un an", type="primary", use_container_width=True):
        vieillir(g)
        st.rerun()
    cur = None
    for a, t in reversed(g["log"][-40:]):
        if a != cur:
            st.markdown(f"**Âge {a}**"); cur = a
        st.write(t)

with T["🎯 Objectif"]:
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
    ops = [a for a in arc_dispo(g) if a.get("man")]
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

with T["🏋️ Actions"]:
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


with T["👥 Liens"]:
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
                        anim(["⚔️", "💥", "⚔️💥"]); duel(g, p["niv"], p["nom"]); st.rerun()
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

with T["👪 Famille"]:
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


def req_info(g, r):
    t = r[0]
    if t == "nat": return g["nat"].get(r[1], 0) >= r[2], f"{NAT[r[1]]} {r[1]} niv. {r[2]}"
    if t == "pup": return r[1] in g["pupilles"], f"pupille {r[1]}"
    if t == "clan": return g.get("clan") == r[1], f"clan {r[1]}"
    if t == "talent": return bool(g["talent"] and g["talent"]["k"] == r[1]), f"talent {TALENTS[r[1]][0]}"
    return g.get(t, 0) >= r[1], f"{t} ≥ {r[1]}"


with T["🌀 Techniques"]:
    if g["u"] == "Naruto":
        st.subheader("🌀 Natures de chakra")
        if g["nat"]:
            for n, l in g["nat"].items(): st.write(f"{NAT[n]} **{n}** — niveau {l}/5")
        else: st.write("Aucune nature éveillée pour l'instant (éveil à 6 ans).")
        if g["oeil"]: st.write(f"👁️ Pupille héréditaire : {PUP[g['oeil'][0]][0]} {g['oeil'][0]} (éveil à {g['oeil'][1]} ans)")
        st.caption("Tu ne peux apprendre que les techniques de ta voie : ta nature, ton clan, tes pupilles. Fusion à 15 ans : Eau+Vent → Glace, Terre+Eau → Bois, Feu+Terre → Lave (niv. 3 chacune).")
    st.subheader("⚔️ Techniques")
    hors = []
    for k, t in TECH.items():
        if t["u"] != g["u"]: continue
        r = t["req"]
        ok, req_txt = req_info(g, r)
        voie = ok or r[0] in ("mait", "force", "rep", "zone") or (r[0] == "nat" and r[1] in g["nat"])
        if k in g["tech"]:
            st.success(f"✅ {t['n']} (puissance +{t['pw']})")
        elif not voie:
            hors.append((t, req_txt))
        else:
            c1, c2 = st.columns([3, 1])
            c1.write(f"**{t['n']}** — +{t['pw']} puissance — dès {t['a']} ans — requis : {req_txt} — {t['p']} 💴")
            if c2.button("Apprendre", key=f"t{k}", disabled=not ok or g["age"] < t["a"]):
                if g["argent"] >= t["p"]:
                    g["argent"] -= t["p"]; g["tech"].append(k)
                    L(g, f"📖 Technique apprise : {t['n']} !"); st.rerun()
                else: st.toast("Pas assez d'argent.", icon="💴")
    if hors:
        with st.expander(f"🔒 Hors de ta voie ({len(hors)})"):
            for t, rt in hors: st.write(f"{t['n']} — requis : {rt}")
    st.metric("Puissance totale", int(puissance(g)))

if "🏯 Village & clan" in T:
    with T["🏯 Village & clan"]:
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

if "🦊 Bijū" in T:
    with T["🦊 Bijū"]:
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

if "🌑 Akatsuki" in T:
    with T["🌑 Akatsuki"]:
        st.subheader("🌑 Akatsuki")
        st.caption("Tu es un déserteur : ton village te traque, mais l'organisation t'offre des missions sombres.")
        if g["pupilles"]:
            st.write("👁️ Pupilles volées : " + ", ".join(f"{PUP[n][0]} {n}" for n in g["pupilles"]))
        restantes = [n for n in PUP if n not in g["pupilles"]]
        if restantes:
            cible = st.selectbox("Pupille à voler", restantes, format_func=lambda n: f"{PUP[n][0]} {n} (difficulté {PUP[n][1]})")
            pch = int(100 * min(.9, max(.15, puissance(g) / PUP[cible][1] * .6)))
            st.caption(f"Chances de succès estimées : {pch}%")
            if st.button("👁️ Voler la pupille", use_container_width=True):
                if g["pa"] <= 0:
                    st.toast("Plus d'actions !", icon="⏳")
                else:
                    g["pa"] -= 1
                    if random.random() < pch / 100:
                        g["pupilles"].append(cible)
                        ap(g, {"karma": -15, "xp": 40, "rep": -3})
                        L(g, f"👁️ Tu voles le {cible} ! Ta puissance grandit.")
                    else:
                        ap(g, {"sante": -30, "karma": -5})
                        L(g, f"💢 Tu échoues à voler le {cible} et tu es gravement blessé.")
                        if g["sante"] <= 0:
                            mort(g, "Tué en tentant de voler une pupille.")
                    st.rerun()
        else:
            st.success("Tu possèdes toutes les pupilles légendaires.")
        if st.button("🦊 Traquer un jinchūriki", use_container_width=True):
            if g["pa"] <= 0:
                st.toast("Plus d'actions !", icon="⏳")
            else:
                g["pa"] -= 1
                if random.random() < min(.85, max(.15, puissance(g) / 150)):
                    ap(g, {"argent": 300, "xp": 50, "karma": -20})
                    L(g, "🦊 Tu captures un jinchūriki pour l'organisation. Récompense : 300.")
                else:
                    ap(g, {"sante": -30, "karma": -5})
                    L(g, "💢 Le jinchūriki te repousse violemment.")
                    if g["sante"] <= 0:
                        mort(g, "Tué par un jinchūriki.")
                st.rerun()
        k1, k2 = st.columns(2)
        if k1.button("🎭 Kidnapper un ninja", use_container_width=True):
            if depenser(g):
                anim(["🌑", "🥷", "😶‍🌫️"])
                if random.random() < min(.8, max(.2, puissance(g) / 200)):
                    ap(g, {"argent": 200, "xp": 35, "karma": -15}); g["captures"] += 1
                    L(g, "🎭 Tu kidnappes un ninja pour l'organisation. Récompense : 200.")
                else:
                    ap(g, {"sante": -20, "karma": -5}); L(g, "💢 Ta cible t'échappe et te blesse.")
                    if g["sante"] <= 0: mort(g, "Tué lors d'un enlèvement.")
                st.rerun()
            else: st.toast("Plus d'actions !", icon="⏳")
        if k2.button("🗡️ Tuer un hôte de bijū", use_container_width=True):
            if depenser(g):
                anim(["🌑", "🗡️", "💀"])
                if random.random() < min(.7, max(.1, puissance(g) / 260)):
                    ap(g, {"argent": 500, "xp": 80, "karma": -25, "rep": -5}); g["captures"] += 1
                    L(g, "🗡️ Tu élimines un jinchūriki : l'organisation te félicite.")
                else:
                    ap(g, {"sante": -35, "karma": -8}); L(g, "💢 Le bijū se déchaîne : tu t'en sors à peine.")
                    if g["sante"] <= 0: mort(g, "Dévoré par le chakra d'un bijū.")
                st.rerun()
            else: st.toast("Plus d'actions !", icon="⏳")
        if st.button("🚪 Quitter l'organisation", use_container_width=True):
            if random.random() < .5:
                g["akatsuki"] = False
                ap(g, {"karma": 10})
                L(g, "🚪 Tu réussis à quitter l'Akatsuki.")
            else:
                ap(g, {"sante": -40})
                L(g, "🔪 L'organisation te punit pour ta tentative de fuite.")
                if g["sante"] <= 0:
                    mort(g, "Éliminé par l'Akatsuki pour trahison.")
            st.rerun()

if "⭐ Miracles" in T:
    with T["⭐ Miracles"]:
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

with T["🤝 Alliances"]:
    nal = sum(f["allie"] for f in g["fact"].values())
    st.subheader(f"🤝 Alliances ({nal}/3)")
    st.caption("Chaque allié : +7 puissance, +XP, +réputation et +argent chaque année. Un karma très bas fait fuir tes alliés.")
    for n, f in g["fact"].items():
        if n == (g["gang"] or {}).get("nom"): continue
        with st.expander(f"{'🤝' if f['allie'] else '⚔️'} {n} — relation {f['rel']}"):
            st.progress(f["rel"] / 100)
            c1, c2 = st.columns(2)
            if c1.button("🎁 Offrir un tribut (80)", key=f"tr{n}", disabled=g["age"] < 10):
                if g["argent"] >= 80 and g["pa"] > 0:
                    g["argent"] -= 80; g["pa"] -= 1; f["rel"] = min(100, f["rel"] + 12)
                    L(g, f"🎁 {n} apprécie ton tribut."); st.rerun()
                else:
                    st.toast("Il faut 80 d'argent et une action.", icon="💴")
            if not f["allie"]:
                cout = 100 * (nal + 1)
                pa_ = int(100 * min(.9, f["rel"] / 100 * .8 + g["rep"] / 250))
                c2.caption(f"Coût {cout} • chances {pa_}%")
                if c2.button("📜 Proposer une alliance", key=f"al{n}", disabled=g["age"] < 12 or nal >= 3):
                    if g["argent"] < cout or g["pa"] <= 0:
                        st.toast("Argent ou action insuffisant.", icon="💴")
                    else:
                        g["argent"] -= cout; g["pa"] -= 1
                        if random.random() < pa_ / 100:
                            f["allie"] = True; ap(g, {"rep": 5})
                            L(g, f"🤝 Alliance conclue avec {n} !")
                        else:
                            f["rel"] = max(0, f["rel"] - 5)
                            L(g, f"🙅 {n} refuse ton alliance.")
                        st.rerun()
            elif c2.button("🗡️ Trahir cet allié", key=f"bt{n}"):
                f["allie"] = False; f["rel"] = 0
                ap(g, {"karma": -20, "argent": 200, "rep": -10})
                L(g, f"🗡️ Tu trahis {n} et pille leurs ressources.")
                st.rerun()

if "🏟️ Matchs" in T:
    with T["🏟️ Matchs"]:
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
                st.subheader("📅 Calendrier de l'année")
                shown = False
                for key, (nom, (a0, a1), rounds, rew) in COMP.items():
                    if key == "nba": continue
                    if g["age"] < a0:
                        st.write(f"🔒 {nom} — dès {a0} ans")
                    elif g["age"] <= a1:
                        shown = True
                        dispo = g["cal"].get(key)
                        c1, c2 = st.columns([3, 1])
                        c1.write(f"{'🟢' if dispo else '✅'} **{nom}** — {len(rounds)} tours — récompense : {rew}")
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

if "🥊 Dojo" in T:
    with T["🥊 Dojo"]:
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


if "🏍️ Gang" in T:
    with T["🏍️ Gang"]:
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

if "🇺🇸 NBA" in T:
    with T["🇺🇸 NBA"]:
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

with T["🛒 Boutique"]:
    st.subheader("🛒 Boutique")
    for k, (nm, pr, ds, eff, uu, ag) in SHOP.items():
        if uu and uu != g["u"]: continue
        c1, c2 = st.columns([3, 1])
        deja = k in ONCE_SHOP and k in g["achats"]
        c1.write(f"**{nm}** — {ds} *(dès {ag} ans)*" + (" ✅ possédé" if deja else ""))
        if c2.button(f"{pr} 💴", key=f"s{k}", disabled=g["age"] < ag or deja):
            if g["argent"] >= pr:
                g["argent"] -= pr
                ap(g, eff)
                if k in ONCE_SHOP: g["achats"].append(k)
                L(g, f"🛍️ Achat : {nm}")
                st.rerun()
            else: st.toast("Pas assez d'argent.", icon="💴")
    st.caption(f"🎁 Cadeaux : {g['cadeau']} • ⏳ Time Leap : {g['revive']}")

with T["⚰️ Cimetière"]:
    tab_cimetiere(prof)

with T["🏅 Site"]:
    s1, s2 = st.tabs(["🏅 Défis du site", "💎 Boutique de l'âme"])
    with s1: tab_defis_site(prof)
    with s2: tab_boutique_ame(prof)

with T["💾 Sauver"]:
    bloc_sauvegarde(prof, g, "jeu")
    if st.button("🗑️ Abandonner cette vie (elle ira au cimetière)"):
        g["dead"] = True; g["cause"] = "A abandonné sa vie."
        st.rerun()
