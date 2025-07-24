# encoding = utf-8

import os
import pandas as pd
import logging
# uti = Utils()
# logger = uti.log_init()


class Utils():
    def __init__(self) -> None:
        self.log_init()


    def get_cur_script_user(self):
        import os
        import getpass
        import ctypes
        import ctypes.wintypes
        import subprocess

        # 方法一: os.getlogin()
        try:
            current_user = os.getlogin()
            print(f"当前执行脚本的用户是 (os.getlogin()): {current_user}")
        except OSError:
            print("无法获取当前登录用户 (os.getlogin())")

        # 方法二: getpass.getuser()
        current_user = getpass.getuser()
        print(current_user, '当前执行脚本的用户是')

    def get_script_name(self):
        import inspect
        """获取调用该函数的脚本的文件名（不带扩展名）"""
        # 获取调用栈信息
        frame = inspect.stack()[1]
        # 获取调用该函数的文件路径
        caller_file_path = frame.filename
        # 提取文件名（不带扩展名）
        file_name = os.path.basename(caller_file_path).split('.')[0]
        print(file_name)
        return file_name

    def log_init(self, file_name  = ''):
        import logging
        if not file_name:
            self.get_script_name()
        # raise Exception
        # self.get_cur_script_user()
        file_name = '%s.log' % file_name
        # 创建 Logger 实例
        self.checkout_file_is_exist(file_name)
        print(file_name,'file_name')
        self.checkout_dir_is_exist(file_name)

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)  # 设置全局日志级别

        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # 控制台只显示 INFO 及以上级别

        # 创建文件处理器
        file_handler = logging.FileHandler(file_name, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)  # 文件记录所有 DEBUG 及以上级别

        # 定义日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 将格式绑定到处理器
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # 将处理器添加到 Logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        # 使用示例
        return logger
    def read_df(self, file_path = ''):
        df = pd.read_excel(
            file_path )
        print('read file as df : %s' %  file_path)
        return df
    def insert_row(self, df, new_row):
        df.loc[len(df)] = new_row
        return df
    def find_keyword_in_file(self,file_path, keyword):
        # with open(file_path, 'r') as file:
        with open(file_path, 'r', errors='ignore') as file:
            for line_number, line in enumerate(file, start=1):
                # print(line, 'line')
                # print(keyword, 'keyword')

                if keyword in line:
                    # raise Exception
                    return line_number
        return -1  # 如果未找到关键字，返回-1
    
    def write_df(self, df=None, path = ''):

        df.to_excel(path,index=False)

    def json_d(self,response_data):
        import json
        json.dumps(response_data, ensure_ascii=False).encode('utf8')

if __name__ == "__main__":
    util = Utils()
    util.json_d()