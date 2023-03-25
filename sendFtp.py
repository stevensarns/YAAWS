
import ftplib

def send():
        try:
                ftp = ftplib.FTP()
                host = "xxx.com"
                port = 21
                ftp.connect(host, port)
                ftp.login("xxx", "xxx")
                ftp.cwd('/public_html/wimages')
                filename = 'vout.png'
                ftp.storbinary('STOR '+filename, open(filename, 'rb'))
                filename = 'tin.png'
                ftp.storbinary('STOR '+filename, open(filename, 'rb'))
                filename = 'pout.png'
                ftp.storbinary('STOR '+filename, open(filename, 'rb'))
                filename = 'tout.png'
                ftp.storbinary('STOR '+filename, open(filename, 'rb'))
                # filename = 'pic.jpg'
                # ftp.storbinary('STOR '+filename, open(filename, 'rb'))
                ftp.quit()
        except:
                print("FTP fail")

