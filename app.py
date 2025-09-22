from flask import Flask, render_template, request, jsonify, Response
from auth import auth_bp
from utils import Utils
import logging
from read_report import ExcelControl
from read_pdf import ReadPdf
import hashlib

app = Flask(__name__)
app.register_blueprint(auth_bp, url_prefix='/auth')

# 初始化工具类和日志
uti = Utils()
logger = uti.log_init()

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/index2.html')
# def index2():
#     # status = '200 OK'
#     # response_headers = [
#     #     ('Content-Type', 'text/html; charset=utf-8'),
#     #     ('Access-Control-Allow-Origin', '*')
#     # ]
#     # start_response(status, response_headers)
    
#     # 从文件读取HTML内容
#     try:
#         with open('/Users/linzhenhui/Desktop/startBook/templates/index2.html', 'r', encoding='utf-8') as f:
#             html_content = f.read()
#     except FileNotFoundError:
#         html_content = "<h1>文件未找到</h1>"
    
#     return [html_content.encode('utf-8')]

@app.route('/index2.html')
def index2():
    try:
        return render_template('index2.html')
    except Exception as e:
        logger.error(f"加载index2.html失败: {e}")
        return "<h1>页面加载失败</h1>", 404
    
@app.route('/indexdt_20250904_151211.html')
def index3():
    try:
        return render_template('indexdt_20250904_151211.html')
    except Exception as e:
        logger.error(f"indexdt_20250904_151211.html失败: {e}")
        return "<h1>页面加载失败</h1>", 404
    
# --------------------------
# 基础测试接口 (来自post_app.py)
# --------------------------
@app.route('/post-endpoint', methods=['POST'])
def handle_post():
    data = request.get_json()
    print(f"Received data: {data}")
    return jsonify({"status": "success", "received": data}), 200

@app.route('/get-endpoint', methods=['GET'])
def handle_get():
    message = request.args.get('message', 'No message received')
    return {"response": f"Received: {message}"}

# --------------------------
# 任务统计接口 (来自post_app.py)
# --------------------------
@app.route('/get-day-cnt', methods=['GET'])
def handle_get_day_cnt():
    try:
        write_file = ExcelControl().get_cur_week_file()
        ec = ExcelControl(wrt_path=write_file)
        ec.get_week_task_expect_cnt()
        ec.get_hour_passed()
        ret = ec.get_hour_task_expect_cnt()
        ret1 = ec.cnt_hour_detail()
        message = request.args.get('message', 'summery:%s ; detail:%s' % (str(ret), str(ret1)))
    except Exception as e:
        logger.error(e)
    return {"response": "Received: %s" % message}

@app.route('/get-day-cnt-test', methods=['GET'])
def handle_alert_test():
    write_file = ExcelControl().get_cur_week_file()
    bf_cnt = request.args.get('bf_cnt', 0)
    task_name = request.args.get('task_name', 'machin_learn')
    ec = ExcelControl(wrt_path=write_file)
    
    task_status = ec.get_hour_task_expect_cnt(
        day_before_cnt=bf_cnt,
        task_lst=[task_name]
    )
    todo_ret = task_status.get(task_name, {}).get('todo_cnt', 0)
    
    logger.info(f"未完成任务数: {todo_ret}")
    
    if todo_ret <= 0:
        return '0'
    
    ret = ec.cnt_hour_fix()
    return f'{ret}'

# --------------------------
# 书籍阅读接口 (来自post_app.py)
# --------------------------
@app.route('/get-book', methods=['GET'])
def handle_get_book():
    import json
    try:
        book_name = request.args.get('book_name', '')
        page_rows = request.args.get('page_rows', 30)
        
        reader = ReadPdf(wrt_path='/opt/code/post_app/book_helper.xlsx')
        message = reader.read_book(task_name=book_name, page_rows=page_rows)
        
        response_data = {"status": "success", "received": f'{message}'}
        response_json = json.dumps(response_data, ensure_ascii=False).encode('utf8')
    except Exception as e:
        logger.error(e)
        response_data = {"status": "error", "message": str(e)}
        response_json = json.dumps(response_data, ensure_ascii=False).encode('utf8')
    
    return Response(response_json, content_type='application/json; charset=utf-8')

@app.route('/page-book', methods=['GET'])
def handle_page_book():
    import json
    try:
        book_name = request.args.get('book_name', 'deepl')
        page_ind = request.args.get('page_ind', 0)
        
        reader = ReadPdf(wrt_path='/opt/code/post_app/book_helper.xlsx')
        message = reader.update_start_line(
            is_done=1,
            task_name=book_name,
            update_index=page_ind
        )
        
        response_data = {"status": "success", "message": f"更新成功: {message}"}
        response_json = json.dumps(response_data, ensure_ascii=False).encode('utf8')
    except Exception as e:
        logger.error(e)
        response_data = {"status": "error", "message": str(e)}
        response_json = json.dumps(response_data, ensure_ascii=False).encode('utf8')
    
    return Response(response_json, content_type='application/json; charset=utf-8')

