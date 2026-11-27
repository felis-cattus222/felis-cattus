#!/usr/bin/env python3
# Felis cattus affiliate site - static generator (MVP)
# Product data source of truth: ~/workspace/felis_cattus/ad_list.md etc.
# This script holds a curated subset for the MVP pages.
import os, html, urllib.parse

OUT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://felis-cattus222.github.io/felis-cattus/"

def rsearch(query):
    # Plain Rakuten search link (NOT an affiliate link).
    # Rakuten affiliate (hb.afl) links will replace these once issued.
    return "https://search.rakuten.co.jp/search/mall/" + urllib.parse.quote(query) + "/"

NAV = [
    ("index.html", "トップ"),
    ("map.html", "12星座×身体マップ"),
    ("books.html", "学ぶ"),
    ("aroma.html", "香る"),
    ("goods.html", "整える"),
    ("cats.html", "猫と暮らす"),
    ("shop.html", "鑑定・商品"),
    ("about.html", "Felis cattusについて"),
]

GOOGLE_VERIFY = "t9t3j8rCoSz4DWg8ylktuEGbVX-RqLjXez0lJ0F6ABY"  # Search Console verification (issued 2026-11-16)

def page(title, desc, body, fname, pr=False):
    nav = "\n".join(f'<a href="{h}">{t}</a>' for h, t in NAV)
    pr_note = '<p class="pr">PR：このページにはアフィリエイトリンク（広告）が含まれます。</p>' if pr else ""
    url = BASE if fname == "index.html" else BASE + fname
    verify = f'\n<meta name="google-site-verification" content="{GOOGLE_VERIFY}">' if GOOGLE_VERIFY else ""
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "name": "Felis cattus｜エナジー・ゾディアック", "url": BASE},
            {"@type": "Person", "name": "平賀建人", "jobTitle": ["鍼灸師", "登録販売者", "パーソナルトレーナー"],
             "description": "臨床30年のセラピスト。独自メソッド「エナジー・ゾディアック」提唱者。"},
            {"@type": "WebPage", "name": title, "description": desc, "url": url, "isPartOf": {"@type": "WebSite", "url": BASE}},
        ],
    }
    import json as _json
    ld_json = _json.dumps(ld, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}｜Felis cattus</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">{verify}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Felis cattus｜エナジー・ゾディアック">
