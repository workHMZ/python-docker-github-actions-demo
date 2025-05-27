import requests
import json
from datetime import datetime

# 设置目标 URL（百度热搜 API）
baidu_hotsearch_url = "https://top.baidu.com/api/board?tab=realtime"

# 设置请求头，模拟浏览器行为以避免反爬机制
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://top.baidu.com/board',
    'Accept': 'application/json, text/plain, */*'
}

# 保存结果到文件的函数
def save_to_file(data, filename="baidu_hotsearch.json"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output_data = {
        "timestamp": timestamp,
        "hotsearch": data
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    print(f"Data saved to {filename}")

# 爬取百度热搜数据的函数
def scrape_baidu_hotsearch():
    try:
        # 发送请求并设置超时时间
        response = requests.get(baidu_hotsearch_url, headers=headers, timeout=10)
        
        # 打印调试信息
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        
        # 输出响应内容的前 200 个字符以便调试
        response_text = response.text[:200] if len(response.text) > 200 else response.text
        print(f"Response Content (first 200 chars): {response_text}")

        if response.status_code == 200:
            # 尝试解析 JSON 数据
            try:
                data = response.json()
                # 检查是否包含热搜数据
                if 'data' in data and 'cards' in data['data'] and len(data['data']['cards']) > 0:
                    hotsearch_list = data['data']['cards'][0].get('content', [])
                    print("Successfully retrieved Baidu hotsearch data.")
                    return hotsearch_list
                else:
                    print("Unexpected data format received or no hotsearch data found.")
                    return {"error": "Unexpected data format or no data"}
            except json.JSONDecodeError as e:
                error_msg = f"Error decoding JSON: {e}"
                print(error_msg)
                print("Response might not be in JSON format. Check the content above.")
                return {"error": error_msg}
        else:
            error_msg = f"Failed to retrieve data. Status code: {response.status_code}"
            print(error_msg)
            return {"error": error_msg}

    except requests.exceptions.RequestException as e:
        error_msg = f"Error during request: {e}\nPlease check your internet connection or the URL."
        print(error_msg)
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        print(error_msg)
        return {"error": error_msg}

# 自定义显示函数，避免字段重复带来的视觉混乱
def display_hotsearch_data(data):
    simplified_data = []
    for item in data[:10]:  # 仅显示前 10 条
        simplified_item = {
            "index": item["index"],
            "word": item["word"],
            "desc": item["desc"] if item["desc"] else "No description available",
            "hotScore": item["hotScore"],
            "hotChange": item["hotChange"]
        }
        simplified_data.append(simplified_item)
    return simplified_data

# 主函数
if __name__ == "__main__":
    print("Starting web scraping for Baidu Hotsearch...")
    hotsearch_data = scrape_baidu_hotsearch()
    
    # 打印结果为 JSON 格式，确保标题只出现一次
    if "error" not in hotsearch_data:
        print("\n=== Baidu Hotsearch Data (JSON Format) ===")
        # 显示简化的数据，避免重复字段
        simplified_data = display_hotsearch_data(hotsearch_data)
        print(json.dumps(simplified_data, ensure_ascii=False, indent=2))
        print("\nNote: Only selected fields and first 5 items are shown above for clarity.")
        print("Full data with all fields is saved in the JSON file.")
        
        # 保存完整数据到 JSON 文件
        #save_to_file(hotsearch_data)
    else:
        print(f"\nError: {hotsearch_data['error']}")
    
    print("\n热搜爬取完毕.")
