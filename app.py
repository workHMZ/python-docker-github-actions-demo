import requests
import json
from datetime import datetime

# --- 全局设置 / グローバル設定 ---

# 设置目标 URL (百度热搜 API)
# ターゲットURLを設定 (BaiduホットリサーチAPI)
baidu_hotsearch_url = "https://top.baidu.com/api/board?tab=realtime"

# 设置请求头，模拟浏览器行为以避免反爬机制
# リクエストヘッダーを設定し、ブラウザの挙動を模倣してスクレイピング対策を回避
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://top.baidu.com/board',
    'Accept': 'application/json, text/plain, */*'
}

# --- 函数定义 / 関数定義 ---

def print_header(title_cn, title_ja):
    """
    打印美化后的标题框。
    整形されたタイトルボックスを出力する。
    """
    print("\n" + "#" * 80)
    print(f"## {title_cn}")
    print(f"## {title_ja}")
    print("#" * 80)

def print_footer(message_cn, message_ja):
    """
    打印美化后的结尾框。
    整形されたフッターボックスを出力する。
    """
    print("#" * 80)
    print(f"## {message_cn}")
    print(f"## {message_ja}")
    print("#" * 80)


def scrape_baidu_hotsearch():
    """
    爬取百度热搜数据的函数。
    Baiduホットリサーチデータをスクレイピングする関数。
    """
    try:
        # 发送请求并设置10秒超时
        # リクエストを送信し、タイムアウトを10秒に設定
        response = requests.get(baidu_hotsearch_url, headers=headers, timeout=10)
        
        # 检查HTTP响应状态码，确保请求成功
        # HTTPレスポンスのステータスコードをチェックし、リクエストが成功したことを確認
        if response.status_code == 200:
            try:
                data = response.json()
                # 检查返回的数据结构是否符合预期
                # 返されたデータ構造が期待通りか確認
                if 'data' in data and 'cards' in data['data'] and len(data['data']['cards']) > 0:
                    hotsearch_list = data['data']['cards'][0].get('content', [])
                    print("[OK] 成功获取并解析了热搜数据 / [OK] ホットリサーチデータの取得と解析に成功しました。")
                    return hotsearch_list
                else:
                    print("[Error] 返回的数据格式不正确或数据为空 / [Error] 受信したデータ形式が正しくないか、データが空です。")
                    return {"error": "Unexpected data format or no data"}
            except json.JSONDecodeError:
                print(f"[Error] JSON 解析失败 / [Error] JSON のデコードに失敗しました。")
                return {"error": "Error decoding JSON"}
        else:
            print(f"[Error] 请求失败，状态码 / [Error] リクエストに失敗しました。ステータスコード: {response.status_code}")
            return {"error": f"Failed to retrieve data. Status code: {response.status_code}"}

    except requests.exceptions.RequestException as e:
        print(f"[Error] 网络请求期间发生错误 / [Error] リクエスト中にエラーが発生しました: {e}")
        return {"error": f"Error during request: {e}"}
    except Exception as e:
        print(f"[Error] 发生未知错误 / [Error] 不明なエラーが発生しました: {e}")
        return {"error": f"Unexpected error: {e}"}

def display_hotsearch_data(data):
    """
    自定义显示函数，提取关键字段并格式化，仅显示前10条。
    カスタム表示関数。主要なフィールドを抽出し、見やすくフォーマットする（最初の10件のみ表示）。
    """
    simplified_data = []
    # 仅提取前10条数据用于展示
    # 最初の10件のデータのみを抽出して表示
    for item in data[:10]:
        simplified_item = {
            "排名 (Rank)": item.get("index", "N/A"),
            "关键词 (Keyword)": item.get("word", "N/A"),
            "描述 (Description)": item.get("desc", "没有描述 / 説明なし"),
            "热度 (Score)": item.get("hotScore", 0)
        }
        simplified_data.append(simplified_item)
    return simplified_data

# --- 主程序入口 / メインプログラム ---
if __name__ == "__main__":
    print_header("开始爬取百度实时热搜榜", "Baiduリアルタイムホットリサーチのスクレイピングを開始します")
    
    hotsearch_data = scrape_baidu_hotsearch()
    
    # 如果没有错误，则打印结果
    # エラーがない場合は結果を出力
    if "error" not in hotsearch_data:
        print_header("百度热搜榜 Top 10 (JSON 格式)", "Baiduホットリサーチ Top 10 (JSONフォーマット)")
        
        # 显示简化的、格式化的数据
        # シンプルで整形されたデータを表示
        simplified_data = display_hotsearch_data(hotsearch_data)
        
        # 使用json.dumps美化输出，并设置 ensure_ascii=False 以正确显示中文和日文
        # json.dumpsを使用して出力を整形し、ensure_ascii=Falseで日本語と中国語を正しく表示
        print(json.dumps(simplified_data, ensure_ascii=False, indent=4))
        
        print_footer("数据爬取和展示完成", "データのスクレイピングと表示が完了しました")
    else:
        # 如果有错误，则打印错误信息
        # エラーがある場合はエラーメッセージを出力
        print_footer(f"程序出错: {hotsearch_data['error']}", f"プログラムエラー: {hotsearch_data['error']}")