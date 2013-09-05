#coding:utf-8
import os
import re
import ftplib
import calendar
import MySQLdb
import logging

import settings  # This is mine. Your settings is up to you

from datetime import timedelta, date
from time import strftime,localtime


def login_ftp(host, user, pswd, port=None):
    try:
        if port:
            ftp_handle = ftplib.FTP()
            ftp_handle.connect(host, port)
        else:
            ftp_handle = ftplib.FTP(host)
    except:
        import traceback
        logging.error(u'opened ftp connection error')
        traceback.print_exc()
    logging.info(u'connected ftp success: %s' %host)

    try:
        ftp_handle.login(user,pswd)
    except:
        logging.error(u'login ftp error')
        ftp_handle.quit()
        return 0
    ftp_handle.set_pasv(0)

    return ftp_handle

def get_manychnl_file(date, ftp_setting):
    ftp_handle = login_ftp(ftp_setting['HOST'],
                           ftp_setting['manychnl']['USER'],
                           ftp_setting['manychnl']['PSWD'])
    get_dir(ftp_handle,
            ftp_setting['manychnl']['from'],
            ftp_setting['manychnl']['to'],
            date,
            r'^\d+_%s.zip$' % date.strftime('%Y%m%d'))
    ftp_handle.quit()

def get_other_file(date, ftp_setting):
    ftp_handle = login_ftp(ftp_setting['other']['HOST'],
                           ftp_setting['other']['USER'],
                           ftp_setting['other']['PSWD'])
    get_dir(ftp_handle,
            ftp_setting['other']['from'],
            ftp_setting['other']['to'],
            date,
            r'^ACC%sCHK$' % date.strftime('%Y%m%d'),
            'other')
    ftp_handle.quit()

def get_all_file(date):
    ftp_setting = settings.PAYCHNL_FTP

    get_manychnl_file(date, ftp_setting)
    get_other_file(date, ftp_setting)

def get_dir(ftp_handle, remote_dir, local_dir, date, file_format, other_name=None):
    logging.info(u'download remote dir: %s' % remote_dir)
    try:
        ftp_handle.cwd(remote_dir)
    except:
        logging.error(u'did not cd to ftp remote dir: %s' %remote_dir)
        return -1

    #file_format = '%s' %date.strftime('%m%d')
    dl_files =  []
    if other_name in ['other']:
        ftp_handle.set_pasv(True)
    all_files = ftp_handle.retrlines('NLST', lambda name: dl_files.append(name) if re.compile(file_format).match(name) else None)
    logging.info(u'dl_files: %s' % dl_files)
    logging.info(u'all_files: %s' % all_files)

    for fn in dl_files:
        try:
            ftp_handle.retrbinary('RETR %s'%fn, open(local_dir+fn, 'wb').write, 1024)
        except:
            logging.error(u'did not download files：%s%s' % (remote_dir, fn))
        else:
            logging.info(u'download files over：%s%s' % (remote_dir, fn))
    logging.info(u'download dir over：%s' % remote_dir)

def get_file(ftp_handle, remote_path, local_path):
    logging.info(u'download remote file: %s' % remote_path)
    remote_dir = os.path.dirname(remote_path)
    fn = os.path.basename(remote_path)
    try:
        ftp_handle.cwd(remote_dir)
    except:
        logging.error(u'did not cd to ftp remote dir: %s' %remote_dir)
        return -1

    try:
        ftp_handle.retrbinary('RETR %s' % fn, open(local_path, 'wb').write, 1024)
    except:
        logging.error(u'did not download files：%s%s' % (remote_dir, fn))
    else:
        logging.info(u'download files over：%s%s' % (remote_dir, fn))

if __name__=='__main__':
    yest = date.today()-timedelta(days=1)
    get_all_file(yest)
