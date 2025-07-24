# encoding = utf-8

import os
import pandas as pd
import datetime
import fitz  # PyMuPDF
from PIL import Image
import io
from dateutil.relativedelta import relativedelta


class Utils():
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
    def  checkout_file_is_exist(self, path):
        from pathlib import Path

        file_path = Path(path)

        # 检查文件是否存在
        if not file_path.exists():
            # 文件不存在，创建文件
            file_path.touch()  # 创建空文件
            print(f"文件 {file_path} 已创建")
        else:
            print(f"文件 {file_path} 已存在")
        # else:
        #     print('目录已存在')
    def log_init(self,file_name = 'test'):
        import logging
        if not file_name:
            self.get_script_name()
        # raise Exception
        self.get_cur_script_user()
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

    def dow_file(self, url):
        #     print('>')
        #     import requests

        #     url = "https://arxiv.org/pdf/2503.10547"
        #     response = requests.get(url)

        #     if response.status_code == 200:
        #         with open("2503.10547.pdf", "wb") as file:
        #             file.write(response.content)
        #         print("文件下载成功")
        #     else:
        #         print(f"下载失败，状态码: {response.status_code}")
        import requests
        file_no = url.split('/')[-1]

        # 要下载的 PDF 文件 URL
        # url = "https://arxiv.org/pdf/2503.10547"

        # 发送请求获取内容
        out_path = "/Users/meta/lam/deep/Understanding/Chinese-Pretrain-MRC-Model/app/files/input/%s.pdf" % file_no
        if os.path.exists(out_path):
            return out_path
            print("文件存在")
        response = requests.get(url, stream=True)

        # 确保请求成功
        if response.status_code == 200:
            with open(out_path,
                      "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print("下载完成：%s.pdf" % file_no)
        else:
            print("下载失败，状态码：", response.status_code)
        return out_path

    def get_date_columns(self, str_info='',
                         cur_date=None,
                         date_formate='%Y%m',
                         db_type='', before_month_cnt=0,
                         ):
        """
        获取当前时间
        :return: 注意:cur_date 如果不指定, 默认为当月一号
        """
        import datetime
        if not cur_date:  # 默认查询当月的一号零点
            cur_date = datetime.datetime.strptime(
                datetime.datetime.now().strftime('%Y%m'), '%Y%m')
        # print(cur_date, 'cur_date')
        if str_info == '该月最后一天的零点':
            return (cur_date.
                    replace(day=1) +
                    relativedelta(months=1) -
                    datetime.timedelta(days=1)).strftime(date_formate)
        elif str_info == '该月月份':
            return (cur_date).strftime(date_formate)
        elif str_info == '上月月份':
            return (cur_date +
                    relativedelta(months=-1)).strftime(date_formate)
        elif str_info == '下月月份':
            return (cur_date +
                    relativedelta(months=1)).strftime(date_formate)
        elif str_info == '上6个月月份':
            return (cur_date +
                    relativedelta(months=-6)).strftime(date_formate)
        elif str_info == '上3个月月份':
            return (cur_date +
                    relativedelta(months=-3)).strftime(date_formate)
        elif str_info == '上n个月月份':
            return (cur_date +
                    relativedelta(months=-before_month_cnt)).strftime(date_formate)
        elif str_info == '上n个月月份的最后一天':
            return ((cur_date +
                     relativedelta(months=-before_month_cnt+1)).
                    replace(day=1)-datetime.timedelta(days=1)).strftime(date_formate)
        elif str_info == '该月一号的零点':
            return (cur_date.
                    replace(day=1)).strftime(date_formate)  # '202304' # 查询两月前
        elif str_info == '上月一号的零点':

            return (cur_date +
                    relativedelta(months=-1)).replace(day=1).strftime(date_formate)  # '202304' # 查询两月前
        elif str_info == '上月最后一天':

            return (cur_date.
                    replace(day=1)-datetime.timedelta(days=1)).strftime(date_formate)  # '202304' # 查询两月前
        elif str_info == '下月一号的零点':

            return (cur_date +
                    relativedelta(months=1)).replace(
                day=1).strftime(date_formate)  # '202304' # 查询两月前
        elif str_info == '该月上周':
            return (cur_date -
                    relativedelta(weeks=1)).strftime(date_formate)  # '202304' # 查询两月前
        elif str_info == '该月上上周':
            return (cur_date -
                    relativedelta(weeks=2)).strftime(date_formate)  # '202304' # 查询两月前

        # elif  str_info == '今天':
        #     return (cur_date).strftime(date_formate)  # '202304' # 查询两月前
        elif str_info == '今天零点':
            cur_date = datetime.datetime.now()
            return (cur_date).strftime(date_formate)  # '202304' # 查询两月前
        elif str_info == '昨天':
            cur_date = datetime.datetime.now()
            # '202304' # 查询两月前
            return (cur_date - relativedelta(days=1)).strftime(date_formate)
        elif str_info == '前天':
            cur_date = datetime.datetime.now()
            # '202304' # 查询两月前
            return (cur_date - relativedelta(days=2)).strftime(date_formate)
        elif str_info == '年初':
            from datetime import datetime, time

            # 获取当前年份
            current_year = datetime.now().year

            # 创建年初的 datetime 对象，指定时间为 00:00:00
            beginning_of_year = datetime.combine(
                datetime(current_year, 1, 1), time())

            # print(beginning_of_year)
            return beginning_of_year.strftime(date_formate)  # '202304' # 查询两月前
        else:
            return ''

    def read_df(self, file_path=''):
        df = pd.read_excel(
            file_path)
        print('read file as df : %s' % file_path)
        return df

    def insert_row(self, df, new_row):
        df.loc[len(df)] = new_row
        return df

    def find_keyword_in_file(self, file_path, keyword):
        # with open(file_path, 'r') as file:
        with open(file_path, 'r', errors='ignore') as file:
            for line_number, line in enumerate(file, start=1):
                # print(line, 'line')
                # print(keyword, 'keyword')

                if keyword in line:
                    # raise Exception
                    return line_number
        return -1  # 如果未找到关键字，返回-1

    def write_df(self, df=None, path=''):

        df.to_excel(path, index=False)

    def json_d(self, response_data):
        import json
        json.dumps(response_data, ensure_ascii=False).encode('utf8')

    def pdf_to_text_with_images(
            self, pdf_path, output_text_path, output_image_folder, need_return_text=False):
        # 打开PDF文件
        import fitz
        pdf_document = fitz.open(pdf_path)
        text_content = ""

        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            # print(page)
            # raise Exception
            text_content += page.get_text("text")

            # 提取图片
            image_list = page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image = Image.open(io.BytesIO(image_bytes))
                image_path = f"{output_image_folder}/page_{page_num + 1}_img_{img_index + 1}.{image_ext}"
                image.save(image_path)
                text_content += f"\n[Image saved as {image_path}]\n"

        # 将文本内容写入文件
        with open(output_text_path, "w", encoding="utf-8") as text_file:
            text_file.write(text_content)
        if need_return_text:
            return text_content

    def read_pdf(self,
                 pdf_path='/Users/meta/lam/deep/Understanding/Chinese-Pretrain-MRC-Model/app/files/input/2503.10547.pdf',
                 output_text_path='/Users/meta/lam/deep/Understanding/Chinese-Pretrain-MRC-Model/app/files/output/output_text.txt',
                 output_image_folder='/Users/meta/lam/deep/Understanding/Chinese-Pretrain-MRC-Model/app/files/output/images',
                 need_return_text=True):

        # 使用示例
        pdf_path = pdf_path
        output_text_path = output_text_path
        output_image_folder = output_image_folder

        import os
        if not os.path.exists(output_image_folder):
            os.makedirs(output_image_folder)

        return self.pdf_to_text_with_images(
            pdf_path, output_text_path, output_image_folder, need_return_text=need_return_text)

    def checkout_dir_is_exist(self, path):
        from pathlib import Path
        path_obj = Path(path)
        folder_path = str(path_obj.parent)
        print('检查路径是否存在:%s' % path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
            print('路径已创建:%s' % path)
        else:
            print('目录已存在')

    def get_filename_date_tag(self):
        return "dt_%s" % datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def write_file(self, filename, data, mod='a'):
        import datetime

        self.checkout_dir_is_exist(path=filename)
        with open(filename, mod, encoding="utf-8") as file:
            file.write('%s%s' % (datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"), '文件开始写入\n'))
            for msg in data:
                file.write('{ms}\n'.format(ms=msg))


if __name__ == "__main__":
    tool = Utils()
    # print(tool.get_date_columns(str_info='该月最后一天的零点'))
    print(tool.dow_file())
    # print(tool.read_pdf())
