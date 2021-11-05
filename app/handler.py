from paramiko import SSHClient, AutoAddPolicy, RSAKey
from app import app

class NodeHandler():
    def __init__(self, template, ip, login="root", password=""):
        self.ip = ip
        self.login = login
        self.password = password
        self.template = template

    def conect(self):
        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        try:
            if self.password:
                self.ssh.connect(hostname=self.ip, username=self.login, password=self.password, look_for_keys=False, allow_agent=False)
            else:
                key = RSAKey.from_private_key_file(app.config['DEFAULT_SSH_KEY_PATH'] + 'id_rsa')
                self.ssh.connect(hostname=self.ip, username=self.login, pkey=key, look_for_keys=False)
            return True
        except:
            return False

    def disconect(self):
        self.ssh.close()

    def query(self):
        result = {}
        for query in self.template.get('queries'):
            n = query.get("name")
            c = query.get("command")
            t = 1
            if query.get("timeout"):
                t = query["timeout"]
            if n and c:
                stdin, stdout, stderr = self.ssh.exec_command(c, timeout=t)
                result[n] = ''.join([i.replace("\n", "<br>") for i in stdout.readlines()])
        return result