# --------------------------
# 历史任务统计 (来自post_app.py)
# --------------------------
@app.route('/get-before-day-cnt', methods=['GET'])
def handle_get_before_day_cnt():
    from read_report import ExcelControl
    try:
        bf_cnt = int(request.args.get('bf_cnt', 0))
        
        write_file = ExcelControl().get_cur_week_file(day_before_cnt=bf_cnt)
        ec = ExcelControl(wrt_path=write_file)
        
        ec.get_week_task_expect_cnt()
        ret = ec.get_hour_task_expect_cnt(day_before_cnt=bf_cnt)
        ret1 = ec.cnt_hour_detail(day_before_cnt=bf_cnt)
        
        message = request.args.get('message', f'summery:{ret} ; detail:{ret1}')
    except Exception as e:
        logger.error(e)
        message = f"查询失败: {str(e)}"
    
    return {"response": f"Received: {message}"}

# --------------------------
# 历史lose_money统计
# --------------------------
@app.route('/get-total-lose-money', methods=['GET'])
def handle_get_total_lose_money():
    try:
        excel_control = ExcelControl()
        total_lose_money = excel_control.get_total_lose_money_before_today()
        message = f"今天以前的所有lose_money总和为: {total_lose_money}"
    except Exception as e:
        logger.error(e)
        message = f"查询失败: {str(e)}"
    
    return {"response": message}

# --------------------------
# 打卡管理接口 (来自post_app.py)
# --------------------------
@app.route('/add-day-point', methods=['GET'])
def handle_add_day_point():
    from read_report import ExcelControl
    logger.info('开始补卡操作')
    
    # try:
    day_before_cnt = request.args.get('day_before_cnt')
    task_name = request.args.get('task_name')
    update_type = request.args.get('update_type')
    day_ind = request.args.get('day_ind', '')
    add_values = float(request.args.get('add_values', 1))
    
    logger.info(f'请求参数: {request.args}')
    
    write_file = ExcelControl().get_cur_week_file(day_before_cnt=day_before_cnt)
    ec = ExcelControl(wrt_path=write_file)
    
    is_add = True
    if update_type == '0':
        is_add = True
        logger.info(f'准备为任务[{task_name}]补卡')
    elif update_type == '1':
        is_add = False
        logger.info(f'准备为任务[{task_name}]减卡')
    
    logger.info('开始更新任务数据')
    update_df = ec.update_df_new(
        update_type=is_add,
        day_ind=day_ind,
        tag_df=None,
        add_values=add_values,
        day_before_cnt=day_before_cnt
    )
    ec.write_df(update_df)
    
    logger.info('开始更新时间明细')
    update_df2 = ec.update_hour_detail(
        add_values=add_values,
        day_before_cnt=day_before_cnt,
        update_type=is_add
    )
    ec.write_df(update_df2)
    
    logger.info('打卡操作完成')
# except Exception as e:
    # logger.error(f'打卡操作异常: {e}')
    
    return {"response": "Received: ok"}

# --------------------------
# 微信公众平台接口 (来自post_app.py)
# --------------------------
@app.route('/wx', methods=['GET'])
def handle_wg_get():
    try:
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echostr = request.args.get('echostr', '')
        token = "wxgzh2025"
        
        if not all([signature, timestamp, nonce, echostr]):
            return "hello, this is handle view"
        
        params = [token, timestamp, nonce]
        params.sort()
        sha1 = hashlib.sha1()
        for item in params:
            sha1.update(item.encode('utf-8'))
        hashcode = sha1.hexdigest()
        
        if hashcode == signature:
            return echostr
        return ""
    except Exception as e:
        print(f"验证异常: {e}")
        return str(e)

@app.route('/wx', methods=['POST'])
def handle_wg_post():
    data = request.get_json()
    print(f"收到微信消息: {data}")
    return jsonify({"status": "success", "received": data}), 200

# --------------------------
# 获取static文件列表接口
# --------------------------
@app.route('/get-static-files', methods=['GET'])
def handle_get_static_files():
    import os
    try:
        static_files = []
        base_url = "http://39.108.219.192/"
        # base_url = "http://0.0.0.0/"
        
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
        html_content = """
<!DOCTYPE html>
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
        <p>共找到 <span class="count">%(count)s</span> 个文件</p>
        <ul class="file-list">
""" % {'count': len(static_files)}
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
        
        return html_content
        
    except Exception as e:
        logger.error(f"获取static文件列表失败: {e}")
        return f"<h1>错误</h1><p>获取文件列表失败: {str(e)}</p>"

# --------------------------
# 主程序入口 (合并优化)
# --------------------------
if __name__ == '__main__':
    # 开发模式使用调试设置
    app.run(debug=True, host='0.0.0.0', port=5001)
    
    # 生产部署时取消下面注释
    # app.run(host='0.0.0.0', port=80)