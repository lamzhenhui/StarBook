# encoding = utf-8

from utils import Utils
import logging
uti = Utils()
logger = uti.log_init()
from read_report import ExcelControl

from flask import Flask, request, jsonify, Response
# from flask import 
import hashlib
from utils import Utils
uti = Utils()
app = Flask(__name__)

@app.route('/post-endpoint', methods=['POST'])
def handle_post():
    data = request.get_json()  # 获取请求中的 JSON 数据
    print(f"Received data: {data}")
    return jsonify({"status": "success", "received": data}), 200

@app.route('/get-endpoint', methods=['GET'])
def handle_get():
    # Get query parameters
    message = request.args.get('message', 'No message received')
    return {"response": f"Received: {message}"}

# get-day-cnt 查询进展
@app.route('/get-day-cnt', methods=['GET'])
def handle_get_day_cnt():
    # Get query parameters
    try:

        sorce_path = '/Users/meta/lam/deep/Understanding/SemBERT/report_tmp.xlsx'
        # target_path = '/Users/meta/lam/deep/Understanding/SemBERT/report_tmp.xlsx'
        write_file= ExcelControl().get_cur_week_file()
        
        # write_file = ec.get_cur_week_file()
        ec = ExcelControl(wrt_path=write_file)
        print(ec.wrt_path)
        # # print(ec.get_cur_weekday())
        print(ec.get_day_cnt())

        ec.get_week_task_expect_cnt()
        ec.get_hour_passed()
        ret = ec.get_hour_task_expect_cnt()
        ret1 = ec.cnt_hour_detail()
        message = request.args.get('message', 'summery:%s ; detail:%s' % (str(ret),str(ret1)))
    except Exception as e:
        logger.error(e)
    return {"response": "Received: %s"  % message}
@app.route('/get-day-cnt', methods=['GET'])
def handle_get_day_cnt_bak_0513():
    # Get query parameters
    try:

        sorce_path = '/Users/meta/lam/deep/Understanding/SemBERT/report_tmp.xlsx'
        # target_path = '/Users/meta/lam/deep/Understanding/SemBERT/report_tmp.xlsx'
        write_file= ExcelControl().get_cur_week_file()
        
        # write_file = ec.get_cur_week_file()
        ec = ExcelControl(wrt_path=write_file)
        print(ec.wrt_path)
        # # print(ec.get_cur_weekday())
        print(ec.get_day_cnt())

        ec.get_week_task_expect_cnt()
        ec.get_hour_passed()
        ret = ec.get_hour_task_expect_cnt()
        ret1 = ec.cnt_hour_detail()
        message = request.args.get('message', 'summery:%s ; detail:%s' % (str(ret),str(ret1)))
    except Exception as e:
        logger.error(e)
    return {"response": "Received: %s"  % message}

# 检查惩罚情况
@app.route('/get-day-cnt-test', methods=['GET'])
def handle_alert_test():
    write_file= ExcelControl().get_cur_week_file()
    bf_cnt = request.args.get('bf_cnt', 0)
    task_name = request.args.get('task_name', 'machin_learn')
    ec = ExcelControl(wrt_path=write_file)
    # print(ec.wrt_path)
    # # print(ec.get_cur_weekday())
    todo_ret = ec.get_hour_task_expect_cnt(day_before_cnt=bf_cnt,
                                      task_lst=['%s' % task_name]
                                      )[task_name].get('todo_cnt', 0)
    logger.info(str(todo_ret))
    if todo_ret <= 0:
        return '0'
    ret = ec.cnt_hour_fix()
    # message = request.args.get('message', 'summery:%s ; detail:%s' % (str(1),str(1)))
    return '%s' % ret


@app.route('/get-book', methods=['GET'])
def handle_get_book():
    # Get query parameters
    import json
    from read_report import ExcelControl
    from read_pdf import ReadPdf
    try:
        book_name = request.args.get('book_name', 0)
        page_rows = request.args.get('page_rows', 30)
        print(page_rows, 'page_rows>>>')
        print(book_name, 'book_name')

        message= ReadPdf(wrt_path='/opt/code/post_app/book_helper.xlsx').read_book(task_name=book_name,page_rows =page_rows)
        response_data = {"status": "success", "received": '%s' % message}
        response_json = json.dumps(response_data, ensure_ascii=False).encode('utf8')
    except Exception as e:
        logger.error(e)
    return Response(response_json, content_type='application/json; charset=utf-8')

@app.route('/page-book', methods=['GET'])
def handle_page_book():
    # Get query parameters
    import json
    from read_report import ExcelControl
    from read_pdf import ReadPdf
    try:
        book_name = request.args.get('book_name',  'deepl')
        page_ind = request.args.get('page_ind', 0)
        message= ReadPdf(wrt_path='/opt/code/post_app/book_helper.xlsx').update_start_line(
            is_done=1,
            task_name=book_name,
            update_index=page_ind)
        # message = '你好'
        # return jsonify({"response": f"Received: %s"  % message})
        # return jsonify({"status": "success", "received": '你好'}), 200

        response_data = {"status": "success", "received": '%s' % message}
        response_json = json.dumps(response_data, ensure_ascii=False).encode('utf8')
        # return {"response": "Received: %s"  % response_json}
    except Exception as e:
        logger.error(e)
    
    # return Response(response_json, content_type='application/json; charset=utf-8')
    return Response(response_json, content_type='application/json; charset=utf-8')


