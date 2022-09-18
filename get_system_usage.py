import pytest
import paramiko
import pandas as pd
import datetime
import os


def shh_connect(host, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)
    return ssh


def ssh_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read()


def execute_command(command):
    host = '192.168.31.56'
    username = 'dipesh'
    password = '1234'
    ssh = shh_connect(host, username, password)
    output = ssh_command(ssh, command)
    return output


# save the output of the command in a csv file
def save_csv(key, value):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [timestamp, key, value]
    df = pd.DataFrame([row], columns=['timestamp', 'key', 'value'])
    df.to_csv('output.csv', mode='a', header=False, index=False)

    header = ['timestamp', 'key', 'value']
    # if df does not have header then add header
    if not pd.read_csv('output.csv').columns.tolist() == header:
        df.to_csv('output.csv', header=header, index=False)
    else:
        df.to_csv('output.csv', mode='a', header=False, index=False)


def check_dir():
    directory = 'pytesthtml'
    if not os.path.exists(directory):
        os.mkdir(directory)


class TestSsh:

    @pytest.mark.cli
    def test_cpu_usage(self):
        # command to get cpu usage
        cmd = "top -bn1 | grep load | awk '{printf \"%.2f%%\", $(NF-2)}'"
        output = execute_command(cmd)
        output = output.decode('utf-8').replace("%", "")
        save_csv('cpu_usage', output)
        assert float(output) < 80.00

    @pytest.mark.cli
    def test_memory_usage(self):
        # command to get memory usage
        cmd = "free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'"
        output = execute_command(cmd)
        output = output.decode('utf-8').replace("%", "")
        save_csv('memory_usage', output)
        assert float(output) < 80.00

    @pytest.mark.cli
    def test_disk_usage(self):
        # command to get disk usage
        cmd = "df -h | awk '$NF==\"/\"{printf \"%s\", $5}'"
        output = execute_command(cmd)
        output = output.decode('utf-8').replace("%", "")
        save_csv('disk_usage', output)
        assert float(output) < 80.00
