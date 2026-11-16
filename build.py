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

def page(title, desc, body, pr=False):
    nav = "\n".join(f'<a href="{h}">{t}</a>' for h, t in NAV)
    pr_note = '<p class="pr">PR：このページにはアフィリエイトリンク（広告）が含まれます。</p>' if pr else ""
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}｜Felis cattus｜エナジー・ゾディアック</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="icon" href="favicon.ico">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
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

def card(title, text, url, label="楽天で探す", sponsored=False):
    rel = "sponsored nofollow noopener" if sponsored else "noopener"
    return f"""<div class="card">
<h3>{html.escape(title)}</h3>
<p>{html.escape(text)}</p>
<p><a class="btn" href="{url}" target="_blank" rel="{rel}">{label}</a></p>
</div>"""

def cards(items):
    return '<div class="grid">\n' + "\n".join(items) + "\n</div>"

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
sign_links = "\n".join(
    f'<a class="sign" href="map.html#{s[0]}">{s[0]}<span>{s[1]}</span></a>' for s in SIGNS)
index_body = f"""
<section class="hero">
<p class="hero-logo"><img src="logo.png" alt="黒猫と白猫とホロスコープの環"></p>
<h1>明日の星を、身体で読む。</h1>
<p class="statement">エナジー・ゾディアックは、12星座と身体・経絡・感情の対応を読み解く、Felis cattus の独自メソッドです。提唱者は臨床30年の鍼灸師。星の位置は天文データで検証し、裏付けのない対応は作りません。</p>
<p>このサイトは、そのメソッドの入口です。毎日の星読みは <a href="https://note.com/felis_cattus">note「Felis cattus」</a> で毎夕更新しています。</p>
</section>
<h2>はじめ方｜3つのステップ</h2>
{cards([
    card("STEP 1｜毎日の星読みを読む", "明日のチャートと身体のテーマを、毎夕noteで無料配信。まず流れをつかむところから。", "https://note.com/felis_cattus", "noteで読む"),
    card("STEP 2｜自分の星座の身体マップを知る", "あなたの星座は、身体のどこ・どの経絡・どんな感情と対応しているのか。メソッドの中心にある対応表です。", "map.html", "マップを見る"),
    card("STEP 3｜自分専用の鑑定書を注文する", "出生図と2027年の流れを読む、あなただけの鑑定書（A4・8ページ）。", "shop.html", "鑑定・商品を見る"),
])}
<h2>まず自分の星座から</h2>
<div class="signs">{sign_links}</div>
<h2>カテゴリ</h2>
{cards([
    card("学ぶ｜本の道具箱", "占星術・経絡・身体構造。メソッドの土台になった本と、現場で使われる専門書。", "books.html", "ページを開く"),
    card("香る｜星座とアロマ", "12星座×アロマ対応表の無料要約との精油リンク。", "aroma.html", "ページを開く"),
    card("整える｜月と星の道具", "プラネタリウム、月ライト、猫と星の雑貨。夜の星読み時間のお供に。", "goods.html", "ページを開く"),
    card("猫と暮らす", "楽天のペット用品と、222キャラ工房のLINEスタンプ。", "cats.html", "ページを開く"),
])}
<h2>Felis cattus の商品（noteで販売中）</h2>
{cards([
    card("2027年 年間読み 鑑定書（受注生産）", "あなたの出生図と2027年のトランジットを読む、A4・8ページの鑑定書。月10名まで、¥2,222。", "https://note.com/felis_cattus/n/nf3da15ac7ff5", "noteで注文する"),
    card("12星座×アロマ対応表", "7つの資料を突き合わせた対応表の有料記事。¥222。無料要約は「香る」のページに。", "aroma.html", "まず無料要約を読む"),
])}
"""
write = lambda name, content: open(os.path.join(OUT, name), "w", encoding="utf-8").write(content)
write("index.html", page("トップ", "「明日の星を、身体で読む。」独自メソッド「エナジー・ゾディアック」の公式サイト。12星座×身体マップ、本、アロマ、月と星のグッズ、鑑定書。", index_body))

# ---------- map ----------
rows = "\n".join(
    f'<div class="card sign-card" id="{s[0]}"><h3>{s[0]} <span>{s[1]}</span></h3>'
    f"<p><strong>身体</strong>：{s[2]}</p><p><strong>経絡</strong>：{s[3]}</p>"
    f"<p><strong>臓腑</strong>：{s[4]}</p><p><strong>感情（情志）</strong>：{s[5]}</p>"
    f"<p><strong>セルフケア</strong>：{s[6]}</p></div>" for s in SIGNS)
