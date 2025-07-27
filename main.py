# main.py

import sys
import os
import pytz
from datetime import datetime
import pyshorteners
from dotenv import load_dotenv

# 各モジュールから関数をインポート
from sheets import get_eligible_app
from twitter_api import get_clients, upload_image, post_tweet
from content_generator import generate_tweet_parts

# 環境変数をロード
load_dotenv()

# --- メイン処理 ---
def main():
    print(f"\n--- 処理開始: {datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S')} ---")

    # STEP 1: スプレッドシートから投稿対象のアプリ情報を取得
    app_info = get_eligible_app()
    if not app_info:
        sys.exit("処理を終了します。")

    # STEP 2: X (Twitter) APIに接続
    print("\nSTEP 2: X APIに接続中...")
    client_v2, api_v1 = get_clients()
    if not client_v2 or not api_v1:
        sys.exit("処理を終了します。")

    # STEP 3: Geminiでツイート内容を生成
    print("\nSTEP 3: Geminiでツイート内容を生成中...")
    tweet_parts = generate_tweet_parts(app_info)
    if not tweet_parts:
        sys.exit("処理を終了します。")

    # STEP 4: 投稿に必要な情報を準備
    print("\nSTEP 4: 投稿情報を準備中...")
    
    # 4-1. アフィリエイトリンクを短縮
    long_url = app_info.get('アフィリエイトリンク', '')
    short_url = long_url
    if long_url:
        try:
            s = pyshorteners.Shortener()
            short_url = s.tinyurl.short(long_url)
            print(f"  ✅ URLを短縮しました: {short_url}")
        except Exception as e:
            print(f"  ⚠️ URLの短縮に失敗: {e}。元のURLを使用します。")
    
    # 4-2. 画像をアップロード
    media_id = upload_image(api_v1, app_info.get('画像URL'))

    # 4-3. ハッシュタグをフォーマット
    hashtags = tweet_parts.get('hashtags', [])
    formatted_hashtags = " ".join(hashtags)
    print(f"  ✅ ハッシュタグを準備: {formatted_hashtags}")

    # 4-4. ★★★ ツイート本文を「さき」のキャラクターに合わせて組み立て ★★★
    app_name = app_info.get('アプリ名', 'このアプリ')
    
    text = f"""{tweet_parts.get('kyokan_tweet', '')}

『{app_name}』を使ってみた私の正直レポ✍️

【ココが良い！💖】
{tweet_parts.get('good_point', '特におすすめのポイントがあります！')}

【注意したいかも…⚠️】
{tweet_parts.get('caution_point', '人によっては合わない部分もあるかも。')}

個人的な感想だけど、参考になると嬉しいな〜！
みんなはどう思う？🤔

🔗 {short_url}

{formatted_hashtags}
"""
    print("  ✅ 投稿テキストを作成しました。")
    print("--- 生成された投稿 ---")
    print(text)
    print("--------------------")


    # STEP 5: X (Twitter)に投稿
    post_tweet(client_v2, text, media_id)

    print(f"\n--- 処理完了: {datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S')} ---")


if __name__ == '__main__':
    main()
