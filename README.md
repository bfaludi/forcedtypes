# forcedtypes 

[![Build Status](https://travis-ci.org/bfaludi/forcedtypes.svg)](https://travis-ci.org/bfaludi/forcedtypes)
![Downloads](https://img.shields.io/pypi/dm/forcedtypes.svg)
![Version](https://img.shields.io/pypi/v/forcedtypes.svg)
![License](https://img.shields.io/pypi/l/forcedtypes.svg)

Force crappy data into Python type. Yeah, I know It sounds strange but It could be useful sometimes. Ohh, did I mention that It is working with Python **2.7** & **3.3+**.

Supported types:

- t.Bool -> `bool`
- t.Int -> `long` in PY2, `int` in PY3
- t.Float -> `float`
- t.Date -> `datetime.date`
- t.Datetime -> `datetime.datetime`
- t.Str -> `unicode` in PY2, `str` in PY3

### How to install

You can use `easy_install` or `pip` to install the package.

```bash
$ easy_install forcedtypes
```

### Examples

Let's see some examples for this awesomeness.

```python
>>> import forcedtypes as t
```

##### 1. Date parsing

```python
>>> t.Date('3/4/15')
datetime.date(2015, 3, 4)
>>> t.Date('3/4/15', dayfirst=True)
datetime.date(2015, 4, 3)
```

##### 2. String to boolean

```python
>>> t.Bool('yes') == t.Bool('t') == t.Bool(1.0) == True
True
```

##### 3. Float with unique separator

If you want to convert `3,400` to `float` It will give you error:

```python
>>> float('3,400')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: could not convert string to float: '3,400'
```

The `forcedtypes` package makes it easier.

```python
>>> t.Float('3,400')
3.4
>>> t.Float('3,400', locale='de_DE')
3.4
>>> t.Float('3,400', locale='en_US')
3400.0
```

##### 4. Eliminate empty strings

```python
>>> t.Str('     ') is None
True
```

##### 5. Use for type enforcement

If you have a file like this one,

```csv
1;3.4;Item 1.
3;55.6;Item 2.
4;44,5;
6;77.5;Item 4.
```

You can use this script ...

```python
import forcedtypes as t

with open('file.csv','r', encoding='utf-8') as fd:
    for line in fd.readlines():
        id, price, name = map(lambda x,: x[0](x[1]), 
        	zip([int, t.Float, t.Str], line.split(';')))
        print(repr(id), repr(price), repr(name))
```

... to get the correct result:

```tsv
1 3.4 'Item 1.\n'
3 55.6 'Item 2.\n'
4 44.5 None
6 77.5 'Item 4.'
```

##### 6. Type conversion based on rule

You can create a new type based on additional attribute.

```python
>>> ft = t.new(t.Float, locale='en_US')
>>> ft('3,4')
34.0
>>> ft('3.4')
3.4
>>> ft('3,400.43')
3400.43
```