<meta property="og:title" content="{html.escape(title)}｜Felis cattus">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}logo.png">
<meta name="twitter:card" content="summary">
<script type="application/ld+json">{ld_json}</script>
<link rel="icon" href="favicon.ico">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="sister-bar"><span class="sister-label">姉妹サイト</span><a href="https://felis-cattus222.github.io/beauty-site/">美容の道具箱</a><a href="https://felis-cattus222.github.io/felis-cattus/">Felis cattus</a><a href="https://tomyree-source.github.io/sites/fashion/">POSTURE &amp; STYLE</a><a href="https://tomyree-source.github.io/sites/yoga/">Simple Yoga Life</a><a href="https://tomyree-source.github.io/sites/belly-dance/">ベリーダンス手帖</a><a href="https://tomyree-source.github.io/sites/aroma-notes/">アロマと休息の手帖</a></div>
<header>
<div class="brand"><a href="index.html"><img class="logo" src="logo.png" alt="Felis cattus ロゴ（黒猫と白猫）"><span class="brand-text">Felis cattus｜エナジー・ゾディアック<span class="brand-sub">星と身体の道具箱</span></span></a></div>
<nav>{nav}</nav>
</header>
<main>
{pr_note}
{body}
</main>
<footer>
<p>当サイトの一部リンクは、楽天アフィリエイト等の広告リンクです。リンク先で購入された場合、当サイトが紹介料を受け取ることがあります。</p>
<p><a href="disclosure.html">アフィリエイト開示・プライバシー</a> ／ お問い合わせ：felis.cattus222@gmail.com</p>
<p>星読みは自己理解のための読み物です。身体の対応は各体系の伝統とFelis cattusのメソッドに基づくもので、医療の診断・治療の根拠ではありません。</p>
<p>© Felis cattus</p>
</footer>
</body>
</html>
"""

def card(title, text, url, label="楽天で探す", sponsored=False, img=None, alt=""):
    rel = "sponsored nofollow noopener" if sponsored else "noopener"
    img_html = f'<a class="card-img" href="{url}" target="_blank" rel="{rel}"><img src="{img}" alt="{html.escape(alt)}" loading="lazy"></a>' if img else ""
    return f"""<div class="card">
{img_html}<h3>{html.escape(title)}</h3>
<p>{html.escape(text)}</p>
<p><a class="btn" href="{url}" target="_blank" rel="{rel}">{label}</a></p>
</div>"""

def cards(items):
    return '<div class="grid">\n' + "\n".join(items) + "\n</div>"

def cards_img(items):
    return '<div class="grid cards-img">\n' + "\n".join(items) + "\n</div>"

# ---------- 12 signs (master_correspondence.md, ch.2 flow order canonical) ----------
SIGNS = [
    # sign, dates, body, meridian, organ, emotion, selfcare
    ("牡羊座", "3/21–4/19", "頭部・脳・顔面", "手の太陰肺経（呼吸・境界）", "肺", "悲・憂（肺の五志・伝統対応）", "百会と湧泉の垂直軸。天地を貫く柱を意識し、呼吸を通す"),
    ("牡牛座", "4/20–5/20", "喉・頸部・甲状腺", "手の陽明大腸経（純化）", "大腸", "悲・憂（表裏の肺を介した接続）", "足裏全体の接地。大地に根ざし、不要な執着を地へ流す"),
    ("双子座", "5/21–6/21", "肩・腕・手・肺", "足の陽明胃経（情報の摂取）", "胃", "思（表裏の脾を介した接続）", "拇指球の踏み込み。世界を咀嚼する前進の力"),
    ("蟹座", "6/22–7/22", "胸部・胃・乳房", "足の太陰脾経（滋養・安心）", "脾", "思（脾の五志・伝統対応）", "土踏まずの柔軟性。内なる聖域を守り、大地のぬくもりで基盤を安定させる"),
    ("獅子座", "7/23–8/22", "心臓・背中・脊柱", "手の少陰心経（魂の喜び）", "心", "喜（心の五志・伝統対応）", "踵（かかと）の安定。自己の核を支える不動の軸"),
    ("乙女座", "8/23–9/22", "腹部・腸・消化器系", "手の太陽小腸経（秩序）", "小腸", "喜（表裏の心を介した接続）", "足裏の外側エッジ。清濁を分ける境界線を意識し、必要なものだけを識別する"),
    ("天秤座", "9/23–10/23", "腰部・腎臓・バランス感覚", "足の太陽膀胱経（均衡）", "膀胱", "恐・驚（表裏の腎を介した接続）", "左右の足重心の均等化。自分と世界の均衡点を見出す"),
    ("蠍座", "10/24–11/22", "生殖器・排泄器官・骨盤底", "足の少陰腎経（変容・意志）", "腎", "恐・驚（腎の五志・伝統対応）", "湧泉の吸気。大地の深淵から意志を汲み上げる"),
    ("射手座", "11/23–12/21", "臀部・大腿部（太もも）・肝臓", "手の厥陰心包経（境界）", "心包", "—（心包には五志の単独対応がないため、対応は置いていません）", "足首の解放と回転。理想へ跳躍するための自由な支点"),
    ("山羊座", "12/22–1/19", "膝・骨格全体・皮膚", "手の少陽三焦経（連動）", "三焦", "—（三焦には五志の単独対応がないため、対応は置いていません）", "膝の柔軟なクッション。社会の重圧を膝を通じて地に逃がす"),
    ("水瓶座", "1/20–2/18", "下腿・足首・循環器系", "足の少陽胆経（変革・決断）", "胆", "怒（表裏の肝を介した接続）", "足の外側のライン。既存の枠を突破する踏ん張り"),
    ("魚座", "2/19–3/20", "足・足裏・リンパ系", "足の厥陰肝経（統合・再生）", "肝", "怒（肝の五志・伝統対応）", "足指の完全な解放。すべてを大地（海）へ還す統合"),
]

# ---------- index ----------
SLUGS = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]
sign_links = "\n".join(
    f'<a class="sign" href="sign-{SLUGS[i]}.html">{s[0]}<span>{s[1]}</span></a>' for i, s in enumerate(SIGNS))
index_body = f"""
<section class="hero">
<div class="hero-visual"><img src="top-hero.webp" alt="星空の下、金のホロスコープの環と月を背景に座る黒猫と白猫"><div class="hero-visual-text"><h1>明日の星を、身体で読む。</h1></div></div>
<p class="statement">エナジー・ゾディアックは、12星座と身体・経絡・感情の対応を読み解く、Felis cattus の独自メソッドです。提唱者は臨床30年の鍼灸師。星の位置はNASA JPLの天文暦（DE421）で計算し、毎日の記事は公開前に、日付・曜日・月のサイン・天文イベントを全件照合しています。裏付けのない対応は作りません。</p>
<p>このサイトは、そのメソッドの入口です。毎日の星読みは <a href="https://note.com/felis_cattus">note「Felis cattus」</a> で毎夕更新しています。</p>
</section>
<h2>はじめ方｜3つのステップ</h2>
{cards_img([
    card("STEP 1｜毎日の星読みを読む", "明日のチャートと身体のテーマを、毎夕noteで無料配信。まず流れをつかむところから。", "https://note.com/felis_cattus", "noteで読む", img="top-step-note.webp", alt="星空の下で開いた星読みの書物を見る黒猫と白猫"),
    card("STEP 2｜自分の星座の身体マップを知る", "あなたの星座は、身体のどこ・どの経絡・どんな感情と対応しているのか。メソッドの中心にある対応表です。", "map.html", "マップを見る", img="top-step-map.webp", alt="金の光の線と星座記号に包まれた猫のシルエット"),
    card("STEP 3｜自分専用の鑑定書を注文する", "出生図と2027年の流れを読む、あなただけの鑑定書（A4・8ページ）。", "shop.html", "鑑定・商品を見る", img="top-step-shop.webp", alt="金のリボンの巻物のそばに座る黒猫と白猫"),
])}
<h2>読みの実例｜週間星読み新聞より</h2>
<p>毎週日曜のnoteでは、その週の星の流れを振り返る「週間星読み新聞」を出しています。11月9日〜15日の回（新月と、水星・金星の順行が重なった週）から、読みの一部を紹介します。</p>
<blockquote class="sample-read">明日は「内に深く潜る力」と「外へ大きく動く力」が同時に強い日です。蠍座の太陽と水星は、ひとつのことを掘り下げる集中力を示します。獅子座の火星と木星の重なりは、その掘り下げたものを外へ表現する勢いを添えます。ただ、勢いが前のめりになりやすいところも。無理に一気に進めようとせず、明日は「掘り下げたものを、ひとつだけ形にする」くらいのペースがちょうどよさそうです。</blockquote>
<p><a class="btn" href="https://note.com/felis_cattus/n/n728ecaca3a2d">週間星読み新聞を読む（note）</a></p>
<h2>まず自分の星座から</h2>
<div class="signs">{sign_links}</div>
<h2>カテゴリ</h2>
{cards_img([
    card("学ぶ｜本の道具箱", "占星術・経絡・身体構造。メソッドの土台になった本と、現場で使われる専門書。", "books.html", "ページを開く", img="top-books.webp", alt="古い本の積み重ねと眼鏡、そばに座る猫"),
    card("香る｜星座とアロマ", "12星座×アロマ対応表の無料要約との精油リンク。", "aroma.html", "ページを開く", img="top-aroma.webp", alt="月明かりの下のアロマボトルとハーブ、黒猫と白猫"),
    card("整える｜月と星の道具", "プラネタリウム、月ライト、猫と星の雑貨。夜の星読み時間のお供に。", "goods.html", "ページを開く", img="top-goods.webp", alt="光るムーンランプと壁に映る星を見上げる猫"),
    card("猫と暮らす", "楽天のペット用品と、222キャラ工房のLINEスタンプ。", "cats.html", "ページを開く", img="top-cats.webp", alt="ペット用品のある室内でくつろぐ黒猫と白猫"),
])}
<h2>Felis cattus の商品（noteで販売中）</h2>
{cards_img([
    card("2027年 年間読み 鑑定書（受注生産）", "あなたの出生図と2027年のトランジットを読む、A4・8ページの鑑定書。月10名まで、¥2,222。", "https://note.com/felis_cattus/n/nf3da15ac7ff5", "noteで注文する", img="top-step-shop.webp", alt="金のリボンの巻物のそばに座る黒猫と白猫"),
    card("12星座×アロマ対応表", "7つの資料を突き合わせた対応表の有料記事。¥222。無料要約は「香る」のページに。", "aroma.html", "まず無料要約を読む", img="top-aroma.webp", alt="月明かりの下のアロマボトルとハーブ、黒猫と白猫"),
    card("月相×アロマ対応表", "月の満ち欠け8段階で選ぶ香りの対応表。¥222。「12星座×アロマ対応表」と対になる記事。", "https://note.com/felis_cattus/n/n0c1126c25c9a", "noteで見る", img="top-moon.webp", alt="空に弧を描く月の満ち欠けと、見上げる黒猫と白猫"),
])}
"""
write = lambda name, content: open(os.path.join(OUT, name), "w", encoding="utf-8").write(content)
write("index.html", page("エナジー・ゾディアック｜12星座×身体マップと毎日の星読み", "臨床30年の鍼灸師が提唱する独自メソッド「エナジー・ゾディアック」の公式サイト。12星座と身体部位・経絡・感情の対応表、毎日の星読み（note）、星座別アロマ、年間読み鑑定書¥2,222まで。星の位置はNASA JPLの天文暦で検証しています。", index_body, "index.html"))

# ---------- map ----------
rows = "\n".join(
    f'<div class="card sign-card" id="{s[0]}"><h3>{s[0]} <span>{s[1]}</span></h3>'
    f"<p><strong>身体</strong>：{s[2]}</p><p><strong>経絡</strong>：{s[3]}</p>"
    f"<p><strong>臓腑</strong>：{s[4]}</p><p><strong>感情（情志）</strong>：{s[5]}</p>"
    f"<p><strong>セルフケア</strong>：{s[6]}</p>"
    f'<p><a href="sign-{SLUGS[i]}.html">{s[0]}の詳しい読み →</a></p></div>' for i, s in enumerate(SIGNS))
map_body = f"""
<h1>12星座×身体マップ｜対応表</h1>
<p>エナジー・ゾディアックの中心にある対応表です。12星座それぞれに、身体部位・担当経絡・五臓六腑・感情（情志）・セルフケアを対応させています。身体部位は連載「解体新書」第4回、経絡は連載「星と巡る身体の地図」第2章の流注順（肺経から始まる気の巡りの順）を正本としています。感情（情志）は『黄帝内経』以来の伝統対応で、経絡の表裏を介した接続の場合はその旨を添えています。裏付けのない対応は作らず、空欄のままにしています。</p>
<h2>この対応表の読み方</h2>
<p>5つの欄は、それぞれ別の体系から来ています。<strong>身体部位</strong>は、西洋占星術に古くから伝わる身体対応（メロテシア）の伝統です。<strong>経絡</strong>は中医学の十二経絡で、星座の順番に気の巡りの順（流注順）を重ねています。<strong>臓腑</strong>は、その経絡が属する五臓六腑です。<strong>感情（情志）</strong>は、五臓に結びつくとされてきた感情の伝統対応で、経絡の表裏ペアを介してつながる場合は「表裏を介した接続」と明記しています。<strong>セルフケア</strong>は、その星座のテーマに沿った、足と呼吸を中心とした小さな実践です。星座名をタップすると、その星座だけを詳しく読むページに進めます。</p>
<h2>経絡は「流注順」が正本です</h2>
<p>経絡の対応は、肺経から始まって大腸経・胃経・脾経・心経・小腸経・膀胱経・腎経・心包経・三焦経・胆経・肝経と巡る「流注順」に統一しています。これは中医学で気の流れが一周する順番そのもので、牡羊座に肺経が来るのは「一日の気は肺から始まる」という伝統の考え方に基づきます。初期の記事には別の割り当てが混ざっていた時期がありましたが、現在はこの流注順を正本として、すべての記事と鑑定書を統一しています。</p>
<div class="grid">{rows}</div>
<h2>五臓六腑と感情（情志）について</h2>
<p>中医学の伝統では、五臓には感情が結びつくとされてきました。肝は怒、心は喜、脾は思、肺は悲・憂、腎は恐・驚です。この表では、星座の担当経絡が属する臓腑の情志を基本とし、経絡の表裏ペア（たとえば大腸経と肺経）を介してつながる場合は、その旨を添えて書いています。心包と三焦には五志の単独対応がないため、射手座と山羊座の情志欄は空欄のままにしています。伝統にない対応を、もっともらしく作ることはしません。これらは伝統的な考え方の紹介であり、医療の診断や治療の根拠ではありません。</p>
<h2>エレメントで見る4つのグループ</h2>
<p><strong>火の星座（牡羊座・獅子座・射手座）</strong>は、頭・心臓・大腿部と、始める力・燃える力に対応します。経絡では肺経・心経・心包経が担い、身体の「点火」と循環の中心です。<strong>地の星座（牡牛座・乙女座・山羊座）</strong>は、喉・腸・膝と、受け止めて形にする力に対応します。大腸経・小腸経・三焦経が担い、消化と構造のグループです。<strong>風の星座（双子座・天秤座・水瓶座）</strong>は、肩と腕・腰・下腿と、巡らせて伝える力に対応します。胃経・膀胱経・胆経が担い、流れとバランスのグループです。<strong>水の星座（蟹座・蠍座・魚座）</strong>は、胸と胃・骨盤底・足裏と、蓄えて深める力に対応します。脾経・腎経・肝経が担い、滋養と再生のグループです。</p>
<h2>連載で読む</h2>
<p>この対応表は、noteの連載「星と巡る身体の地図」で1星座ずつ章を重ねて解説しています。目次と各章へのリンクは <a href="https://note.com/felis_cattus/n/na1ab441528d1">「12のライン身体マップ図鑑｜目次」</a> にまとめています。対応表の成り立ちを解説した第2章「12のラインの対応」も、そこから読めます。</p>
<p>この対応をあなたの出生図で読むのが、年間読み鑑定書です。詳しくは <a href="shop.html">鑑定・商品</a> のページへ。</p>
"""
write("map.html", page("12星座×身体マップ対応表｜星座別の身体部位・経絡・五臓六腑と感情", "12星座それぞれの身体部位・担当経絡・五臓六腑・感情（情志）・セルフケアをまとめた対応表。経絡は流注順が正本、裏付けのない対応は作らない——エナジー・ゾディアックの中心素材を全公開しています。", map_body, "map.html"))

# ---------- books ----------
books = [
    ("鏡リュウジの占星術の教科書I 第2版：自分を知る編", "ホロスコープ基礎の土台に。毎日の読みの出発点。", "4562072563"),
    ("鏡リュウジの占星術の教科書II 第2版：相性と未来を知る編", "トランジットと相性の読みに。年間読みの下支え。", "4562073829"),
    ("鏡リュウジの占星術の教科書III：深く未来を知る ステップアップ編", "プログレス法など、未来の流れを読むステップアップに。", "456205865X"),
    ("ホロスコープが読めるようになる西洋占星術（説話社占い選書）／いけだ笑み", "エレメントとサインの回、12星座の身体マップの参考に。", "4910924183"),
    ("アスペクト解釈大事典／松村 潔", "天体同士の角度を読む回に。", "4906828345"),
    ("ツボがある本当の意味／栗原誠", "経絡理論を根底から見直す一冊。ツボ観を更新したいときに。", "4814201982"),
    ("図解 経絡と解剖学／吉田 啓", "経絡×解剖学。エナジー・ゾディアックの核心に直結する一冊。", "449806934X"),
    ("閃めく経絡／ダニエル・キーオン", "経絡とファシアを科学寄りに捉える回に。", "4752910365"),
    ("アナトミー・トレイン 第4版 Web動画付", "筋膜経線の原典。身体マップの構造理解に。", "4260049240"),
    ("世界一わかりやすい 筋肉のつながり図鑑／きまたりょう", "筋肉のつながり入門に。", "4046062525"),
]
specialist = [
    ("経穴インパクト", "経穴をインパクトで捉える専門書。", "4752911493"),
    ("プロメテウス解剖学アトラス 第3版", "現場で使われる解剖学アトラス。", "4260025341"),
    ("ネッター解剖学アトラス 原書第7版", "解剖学の定番アトラス原書。", "4524230084"),
    ("骨格筋の形と触察法 改訂第2版", "触察の実務に。", "4998068628"),
    ("筋骨格系のキネシオロジー 原著第3版", "運動学の専門書。", "4263265815"),
    ("姿勢の教科書", "姿勢を体系的に学ぶ一冊。", "4816359257"),
]
books_body = "<h1>学ぶ｜本の道具箱</h1><p>メソッドの土台になった本を、テーマ別に置いています。価格は変動するため表示していません。各リンク先でご確認ください。リンクは楽天市場の検索ページへの通常リンクです（楽天アフィリエイトリンクは準備中）。</p>"
books_body += "<h2>占星術・経絡・身体構造の参考書</h2>" + cards([card(t, x, rsearch(t)) for t, x, a in books])
books_body += "<h2>現場で使われる専門書</h2>" + cards([card(t, x, rsearch(t)) for t, x, a in specialist])
write("books.html", page("占星術と経絡の本｜メソッドの土台になった参考書と専門書", "西洋占星術の教科書から経絡・解剖学の専門書まで、エナジー・ゾディアックの土台になった本棚。鏡リュウジの占星術の教科書、経穴インパクト、プロメテウス解剖学アトラスなど、初学者向けと現場の専門書を分けて紹介します。", books_body, "books.html"))

# ---------- aroma ----------
oils = [
    ("ローズ 精油 10ml（Kahuro）", "ローズの香り。", "B0CYT3YRQ7"),
    ("フランキンセンス 精油 10ml（Kahuro）", "フランキンセンスの香り。", "B0CYT4MTNC"),
    ("ローズマリー 精油 50ml（Kahuro）", "ローズマリーの香り。", "B0CCNN791F"),
    ("生活の木 エッセンシャルオイル 3本セット", "オレンジスイート・ラベンダー・ペパーミント各5ml。まず試すならこのセット。", "B0FC66FMQG"),
]
aroma_body = """
<h1>香る｜星座とアロマ</h1>
<p class="warn">⚠ 精油は猫に使いません。猫のいる空間での使用は避け、換気と保管にご注意ください。このページの香りは、人のための楽しみとして紹介しています。</p>
<p>12星座と香りの対応は、7つの資料を突き合わせて作った有料記事「12星座×アロマ対応表」（note・¥222）にまとめています。ここでは考え方だけを無料で紹介します。</p>
<h2>考え方</h2>
<p>星座のエレメント（火・地・風・水）と、その星座の経絡・感情のテーマに合わせて香りを選ぶのがFelis cattusのやり方です。効能を約束するものではなく、その日の自分を眺めるための小さな道具として使います。星座ごとの対応表は有料記事でどうぞ。</p>
<p><a class="btn" href="https://note.com/felis_cattus">note「Felis cattus」で対応表を見る</a></p>
<h2>香りの候補</h2>
<p>実在が確認できた精油だけを置いています。リンクは楽天市場の検索ページへの通常リンクです（楽天アフィリエイトリンクは準備中）。</p>
""" + cards([card(t, x, rsearch(t)) for t, x, a in oils])
write("aroma.html", page("12星座×アロマ対応表｜星座別のおすすめ精油と選び方", "12星座と精油の対応を、7つの資料を突き合わせて整理。星座のエレメントと経絡・感情のテーマから選ぶ、Felis cattusのアロマ対応表（有料記事¥222）の考え方と無料要約を紹介します。精油は猫には使いません。", aroma_body, "aroma.html"))

# ---------- goods ----------
goods = [
    ("HOMESTAR Classic（セガフェイブ）", "おうちで星空を眺める道具。星読みの夜のお供に。", "B00BB2NIXC"),
    ("Gloture 浮く月ライト Moon G", "浮いて光る月のライト。満月の週のインテリアに。", "B0CLVHY97C"),
    ("TOOGE 月ライト 4代目（直径18cm）", "月の形のライト。夜のデスクに。", "B01N6C4RPB"),
    ("YunLone プラネタリウム 家庭用", "星空・星雲・月を天井に投影。フィルムディスク13枚付き。", "B0BYVG772M"),
    ("EnergyPower 電動招き猫 白磁製 大型プレミアムモデル（27cm）", "電動で手が動く招き猫。店頭や玄関の縁起物として。", "B0C5WVF8KL"),
    ("Lulu's ムーンライト キャット ハーバリウム", "猫シルエット＋三日月＋星のハーバリウム。黒猫と白猫の世界観に。", "B0BLGZN5XB"),
    ("ピントー ボールライトパズル「月とふわふわ猫」", "完成後はType-C充電式ライトになるパズル。", "B0DJNFRWGL"),
    ("ポカロティー ねこコップ 2個セット", "黒猫と白猫のペア耐熱ガラスマグ。毎日のお茶時間に。", "B0DPJ6PZSN"),
    ("ムーンオロジーオラクルカード（ヤスミン・ボーランド）", "月と星座の記事のお供に。結果を断定するものではなく、眺める道具として。", "4908650926"),
]
goods_body = "<h1>整える｜月と星の道具</h1><p>月・星・猫のモチーフの道具と雑貨。週替わりコーナー「今週の開運グッズ」（note・毎週月曜）の置き場も兼ねています。縁起物・インテリアとしての紹介で、効果を約束するものではありません。価格は変動するため表示していません。</p>"
goods_body += "<p>リンクは楽天市場の検索ページへの通常リンクです（楽天アフィリエイトリンクは準備中）。</p>" + cards([card(t, x, rsearch(t)) for t, x, a in goods])
write("goods.html", page("月と星のグッズ｜プラネタリウム・月ライト・猫モチーフ雑貨", "ホームプラネタリウム、浮く月ライト、招き猫、黒猫と白猫の雑貨など、星読みの夜のお供になる月と星の道具。noteの週替わりコーナー「今週の開運グッズ」の置き場も兼ねています。効果を約束するものではありません。", goods_body, "goods.html"))

# ---------- cats (Rakuten links verbatim from affiliate_materials_2026-11-15.md) ----------
rakuten = [
    ("ピュリナワン キャット（ドライフード）", "https://hb.afl.rakuten.co.jp/ichiba/5984f8d2.9c7dc2b0.5984f8d3.560194b0/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fnyanzaq%2Fmtm0457%2F&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ%3D%3D"),
    ("黒缶パウチ アイシア 12個セット（ウェットフード）", "https://hb.afl.rakuten.co.jp/ichiba/5984fb2e.75083cdd.5984fb2f.ecbab247/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fuchinomofu%2Fkurokan-6x2%2F&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ%3D%3D"),
    ("アイリスオーヤマ 紙の猫砂 7L×6袋", "https://hb.afl.rakuten.co.jp/ichiba/5984fc27.134325de.5984fc28.91e82761/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fcat-land%2Fa533439%2F&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ%3D%3D"),
    ("爪とぎソファ型 キーテイル", "https://hb.afl.rakuten.co.jp/ichiba/5984fcfa.7f42805c.5984fcfb.e7fff84e/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fkeytail%2Fcp-016%2F&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ%3D%3D"),
    ("スリッカーブラシ ベルプラージュ", "https://hb.afl.rakuten.co.jp/ichiba/5984fda3.bd1292fd.5984fda4.a38badad/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fbelleplage%2Fpet-brush2%2F&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ%3D%3D"),
    ("ライオン PETKISS 歯みがきシート", "https://hb.afl.rakuten.co.jp/ichiba/598500f9.bf05e775.598500fa.6470c262/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fchanet%2F177329%2F&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ%3D%3D"),
]
cats_body = "<h1>猫と暮らす</h1><p>一緒に暮らす猫のための日用品（楽天）と、Felis cattusの世界観のLINEスタンプ。</p><h2>楽天のペット用品</h2>"
cats_body += cards([card(t, "楽天市場の商品ページへ（広告リンク）。", u, "楽天で見る", sponsored=True) for t, u in rakuten])
cats_body += """
<h2>LINEスタンプ｜222キャラ工房</h2>
<p>セラフィナのヨガスタンプ、専門家シリーズ、猫の毎日スタンプなど全14セット。制作者ページからどうぞ。</p>
<p><a class="btn" href="https://store.line.me/stickershop/author/6795103/ja" target="_blank" rel="noopener">222キャラ工房のページ</a></p>
<p>猫モチーフの雑貨は <a href="goods.html">整える</a> のページにも置いています。</p>
"""
write("cats.html", page("猫用品とLINEスタンプ｜楽天ペット用品と222キャラ工房", "一緒に暮らす猫のための楽天ペット用品6点（フード・猫砂・爪とぎ・ケア用品）と、222キャラ工房のLINEスタンプ全14セット。Felis cattusの黒猫と白猫の世界観で選んでいます。", cats_body, "cats.html", pr=True))

# ---------- shop ----------
shop_body = """
<h1>鑑定・商品</h1>
<p>Felis cattus の自社商品は note で販売しています（決済・受け渡しは note の仕組みを使います）。</p>
""" + cards([
    card("2027年 年間読み 鑑定書（受注生産）¥2,222", "出生図＋2027年のトランジットを読むA4・8ページの鑑定書PDF。月10名まで／納期7日以内。注文はnoteのチケット記事から、申込フォームで出生日時・場所をお聞きします。", "https://note.com/felis_cattus/n/nf3da15ac7ff5", "noteで注文する"),
    card("12星座×アロマ対応表 ¥222", "7資料を突き合わせた対応表の有料記事。無料要約はこのサイトの「香る」に。", "https://note.com/felis_cattus/n/n5099cf9691ef", "noteで見る"),
    card("月相×アロマ対応表 ¥222", "月の満ち欠け8段階で選ぶ香りの対応表。「12星座×アロマ対応表」と対になる、月の側の地図。", "https://note.com/felis_cattus/n/n0c1126c25c9a", "noteで見る"),
    card("恋の設計図（ハート・メロテシア入門記事）¥555", "恋愛版メソッド「ハート・メロテシア」の入門記事。年明け〜バレンタインの時期に発売予定。", "https://note.com/felis_cattus", "発売をnoteで待つ"),
]) + """
<h2>鑑定書の見本</h2>
<p>年間読み鑑定書のサンプル（1977年4月18日生まれの方の例）です。構成は、表紙／出生チャート図と配置表／チャートの骨格／2027年全体テーマ／月別読み／身体マップとセルフケア／おわりに、の全8ページ。星の位置はNASA JPLの天文暦で計算し、文章中の日付・サイン・角度は納品前に検証ツールで照合します。</p>
<div class="samples">
<figure><img src="sample_cover.webp" alt="鑑定書サンプルの表紙"><figcaption>表紙</figcaption></figure>
<figure><img src="sample_chart.webp" alt="鑑定書サンプルの出生チャート図"><figcaption>出生チャート図</figcaption></figure>
<figure><img src="sample_monthly.webp" alt="鑑定書サンプルの月別読み"><figcaption>月別読み</figcaption></figure>
<figure><img src="sample_body.webp" alt="鑑定書サンプルの身体マップ"><figcaption>身体マップ</figcaption></figure>
</div>
<h2>お預かりする情報について</h2>
<p>鑑定のお申し込みでは、申込フォームで生年月日・出生時刻・出生地と、納品先のメールアドレスをお聞きします。これらの情報は、鑑定書の制作と納品のためだけに使います。第三者へ提供することはなく、ほかの目的に使うこともありません。鑑定の内容や、お申し込みがあったこと自体を公開したり、宣伝に使ったりすることもありません。制作後の情報の削除をご希望の場合は、メールでご連絡いただければ対応します。</p>
<h2>毎日の発信</h2>
<p>note（毎日の星読み）／ Instagram <a href="https://www.instagram.com/felis.cattus222">@felis.cattus222</a> ／ Threads <a href="https://www.threads.com/@felis.cattus222">@felis.cattus222</a> ／ X <a href="https://x.com/felis_cattus222">@felis_cattus222</a></p>
"""
write("shop.html", page("鑑定書と有料記事｜2027年年間読み¥2,222・アロマ対応表¥222", "出生図と2027年の流れを読む年間読み鑑定書¥2,222（月10名まで・A4全8ページの見本あり）、12星座×アロマ対応表¥222、月相×アロマ対応表¥222。お預かりする出生情報の取り扱い方針も明記しています。", shop_body, "shop.html"))

# ---------- about / disclosure ----------
about_body = """
<h1>Felis cattus について</h1>
<p>Felis cattus は、星読みと身体をつなぐ独自メソッド「エナジー・ゾディアック」の発信アカウントです。12星座に、身体部位・経絡・五臓六腑・感情（情志）の対応を重ねて読むことで、「星の流れ」と「いまの自分の身体と心」を一枚の地図で眺める方法を提案しています。</p>
<h2>エナジー・ゾディアックとは</h2>
<p>西洋占星術の12星座（メロテシアの伝統）、中医学の経絡と五臓の伝統対応、そして身体のつながりを重ねた、Felis cattus オリジナルの読みの枠組みです。対応の正本は <a href="map.html">12星座×身体マップ</a> に公開しています。裏付けのない対応は作らないことが、このメソッドの約束です。</p>
<p>星読みは自己理解のための読み物です。医療の診断・治療の代わりにはなりません。体調の心配は専門家へご相談ください。</p>
<h2>提唱者について</h2>
<p>平賀建人（ひらが・けんと）――臨床30年のセラピスト、鍼灸師。資格：鍼灸師／登録販売者／パーソナルトレーナー。施術の現場で経絡と身体に向き合ってきた経験と、武術45年の稽古で培った身体感覚を土台に、占星術の伝統的な身体対応（メロテシア）を重ねて「エナジー・ゾディアック」を組み立てました。</p>
<p>星の位置の計算にはNASA JPLの天文データを使い、毎日の記事は公開前に日付・サイン・天文イベントを全件照合しています。「裏付けのない対応は作らない」は、このメソッドの一番の約束です。</p>
<h2>お問い合わせ</h2>
<p>メール：felis.cattus222@gmail.com</p>
"""
write("about.html", page("Felis cattusについて｜提唱者・平賀建人（鍼灸師・臨床30年）", "独自メソッド「エナジー・ゾディアック」とは何か。提唱者・平賀建人（臨床30年、鍼灸師／登録販売者／パーソナルトレーナー、武術45年）のプロフィールと、「裏付けのない対応は作らない」というメソッドの約束について。", about_body, "about.html"))

disclosure_body = """
<h1>アフィリエイト開示・プライバシー</h1>
<h2>アフィリエイトについて</h2>
<p>当サイトは、楽天アフィリエイト等の参加者です。「猫と暮らす」ページの楽天リンクは広告リンクで、リンクから商品を購入された場合、当サイトが紹介料を受け取ることがあります。広告リンクのあるページには「PR」表記を置いています。「学ぶ」「香る」「整える」ページのリンクは、楽天市場の検索ページへの通常リンクです（アフィリエイトリンクは準備中）。商品価格は変動するため、当サイトでは原則として表示していません。各販売ページでご確認ください。</p>
<h2>表現について</h2>
<p>当サイトは効能・効果や運気の向上を約束する表現を使いません。星読みは自己理解のための読み物としてお楽しみください。精油は猫に使用しないでください。</p>
<h2>プライバシー</h2>
<p>当サイトは静的サイトであり、独自に個人情報を収集する仕組みを持ちません。アクセス解析を導入する場合は、このページで告知します。お問い合わせメールでいただいた情報は、返信以外の目的には使いません。</p>
"""
write("disclosure.html", page("アフィリエイト開示・プライバシー", "当サイトのアフィリエイト広告の開示、表現についての方針、プライバシー（個人情報の取り扱い）についてまとめています。", disclosure_body, "disclosure.html"))

# ---------- sign pages (SEO article layer, 2026-11-16) ----------
SHORT_MERIDIAN = ["肺経", "大腸経", "胃経", "脾経", "心経", "小腸経", "膀胱経", "腎経", "心包経", "三焦経", "胆経", "肝経"]
SIGN_NOTES = [
    "始まりの星座です。肺経は十二経絡の巡りの起点で、呼吸と「境界」を担うとされてきました。頭部・脳・顔面に対応し、セルフケアの軸は、頭頂の百会と足裏の湧泉を結ぶ垂直の柱です。吸う息とともに天地を貫く一本の軸を思い描くことが、この星座の実践の入口になります。連載「星と巡る身体の地図」第3章で、章を挙げて扱いました。",
    "受け取る星座です。大腸経は肺経と表裏のペアで、「純化」を担います。喉・頸部・甲状腺に対応し、セルフケアの軸は足裏全体の接地です。大地に根ざす感覚を丁寧に味わうことが、受け取る力の土台になります。連載「星と巡る身体の地図」第4章で、章を挙げて扱いました。",
    "巡らせる星座です。胃経は「情報の摂取」——取り入れて咀嚼する働きに重ねて読みます。肩・腕・手と肺に対応し、セルフケアの軸は拇指球の踏み込みです。世界を取り込むときの前進の力を、足の前方で感じる星座です。",
    "守る星座です。脾経は「滋養・安心」を担い、胸部・胃・乳房に対応します。セルフケアの軸は土踏まずの柔軟性です。内なる聖域を守り、大地のぬくもりで基盤を安定させることが、この星座のテーマになります。",
    "輝く星座です。心経は「魂の喜び」を担い、心臓・背中・脊柱に対応します。セルフケアの軸は踵（かかと）の安定です。自己の核を支える不動の軸が、背筋の伸びに表れる星座です。",
    "整える星座です。小腸経は「秩序」——清濁を分ける働きに重ねて読みます。腹部・腸・消化器系に対応し、セルフケアの軸は足裏の外側エッジです。必要なものだけを識別する境界線を、身体の側でも意識する星座です。",
    "量る星座です。膀胱経は「均衡」を担い、腰部・腎臓・バランス感覚に対応します。セルフケアの軸は、左右の足重心の均等化です。自分と世界の均衡点を、立つ姿勢の中で探す星座です。",
    "深める星座です。腎経は「変容・意志」を担い、生殖器・排泄器官・骨盤底に対応します。セルフケアの軸は湧泉の吸気です。大地の深いところから意志を汲み上げるイメージが、この星座の実践になります。",
    "跳ぶ星座です。心包経は「境界」を担い、臀部・大腿部（太もも）・肝臓に対応します。セルフケアの軸は足首の解放と回転です。心包には五志の単独対応がないため、情志の欄は空欄のままにしています。理想へ跳躍するための自由な支点を持つ星座です。",
    "積む星座です。三焦経は「連動」を担い、膝・骨格全体・皮膚に対応します。セルフケアの軸は膝の柔軟なクッションです。三焦にも五志の単独対応がないため、情志の欄は空欄のままにしています。社会の重圧を、膝を通じて地に逃がす星座です。",
    "変える星座です。胆経は「変革・決断」を担い、下腿・足首・循環器系に対応します。セルフケアの軸は足の外側のラインです。既存の枠を突破する踏ん張りが、この星座の持ち味になります。",
    "溶ける星座です。肝経は「統合・再生」を担い、足・足裏・リンパ系に対応します。セルフケアの軸は足指の完全な解放です。流注順の締めくくりの経絡で、巡りはここからまた肺経へと戻っていきます。すべてを大地（海）へ還す統合の星座です。",
]
CHAPTER_URLS = {
    "牡羊座": ("第3章｜牡羊座——頭部と肺経、始まりの呼吸", "https://note.com/felis_cattus/n/n68f6074f9907"),
    "牡牛座": ("第4章｜牡牛座——喉と大腸経、受け取る力の土台", "https://note.com/felis_cattus/n/nc57037a113bc"),
}
INDEX_ARTICLE = "https://note.com/felis_cattus/n/na1ab441528d1"
for i, s in enumerate(SIGNS):
    slug = SLUGS[i]
    prev_s = SIGNS[i - 1]
    next_s = SIGNS[(i + 1) % 12]
    if s[0] in CHAPTER_URLS:
        ct, cu = CHAPTER_URLS[s[0]]
        series_link = f'<p>この星座は、noteの連載「星と巡る身体の地図」で章を挙げて解説しています。<a href="{cu}">連載{ct}（note）</a>／<a href="{INDEX_ARTICLE}">連載の目次</a></p>'
    else:
        series_link = f'<p>この星座の連載の章は順次公開中です。<a href="{INDEX_ARTICLE}">連載「星と巡る身体の地図」の目次（note）</a>から、公開済みの章を読めます。</p>'
    body = f"""
