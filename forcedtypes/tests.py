
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

import unittest
import forcedtypes as t
from datetime import date, datetime

class TestNewFunction(unittest.TestCase):
    def test_parameter(self):
        self.assertEqual( t.new(t.Float, locale = 'hu')('4,1232'), 4.1232 )
        self.assertEqual( t.new(t.Float, locale = 'en_US')('4,1232'), 41232 )

    def test_without_parameter(self):
        self.assertEqual( t.new(t.Float)('4,1232'), 4.1232 )

class TestFloat(unittest.TestCase):
    def test_type(self):
        self.assertEqual(type(t.Float('4')), float)

    def test_bool(self):
        self.assertEqual(t.Float(True), 1.0)
        self.assertEqual(t.Float(False), 0.0)

    def test_int(self):
        self.assertEqual(t.Float(4), 4.0)
        self.assertEqual(t.Float('4'), 4.0)
        self.assertEqual(t.Float(' 4 '), 4.0)

    def test_float(self):
        self.assertEqual(t.Float(4.1232), 4.1232)
        self.assertEqual(t.Float('4.1232'), 4.1232)
        self.assertEqual(t.Float('4,1232'), 4.1232)

        self.assertEqual(t.Float('4,1232', locale = 'hu'), 4.1232)
        self.assertEqual(t.Float('4,1232', locale = 'en_US'), 41232)

    def test_str(self):
        self.assertIsNone(t.Float('str'))

    def test_date(self):
        self.assertIsNone(t.Float(date.today()))

    def test_datetime(self):
        self.assertIsNone(t.Float(datetime.now()))

    def test_none(self):
        self.assertIsNone(t.Float(''))
        self.assertIsNone(t.Float(None))

class TestInt(unittest.TestCase):
    def test_type(self):
        self.assertEqual(type(t.Int('4')), t.long)

    def test_bool(self):
        self.assertEqual(t.Int(True), 1)
        self.assertEqual(t.Int(False), 0)

    def test_int(self):
        self.assertEqual(t.Int(4), 4)
        self.assertEqual(t.Int('4'), 4)
        self.assertEqual(t.Int(' 4 '), 4)

    def test_float(self):
        self.assertEqual(t.Int(4.1232), 4)
        self.assertEqual(t.Int('4.1232'), 4)
        self.assertEqual(t.Int('4,1232'), 4)

    def test_str(self):
        self.assertIsNone(t.Int('str'))

    def test_date(self):
        self.assertIsNone(t.Int(date.today()))

    def test_datetime(self):
        self.assertIsNone(t.Int(datetime.now()))

    def test_none(self):
        self.assertIsNone(t.Int(''))
        self.assertIsNone(t.Int(None))

class TestBool(unittest.TestCase):
    def test_type(self):
        self.assertEqual(type(t.Bool('t')), bool)

    def test_none(self):
        self.assertIsNone(t.Bool(None))

    def test_bool(self):
        self.assertTrue(t.Bool(True))
        self.assertFalse(t.Bool(False))

    def test_int(self):
        self.assertTrue(t.Bool(1))
        self.assertFalse(t.Bool(0))
        self.assertTrue(t.Bool('1'))
        self.assertFalse(t.Bool('0'))

    def test_str(self):
        self.assertTrue(t.Bool('tRuE'))
        self.assertFalse(t.Bool('fAlSe'))
        self.assertTrue(t.Bool('Yes'))
        self.assertFalse(t.Bool('No'))
        self.assertTrue(t.Bool('t'))
        self.assertFalse(t.Bool('F'))
        self.assertTrue(t.Bool('Y'))
        self.assertFalse(t.Bool('n'))

        self.assertFalse(t.Bool(''))
        self.assertTrue(t.Bool('sth'))

    def test_float(self):
        self.assertTrue(t.Bool(1.0))
        self.assertFalse(t.Bool(0.0))
        self.assertTrue(t.Bool('1.0'))
        self.assertFalse(t.Bool('0.0'))

    def test_date(self):
        self.assertTrue(t.Bool(date.today()))

    def test_datetime(self):
        self.assertTrue(t.Bool(datetime.now()))

class TestStr(unittest.TestCase):
    def test_type(self):
        self.assertEqual(type(t.Str(4)), t.unicode)

    def test_str(self):
        self.assertEqual(t.Str(u'sth'), u'sth')

    def test_bool(self):
        self.assertEqual(t.Str(True), 'True')
        self.assertEqual(t.Str(False), 'False')

    def test_none(self):
        self.assertIsNone(t.Str(None))
        self.assertIsNone(t.Str(u''))

    def test_int(self):
        self.assertEqual(t.Str(3), '3')

    def test_float(self):
        self.assertEqual(t.Str(3.12), '3.12')

    def test_date(self):
        self.assertEqual(t.Str(date.today()), str(date.today()))

    def test_datetime(self):
        dt = datetime.now(); self.assertEqual(t.Str(dt), str(dt))

