此项目可以调用LLM api自动修改论文的语法错误

src目录下有以下文件：
- main.py: 主程序
- ask.py: 里面存放ask函数，传入一段str，返回LLM的回复，调用openai的标准库（见下文）

prompt目录下有以下文件：
- prompt.txt: 每次请求的prompt，其中的“[content]”用真实的上下文替代，不要修改该文件
- demands.md: 用于描述项目整体需求，不要修改

files目录下有以下文件:
- input.\*: 输入的论文
- optput.\*: 输出的论文

此外在项目根目录下还有以下文件：
- init.bat: 创建项目python虚拟环境，即venv目录（在项目根目录），安装必要的库
- start.bat: 调用main进行论文修改
- README.md: 项目说明，有英文和中文版本，符合github格式
- .gitignore: 无视venv等内容

start.bat设置的环境变量：
BASE_URL="https://api.deepseek.com",
MODEL="deepseek-chat",
API_KEY="<DeepSeek API Key>"
MAX_CHAR=2048

请求示例：
```
# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)
```

main.py运行逻辑（与用户的交互用英文输出）；
1. 检索files目录下形如input.\*的文件数目，若不存在或有多个，提醒用户需要唯一的files目录下形如input.\*的文件，当前有x个，并结束程序。若存在唯一，则告知用户该文件名，BASE_URL，MODEL，MAX_CHAR。若API_KEY="<DeepSeek API Key>"，提醒用户在start.bat设置API Key并结束程序，否则提醒用户API Key已设定，Press Enter to continue
2. 读取该input文件，从第一行开始取行，使得总字符数恰好小于MAX_CHAR（即再多一行就大于MAX_CHAR）。若第一行已经大于MAX_CHAR，则只取第一行。用这些内容替换掉prompt.txt中的"[content]\n"，然后调用ask函数进行请求，将请求的结果保存下来。之后不断按照类似规则分块请求直到结束，把所有LLM的回复拼接起来输出到output文件，后缀名与input文件相同，然后提示用户任务成功。