<p><a href="map.html">← 12星座×身体マップ（対応表）へ戻る</a></p>
<h1>{s[0]}×{SHORT_MERIDIAN[i]}｜{s[2]}の身体マップ</h1>
<p>{s[0]}（{s[1]}）の身体対応を、エナジー・ゾディアックの対応表から抜き出して解説するページです。対応の正本は <a href="map.html">12星座×身体マップ</a> で、ここでは{s[0]}だけを取り上げます。</p>
<div class="card sign-card">
<p><strong>身体</strong>：{s[2]}</p><p><strong>経絡</strong>：{s[3]}</p>
<p><strong>臓腑</strong>：{s[4]}</p><p><strong>感情（情志）</strong>：{s[5]}</p>
<p><strong>セルフケア</strong>：{s[6]}</p>
</div>
<h2>{s[0]}の読み</h2>
<p>{SIGN_NOTES[i]}</p>
<h2>セルフケアの考え方</h2>
<p>{s[6]}——これが{s[0]}のセルフケアの軸です。星読みは自己理解のための読み物であり、ここでの実践は、その日の自分の身体を眺めるための小さな習慣として提案しています。体調に心配がある場合は、専門家へご相談ください。</p>
{series_link}
<p>自分の出生図でこの対応を読む場合は、<a href="shop.html">年間読み鑑定書</a>であなたの{s[0]}の天体と2027年の流れを合わせて読みます。</p>
<p class="sign-nav"><a href="sign-{SLUGS[i - 1]}.html">← {prev_s[0]}</a>　｜　<a href="sign-{SLUGS[(i + 1) % 12]}.html">{next_s[0]} →</a></p>
"""
    write(f"sign-{slug}.html", page(f"{s[0]}と{SHORT_MERIDIAN[i]}｜{s[2]}の身体対応とセルフケア",
        f"{s[0]}の身体対応（{s[2]}）、担当経絡の{s[3]}、臓腑の{s[4]}、感情（情志）とセルフケア。エナジー・ゾディアックの12星座×身体マップ、{s[0]}のページです。",
        body, f"sign-{slug}.html"))

# ---------- style / robots / sitemap / readme ----------
write("style.css", """
:root{--bg:#12122b;--bg2:#1b1b3a;--gold:#c9a86a;--ink:#f2ecdd;--sub:#b9b4a3}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif;line-height:1.8}
a{color:var(--gold)}
.sister-bar{display:flex;gap:18px;align-items:center;overflow-x:auto;background:var(--bg2);border-bottom:1px solid #34345e;padding:7px 16px;font-size:.78rem;letter-spacing:.06em;white-space:nowrap;scrollbar-width:none}
.sister-bar::-webkit-scrollbar{display:none}
.sister-bar a{color:var(--ink);text-decoration:none;flex:0 0 auto}
.sister-bar a:hover{color:var(--gold)}
.sister-label{color:var(--gold);font-weight:600;flex:0 0 auto}
header{background:var(--bg2);padding:14px 20px;border-bottom:1px solid var(--gold)}
.brand a{color:var(--ink);text-decoration:none;font-weight:bold;font-size:1.1rem;display:flex;align-items:center;gap:12px}
.brand .logo{width:46px;height:46px;border-radius:50%;flex:none}
.brand-text{line-height:1.35}
.brand-sub{display:block;font-size:.78rem;color:var(--sub);font-weight:normal;letter-spacing:.12em}
h1,h2,.brand a{font-family:"Noto Serif JP","Hiragino Mincho ProN","Yu Mincho",serif}
.hero-logo{margin:0 0 12px}
.hero-logo img{width:118px;height:118px;border-radius:50%}
.statement{font-size:1.03rem}
nav{margin-top:8px;display:flex;flex-wrap:wrap;gap:6px 16px}
nav a{text-decoration:none;font-size:.92rem}
main{max-width:960px;margin:0 auto;padding:24px 20px 48px}
.hero{padding:24px 0 8px}
.hero h1{font-size:2rem;color:var(--gold);margin:0 0 8px}
h2{color:var(--gold);border-bottom:1px solid #34345e;padding-bottom:4px;margin-top:36px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px;margin-top:16px}
.card{background:var(--bg2);border:1px solid #34345e;border-radius:10px;padding:16px}
.card h3{margin:0 0 6px;font-size:1.02rem}
.card p{margin:4px 0;font-size:.94rem;color:var(--ink)}
.btn{display:inline-block;background:var(--gold);color:#12122b !important;padding:6px 14px;border-radius:6px;text-decoration:none;font-weight:bold}
.signs{display:flex;flex-wrap:wrap;gap:10px}
.sign{background:var(--bg2);border:1px solid var(--gold);border-radius:8px;padding:8px 14px;text-decoration:none;text-align:center}
.sign span{display:block;font-size:.75rem;color:var(--sub)}
.pr,.warn{background:#2a2417;border:1px solid var(--gold);border-radius:8px;padding:10px 14px;font-size:.9rem}
footer{background:var(--bg2);padding:20px;font-size:.85rem;color:var(--sub);border-top:1px solid #34345e}
.sign-card span{font-size:.8rem;color:var(--sub)}
.samples{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:14px;margin-top:16px}
.samples figure{margin:0}
.samples img{width:100%;border-radius:6px;border:1px solid var(--gold);display:block}
.samples figcaption{font-size:.85rem;color:var(--sub);text-align:center;margin-top:6px}
blockquote.sample-read{margin:16px 0;padding:14px 18px;background:var(--bg2);border-left:3px solid var(--gold);border-radius:0 8px 8px 0;font-size:.98rem}
.hero-visual{position:relative;border-radius:14px;overflow:hidden;margin:0 0 20px;background:#0a0a1c}
.hero-visual img{display:block;width:100%;height:auto}
.hero-visual-text{position:absolute;left:0;top:0;bottom:0;width:58%;display:flex;flex-direction:column;justify-content:center;padding:28px 34px;background:linear-gradient(90deg,rgba(10,10,28,.90) 30%,rgba(10,10,28,.50) 68%,rgba(10,10,28,0))}
.hero-visual-text h1{font-size:2rem;color:var(--gold);margin:0;line-height:1.4}
.cards-img .card{padding:0 0 16px;overflow:hidden}
.cards-img .card h3{padding:14px 16px 0}
.cards-img .card p{padding:0 16px}
.card-img{display:block}
.card-img img{display:block;width:100%;height:180px;object-fit:cover}
@media(max-width:640px){.hero-visual-text{width:100%;background:linear-gradient(180deg,rgba(10,10,28,.88),rgba(10,10,28,.45) 75%,rgba(10,10,28,0));justify-content:flex-start;padding:18px 20px}.hero-visual-text h1{font-size:1.45rem}}
""")
pages = ["index.html","map.html","books.html","aroma.html","goods.html","cats.html","shop.html","about.html","disclosure.html"] + [f"sign-{s}.html" for s in SLUGS]
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(f"<url><loc>{BASE if p == 'index.html' else BASE + p}</loc></url>" for p in pages) + "\n</urlset>\n"
write("sitemap.xml", sitemap)
write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
write("README.md", """# Felis cattus｜エナジー・ゾディアック（星と身体の道具箱）

Felis cattus のアフィリエイトサイト（GitHub Pages）。
生成：`python3 build.py` で HTML を再生成します。商品の正本は `~/workspace/felis_cattus/ad_list.md` 系。

## 公開手順
1. GitHub アカウント felis-cattus222（felis.cattus222@gmail.com で新規登録）でリポジトリ `felis-cattus` を作成
2. このフォルダの中身を push
3. Settings → Pages → Branch: main / root で公開
4. アフィリエイトは楽天中心（2026-11-15 本人決定でAmazonは使わない）。楽天アフィリエイトリンクが発行できたら、検索リンクを hb.afl リンクへ差し替える
5. Google Search Console に登録し、sitemap.xml を送信
""")
print("built:", pages)
