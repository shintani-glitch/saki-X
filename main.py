# main.py

import sys
import os
import pytz
from datetime import datetime
import pyshorteners
from dotenv import load_dotenv

from sheets import get_eligible_app
from twitter_api import get_clients, upload_image, post_tweet
from content_generator import generate_tweet_parts

load_dotenv()

def main():
    print(f"\n--- 処理開始: {datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S')} ---")

    app_info = get_eligible_app()
    if not app_info:
        sys.exit("処理を終了します。")

    print("\nSTEP 2: X APIに接続中...")
    client_v2, api_v1 = get_clients()
    if not client_v2 or not api_v1:
        sys.exit("処理を終了します。")

    print("\nSTEP 3: Geminiでツイート内容を生成中...")
    tweet_parts = generate_tweet_parts(app_info)
    if not tweet_parts:
        sys.exit("処理を終了します。")

    print("\nSTEP 4: 投稿情報を準備中...")
    
    long_url = app_info.get('アフィリエイトリンク', '')
    short_url = long_url
    if long_url:
        try:
            s = pyshorteners.Shortener()
            short_url = s.tinyurl.short(long_url)
            print(f"  ✅ URLを短縮しました: {short_url}")
        except Exception as e:
            print(f"  ⚠️ URLの短縮に失敗: {e}。元のURLを使用します。")
    
    media_id = upload_image(api_v1, app_info.get('画像URL'))

    hashtags = tweet_parts.get('hashtags', [])
    banned_tags = ['#r-18', '#r18']
    filtered_hashtags = [tag for tag in hashtags if tag.lower() not in banned_tags]
    formatted_hashtags = " ".join(filtered_hashtags)
    print(f"  ✅ ハッシュタグを準備（フィルター後）: {formatted_hashtags}")

    # ★★★ ツイート本文の組み立てを修正 ★★★
    text = f"""{tweet_parts.get('kyokan_tweet', '')}

【ココが良い！💖】
{tweet_parts.get('good_point', '特におすすめのポイントがあります！')}

🔗 {short_url}

{formatted_hashtags}
"""
    print("  ✅ 投稿テキストを作成しました。")

    final_length = len(text)
    if final_length > 140:
        print(f"  ⚠️ 警告: 生成されたテキストが140文字を超えています。（現在 {final_length} 文字）")
    else:
        print(f"  ✅ 文字数チェックOK。（現在 {final_length} 文字）")
    
    print("--- 生成された投稿 ---")
    print(text)
    print("--------------------")

    post_tweet(client_v2, text, media_id)

    print(f"\n--- 処理完了: {datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S')} ---")


if __name__ == '__main__':
    main()
