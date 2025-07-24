# encoding = utf-8

from utils import Utils
import logging
uti = Utils()
logger = uti.log_init()
import PyPDF2
from utils import Utils
uti = Utils()
class ReadPdf():
    def __init__(self,wrt_path='') -> None:
        self.wrt_path = wrt_path
    def pdf_to_text(self,pdf_path):
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        return text
    def run_pdf_to_text(self,pdf_path):
        pdf_path = 'deepl.pdf'
        text = self.pdf_to_text(pdf_path)
        with open('deepl.txt', 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)
    def find_line(self, task_name = 'deepl',keyword = ''):
        path = self.read_file_path(task_name=task_name)
        return uti.find_keyword_in_file(file_path = path,keyword=keyword)

    def read_lines_from_file(self,file_path, start_line, page_rows=30):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                # 获取指定范围的行
                selected_lines = lines[start_line-1:start_line+page_rows]
                return ''.join(selected_lines)
        except Exception as e:
            logger.error(e)
    def find_row_with_keyword(self, df,keyword):
        for idx, row in df.iterrows():
            for cell in row:
                if isinstance(cell, str) and keyword in cell:
                    return idx + 1  # 返回行号，从1开始计数
        return None  # 如果没有找到，返回None
    def is_first_row_empty(self,df=None, check_row = 0):
        
        if df.empty:
            return True
        
        if check_row < 0 or check_row >= len(df):
            print(f"Row index {check_row} is out of bounds")
            return True
        first_row = df.iloc[check_row]
        return first_row.isnull().all()
        
    def add_task(self,path='', task_name = '', start_page_index =0, update_type =1):
        """
        update_type : 1 代表增加
        """


        tag_df = uti.read_df(self.wrt_path)
        # self.find_row_with_keyword(tag_df,'')
        begin_row_index = 0 
        # ret = self.is_first_row_empty(df = tag_df,check_row = 2)
        # print(ret)
        new_row = [task_name,	path,	0,	0]
        for item in range(1000):
            if self.is_first_row_empty(df = tag_df,check_row = item):
                uti.insert_row(tag_df,new_row=new_row)
                uti.write_df(df=tag_df,path=self.wrt_path)
                break
    def update_task(self,path='', task_name = '', is_done =0):
        """
        update_type : 1 代表增加
        """
        tag_df = uti.read_df(self.wrt_path)
        row_val =self.find_row_with_keyword(tag_df,task_name)
        print(row_val)
    def update_start_line(self,path='', task_name = 'deepl', is_done =0,update_index =0):
        """
        update_type : 1 代表增加
        """
        tag_df = uti.read_df(self.wrt_path)
        row_val =self.find_row_with_keyword(tag_df,task_name)
        default_add = 10
        if update_index :
            default_add =update_index
            tag_df.loc[row_val-1, 
                'page_index'
                ] =default_add
            uti.write_df(tag_df,path=self.wrt_path)
            return 
        if is_done:
            get_val =tag_df.loc[row_val-1, 
                'is_done'
                ]
            print(get_val, 'get_val')
            if get_val != 1 and is_done:
                # tag_df.loc[row_val-1, 
                # 'is_done'
                # ] =0
                tag_df.loc[row_val-1, 
                'page_index'
                ] +=default_add
        else:
            tag_df.loc[row_val-1, 
                'page_index'
                ] -=default_add


        uti.write_df(tag_df,path=self.wrt_path)
        print(row_val)

    def read_file_start_line(self,task_name =''):
        df = uti.read_df(self.wrt_path)
        task_row =self.find_row_with_keyword(df,keyword=task_name)
        print(task_row , 'task_row')
        info =df.loc[task_row-1, 
               'page_index'
               ]
        # print(info)
        return info
    def read_file_path(self,task_name =''):
        df = uti.read_df(self.wrt_path)
        task_row =self.find_row_with_keyword(df=df,keyword=task_name)
        print(task_row , 'task_row')
        info =df.loc[task_row-1, 
               'file_path'
               ]
        # print(info)
        return info


    def read_book(self, task_name='deepl',start_line=0,page_rows = 30):
        try:
            path = self.read_file_path(task_name=task_name)
            if not start_line:
                book_index = self.read_file_start_line(task_name= task_name)
                
                print('get book index %s' % book_index)
            else:
                book_index = start_line
        except Exception as e:
            logger.error(e)
        # path = self.read_file_start_line(task_name=task_name)
        logger.info('>>>2')
        return self.run_read_lines_from_file(path,start_line=book_index,page_rows=page_rows)


    def run_read_lines_from_file(self,file_path='', start_line=1, page_rows=30):
        # 示例用法
        logger.info('run_read_lines_from_file>>>')
        try:
            content = self.read_lines_from_file(file_path, start_line,page_rows=page_rows)
            logger.info(content)
            logger.info('content>>>')
        except Exception as e:
            logger.error(e)
        return content
if __name__ == '__main__':
    rp = ReadPdf(wrt_path='/opt/code/post_app/book_helper.xlsx')
    # rp.run_read_lines_from_file()
    # rp.add_task(
    #     path='/opt/code/post_app/2305_11344.txt',
    #     task_name='2305_11344'

    # )
    # rp.update_task(task_name='deepl')
    #阅读
    
    print(rp.read_book(task_name='2305_11344',
    page_rows = 1
                    #    , start_line = 2
                       ))
    # print(rp.read_book(task_name='gpt_as'
    #                 #    , start_line = 2
    #                    ))
    
    # 找到对应的页数
    # print(rp.find_line(task_name='deepl', keyword='成到球壳'))

    # 翻页
    # rp.update_start_line(is_done= 1, update_index = 11405)
