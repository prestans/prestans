# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
#  prestans, a standards based WSGI compliant REST framework for Python
#  http://prestans.org
#
#  Copyright (c) 2013, Eternity Technologies Pty Ltd.
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#      * Neither the name of Eternity Technologies nor the
#        names of its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL ETERNITY TECHNOLOGIES BE LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import inspect
import copy
import re
import os
import base64

from datetime import datetime
from datetime import date
from datetime import time

import prestans.parsers
import prestans.exceptions

#:
#: Base type classes
#: 

class DataType(object):
    
    def validate(self, value):
        raise exceptions.DirectUserNotAllowed("validate", self.__class__.__name__)

class DataStructure(DataType):
    """
    Wrappers on Python types generally represented as structures e.g DateTime

    as_serializable methods signature for %DataStructure is different to that of DataCollection
    it requires a value to be passed in, this is because the python type of structures is 
    difference to what gets serialized.

    E.g DateTime serializes itself as a ISO string
    """
    
    def as_serializable(self, value):
        raise prestans.exceptions.DirectUseNotAllowed("as_serializable", self.__class__.__name__)

class DataCollection(DataType):

    def validate(self, value, attribute_filter=None):
        raise prestans.exceptions.DirectUseNotAllowed("validate", self.__class__.__name__)

    def as_serializable(self, attribute_filter=None):
        raise prestans.exceptions.DirectUseNotAllowed("as_serializable", self.__class__.__name__)

    def get_attribute_filter(self):
        raise prestans.exceptions.DirectUseNotAllowed("get_attribute_fitler", self.__class__.__name__)

#:
#: Basic Types
#:

class String(DataType):
    
    def __init__(self, 
                 default=None, 
                 min_length=None, 
                 max_length=None, 
                 required=True, 
                 format=None, 
                 choices=None, 
                 utf_encoding='utf-8'):

        if min_length and max_length and min_length > max_length:
            pass

        if required and min_length and min_length < 1:
            pass

        self._default = default
        self._min_length = min_length
        self._max_length = max_length
        self._required = required
        self._format = format
        self._choices = choices
        self._utf_encoding = utf_encoding

    def validate(self, value):

        _validated_value = None
        
        if self._required and self._default is None and value is None:
            raise prestans.exceptions.RequiredAttribute()
        elif self._required and value is None:
            value = self._default
        elif not self._required and self._default is None and value is None:
            return _validated_value
        elif not self._required and value is None:
            value = self._default
        
        try:
            if isinstance(value, unicode):
                _validated_value = str(value.decode(self._utf_encoding))
            else:
                _validated_value = str(value)
        except:
            raise prestans.exceptions.ParseFailed(value, 'String')
        
        if not self._required and len(_validated_value) == 0:
            return _validated_value
        
        if _validated_value is not None and self._min_length and len(_validated_value) < self._min_length:
            raise prestans.exceptions.UnacceptableLength(value, self._min_length, self._max_length)
        if _validated_value is not None and self._max_length and len(_validated_value) > self._max_length:
            raise prestans.exceptions.UnacceptableLength(value, self._min_length, self._max_length)
            
        if self._choices is not None and not _validated_value in self._choices:
            raise prestans.exceptions.InvalidChoice(value, self._choices)
            
        if self._format is not None and re.search(self._format, _validated_value) is None:
            raise prestans.exceptions.InvalidValue(_validated_value)
        
        return _validated_value

class Integer(DataType):

    def __init__(self, 
                 default=None, 
                 minimum=None, 
                 maximum=None, 
                 required=True, 
                 choices=None):

        if minimum and maximum and minimum > maximum:
            pass

        self._default = default
        self._minimum = minimum
        self._maximum = maximum
        self._required = required
        self._choices = choices

    def validate(self, value):

        _validated_value = None
        
        if self._required and self._default is None and value is None:
            raise prestans.exceptions.RequiredAttribute()
        elif self._required and value is None:
            value = self._default
        elif not self._required and self._default is None and value is None:
            return _validated_value
        elif not self._required and value is None:
            value = self._default
        
        try:
            _validated_value = int(value)
        except:
            raise prestans.exceptions.ParseFailed(value, 'Integer')
        
        if _validated_value and self._minimum is not None and _validated_value < self._minimum:
            raise prestans.exceptions.LessThanMinimum(value, self._minimum)
        if _validated_value and self._maximum is not None and _validated_value > self._maximum:
            raise prestans.exceptions.MoreThanMaximum(value, self._maximum)
            
        if self._choices is not None and not _validated_value in self._choices:
            raise prestans.exceptions.InvalidChoice(value, self._choices)
        
        return _validated_value

