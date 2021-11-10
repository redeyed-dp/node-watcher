from app import db
import requests

class Proxy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proto = db.Column(db.String(8))
    ip = db.Column(db.String(15))
    port = db.Column(db.Integer)
    login = db.Column(db.String(16))
    password = db.Column(db.String(32))

    def test(self):
        if self.proto in ('socks4', 'socks5'):
            proto=f"{self.proto}://"
        elif self.proto == 'http':
            proto=''
        else:
            return f"Unknown proxy protocol: {self.proto}"
        credentials = ''
        if self.login and self.password:
            credentials = f"{self.login}:{self.password}@"
        proxies = {'https': f"{proto}{credentials}{self.ip}:{self.port}"}
        try:
            r = requests.get('https://ifconfig.me', proxies=proxies)
            if r.status_code == 200:
                return r.text
            else:
                return f"Error: {r.status_code}"
        except Exception as e:
            return f"Error: {e}"
