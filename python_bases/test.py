# -*- coding: utf-8 -*-
# ===================================
# ScriptName : test.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2016-09-06 17:19
# ===================================
import six

class Field(object):
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)

class StringField(Field):
    def __init__(self, name):
        super(StringField, self).__init__(name, 'varchar(100)')

class IntegerField(Field):
    def __init__(self, name):
        super(IntegerField, self).__init__(name, 'bigint')

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)

        mappings = dict()
        for k, v in attrs.iteritems():
            if isinstance(v, Field):
                mappings[k] = v
        for k in mappings.iterkeys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings
        attrs['__table__'] = name
        return type.__new__(cls, name, bases, attrs)

@six.add_metaclass(ModelMetaclass)
class Model(dict):
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, item):
        print 'key:',item
        try:
            return self[item]
        except KeyError:
            raise AttributeError("'Model' object has no attribute '%s'" %item)

    def __setattr__(self, key, value):
        print 'key:value = %s:%s'%(key, value)
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.iteritems():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        print 'SQL: %s' % sql
        print 'ARGS: %s' % str(args)

class User(Model):
    id = IntegerField('uid')
    print id
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')




if __name__ == '__main__':
    u = User(id=123456, name='WFJ', email='wfj_sc@163.com', password='abc')
    u.save()
    