class Float(DataType):

    def __init__(self, 
                 default=None, 
                 minimum=None, 
                 maximum=None, 
                 required=True, 
                 choices=None):
        
        if minimum and maximum and minimum > maximum:
            pass
        
        self._default = default
        self._minimum = minimum
        self._maximum = maximum
        self._required = required
        self._choices = choices

    def validate(self, value):

        _validated_value = None
        
        if self._required and self._default is None and value is None:
            raise prestans.exceptions.RequiredAttribute()
        elif self._required and value is None:
            value = self._default
        elif not self._required and self._default is None and value is None:
            return _validated_value
        elif not self._required and value is None:
            value = self._default
        
        try:
            _validated_value = float(value)
        except:
            raise prestans.exceptions.ParseFailed(value, 'Float')
        
        if _validated_value and self._minimum is not None and _validated_value < self._minimum:
            raise prestans.exceptions.LessThanMinimum(value, self._minimum)
        if _validated_value and self._maximum is not None and _validated_value > self._maximum:
            raise prestans.exceptions.MoreThanMaximum(value, self._maximum)
            
        if self._choices is not None and not _validated_value in self._choices:
            raise prestans.exceptions.InvalidChoice(value, self._choices)
        
        return _validated_value

        
class Boolean(DataType):

    def __init__(self, 
                 default=None, 
                 required=True):


        self._default = default
        self._required = required

    def validate(self, value):

        _validated_value = None
        
        if self._required and self._default is None and value is None:
            raise prestans.exceptions.RequiredAttribute()
        elif self._required and value is None:
            value = self._default
        elif not self._required and self._default is None and value is None:
            return _validated_value
        elif not self._required and value is None:
            value = self._default
        
        try:
            _validated_value = bool(value)
        except: 
            raise prestans.exceptions.ParseFailed(value, 'Boolean')
        
        return _validated_value


class DataURLFile(DataType):
    """
    Accepts a Fileupload as part of the JSON body using FileReader's readAsDataURL

    readAsDataURL, encodes the contents of the file as a DataURLScheme, 
    http://en.wikipedia.org/wiki/Data_URI_scheme

    Example
    http://www.html5rocks.com/en/tutorials/file/dndfiles/

    Meta information about the file upload is upto the implementing application
    """

    @classmethod
    def generate_filename(cls):
        import uuid
        return uuid.uuid4().hex

    def __init__(self, 
                 required=True, 
                 allowed_mime_types=[]):

        self._required = required
        self._allowed_mime_types = allowed_mime_types

        if isinstance(allowed_mime_types, str):
            self._allowed_mime_types = [allowed_mime_types]

        self._mime_type = None
        self._file_contents = None

    @property
    def mime_type(self):
        return self._mime_type

    @property
    def file_contents(self):
        return self._file_contents        

    def validate(self, value):

        _validated_value = self.__class__()

        if self._required and value is None:
            raise prestans.exceptions.RequiredAttribute()

        if self._required is False and value is None:
            return value

        try:
            data_url, delimiter, base64_content = value.partition(',')
            _validated_value._mime_type = data_url.replace(';base64', '').replace('data:', '')
            _validated_value._file_contents = base64.b64decode(base64_content)
        except Exception, err:
            raise prestans.exceptions.ParseFailed(value, 'DataURLFile')

        if self._allowed_mime_types and len(self._allowed_mime_types) > 0 \
        and not _validated_value._mime_type in self._allowed_mime_types:
            raise prestans.exceptions.InvalidChoice(_validated_value._mime_type, self._allowed_mime_types)

        return _validated_value

    def save(self, path):
        """
        Writes file to a particular location

        This won't work for cloud environments like Google's Appengine, use with caution
        ensure to catch exceptions so you can provide informed feedback.

        prestans does not mask File IO exceptions so your handler can respond better.
        """
        
        file_handle = open(path, 'wb')
        file_handle.write(self._file_contents)
        file_handle.close()

#:
#: DataStructures
#:

