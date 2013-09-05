#coding=utf-8

import time
import pdb
import xlrd

from pyExcelerator import *


def write(ws, line, value):
    t_width = 0x12dc
    for i in value:
        ws.write(line, i, value[i])
        ws.col(i).width = t_width

def to_excel(sheet_name, table_title, table_data, file_name, path):
    """生成excel
    Args:
        sheet_name: sheet名称
        table_title: 表头
        table_data: 表数据
        file_name: 文件名
        path: 路径
    Returns:
        path: 生成excel路径
    """
    wb = Workbook()
    ws = wb.add_sheet(sheet_name)

    line = 0
    write(ws, line, table_title)

    for k, v in table_data.iteritems():
        line += 1
        value = {}
        for i in table_title:
            if i:
                value[i] = v[i-1]
            else:
                value[i] = k
        write(ws, line, value)

    wb.save(path + file_name)

    return path + file_name

def write_list(ws, line, value):
    t_width = 0x12dc
    for i, v in enumerate(value):
        try:
            ws.write(line, i, v)
        except UnicodeDecodeError, e:
            ws.write(line, i, v.decode('utf8'))
        ws.col(i).width = t_width

def list2excel(sheet_name, table_title, table_data, file_name, path):
    """生成excel
    Args:
        sheet_name: sheet名称
        table_title: 表头
        table_data: 表数据
        file_name: 文件名
        path: 路径
    Returns:
        path: 生成excel路径
    """
    wb = Workbook()
    ws = wb.add_sheet(sheet_name)

    line = 0
    write_list(ws, line, table_title)

    for i, v in enumerate(table_data):
        line += 1
        write_list(ws, line, v)

    wb.save(path + file_name)

    return path + file_name

def list2excel_sheets(sheet_list, titles_list, contents_list, file_name, modeladmin=None, request=None):
    """生成多sheet的excel
    Args:
        sheet_list: 多sheet名称列表
        titles_list: 多表头列表
        contents_list: 多表数据列表
        file_name: 文件名
        modeladmin: admin对象
        request: request
    Returns:
        path: 生成excel路径
    """
    wb = Workbook()

    for sheet, titles, contents in zip(sheet_list, titles_list, contents_list):
        ws = wb.add_sheet(sheet)
        write_list(ws, 0, titles)
        for i, v in enumerate(contents):
            write_list(ws, i+1, v)

    path = '/tmp/%s.xls' % (file_name)
    wb.save(path)

    if modeladmin and request:
        uid = request.user.id
        vname = modeladmin.model._meta.verbose_name
        from audit.models import OpLog
        OpLog.objects.create(admin_id=uid, op_type=5, action=u'¿?¿?¿?¿?', memo='', detail='¿?¿?¿?%d¿?¿?%s¿?¿?'%(uid,vname))

    return path

def xls2list(file_name):
    hfile = xlrd.open_workbook(file_name.decode('utf8'))  # 仅支持xls
    sheets_index = range(hfile.nsheets)

    # 一次性全部读取xls信息
    data = []
    for sheet_id in sheets_index:
        sheet = hfile.sheet_by_index(sheet_id)
        for row in range(sheet.nrows):
            data.append(sheet.row_values(row))

    return data


class XlsWriter(object):
    def __init__(self, sheet_name, table_title, file_name, path):
        self.sheet_name = sheet_name
        self.table_title = table_title
        self.file_name = file_name
        self.path = path
        self.line = 0
        self.col_width = 0x12dc
        self.wb = Workbook()
        self.ws = self.wb.add_sheet(sheet_name)

        self.write_list(self.table_title)

    def write_line(self, *args, **kwargs):
        cols = int(args[0])

        for i in range(cols):
            val = kwargs.get(str(i), '')
            self.ws.write(self.line, i, val)
        self.line += 1
        return True

    def write_string(self, strline, delimiter):
        """write a string which is split by ....
        """
        splits = strline.split(delimiter)
        for i, v in enumerate(splits):
            try:
                self.ws.write(self.line, i, v)
            except UnicodeDecodeError, e:
                self.ws.write(self.line, i, v.decode('utf8'))
        self.line += 1
        return True

    def write_list(self, varlist):
        for i, v in enumerate(varlist):
            try:
                self.ws.write(self.line, i, v)
            except UnicodeDecodeError, e:
                self.ws.write(self.line, i, v.decode('utf8'))
            self.ws.col(i).width = self.col_width
        self.line +=1

    def save(self):
        self.wb.save(self.path + self.file_name)
        return True


if __name__ == "__main__":
    pass