# get-before-day-cnt查询历史进展
@app.route('/get-before-day-cnt', methods=['GET'])
def handle_get_before_day_cnt():
    # Get query parameters
    from read_report import ExcelControl
    sorce_path = '/Users/meta/lam/deep/Understanding/SemBERT/report_tmp.xlsx'
    # target_path = '/Users/meta/lam/deep/Understanding/SemBERT/report_tmp.xlsx'

    bf_cnt = request.args.get('bf_cnt', 0)
    print(bf_cnt , 'bf_cnt')
    write_file= ExcelControl().get_cur_week_file(day_before_cnt=bf_cnt)
    
    # write_file = ec.get_cur_week_file()
    ec = ExcelControl(wrt_path=write_file)
    print(ec.wrt_path)
    # # print(ec.get_cur_weekday())
    # print(ec.get_day_cnt(day_before_cnt=bf_cnt))

    ec.get_week_task_expect_cnt()
    # if bf_cnt !=0:

    # ec.get_hour_passed()
    print('start get_hour_task_expect_cnt')
    ret = ec.get_hour_task_expect_cnt(day_before_cnt=bf_cnt)
    print('end get_hour_task_expect_cnt')

    ret1 = ec.cnt_hour_detail(day_before_cnt=bf_cnt)
    message = request.args.get('message', 'summery:%s ; detail:%s' % (str(ret),str(ret1)))
    return {"response": "Received: %s"  % message}

# 打卡 
@app.route('/add-day-point', methods=['GET'])
def handle_add_day_point():
    """
    tag_df, task_name='', day_ind=7, update_type=True):
    
    """
    from read_report import ExcelControl

    row_dic = {
    'machin learn': 0,
    # "面试刷题",
    # "python高级",
    # "数据结构",
    # "成考",
    # "知乎",
    # "自考刷题",
    # "mysql，k8s，http"


}
    logger.info('开始补卡')
    try:
        day_before_cnt = request.args.get('day_before_cnt')
        write_file= ExcelControl().get_cur_week_file(day_before_cnt=day_before_cnt)
        
        # write_file = ec.get_cur_week_file()
        ec = ExcelControl(wrt_path=write_file)
        
        task_name = request.args.get('task_name')
        update_type = request.args.get('update_type')
        day_ind = request.args.get('day_ind','')
        add_values = request.args.get('add_values', 1)
        logger.info('%s' % str(request.args))
        logger.info('%s-%s-%s-%s-%s' % (
        task_name,
        update_type,
        day_ind,
        day_before_cnt,
        add_values         
                ))

        tag_df = None
        print( task_name, update_type)

        if update_type == '0':
            update_type = True
            logger.info('准备打卡')
        elif update_type == '1':
            update_type =False
            logger.info('准备减卡')

        logger.info('start update df :handle_add_day_point')
        update_df = ec.update_df_new(
            update_type=update_type,
            day_ind=day_ind,
            tag_df=tag_df,
            add_values =add_values,
            day_before_cnt=day_before_cnt
        )
        logger.info('write_df')
        ec.write_df(update_df)

        update_df2 = ec.update_hour_detail(
            add_values=add_values,
            day_before_cnt=day_before_cnt,
            update_type=update_type)
        logger.info('update_hour_detail')

        ec.write_df(update_df2)
    except Exception as e:
        logger.error('handle_add_day_point exception : %s' % e)
    # return tag_df
    # message = request.args.get('message', '%s' % str(ret))
    return {"response": "Received: ok"  }

@app.route('/wx', methods=['GET'])
def handle_wg_get():
    try:
        data = app.input()
        if len(data) == 0:
            return "hello, this is handle view"
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        token = "wxgzh2025" #请按照公众平台官网\基本配置中信息填写

        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()
        print ("handle/GET func: %s, %s: " % hashcode, signature)
        if hashcode == signature:
            return echostr
        else:
            return ""
    except Exception as  Argument:
        print(Argument)
        return Argument

@app.route('/wx', methods=['POST'])
def handle_wg_post():
    data = request.get_json()  # 获取请求中的 JSON 数据
    print(f"Received data: {data}")
    return jsonify({"status": "success", "received": data}), 200

if __name__ == '__main__':


    app.run(host='0.0.0.0', port=80)  # 确保监听所有网络接口

    import time
    while True:
        print('定时任务')
        logger.info('定时任务')
        time.sleep(10)

    #http://39.108.219.192/get-endpoint?message=HelloServer
    #nohup /opt/soft/miniconda3/envs/postapp/bin/python  -u post_app.py   >> post_app.log &
    #todo get luw
    # 翻译找原文
    
    # handle_get_before_day_cnt()


"""
todo : 
记录昨天的罚款金额
支持查询所有未上交罚款

"""
