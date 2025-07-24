import pandas as pd
import numpy as np
import ast
from utils import Utils
from datetime import datetime
from datetime import datetime, timedelta
from fractions import Fraction

import logging
uti = Utils()
logger = uti.log_init()
# logger.debug("调试信息")
# raise Exception
row_dic = {
    'machin_learn': 0,
    'lose_money': 6,
    # "面试刷题",
    # "python高级",
    # "数据结构",
    # "成考",
    # "知乎",
    # "自考刷题",
    # "mysql，k8s，http"


}
hour_detail = {

}


class ExcelControl():
    def __init__(self, red_path='', wrt_path='') -> None:
        self.red_path = red_path
        self.wrt_path = wrt_path
        self.tmp_path = './report_tmp.xlsx'

    def get_week_ind(self):
        pass

    def read_df(self, file_path = ''):
        df = pd.read_excel(
            file_path if file_path else  self.red_path )
        logger.info('read file as df : %s' %  file_path)
        return df

    def write_df(self, df=None):
        uti.write_df(df= df,path=self.wrt_path)

    def update_df(self, tag_df = None, task_name='machin_learn', day_ind='', 
                  day_before_cnt = 0,
                  update_type=True, add_values =1):
        """
        day_ind =  周几 数字
        update_type =  1 代表加, 0 代表减"""
        try:
            if update_type:
                add_val = float(add_values)
            else:
                add_val = -float(add_values)
            logger.info("%s %s" % (add_val,'add_val'))
            if not tag_df:
                tag_df = self.read_df(self.wrt_path)
            logger.info('update weekday %s: ' % self.get_cur_year_week_weekday(
                day_before_cnt=day_before_cnt)[2])
            

            if not day_ind:
                target_val = tag_df.loc[row_dic.get(task_name),
                                self.get_cur_year_week_weekday(
                                    day_before_cnt=day_before_cnt)[2]]
                if np.isnan(target_val) :
                    logger.info('查询数值nan')
                    target_val = 0
                logger.info('更新所在周信息%s' % self.get_cur_year_week_weekday(
                                                   day_before_cnt=day_before_cnt)[2] )
                logger.info('打印更新数值')
                
                logger.info(float(target_val))
                logger.info(float(add_val))
                logger.info('>>>>')
                # logger.info(float(
                #             target_val) +add_val)
                logger.info(tag_df.loc[
                    row_dic.get(task_name), 
                    self.get_cur_year_week_weekday(
                        day_before_cnt=day_before_cnt)[2]])
                logger.info('更新前数值')

                tag_df.loc[
                    row_dic.get(task_name), 
                    self.get_cur_year_week_weekday(
                        day_before_cnt=day_before_cnt)[2]] = float(
                           target_val) +add_val
                logger.info(tag_df.loc[
                    row_dic.get(task_name), 
                    self.get_cur_year_week_weekday(
                        day_before_cnt=day_before_cnt)[2]])
                logger.info('更新后数值')
            else:
                target_val = tag_df.loc[row_dic.get(task_name), day_ind]
                if np.isnan(target_val) :
                    logger.info('查询数值nan')
                    target_val = 0
                tag_df.loc[
                    row_dic.get(task_name), day_ind] = float(
                        target_val) + add_val
            # 记录详情
            return tag_df
        except Exception as e:
            logger.error('run update_df: %s' % e)
    
    
    def update_df_new(self, tag_df = None, task_name='machin_learn', day_ind='', 
                  day_before_cnt = 0,
                  update_type=True, add_values =1,
                  need_append = True):
        """
        day_ind =  周几 数字
        update_type =  1 代表加, 0 代表减"""
        logger.info('开始刷新表格')
        try:
            if update_type:
                add_val = float(add_values)
            else:
                add_val = -float(add_values)
            logger.info("%s %s" % (add_val,'add_val'))
            if not tag_df:
                tag_df = self.read_df(self.wrt_path)
            logger.info('update weekday %s: ' % self.get_cur_year_week_weekday(
                day_before_cnt=day_before_cnt)[2])
            
            print(day_ind, 'day_ind')
            if not day_ind:
                tag_df =self.check_task_exist(row_dic.get(task_name),tag_df)
                print(tag_df,"tag_df" )
                target_val = tag_df.loc[row_dic.get(task_name),
                                self.get_cur_year_week_weekday(
                                    day_before_cnt=day_before_cnt)[2]]
                if np.isnan(target_val) :
                    logger.info('查询数值nan')
                    target_val = 0
                logger.info('更新所在周信息%s' % self.get_cur_year_week_weekday(
                                                   day_before_cnt=day_before_cnt)[2] )
                logger.info('打印更新数值')
                
                logger.info(float(
                            target_val) +add_val)
                logger.info(tag_df.loc[
                    row_dic.get(task_name), 
                    self.get_cur_year_week_weekday(
                        day_before_cnt=day_before_cnt)[2]])
                logger.info('更新前数值')
                logger.info(row_dic.get(task_name, ''))
                # raise Exception
                if need_append: # 判断是否累加还是重置
                    update_val = float(
                            target_val) +add_val
                else:
                    update_val = add_val
                logger.info('更新前后数值 %s; %s' % (target_val,add_val))
                tag_df.loc[
                    row_dic.get(task_name), 
                    self.get_cur_year_week_weekday(
                        day_before_cnt=day_before_cnt)[2]] =update_val

                # logger.info('更新后数值%s' % )
            else:
                target_val = tag_df.loc[row_dic.get(task_name), day_ind]
                if np.isnan(target_val) :
                    logger.info('查询数值nan')
                    target_val = 0
                if need_append: # 判断是否累加还是重置
                    update_val = float(
                            target_val) +add_val
                else:
                    update_val = add_val
                logger.info('更新前后数值 %s; %s' % (target_val,add_val))

                tag_df.loc[
                    row_dic.get(task_name), day_ind] = update_val
            # 记录详情
            return tag_df
        except Exception as e:
            logger.error('run update_df: %s' % e)
    
    
    def get_cur_week_file(self,day_before_cnt=0):
        year, week, _ = self.get_cur_year_week_weekday(day_before_cnt)
        file_a3 = './%s_%s.xlsx' % (year,week)
        import os
        import shutil
        # 检查a3.xlsx是否存在
        if not os.path.exists(file_a3):
            # 如果a3.xlsx不存在，则复制a2.xlsx为a3.xlsx
            shutil.copy(self.tmp_path, file_a3)
            logger.info(f"{self.tmp_path} 已复制为 {file_a3}")
        else:
            logger.info(f"{file_a3} 已存在，无需复制")
        print(file_a3, '操作的文件')
        return file_a3

    def check_task_exist(self, task_ind = 0,tag_df = None):
        """
        tag_df.loc[row_dic.get(task_name),
                                self.get_cur_year_week_weekday(
                                    day_before_cnt=day_before_cnt)[2]]"""
        
        import pandas as pd
        logger.info('check_task_exist run')
        print(tag_df)
        print(len(tag_df), 'print len')

        # 示例 DataFrame

        # 检查是否有至少5行
        if len(tag_df) < task_ind+1:
            # 新增空行到第5行（第4个索引）
            for _ in range(task_ind+1 - len(tag_df)):
                logger.info('add columns')
                tag_df.loc[len(tag_df)] = {
                    "项目":'lose_money',
                    	"目标":'',
                    	"1":0,
                    	"备注1":"",
                    	"2":0,
                    	"备注2":"",
                    	"3":0,
                    	"备注3":"",
                    	"4":0,
                    	"备注4":"",
                    	"5":0,
                    	"备注5":"",
                    	"6":0,
                    	"备注6":"",
                    	"7":0,
                    	"备注7":""


                }
        print(tag_df)
        print('after update')
        # 读取第5行（索引4）第1列（col1）
        print(5,0)
        value = tag_df.loc[5,'项目']
        logger.info("第6行的值是%s" %  value)

        return tag_df
    def get_cur_year_week_weekday(self, day_before_cnt = -1):
        from dateutil.relativedelta import relativedelta
        import datetime
        try:
            day_before_cnt = -int(day_before_cnt)
        except Exception as e:
            # logger.info(e, 'day_before_cnt')
            day_before_cnt = -1
        
        today = datetime.date.today()+relativedelta(days = day_before_cnt)
        # logger.info(today, 'today')
        year, week, weekday = today.isocalendar()
        return year, week, weekday
    def get_cur_year_month_day_hour(self, hour_before_cnt=0):


        # 获取当前日期和时间
        now = datetime.now()- timedelta(hours=hour_before_cnt)

        # 提取年、月、日和时
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour

        # logger.info(f"年: {year}")
        # logger.info(f"月: {month}")
        # logger.info(f"日: {day}")
        # logger.info(f"时: {hour}")
        return year, month, day , hour

    # def get_cur_weekday(self):
    #     import datetime
    #     today = datetime.date.today()
    #     day_of_week = today.weekday()
    #     days = [
    #         '周一',
    #         '周二',
    #         '周三',
    #         '周四',
    #         '周五',
    #         '周六',
    #         '周日'
    #     ]
    #     return days[day_of_week]

    def reset_df(self):
        pass

    def get_expect_cnt(self, task_lst = ['machin_learn']):
        pass
    def get_week_task_expect_cnt(
            self,  task_lst = ['machin_learn'], file_path = ''):
        ret = {}
        df = pd.read_excel(
            file_path if file_path else  self.wrt_path )
        for item in task_lst:
            cnt = df.loc[row_dic.get(item), '目标']
            ret[item] = cnt
        
        logger.info('week expect cnt %s' %  ret)
        return ret
    def get_hour_task_expect_cnt(self,  task_lst = ['machin_learn'],df = None,
                                 day_before_cnt = 0):
        
        """
        查询当天累计完成情况
        """
        task_info = self.get_week_task_expect_cnt()
        if day_before_cnt:
            hour_passed_cnt = 15
        else:
            hour_passed_cnt = self.get_hour_passed()
        default_hours = 8
        logger.info('hour_passed_cnt = ', hour_passed_cnt)
        cal_hours = 0
        ret  = {} # 计算未完成任务数
        for item in task_lst:
            if hour_passed_cnt < default_hours:
                cal_hours = hour_passed_cnt
            else:
                cal_hours = default_hours
            # logger.info(cal_hours,'print cal_hours')
            if cal_hours == 0 :
                ret[item] = 0
                continue
            logger.info(item, task_info,default_hours ,cal_hours)
            # 计算未完成任务数
            ret[item] =task_info.get(item)/7*2 /default_hours * cal_hours  - \
                self.get_day_cnt(day_before_cnt=day_before_cnt)
        info = {}
        logger.info('begin get_money')

        for item in task_lst:
            info[item] = {
                'todo_cnt': round(ret.get(item, 0),2), 
                'lose money': round(self.get_money(ret.get(item, 0),day_before_cnt=day_before_cnt)[0],2),
                'lost_finish': self.get_money(ret.get(item, 0),day_before_cnt=day_before_cnt)[1]
            }
            logger.info(info[item].get('lose money', 0))
            logger.info('打印记录的罚款')
            # 记录罚款金额
            update_df = self.update_df_new(
            update_type=True,
            task_name = 'lose_money',
            # day_ind=day_ind,
            # tag_df=tag_df,
            add_values =info[item].get('lose money', 0),
            need_append=False,
            day_before_cnt=day_before_cnt)

            logger.info('记录罚款')
            self.write_df(update_df)
        
        

        logger.info(str(info))
        logger.info('print get_money')
        return info
    def get_hour_task_expect_cnt_bak0515(self,  task_lst = ['machin_learn'],df = None,
                                 day_before_cnt = 0):
        
        """
        查询当天累计完成情况
        """
        task_info = self.get_week_task_expect_cnt()
        if day_before_cnt:
            hour_passed_cnt = 15
        else:
            hour_passed_cnt = self.get_hour_passed()
        default_hours = 8
        logger.info('hour_passed_cnt = ', hour_passed_cnt)
        cal_hours = 0
        ret  = {} # 计算未完成任务数
        for item in task_lst:
            if hour_passed_cnt < default_hours:
                cal_hours = hour_passed_cnt
            else:
                cal_hours = default_hours
            # logger.info(cal_hours,'print cal_hours')
            if cal_hours == 0 :
                ret[item] = 0
                continue
            logger.info(item, task_info,default_hours ,cal_hours)
            # 计算未完成任务数
            ret[item] =task_info.get(item)/7*2 /default_hours * cal_hours  - \
                self.get_day_cnt(day_before_cnt=day_before_cnt)
        info = {}
        logger.info('begin get_money')

        for item in task_lst:
            info[item] = {
                'todo_cnt': round(ret.get(item, 0),2), 
                'lose money': round(self.get_money(ret.get(item, 0),day_before_cnt=day_before_cnt)[0],2),
                'lost_finish': self.get_money(ret.get(item, 0),day_before_cnt=day_before_cnt)[1]
            }

            # 记录罚款金额
            # update_df = self.update_df(
            # update_type=True,
            # # day_ind=day_ind,
            # # tag_df=tag_df,
            # add_values =info[item].get('lose money', 0),
            # # need_append=False,
            # day_before_cnt=day_before_cnt)

            # logger.info('记录罚款')
            # self.write_df(update_df)
        
        

        logger.info(str(info))
        logger.info('print get_money')
        return info


    def init_lose_money(self,day_before_cnt):
        cur_hour =self.get_cur_year_month_day_hour()[-1] 
        if int(day_before_cnt) >= 1:
            return 400 * 4

        if cur_hour < 10:
            return 0
        #[10,11],[12,13],[14,15],[16,17]
        elif 10 <= cur_hour <=11 :
            return 400
        elif 12 <= cur_hour <=13 :
            return 400 * 2
        elif 14 <= cur_hour <=15 :
            return 400 * 3
        elif 16 <= cur_hour <=17 :
            return 400 * 4
        
    def get_money(self,cnt, task_name = 'machin_learn',day_before_cnt =0):
        """
        cnt 待打卡次数"""
        logger.info('run get_money')
        logger.info('打印参数:%s' % cnt)
        money = 100
            
        # for _ in range(int(cnt)):
        if cnt >0:
            money = 2 * money * cnt
        elif cnt <= 0:
            money = cnt * 100 # 超额完成任务每次打卡只能抵扣100

        # 分析 任务是否按时完成
        exit_done =self.cnt_hour_detail([task_name],day_before_cnt=day_before_cnt)[task_name]

        if pd.isna(exit_done):
            exit_done = '{}'
        
        logger.info('exit_done : %s' % exit_done)
        # cut_money = 0
        lost_finish_money = self.init_lose_money(day_before_cnt =day_before_cnt)

        
        logger.info('get_money-day_before_cnt : %s' % day_before_cnt)
        msg = 'lost_finish:'

        try: 
            logger.info('>>>>')
            if day_before_cnt:
                day_before_cnt = int(day_before_cnt)
            if day_before_cnt > 0:
                cur_hour = 24
            else:
                cur_hour =self.get_cur_year_month_day_hour()[-1]
            logger.info('>>>>')
            logger.info('ast.literal_eval(exit_done).items()')
            exis_info = ast.literal_eval(exit_done).items()
            new_exis_info = {key:value for key, value in exis_info}
            # logger.info('new_exis_info: %s' % new_exis_info)
            for k in [11,13,15,17]:
                if k not in new_exis_info:
                    new_exis_info[k] = 0
            logger.info('%s' % new_exis_info)
            # logger.info('>>>2')
            for k,v in new_exis_info.items():
                logger.info('%s,%s,%s' % (cur_hour,v,k))
                for item in ([10,11],[12,13],[14,15],[16,17]):
                    if item[0] <= k  <=item[1] and v !=0:
                        logger.info( '免除罚款: %s' % item)
                        lost_finish_money -= 400
                    if item[0] <= cur_hour  <=item[1] \
                        and v ==0:
                        logger.info('罚款所在时间点: %s' % cur_hour)
                        logger.info('msg')
                        msg+=str(item)
                        logger.info('msg2')

                    # if cur_hour < 10:
                    #     logger.info('还没到点,免除罚款: %s' % item)
                    #     lost_finish_money-=400

                logger.info('>>??')
            logger.info('money %s' % money)
            logger.info('补交 %s ' % lost_finish_money)
            money += lost_finish_money
        except Exception as e:
            logger.info('get_money error: %s' % e)

        logger.info('run get_money end')
        return money, msg



    def get_hour_passed(self):
        from datetime import datetime, time

        # 获取当前时间
        now = datetime.now()

        # 获取当前时间的小时部分
        current_hour = now.hour
        if current_hour <  9:
            current_hour = 9


        # 计算当前小时距离9点过去了多少个小时
        hours_passed = current_hour - 9

        # # 如果当前小时小于9点，则需要处理跨天的情况
        # if hours_passed < 0:
        #     hours_passed += 24
        logger.info(f"当前小时距离9点过去了 {hours_passed} 个小时")
        return hours_passed

        

        


    def get_day_cnt(self,day_before_cnt =0):
        df = self.read_df(self.get_cur_week_file(day_before_cnt=day_before_cnt))
        # print(df[self.get_cur_year_week_weekday(day_before_cnt=day_before_cnt)[2]][:-1])
        column_sum = df[self.get_cur_year_week_weekday(day_before_cnt=day_before_cnt)[2]][:-1].sum()
        logger.info('today point cnt : %s' %  column_sum)
        return column_sum
    def get_hour_detail(self, task_lst = ['machin_learn']):
        df = self.read_df(self.get_cur_week_file())
        ret = []
        for task_name in task_lst:
            # column_info = df['备注%s' % self.get_cur_year_week_weekday()[2]][row_dic['machin_learn']]
            column_info = df.loc[row_dic.get(task_name), '备注%s' % self.get_cur_year_week_weekday()[2]] 
            logger.info(column_info+ 'column_info')
        return column_info
    def get_hour_before(self, before_cnt = 2):
        from datetime import datetime, timedelta

        # 获取当前时间
        now = datetime.now()

        # 获取上一个小时的时间
        ret = []
        for cnt_tmp in range(before_cnt):
            one_hour_ago = now - timedelta(hours=cnt_tmp)

            # 提取上一个小时的小时数
            hour_of_previous_hour = one_hour_ago.hour
            ret.append(hour_of_previous_hour)

        logger.info(f"查询小时列表: {ret}")
        return ret
    def get_hour_before_finish(self, before_cnt = 2, need_cnt = 1, task_lst = ['machin_learn']):
        """
        查询近期小时数 before_cnt
        查询任务完成数 need_cnt
        """
        from datetime import datetime, timedelta

        # 获取当前时间
        now = datetime.now()

        # 获取上一个小时的时间
        ret = []
        for cnt_tmp in range(before_cnt):
            one_hour_ago = now - timedelta(hours=cnt_tmp)

            # 提取上一个小时的小时数
            hour_of_previous_hour = one_hour_ago.hour
            ret.append(hour_of_previous_hour)

        logger.info(f"查询小时列表: {ret}")
        finish_cnt = 0
        finish_info = {}
        for task in task_lst:
            info = self.get_hour_detail(task_lst=['%s' % task])
            logger.info(info+ 'info')
            logger.info(type(info))
            pd.isna(info)
            if not pd.isna(info): 


                dict_info = ast.literal_eval(info)
            else:
                dict_info = {}
            for hour in ret:
                cnt_val = dict_info.get(hour, 0) 
                finish_cnt+=cnt_val
            if finish_cnt < need_cnt:
                finish_info[task] = False
            else:
                finish_info[task] = True

            
            
        return finish_info



    def cnt_hour_detail(self, task_lst = ['machin_learn'],day_before_cnt=0):
        """
        查询各个小时完成情况
        """
        logger.info('查询各个小时完成情况')
        df = self.read_df(self.get_cur_week_file(day_before_cnt=day_before_cnt))
        ret = {}
        column_info  = np.nan
        for task_name in task_lst:
            column_info = df.loc[row_dic.get(task_name), '备注%s' % self.get_cur_year_week_weekday(day_before_cnt=day_before_cnt)[2]] 
            logger.info('cnt_hour_detail_column_info:%s' % type(column_info))
            logger.info('cnt_hour_detail_column_info:%s' % str(column_info))
            logger.info( 'task: %s , get hour details %s' % (task_name,column_info))
            logger.info( '备注%s' % ('备注%s' % self.get_cur_year_week_weekday(day_before_cnt=day_before_cnt)[2]))
            # logger.error('cnt_hour_detail')
            # raise Exception

            ret[task_name] = column_info
            # ret.append(column_info)
        return ret
    def cnt_hour_fix(self, task_name = 'machin_learn',day_before_cnt=0):
        """
        查询惩罚详情"""
        df = self.read_df(self.get_cur_week_file(day_before_cnt=day_before_cnt))


        exit_done =self.cnt_hour_detail([task_name])[task_name]
        logger.info(exit_done)
        logger.info(exit_done)
        exit_done = ast.literal_eval(exit_done)


        hour_bf2 =self.get_cur_year_month_day_hour(hour_before_cnt=2)[-1]
        hour_bf1 = self.get_cur_year_month_day_hour(hour_before_cnt=1)[-1]
        logger.info('两小时前' +hour_bf2 +';' +'一小时前' + hour_bf1)
        if hour_bf1 not in exit_done.keys() and hour_bf2 not in exit_done.keys():
            logger.info('扣多点')
        sum_done = sum([
            exit_done.get(hour_bf2,0),
            exit_done.get(hour_bf1,0),
            # exit_done[hour_bf1]
            ])
        if sum_done < 2:
            return 2-sum_done
        # return ret
    def update_hour_detail(self, task_lst = ['machin_learn'], update_type=True,
                           day_before_cnt = 0,add_values=1):

        df = self.read_df(self.get_cur_week_file(day_before_cnt=day_before_cnt))
        ret_info = {}
        for task_name in task_lst:
            # column_info = df['备注%s' % self.get_cur_year_week_weekday()[2]][row_dic['machin_learn']]
            column_info = df.loc[
                row_dic.get(task_name), '备注%s' % self.get_cur_year_week_weekday(day_before_cnt=day_before_cnt)[2]] 
            logger.info("%s %s" % (column_info ,'column_info<<'))
            logger.info("%s %s" % (row_dic.get(task_name), self.get_cur_year_week_weekday(day_before_cnt=day_before_cnt)[2]))
            if not pd.isna(column_info):
                dict_info = ast.literal_eval(column_info)
            else:
                dict_info = {}
            hour = self.get_cur_year_month_day_hour()[-1]
            logger.info("%s %s" % (type(dict_info) , 'column_info'))
            logger.info("%s %s" % (dict_info ,  'column_info'))
            if update_type:
                add_val = Fraction(add_values)  
            else:
                add_val = -Fraction(add_values)
            logger.info('更新详情打卡数值: %s' % add_val)
            if dict_info.get(hour):
                dict_info[hour] = round(float(dict_info[hour]) +float(add_val),2)
            else:
                dict_info[hour] = 0
                dict_info[hour] = round(float(dict_info[hour]) +float(add_val),2)
                # dict_info[hour] += Fraction(add_val)
            ret_info[task_name]= dict_info
            df.loc[row_dic.get(task_name), '备注%s' % self.get_cur_year_week_weekday(day_before_cnt=day_before_cnt)[2]] =str(dict_info)

        return df



    def get_week_cnt(self):
        pass

    def read_ex(self):
        pass


