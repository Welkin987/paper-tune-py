# Paper-Tune

A tool for automatically correcting grammar errors in academic papers using DeepSeek's LLM API.

## English Instructions

### Overview
Paper-Tune is a simple tool that helps researchers improve the grammar and language in their academic papers by leveraging DeepSeek's language model capabilities. The tool divides papers into manageable chunks, processes them through the API, and then recombines the corrected text.

### Setup
1. Run `init.bat` to create a Python virtual environment and install the required packages
2. Edit the `start.bat` file to add your DeepSeek API key
3. Place your paper in the `files` directory as `input.txt` (or with any other extension)
4. Run `start.bat` to process your paper

### Requirements
- Python 3.6+
- Internet connection
- DeepSeek API key

### Usage
1. Ensure only one `input.*` file exists in the `files` directory
2. Run `start.bat`
3. The corrected paper will be saved as `output.*` with the same extension as your input file

## 中文说明

### 概述
Paper-Tune 是一个简单的工具，通过利用 DeepSeek 的语言模型能力，帮助研究人员改进他们学术论文中的语法和语言表达。该工具将论文分成可管理的块，通过 API 处理它们，然后重新组合已更正的文本。

### 设置
1. 运行 `init.bat` 创建 Python 虚拟环境并安装所需的包
2. 编辑 `start.bat` 文件以添加您的 DeepSeek API 密钥
3. 将您的论文放在 `files` 目录中，命名为 `input.txt`（或使用任何其他扩展名）
4. 运行 `start.bat` 处理您的论文

### 要求
- Python 3.6+
- 网络连接
- DeepSeek API 密钥

### 使用方法
1. 确保 `files` 目录中只有一个 `input.*` 文件
2. 运行 `start.bat`
3. 修正后的论文将保存为 `output.*`，扩展名与您的输入文件相同
