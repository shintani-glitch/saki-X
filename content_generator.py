# content_generator.py

import google.generativeai as genai
import google.generativeai.types as genai_types
import json
import os
from dotenv import load_dotenv

load_dotenv()

def generate_tweet_parts(app_info):
    """Gemini APIのJSONモードを使ってツイートのパーツを生成する"""
    print("STEP 3: Geminiでコンテンツパーツを生成中 (JSONモード)...")
    try:
        # 応答形式をJSONに指定
        generation_config = genai_types.GenerationConfig(
            response_mime_type="application/json"
        )
        
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        
        # モデルに設定を適用
        model = genai.GenerativeModel(
            'gemini-1.5-flash',
            generation_config=generation_config
        )

        # ★★★ プロンプトを「さき」用に変更 ★★★
        prompt = f"""
        # 指令書: X(Twitter)投稿用のマッチングアプリ紹介パーツ生成
        あなたは、マッチングアプリで彼氏探しに奮闘する27歳のOL「さき」です。
        一人称は「私」で、フォロワーに語りかけるような、親しみやすい口調（敬語とタメ口が混ざった感じ）でお願いします。

        Webで「{app_info.get('アプリ名', '')}」というマッチングアプリについて、実際に使っている人のリアルな口コミや評判を調査してください。

        調査結果とあなたのペルソナを基に、以下のキーを持つJSONオブジェクトを生成してください。
        - "kyokan_tweet": 恋活中の女性が「わかる〜！」と共感するような、アプリ利用のあるあるや悩みを交えた導入文（50文字程度、文字列）
        - "good_point": 調査したアプリの特に良い点を1つ、具体的な体験談のように紹介（40文字程度、文字列）
        - "caution_point": 実際に使ってみて感じた注意点や、「こういう人には向かないかも？」というリアルな視点を1つ（40文字程度、文字列）
        - "hashtags": 「#PR」は必ず追加し、その他に「#恋活」「#婚活」「#アプリ名」など、投稿内容に合うハッシュタグを3つまとめた配列（文字列の配列）

        ## 禁止事項
        - `#R-18` など、成人向けのハッシュタグは絶対に含めないでください。
        """

        """
        
        response = model.generate_content(prompt)
        
        # JSONモードなので、応答テキストをそのままJSONとして解析できる
        tweet_parts = json.loads(response.text)
        
        print("  ✅ コンテンツパーツのJSON解析に成功")
        return tweet_parts
        
    except Exception as e:
        print(f"  ❌ Geminiでのコンテンツ生成またはJSON解析に失敗: {e}")
        # エラー時にAIからの応答内容を確認できるようにログ出力
        if 'response' in locals():
            print(f"  - Geminiからの生の応答:\n{response.text}")
        return None