if __name__ == '__main__':

    sorce_path = '/Users/meta/lam/deep/Understanding/SemBERT/report_tmp.xlsx'
    # target_path = '/Users/meta/lam/deep/Understanding/SemBERT/report_tmp.xlsx'
    write_file= ExcelControl().get_cur_week_file()
    
    # write_file = ec.get_cur_week_file()
    ec = ExcelControl(wrt_path=write_file)
    # logger.info(ec.wrt_path)
    # # logger.info(ec.get_cur_weekday())
    ec.get_day_cnt()
    # logger.info(ec.get_hour_task_expect_cnt())
    # raise Exception

    # ec.get_week_task_expect_cnt()
    # ec.get_hour_task_expect_cnt()
    # ec.get_money(cnt=1)
    # ec.get_hour_passed()
    # logger.info(ec.get_hour_task_expect_cnt())
    # raise Exception
    # logger.info(ec.get_hour_detail())
    # logger.info(ec.get_hour_before())
    # logger.info(ec.get_hour_before_finish())
    # logger.info(ec.cnt_hour_detail())
    # print(ec.get_hour_task_expect_cnt())
    # logger.info(ec.cnt_hour_fix())

    # 小时打卡一次
    # update_df = ec.update_hour_detail(day_before_cnt=0)

    # 打卡一次
    # update_df = ec.update_df_new(
    #     # update_type=False
    #     # update_type=True,
    #     # day_before_cnt=0
    # )
    # ec.write_df(update_df)
    raise Exception
    # 打卡一次完成

    

    # raise Exception
"""
#todo 
查询历史进展 done"""