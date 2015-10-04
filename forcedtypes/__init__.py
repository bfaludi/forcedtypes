
# -*- coding: utf-8 -*-

"""
Force crappy data into python type.
Copyright (C) 2015, Bence Faludi (bence@ozmo.hu)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, <see http://www.gnu.org/licenses/>.
"""

import re
import sys
import types
from babel.numbers import parse_decimal, parse_number
from dateutil.parser import parse as parse_datetime
from abc import ABCMeta, abstractmethod
from datetime import date, datetime

# True if we are running on Python 3.
PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str,
    unicode = str
    long = int

else:
    string_types = basestring,
    
remove_space = re.compile(u' ')

class TypeConstructor(object):
    def __init__(self, type, *args, **kwargs):
        self.type = type
        self.args = args
        self.kwargs = kwargs
        
    def __call__(self, value):
        return self.type(value, *self.args, **self.kwargs)

def new(type, *args, **kwargs):
    return TypeConstructor(type, *args, **kwargs)

class Type(object):
    
    __metaclass__ = ABCMeta
    
    def __new__(cls, value, *args, **kwargs):
        if cls.is_empty(value):
            return None
        
        if cls.is_non_convertable(value):
            return value
        
        return cls.get_converted_value(value, *args, **kwargs)
    
    @classmethod
    def is_empty(cls, value):
        return value is None or len(unicode(value).strip()) == 0
    
    @classmethod
    def is_non_convertable(cls, value):
        return isinstance(value, cls.__base__)
    
    @classmethod
    def _try(cls, func, args, kwargs = None):
        try:
            return func(*args, **(kwargs or {}))
            
        except:
            return None
            
    @classmethod
    def coalesce(cls, tests):
        for test in tests:
            if len(test) == 3:
                func, args, kwargs = test
            else:
                func, args = test
                kwargs = None
            
            rvalue = cls._try(func, args, kwargs)
            if rvalue is not None:
                return rvalue
                
        return None
    
    @classmethod
    @abstractmethod
    def get_converted_value(cls, value):
        pass

class Float(Type, float):
    @classmethod
    def get_converted_value(cls, value, locale = None):
        if locale:
            rvalue = cls._try( 
                parse_decimal, 
                (remove_space.sub( u'', unicode(value) ), locale,)
            )
            return float(rvalue) if rvalue else None
        
        return cls.coalesce([
            ( float.__new__, (cls, value, ) ),
            ( float.__new__, (cls, re.sub(u',', u'.', remove_space.sub(u'', unicode(value))), ) ),
        ])

class Int(Type, long):
    @classmethod
    def get_converted_value(cls, value, locale = None):
        return cls.coalesce([
            ( long.__new__, (cls, value,) ),
            ( long.__new__, (cls, Float(value),) ),
        ])
    
class Datetime(Type, datetime):
    @classmethod
    def is_non_convertable(cls, value):
        return value.__class__ is datetime
        
    @classmethod
    def get_converted_value(cls, value, *args, **kwargs):
        if isinstance(value, (tuple, list)):
            return cls._try( datetime, value )
        
        if value.__class__ is date:
            return datetime(value.year, value.month, value.day)
        
        if not isinstance(value, string_types):
            return None
        
        return cls._try( parse_datetime, (value,), kwargs )
                
class Date(Type, date):
    @classmethod
    def is_non_convertable(cls, value):
        return value.__class__ is date
    
    @classmethod
    def get_converted_value(cls, value, *args, **kwargs):
        if isinstance(value, (tuple, list)):
            return cls._try( date, value )
        
        if value.__class__ is datetime:
            return value.date()
        
        if not isinstance(value, string_types):
            return None
        
        rvalue = cls.coalesce([
             ( parse_datetime, (value,), kwargs ),
             ( parse_datetime, (value.split(u' ')[0],), kwargs ),
        ])
        if rvalue:
            return rvalue.date()

class Str(Type, unicode):
    @classmethod
    def get_converted_value(cls, value):
        return unicode.__new__(cls, value)

class Bool(Type):
    TRUE_VALUES = ( 't', 'true', 'yes', 'y', )
    FALSE_VALUES = ( 'f', 'false', 'no', 'n', )
    
    @classmethod
    def is_empty(cls, value):
        return False 
    
    @classmethod
    def get_converted_value(cls, value):
        if value is None:
            return value
        
        if isinstance(value, string_types) and value.lower().strip() in cls.TRUE_VALUES:
            return True
        
        elif isinstance(value, string_types) and value.lower().strip() in cls.FALSE_VALUES:
            return False
        
        elif isinstance(value, string_types) and value.replace(u'.',u'',1).isdigit():
            return bool(Float(value))
        
        return bool(value)
        