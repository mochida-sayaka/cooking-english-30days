#!/usr/bin/env python3
"""
30日間クッキング英語 - コンテンツ生成スクリプト

使い方:
1. ANTHROPIC_API_KEY を環境変数にセット
   export ANTHROPIC_API_KEY="sk-ant-xxxxx"

2. スクリプト実行
   python generate_content.py

3. content/ フォルダにJSONファイルが生成される
"""

import anthropic
import json
import time
import os
import sys

# 30 recipes list
RECIPES = [
    {"day": 1, "en": "Gyoza", "ja": "餃子", "emoji": "🥟"},
    {"day": 2, "en": "Shumai", "ja": "シュウマイ", "emoji": "🟡"},
    {"day": 3, "en": "Karaage", "ja": "唐揚げ", "emoji": "🍗"},
    {"day": 4, "en": "Chicken Nanban", "ja": "チキン南蛮", "emoji": "🍗"},
    {"day": 5, "en": "Yurinjii", "ja": "油淋鶏", "emoji": "🐔"},
    {"day": 6, "en": "Kakuni", "ja": "角煮", "emoji": "🍖"},
    {"day": 7, "en": "Fried Rice", "ja": "チャーハン", "emoji": "🍳"},
    {"day": 8, "en": "Ramen", "ja": "ラーメン", "emoji": "🍜"},
    {"day": 9, "en": "Onigiri", "ja": "おにぎり", "emoji": "🍙"},
    {"day": 10, "en": "Miso Soup", "ja": "味噌汁", "emoji": "🥣"},
    {"day": 11, "en": "Tamagoyaki", "ja": "卵焼き", "emoji": "🥚"},
    {"day": 12, "en": "Teriyaki Chicken", "ja": "照り焼きチキン", "emoji": "🍗"},
    {"day": 13, "en": "Japanese Curry", "ja": "カレー", "emoji": "🍛"},
    {"day": 14, "en": "Okonomiyaki", "ja": "お好み焼き", "emoji": "🥞"},
    {"day": 15, "en": "Takoyaki", "ja": "たこ焼き", "emoji": "🐙"},
    {"day": 16, "en": "Nikujaga", "ja": "肉じゃが", "emoji": "🥔"},
    {"day": 17, "en": "Gyudon", "ja": "牛丼", "emoji": "🥩"},
    {"day": 18, "en": "Tonkatsu", "ja": "とんかつ", "emoji": "🐷"},
    {"day": 19, "en": "Yakitori", "ja": "焼き鳥", "emoji": "🍢"},
    {"day": 20, "en": "Edamame", "ja": "枝豆", "emoji": "🫛"},
    {"day": 21, "en": "Chawanmushi", "ja": "茶碗蒸し", "emoji": "🍮"},
    {"day": 22, "en": "Tempura", "ja": "天ぷら", "emoji": "🍤"},
    {"day": 23, "en": "Soba", "ja": "そば", "emoji": "🍝"},
    {"day": 24, "en": "Udon", "ja": "うどん", "emoji": "🍜"},
    {"day": 25, "en": "Oyakodon", "ja": "親子丼", "emoji": "🐔"},
    {"day": 26, "en": "Katsudon", "ja": "カツ丼", "emoji": "🍱"},
    {"day": 27, "en": "Ochazuke", "ja": "お茶漬け", "emoji": "🍵"},
    {"day": 28, "en": "Takowasa", "ja": "たこわさ", "emoji": "🐙"},
    {"day": 29, "en": "Tsukemono", "ja": "浅漬け", "emoji": "🥒"},
    {"day": 30, "en": "Matcha Pudding", "ja": "抹茶プリン", "emoji": "🍵"},
]