class DateTime(DataStructure):
    """
    Default format is the Date Time Format string, defaults to RFC822
    """

    def __init__(self, 
                 default=None, 
                 required=True, 
                 format="%Y-%m-%d %H:%M:%S"):

        self._default = default
        self._required = required
        self._format = format

class Date(DataStructure):
    pass

class Time(DataStructure):
    pass

#:
#: Collections
#:

class Array(DataCollection):
    
    def __init__(self, 
                 default=None, 
                 required=True, 
                 element_template=None, 
                 min_length=None, 
                 max_length=None):
        
        self._default = default
        self._required = required
        self._element_template = element_template
        self._min_length = min_length
        self._max_length = max_length
        
        self._array_elements = []

    @property
    def element_template(self):
        return self._element_template

    @element_template.setter
    def element_template(self, value):
        self._element_template = value

    def remove(self, value):
        self._array_elements.remove(value)
    
    def __len__(self):
        return len(self._array_elements)
        
    def __iter__(self):
        #: With a little help from 
        #: http://johnmc.co/llum/the-easiest-way-to-implement-__iter__-for-a-python-object/
        for element in self._array_elements:
            yield element

    def __getitem__(self, index):
        return self._array_elements[index]

    def validate(self, value, attribute_filter=None):
        
        if not self._required and not value:
            return None

        _validated_value = self.__class__(element_template=self._element_template, 
                                     min_length=self._min_length, 
                                     max_length=self._max_length)
        
        if not isinstance(value, (list, tuple)):
            raise DataTypeValidationException(ERROR_MESSAGE.NOT_ITERABLE)
            
        for array_element in value:
    
            if issubclass(self._element_template.__class__, DataCollection):
                validated_array_element = self._element_template.validate(array_element, attribute_filter)
            else:
                validated_array_element = self._element_template.validate(array_element)
    
            _validated_value.append(validated_array_element)
    
        if self._min_length is not None and len(_validated_value) < self._min_length:
            raise prestans.exceptions.LessThanMinimum(value, self._minimum)

        if self._max_length is not None and len(_validated_value) > self._max_length:
            raise prestans.exceptions.MoreThanMaximum(value, self._maximum)

        return _validated_value
    
    def append(self, value):
        
        if isinstance(value, (list, tuple)):

            for element in value:
                self.append(element)
            return
        
        if isinstance(self._element_template.__class__, String.__class__) and \
        isinstance(value, str):
            value = self._element_template.__class__().validate(value)
        elif isinstance(self._element_template.__class__, String.__class__) and \
        isinstance(value, unicode):
            value = self._element_template.__class__().validate(value)
        elif isinstance(self._element_template.__class__, Integer.__class__) and \
        isinstance(value, int):
            value = self._element_template.__class__().validate(value)
        elif isinstance(self._element_template.__class__, Float.__class__) and \
        isinstance(value, float):
            value = self._element_template.__class__().validate(value)
        elif isinstance(self._element_template.__class__, Boolean.__class__) and \
        isinstance(value, bool):
            value = self._element_template.__class__().validate(value)
        elif not isinstance(value, self._element_template.__class__):
            raise TypeError("prestans array elements must be of type %s; given %s"
                            (self._element_template.__class__.__name__, value.__class__.__name__))
        
        self._array_elements.append(value)
            
    def as_serializable(self, attribute_filter=None):
        
        _result_array = list()
            
        for array_element in self._array_elements:
        
            if isinstance(array_element, str) or \
            isinstance(array_element, unicode) or \
            isinstance(array_element, float) or \
            isinstance(array_element, int) or \
            isinstance(array_element, bool):

                _result_array.append(array_element)
            else:
                _result_array.append(array_element.as_serializable(attribute_filter))
        
        return _result_array
        
    def get_attribute_filter(self, default_value=False):

        attribute_filter = None

        if issubclass(self._element_template.__class__, DataCollection):
            attribute_filter = self._element_template.get_attribute_filter(default_value)
        elif issubclass(self._element_template.__class__, DataType) or \
            issubclass(self._element_template.__class__, DataStructure):
            attribute_filter = default_value

        return attribute_filter

#:
#: Models
#:
        
class Model(DataCollection):

    def __init__(self, required=True, default=None, **kwargs):

        self._required = required
        self._default = default