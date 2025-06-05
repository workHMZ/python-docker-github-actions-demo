from openai import OpenAI
import os

# 尝试加载.env文件（如果存在）
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # 如果没有安装python-dotenv，继续使用系统环境变量
    pass

def main():
    # 初始化OpenAI客户端
    client = OpenAI()
    
    # 对话ID，用于维护服务器端的对话状态
    conversation_id = None
    
    print("OpenAI Responses API 连续对话程序")
    print("输入 'quit' 或 'exit' 退出程序")
    print("输入 'new' 开始新对话")
    print("-" * 50)
    
    while True:
        try:
            # 获取用户输入
            user_input = input("\n您: ").strip()
            
            # 检查退出命令
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("再见！")
                break
            
            # 检查新对话命令
            if user_input.lower() in ['new', '新对话']:
                conversation_id = None
                print("开始新对话")
                continue
            
            # 如果输入为空，跳过
            if not user_input:
                continue
            
            # 构建API请求参数
            request_params = {
                "model": "gpt-4.1",
                "input": [
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            }
            
            # 如果有对话ID，添加到请求中以继续对话
            if conversation_id:
                request_params["id"] = conversation_id
            
            # 调用OpenAI API
            print("AI正在思考...")
            response = client.responses.create(**request_params)
            
            # 获取AI回复和对话ID
            ai_response = response.output_text
            conversation_id = response.id  # 保存对话ID用于后续请求
            
            # 显示AI回复
            print(f"\nAI: {ai_response}")
            
            # 显示对话ID（可选，用于调试）
            if conversation_id:
                print(f"[对话ID: {conversation_id[:8]}...]")
            
        except KeyboardInterrupt:
            print("\n\n程序被用户中断")
            break
        except Exception as e:
            print(f"\n发生错误: {e}")
            print("请检查您的API密钥和网络连接")
            
            # 询问是否继续
            continue_chat = input("是否继续？(y/n): ").strip().lower()
            if continue_chat not in ['y', 'yes', '是']:
                break

def check_api_key():
    """检查API密钥是否设置"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("错误: 未找到OPENAI_API_KEY环境变量")
        print("请设置您的OpenAI API密钥:")
        print("方法1 - 环境变量:")
        print("  Linux/Mac: export OPENAI_API_KEY='your-api-key-here'")
        print("  Windows: set OPENAI_API_KEY=your-api-key-here")
        print("方法2 - .env文件:")
        print("  创建.env文件并添加: OPENAI_API_KEY=your-api-key-here")
        print("  (确保.env文件在.gitignore中)")
        return False
    return True

if __name__ == "__main__":
    # 检查API密钥
    if check_api_key():
        main()
    else:
        print("程序退出")