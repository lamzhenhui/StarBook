#!/usr/bin/env python3
import subprocess
import sys
import os

def check_port_5000():
    """查询端口号5000的进程ID"""
    try:
        # 根据操作系统选择不同的命令
        if sys.platform == "win32":
            # Windows系统
            cmd = "netstat -ano | findstr :5000"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            
            if not lines or lines == ['']:
                print("端口5000没有被占用")
                return
            
            print("端口5000的进程信息:")
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 5:
                        pid = parts[-1]
                        print(f"进程ID: {pid}")
                        
                        # 获取进程详细信息
                        try:
                            task_cmd = f"tasklist /FI \"PID eq {pid}\""
                            task_result = subprocess.run(task_cmd, shell=True, capture_output=True, text=True)
                            print(f"进程详情: {task_result.stdout.strip()}")
                        except:
                            pass
                            
        else:
            # Unix/Linux/macOS系统
            cmd = "lsof -i :5000"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                # 尝试使用netstat作为备选
                cmd = "netstat -tulnp | grep :5000"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode != 0:
                    # 尝试使用ss命令
                    cmd = "ss -tulnp | grep :5000"
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.stdout.strip():
                print("端口5000的进程信息:")
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        print(line)
                        
                        # 尝试提取PID
                        parts = line.split()
                        for part in parts:
                            if '/' in part and part.split('/')[0].isdigit():
                                pid = part.split('/')[0]
                                print(f"进程ID: {pid}")
                                
                                # 获取进程详细信息
                                try:
                                    ps_cmd = f"ps -p {pid} -o pid,ppid,cmd"
                                    ps_result = subprocess.run(ps_cmd, shell=True, capture_output=True, text=True)
                                    if ps_result.stdout.strip():
                                        print(f"进程详情: {ps_result.stdout.strip()}")
                                except:
                                    pass
                                break
            else:
                print("端口5000没有被占用")
                
    except Exception as e:
        print(f"查询端口5000时出错: {e}")

def kill_port_5000():
    """强制关闭端口5000的进程"""
    try:
        if sys.platform == "win32":
            # Windows系统
            cmd = "netstat -ano | findstr :5000"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            
            pids = []
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 5 and parts[-1].isdigit():
                        pids.append(parts[-1])
            
            if pids:
                for pid in set(pids):
                    try:
                        kill_cmd = f"taskkill /F /PID {pid}"
                        subprocess.run(kill_cmd, shell=True, check=True)
                        print(f"已强制关闭进程 {pid}")
                    except subprocess.CalledProcessError:
                        print(f"无法关闭进程 {pid}")
            else:
                print("没有找到占用端口5000的进程")
        else:
            # Unix/Linux/macOS系统
            cmd = "lsof -ti :5000"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    if pid.isdigit():
                        try:
                            kill_cmd = f"kill -9 {pid}"
                            subprocess.run(kill_cmd, shell=True, check=True)
                            print(f"已强制关闭进程 {pid}")
                        except subprocess.CalledProcessError:
                            print(f"无法关闭进程 {pid}")
            else:
                print("没有找到占用端口5000的进程")
                
    except Exception as e:
        print(f"关闭端口5000进程时出错: {e}")


if __name__ == "__main__":
    print("=== 查询端口5000的进程信息 ===")
    # check_port_
    kill_port_5000()