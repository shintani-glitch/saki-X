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
        generation_config = genai_types.GenerationConfig(
            response_mime_type="application/json"
        )
        
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        
        model = genai.GenerativeModel(
            'gemini-1.5-flash',
            generation_config=generation_config
        )

        # ★★★ プロンプトを新しい構成に合わせて修正 ★★★
        prompt = f"""
        # 指令書: 140文字以内のX(Twitter)投稿用パーツ生成

        ## あなたのペルソナ
        あなたは、マッチングアプリで彼氏探しに奮闘する27歳のOL「さき」です。
        一人称は「私」で、友達に話すような親しみやすい口調でお願いします。

        ## 最終的なツイートの構造
        あなたが生成したパーツは、以下のテンプレートに埋め込まれて1つのツイートになります。
        ```
        {{kyokan_tweet}}

        【ココが良い！💖】
        {{good_point}}

        🔗 (URL)

        {{hashtags}}
        ```

        ## 絶対的なルール
        1.  上記の構造と、あなたが生成する全パーツを組み合わせた最終的なツイート全体の文字数が、**絶対に140文字を超えないようにしてください。**
        2.  文字数計算の際、 `🔗 (URL)` の部分は **23文字** としてカウントしてください。
        3.  この文字数制限を守るために、あなたが生成する `kyokan_tweet`, `good_point` の長さを賢く調整してください。

        ## 実行タスク
        Webで「{app_info.get('アプリ名', '')}」のリアルな評判を調査し、上記ルールを厳守した上で、以下のキーを持つJSONオブジェクトを生成してください。
        - "kyokan_tweet": 恋活中の女性が共感するような導入文。
        - "good_point": アプリの良い点を体験談のように紹介。
        - "hashtags": 「#PR」は必ず含め、投稿に合うハッシュタグを3つまとめた配列。

        ## 禁止事項
        - 成人向けや不適切なハッシュタグは絶対に含めないでください。
        """
        
        response = model.generate_content(prompt)
        
        tweet_parts = json.loads(response.text)
        
        print("  ✅ コンテンツパーツのJSON解析に成功")
        return tweet_parts
        
    except Exception as e:
        print(f"  ❌ Geminiでのコンテンツ生成またはJSON解析に失敗: {e}")
        if 'response' in locals():
            print(f"  - Geminiからの生の応答:\n{response.text}")
        return None