PROMPT_TEMPLATE = '''あなたは英語教材を作成する専門家です。英検5級レベル（中1程度）の英語で、日本料理のレシピと関連コンテンツを作成してください。

# 作成する料理
{recipe_en}（{recipe_ja}）

# 学習者のプロフィール
- 日本人女性、オーストラリアでワーキングホリデー予定
- 景色の良いレストラン・カフェが好き（海沿い、山が見える、など）
- カジュアルで落ち着いた雰囲気のお店が好き
- 好きな花：ジャスミン、ミモザ
- 好きな色：ピンク、黄色、ラベンダー

# 出力形式
以下のJSON形式で出力してください。すべての英文は英検5級レベル（中1程度）で書いてください。

```json
{{
  "recipe": {{
    "title": "How to Make {recipe_en}",
    "intro": "（料理の1-2文の説明。例：Gyoza is a Japanese dumpling. It is very popular in Japan.）",
    "ingredients": "（材料リスト。英語で。例：pork, cabbage, garlic, ginger, soy sauce, sesame oil, gyoza wrappers）",
    "steps": [
      "（ステップ1。動詞を太字にする。例：**Cut** the cabbage very small.）",
      "（ステップ2）",
      "（ステップ3）",
      "（ステップ4）",
      "（ステップ5）",
      "（ステップ6。最後は **Enjoy!** で終わる）"
    ]
  }},
  "recipe_vocab": [
    {{"word": "単語", "meaning": "日本語の意味"}},
    ...（8-12個程度）
  ],
  "quiz1": {{
    "question": "（レシピの内容に関する日本語の質問）",
    "options": ["選択肢1", "選択肢2", "選択肢3"],
    "correct": 0
  }},
  "review": {{
    "restaurant": "（架空のオーストラリアのレストラン名。景色が良い、カジュアルで落ち着いた雰囲気のお店）",
    "location": "（ブリスベンまたはシドニーの地名。できれば海沿いや眺めの良い場所）",
    "stars": 5,
    "content": "（レビュー本文。5-7文程度。過去形を使う。景色の良さ、落ち着いた雰囲気、居心地の良さなども描写する。例：I went to ... last weekend. The view was beautiful. I could see the ocean from my table. The restaurant was quiet and cozy. I ordered ... It was delicious.）"
  }},
  "review_vocab": [
    {{"word": "単語", "meaning": "日本語の意味"}},
    ...（8-12個程度）
  ],
  "quiz2": {{
    "question": "（レビューの内容に関する日本語の質問）",
    "options": ["選択肢1", "選択肢2", "選択肢3"],
    "correct": 0
  }},
  "australia_tips": {{
    "title": "（日本語のタイトル。例：オーストラリアで餃子を作るなら）",
    "content": "（日本語で3-4段落。材料の買い方、現地での楽しみ方、ワーホリ中に役立つ情報など。時々、オーストラリアの美しい景色、カフェ文化、ジャスミンやミモザの花が見れる場所や季節などの情報も織り交ぜる）"
  }},
  "conversation": {{
    "scene": "（日本語でシーン説明。例：シェアハウスのキッチンにて、海が見えるカフェにて、など）",
    "lines": [
      {{"speaker": "A", "text": "（英語のセリフ）"}},
      {{"speaker": "B", "text": "（英語のセリフ）"}},
      ...（10-14行程度。料理に関連した自然な会話）
    ]
  }},
  "conversation_vocab": [
    {{"word": "単語", "meaning": "日本語の意味"}},
    ...（8-12個程度）
  ],
  "quiz3": {{
    "question": "（会話の内容に関する日本語の質問）",
    "options": ["選択肢1", "選択肢2", "選択肢3"],
    "correct": 0
  }},
  "try_it_hint": "（日本語で、今日の会話をマネして書ける例文のヒント。例：I'm making ... tonight.）"
}}
```

# 重要なルール
1. 英文は全て英検5級レベル（中学1年生が読める程度）
2. 使う単語は基本的な日常語彙（600語レベル）
3. 文は短く、シンプルに
4. 過去形、現在形、現在進行形を適切に使い分ける
5. 会話は自然で、ワーホリ中にありそうなシチュエーション
6. オーストラリア情報は実用的で具体的に（スーパーの名前、地域名など）
7. vocabリストには必ずその文章で使われている重要単語を含める
8. クイズの正解は "correct" フィールドで0, 1, 2のいずれかで指定（0が最初の選択肢）
9. レビューのレストランは景色が良く、カジュアルで落ち着いた雰囲気のお店にする
10. 30日間でバリエーションを出す（海沿い、山が見える、川沿い、公園の近く、テラス席があるなど）

JSONのみを出力してください。'''


def generate_content(client, recipe):
    """Generate content for a single recipe using Claude API"""
    prompt = PROMPT_TEMPLATE.format(
        recipe_en=recipe["en"],
        recipe_ja=recipe["ja"]
    )
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    response_text = message.content[0].text
    
    # Extract JSON from response
    if "```json" in response_text:
        json_str = response_text.split("```json")[1].split("```")[0]
    elif "```" in response_text:
        json_str = response_text.split("```")[1].split("```")[0]
    else:
        json_str = response_text
    
    return json.loads(json_str.strip())


def main():
    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ エラー: ANTHROPIC_API_KEY が設定されていません")
        print("")
        print("以下のコマンドでAPIキーを設定してください:")
        print('  export ANTHROPIC_API_KEY="sk-ant-xxxxx"')
        print("")
        print("APIキーは https://console.anthropic.com/ で取得できます")
        sys.exit(1)
    
    client = anthropic.Anthropic(api_key=api_key)
    
    os.makedirs("content", exist_ok=True)
    
    all_content = {}
    success_count = 0
    
    print("🍳 30日間クッキング英語 - コンテンツ生成開始")
    print("=" * 50)
    
    for recipe in RECIPES:
        day = recipe["day"]
        
        # Skip if already generated
        if os.path.exists(f"content/day{day}.json"):
            print(f"⏭️  Day {day}: {recipe['en']} - スキップ（既存）")
            with open(f"content/day{day}.json", "r", encoding="utf-8") as f:
                all_content[f"day{day}"] = json.load(f)
            success_count += 1
            continue
        
        print(f"🔄 Day {day}: {recipe['en']} を生成中...")
        
        try:
            content = generate_content(client, recipe)
            content["meta"] = recipe
            all_content[f"day{day}"] = content
            
            # Save individual file
            with open(f"content/day{day}.json", "w", encoding="utf-8") as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Day {day}: {recipe['en']} 完了")
            success_count += 1
            
            # Rate limiting - wait between requests
            if day < 30:
                time.sleep(1)
                
        except json.JSONDecodeError as e:
            print(f"❌ Day {day}: JSONパースエラー - {e}")
            continue
        except Exception as e:
            print(f"❌ Day {day}: エラー - {e}")
            continue
    
    # Save all content to single file
    with open("content/all_content.json", "w", encoding="utf-8") as f:
        json.dump(all_content, f, ensure_ascii=False, indent=2)
    
    print("=" * 50)
    print(f"✅ 生成完了: {success_count}/30 日分")
    print("📁 content/ フォルダにJSONファイルが保存されました")
    print("")
    print("次のステップ:")
    print("  python build_html.py")


if __name__ == "__main__":
    main()
