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
            'gemini-2.5-flash',
            generation_config=generation_config
        )

        # ★★★ プロンプトを新しい構成に合わせて全面的に修正 ★★★
        prompt = f"""
        # 指令書: 140文字以内のX(Twitter)投稿用パーツ生成

        ## あなたのペルソナ
        あなたは、マッチングアプリを紹介する27歳のOL「さき」です。
        アプリの魅力を、友達に教えるような親しみやすい口調で、ポイントを簡潔に紹介してください。

        ## 最終的なツイートの構造
        あなたが生成したパーツは、以下のテンプレートに埋め込まれて1つのツイートになります。
        ```
        💖『{app_info.get('アプリ名', '')}』のおすすめポイント💖

        ✅ {{good_point_1}}
        ✅ {{good_point_2}}

        詳しくはこちら👇
        🔗 (URL)

        #PR {{hashtags}}
        ```

        ## 絶対的なルール
        1.  上記の構造と、あなたが生成する全パーツを組み合わせた最終的なツイート全体の文字数が、**絶対に140文字を超えないようにしてください。**
        2.  文字数計算の際、 `🔗 (URL)` の部分は **23文字**としてカウントしてください。
        3.  この文字数制限を守るために、あなたが生成する `good_point_1` と `good_point_2` の長さを賢く調整してください。

        ## 実行タスク
        Webで「{app_info.get('アプリ名', '')}」のリアルな評判を調査し、上記ルールを厳守した上で、以下のキーを持つJSONオブジェクトを生成してください。
        - "good_point_1": アプリの良い点を1つ、簡潔に紹介。
        - "good_point_2": アプリの良い点をもう1つ、簡潔に紹介。
        - "hashtags": 投稿に合うハッシュタグを**3つ**まとめた配列。（`#PR`は含めないでください）

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
