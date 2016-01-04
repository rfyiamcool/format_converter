#coding:utf-8
import os
import sys
import csv
import json
import codecs

import yaml

PY2 = sys.version_info[0] == 2

def extension(filename):
    _, ext = os.path.splitext(filename)
    return ext


def is_string(variable):
    if PY2:
        return isinstance(variable, basestring)
    else:
        return isinstance(variable, str)


class Reader(object):
    def read(self, filename, encoding='utf-8'):
        with codecs.open(filename, 'r', encoding=encoding) as f:
            return f.read()

    def readJson(self, filename):
        return json.loads(self.read(filename))

    def readYaml(self, filename):
        return yaml.load(self.read(filename))

    def readCsv(self, filename, encoding='utf-8', delimiter=',', headers=False):
        with codecs.open(filename, 'r', encoding=encoding) as f:
            if headers:
                reader = csv.reader(f, delimiter=delimiter)
                h = next(reader)
                a = []
                for r in reader:
                    o = {}
                    for j, e in enumerate(r):
                        o[h[j]] = e
                    a.append(o)
                return a
            else:
                return [i for i in csv.reader(f, delimiter=delimiter)]


class Writer(object):
    def __init__(self, data, kind):
        self.data = data
        self.kind = kind
        self.defaultIndent = 2

    def write(self, ext, filename):
        ext = self.kind or ext

        if is_string(self.data):
            self.writePlain(filename, self.data)
        elif ext == '.json':
            self.writeJson(filename)
        elif ext == '.yml' or ext == '.yaml':
            self.writeYaml(filename)
        elif ext == '.csv' or ext == '.csvh':
            self.writeCsv(filename)
        else:
            self.writePlain(filename, self.data)

    def writePlain(self, filename, data):
        with codecs.open(filename, 'w', encoding='utf-8') as f:
            f.write(data)

    def writeJson(self, filename, indent=None):
        self.writePlain(filename, json.dumps(self.data, indent=indent))

    def writeYaml(self, filename, indent=None):
        self.writePlain(filename, yaml.safe_dump(self.data, indent=indent, default_flow_style=False))

    def writeCsv(self, filename, delimiter=','):
        headers = isinstance(self.data[0], dict) and list(self.data[0].keys())

        with codecs.open(filename, 'w', encoding='utf-8') as f:
            w = csv.writer(f, delimiter=delimiter)
            if headers:
                w.writerow(headers)
            for r in self.data:
                if headers:
                    w.writerow([r[i] for i in headers])
                else:
                    w.writerow(r)

    def __gt__(self, filename):
        ext = extension(filename)
        self.write(ext, filename)

class Converter(object):

    reader = Reader()

    def __init__(self, kind=None):
        self.kind = kind

    def read(self, ext, filename):
        ext = self.kind or ext

        if ext == '.json' or ext == '.pjson':
            return self.reader.readJson(filename)
        elif ext == '.yml' or ext == '.yaml':
            return self.reader.readYaml(filename)
        elif ext == '.csv':
            return self.reader.readCsv(filename)
        else:
            return self.reader.read(filename)

    def __lt__(self, filename):
        ext = extension(filename)
        return self.read(ext, filename)

    def __call__(self, data):
        return Writer(data, self.kind)

    @property
    def json(self):
        return converter('.json')

    @property
    def yaml(self):
        return converter('.yml')

    @property
    def yml(self):
        return converter('.yml')

    @property
    def csv(self):
        return converter('.csv')

converter = Converter()
