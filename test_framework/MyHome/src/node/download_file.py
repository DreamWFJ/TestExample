# -*- coding: utf-8 -*-
# ===================================
# ScriptName : download_file.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-12-06 14:02
# ===================================
import os
from .base import BaseHandler


class DownloadFileHandler(BaseHandler):
    def transmit_data(self, file_path):
        # .*（ 二进制流，不知道下载文件类型）	application/octet-stream
        # txt  -- text/plain
        # img  -- application/x-img
        self.set_header ('Content-Type', 'text/plain')
        self.set_header ('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(file_path)))
        #读取的模式需要根据实际情况进行修改
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(512)
                if not data:
                    break
                self.write(data)
        self.finish()

    def get(self, *args, **kwargs):
        filename = self.get_argument("filename", None)
        print "filename: ", filename
        if filename.endswith(".log"):
            download_log_dir = os.environ["DOWNLOAD_LOG_PATH"]
            log_file_path = os.path.join(download_log_dir, filename)
            print "log_file_path: ", log_file_path
            if os.path.exists(log_file_path):
                self.transmit_data(log_file_path)
            else:
                self.write_error(404)


        elif filename.endswith(".sh") or filename.endswith(".txt") or filename.endswith(".py"):
            download_script_dir = os.environ["DOWNLOAD_SCRIPT_PATH"]
            script_file_path = os.path.join(download_script_dir, filename)
            print "script_file_path: ", script_file_path
            if os.path.exists(script_file_path):
                self.transmit_data(script_file_path)
            else:
                self.write_error(404)
        else:
            self.write_error(404)


    def post(self, *args, **kwargs):
        pass




if __name__ == '__main__':
    pass
    