class TestDate(unittest.TestCase):
    def test_type(self):
        self.assertEqual(type(t.Date('2015-03-14')), date)

    def test_none(self):
        self.assertIsNone(t.Date(None))
        self.assertIsNone(t.Date(''))

    def test_bool(self):
        self.assertIsNone(t.Date(True))
        self.assertIsNone(t.Date(False))

    def test_str(self):
        self.assertEqual(t.Date('2015-03-14'), date(2015, 3, 14))
        self.assertEqual(t.Date('03/04/15'), date(2015, 3, 4))
        self.assertEqual(t.Date('03/04/15', dayfirst = True), date(2015,4,3))

        self.assertEqual(t.Date('2013-02-03'), date(2013, 2, 3))
        self.assertEqual(t.Date('2013/02/03'), date(2013, 2, 3))
        self.assertEqual(t.Date('2013.02.03'), date(2013, 2, 3))
        self.assertEqual(t.Date('02/03/2013'), date(2013, 2, 3))
        self.assertEqual(t.Date('Dec 26, 2012 10:01:26 AM'), date(2012, 12, 26))
        self.assertEqual(t.Date('2012.12.26 10.01.26'), date(2012, 12, 26))

        self.assertIsNone(t.Datetime('invalid'))

    def test_list(self):
        self.assertEqual(t.Date([2013,2,3]), date(2013,2,3))
        self.assertIsNone(t.Date([2013,2,3,11,32,33]))
        self.assertIsNone(t.Date([2013,2]))

    def test_tuple(self):
        self.assertEqual(t.Date((2013,2,3)), date(2013,2,3))
        self.assertIsNone(t.Date((2013,2,3,11,32,33)))
        self.assertIsNone(t.Date((2013,2)))

    def test_int(self):
        self.assertIsNone(t.Date(321312312))

    def test_float(self):
        self.assertIsNone(t.Date(321312312))

    def test_date(self):
        self.assertEqual(t.Date(date(2015,4,3)), date(2015,4,3))

    def test_datetime(self):
        self.assertEqual(t.Date(datetime(2015,4,3,11,12,13)), date(2015,4,3))

class TestDatetime(unittest.TestCase):
    def test_type(self):
        self.assertEqual(type(t.Datetime('2015-03-14')), datetime)

    def test_none(self):
        self.assertIsNone(t.Datetime(None))
        self.assertIsNone(t.Datetime(''))

    def test_bool(self):
        self.assertIsNone(t.Datetime(True))
        self.assertIsNone(t.Datetime(False))

    def test_str(self):
        self.assertEqual(t.Datetime('2015-03-14'), datetime(2015,3,14))
        self.assertEqual(t.Datetime('03/04/15'), datetime(2015,3,4))
        self.assertEqual(t.Datetime('03/04/15', dayfirst = True), datetime(2015,4,3))

        self.assertEqual(t.Datetime('2013-02-03 11:32:33'), datetime( 2013, 2, 3, 11, 32, 33 ) )
        self.assertEqual(t.Datetime('2013.02.03 11:32:33'), datetime( 2013, 2, 3, 11, 32, 33 ) )
        self.assertEqual(t.Datetime('2013/02/03 11:32:33'), datetime( 2013, 2, 3, 11, 32, 33 ) )
        self.assertEqual(t.Datetime('02/03/2013 11:32:33'), datetime( 2013, 2, 3, 11, 32, 33 ) )
        self.assertEqual(t.Datetime('2013-04-04 16:06:58.929515'), datetime( 2013, 4, 4, 16, 6, 58, 929515 ) )

        self.assertIsNone(t.Datetime('invalid'))

    def test_list(self):
        self.assertEqual(t.Datetime([2013,2,3,11,32,33]), datetime(2013, 2, 3, 11, 32, 33))
        self.assertIsNone(t.Datetime([2013,2]))

    def test_tuple(self):
        self.assertEqual(t.Datetime((2013,2,3,11,32,33)), datetime(2013, 2, 3, 11, 32, 33))
        self.assertIsNone(t.Datetime((2013,2)))

    def test_int(self):
        self.assertIsNone(t.Datetime(321312312))

    def test_float(self):
        self.assertIsNone(t.Datetime(321312312))

    def test_date(self):
        self.assertEqual(t.Datetime(date(2015,4,3)), datetime(2015,4,3))

    def test_datetime(self):
        self.assertEqual(t.Datetime(datetime(2015,4,3,11,12,13)), datetime(2015,4,3,11,12,13))
