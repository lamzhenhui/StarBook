#!/usr/bin/env python3
import os

# 模拟新的handle_get_static_files功能
def test_html_output():
    static_files = []
    base_url = "http://39.108.219.192/"
    
    # 检查static目录是否存在
    if not os.path.exists('static'):
        print("static目录不存在")
        return
    
    # 遍历static目录及其子目录
    for root, dirs, files in os.walk('static'):
        for file in files:
            # 获取相对路径
            relative_path = os.path.join(root, file)
            # 将路径转换为URL格式（使用正斜杠）
            url_path = relative_path.replace('\\', '/')
            # 添加URL前缀
            full_url = base_url + url_path
            static_files.append({
                'url': full_url,
                'name': file,
                'path': url_path
            })
    
    # 生成HTML页面
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Static文件列表</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }}
        .file-list {{
            list-style: none;
            padding: 0;
        }}
        .file-item {{
            margin: 10px 0;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 4px;
            transition: background-color 0.3s;
        }}
        .file-item:hover {{
            background: #e9ecef;
        }}
        .file-link {{
            color: #007bff;
            text-decoration: none;
            font-size: 14px;
        }}
        .file-link:hover {{
            text-decoration: underline;
        }}
        .file-path {{
            color: #666;
            font-size: 12px;
            margin-left: 10px;
        }}
        .count {{
            color: #28a745;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Static文件列表</h1>
        <p>共找到 <span class="count">{len(static_files)}</span> 个文件</p>
        <ul class="file-list">
"""
    
    for file_info in static_files:
        html_content += f"""
            <li class="file-item">
                <a href="{file_info['url']}" class="file-link" target="_blank">{file_info['name']}</a>
                <span class="file-path">({file_info['path']})</span>
            </li>
"""
    
    html_content += """
        </ul>
    </div>
</body>
</html>
"""
    
    # 保存HTML文件用于查看
    with open('static_files_list.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("HTML页面已生成: static_files_list.html")
    print(f"共找到 {len(static_files)} 个文件")
    for file_info in static_files:
        print(f"- {file_info['name']}: {file_info['url']}")

if __name__ == "__main__":
    test_html_output()