map_body = f"""
<h1>12星座×身体マップ</h1>
<p>エナジー・ゾディアックの中心にある対応表です。身体部位は連載「解体新書」第4回、経絡は連載「星と巡る身体の地図」第2章の流注順（肺経から始まる気の巡りの順）を正本としています。感情（情志）は『黄帝内経』以来の伝統対応で、経絡の表裏を介した接続の場合はその旨を添えています。裏付けのない対応は作らず、空欄のままにしています。</p>
<div class="grid">{rows}</div>
<p>この対応をあなたの出生図で読むのが、年間読み鑑定書です。詳しくは <a href="shop.html">鑑定・商品</a> のページへ。</p>
"""
write("map.html", page("12星座×身体マップ", "12星座と身体部位・経絡・臓腑・感情・セルフケアの対応表。エナジー・ゾディアックの中心素材。", map_body))

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
write("books.html", page("学ぶ｜本の道具箱", "占星術・経絡・筋膜・解剖学の参考書と専門書。エナジー・ゾディアックの土台の本棚。", books_body))

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
write("aroma.html", page("香る｜星座とアロマ", "12星座×アロマ対応表の考え方と、精油の楽天検索リンク。精油は猫に使わない注意書き付き。", aroma_body))

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
write("goods.html", page("整える｜月と星の道具", "プラネタリウム、月ライト、招き猫、猫と星の雑貨。", goods_body))

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
write("cats.html", page("猫と暮らす", "楽天の猫用品6点と、222キャラ工房のLINEスタンプ。", cats_body, pr=True))

# ---------- shop ----------
shop_body = """
<h1>鑑定・商品</h1>
<p>Felis cattus の自社商品は note で販売しています（決済・受け渡しは note の仕組みを使います）。</p>
""" + cards([
    card("2027年 年間読み 鑑定書（受注生産）¥2,222", "出生図＋2027年のトランジットを読むA4・8ページの鑑定書PDF。月10名まで／納期7日以内。注文はnoteのチケット記事から、申込フォームで出生日時・場所をお聞きします。", "https://note.com/felis_cattus/n/nf3da15ac7ff5", "noteで注文する"),
    card("12星座×アロマ対応表 ¥222", "7資料を突き合わせた対応表の有料記事。無料要約はこのサイトの「香る」に。", "https://note.com/felis_cattus", "noteで見る"),
    card("恋の設計図（ハート・メロテシア入門記事）¥555", "恋愛版メソッド「ハート・メロテシア」の入門記事。年明け〜バレンタインの時期に発売予定。", "https://note.com/felis_cattus", "発売をnoteで待つ"),
]) + """
<h2>毎日の発信</h2>
<p>note（毎日の星読み）／ Instagram <a href="https://www.instagram.com/felis.cattus222">@felis.cattus222</a> ／ Threads <a href="https://www.threads.com/@felis.cattus222">@felis.cattus222</a> ／ X <a href="https://x.com/felis_cattus222">@felis_cattus222</a></p>
"""
write("shop.html", page("鑑定・商品", "年間読み鑑定書¥2,222、アロマ対応表¥222、恋の設計図¥555（予定）。", shop_body))

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
write("about.html", page("Felis cattusについて", "エナジー・ゾディアックとは。提唱者・平賀建人（臨床30年・鍼灸師）のプロフィールと問い合わせ先。", about_body))

disclosure_body = """
<h1>アフィリエイト開示・プライバシー</h1>
<h2>アフィリエイトについて</h2>
<p>当サイトは、楽天アフィリエイト等の参加者です。「猫と暮らす」ページの楽天リンクは広告リンクで、リンクから商品を購入された場合、当サイトが紹介料を受け取ることがあります。広告リンクのあるページには「PR」表記を置いています。「学ぶ」「香る」「整える」ページのリンクは、楽天市場の検索ページへの通常リンクです（アフィリエイトリンクは準備中）。商品価格は変動するため、当サイトでは原則として表示していません。各販売ページでご確認ください。</p>
<h2>表現について</h2>
<p>当サイトは効能・効果や運気の向上を約束する表現を使いません。星読みは自己理解のための読み物としてお楽しみください。精油は猫に使用しないでください。</p>
<h2>プライバシー</h2>
<p>当サイトは静的サイトであり、独自に個人情報を収集する仕組みを持ちません。アクセス解析を導入する場合は、このページで告知します。お問い合わせメールでいただいた情報は、返信以外の目的には使いません。</p>
"""
write("disclosure.html", page("アフィリエイト開示・プライバシー", "アフィリエイト開示とプライバシー方針。", disclosure_body))

# ---------- style / robots / sitemap / readme ----------
write("style.css", """
:root{--bg:#12122b;--bg2:#1b1b3a;--gold:#c9a86a;--ink:#f2ecdd;--sub:#b9b4a3}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif;line-height:1.8}
a{color:var(--gold)}
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
""")
pages = ["index.html","map.html","books.html","aroma.html","goods.html","cats.html","shop.html","about.html","disclosure.html"]
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(f"<url><loc>{BASE}{p}</loc></url>" for p in pages) + "\n</urlset>\n"
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
