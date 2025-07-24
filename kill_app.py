import psutil
import subprocess

def kill_post_py_processes():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # 检查进程名是否为 'python' 或 'python3' 并且命令行参数包含 'post.py'
            print(proc.info['name'] , '')
            print(proc.info['cmdline'] , '')
            if proc.info['name'] in ['python', 'python3'] and 'post_app.py' in proc.info['cmdline']:
                print(f"Killing process {proc.info['pid']} with command line {proc.info['cmdline']}")
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
def run_command_in_background():
    command = 'nohup /opt/soft/miniconda3/envs/postapp/bin/python -u post_app.py >> nohup.log &'
    
    # 使用subprocess.Popen来执行命令
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # 打印进程ID
    print(f"Process started with PID: {process.pid}")

if __name__ == "__main__":
    kill_post_py_processes()
    run_command_in_background()