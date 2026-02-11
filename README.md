# 🍳 30日間クッキング英語

英検5級レベルの英語を、料理コンテンツで学ぶ30日間のワークシート。

## 🚀 セットアップ

### 1. APIキーの設定

Anthropic APIキーを環境変数に設定：

```bash
export ANTHROPIC_API_KEY="sk-ant-xxxxx"
```

APIキーは [Anthropic Console](https://console.anthropic.com/) で取得できます。

### 2. コンテンツ生成

```bash
python generate_content.py
```

30日分のJSONコンテンツが `content/` フォルダに生成されます（約5-10分）。

### 3. HTML生成

```bash
python build_html.py
```

`docs/` フォルダにHTMLファイルが生成されます。

### 4. ローカルで確認

```bash
open docs/index.html
```

または

```bash
python -m http.server 8000 --directory docs
# ブラウザで http://localhost:8000 を開く
```

## 🌐 デプロイ

### Cloudflare Pages

1. GitHubにリポジトリを作成してプッシュ
2. [Cloudflare Pages](https://pages.cloudflare.com/) でリポジトリを接続
3. Build settings:
   - Build command: (空欄)
   - Build output directory: `docs`
4. デプロイ！

### GitHub Pages

1. GitHubにリポジトリをプッシュ
2. Settings → Pages → Source: `main` branch, `/docs` folder
3. Save

## 📁 ファイル構成

```
cooking-english/
├── generate_content.py  # コンテンツ生成スクリプト
├── build_html.py        # HTML生成スクリプト
├── README.md            # このファイル
├── content/             # 生成されたJSON（30ファイル）
│   ├── day1.json
│   ├── day2.json
│   └── ...
└── docs/                # 生成されたHTML（公開用）
    ├── index.html
    ├── day1.html
    ├── day2.html
    └── ...
```

## 🍱 30日間のメニュー

| Day | 料理 | Day | 料理 |
|-----|------|-----|------|
| 1 | 🥟 餃子 | 16 | 🥔 肉じゃが |
| 2 | 🟡 シュウマイ | 17 | 🥩 牛丼 |
| 3 | 🍗 唐揚げ | 18 | 🐷 とんかつ |
| 4 | 🍗 チキン南蛮 | 19 | 🍢 焼き鳥 |
| 5 | 🐔 油淋鶏 | 20 | 🫛 枝豆 |
| 6 | 🍖 角煮 | 21 | 🍮 茶碗蒸し |
| 7 | 🍳 チャーハン | 22 | 🍤 天ぷら |
| 8 | 🍜 ラーメン | 23 | 🍝 そば |
| 9 | 🍙 おにぎり | 24 | 🍜 うどん |
| 10 | 🥣 味噌汁 | 25 | 🐔 親子丼 |
| 11 | 🥚 卵焼き | 26 | 🍱 カツ丼 |
| 12 | 🍗 照り焼きチキン | 27 | 🍵 お茶漬け |
| 13 | 🍛 カレー | 28 | 🐙 たこわさ |
| 14 | 🥞 お好み焼き | 29 | 🥒 浅漬け |
| 15 | 🐙 たこ焼き | 30 | 🍵 抹茶プリン |

## 📝 各日のコンテンツ構成

1. **Recipe** - レシピ（英語）
2. **Quiz 1** - 内容理解チェック
3. **Review** - オーストラリアのレストランレビュー（英語）
4. **Quiz 2** - 内容理解チェック
5. **Australia Tips** - オーストラリア生活情報（日本語）
6. **Conversation** - ワーホリ中の会話（英語）
7. **Quiz 3** - 内容理解チェック
8. **Try It!** - 3行日記チャレンジ
9. **学習サマリー** - ChatGPTにコピペして解説をもらう

## 🔧 カスタマイズ

### レシピを変更する

`generate_content.py` の `RECIPES` リストを編集：

```python
RECIPES = [
    {"day": 1, "en": "Gyoza", "ja": "餃子", "emoji": "🥟"},
    # 追加・変更・削除
]
```

### デザインを変更する

`build_html.py` の `HTML_TEMPLATE` を編集。

## ❓ トラブルシューティング

### APIキーエラー

```
❌ エラー: ANTHROPIC_API_KEY が設定されていません
```

→ `export ANTHROPIC_API_KEY="sk-ant-xxxxx"` を実行

### JSONパースエラー

→ 該当のdayを削除して再実行（スキップ機能あり）

```bash
rm content/day5.json
python generate_content.py
```

## 📄 ライセンス

教育目的での使用は自由です。
