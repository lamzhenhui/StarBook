#!/usr/bin/env python3
import os
import json

# 模拟新添加的GET方法功能
def test_get_static_files():
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
            static_files.append(full_url)
    
    # 输出结果
    result = {
        "status": "success",
        "files": static_files,
        "count": len(static_files)
    }
    
    print("测试结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_get_static_files()