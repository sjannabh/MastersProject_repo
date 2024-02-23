<h1 align="center">E-Commerce with Product Recommendation System 🚀</h1>
<p align="center">
  <img src="https://img.shields.io/npm/v/readme-md-generator.svg?orange=blue" />
  <a href="https://github.com/kefranabg/readme-md-generator/blob/master/LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-yellow.svg" target="_blank" />
  </a>
</p>

> CLI that generates beautiful README.md files.<br /> `readme-md-generator` will suggest you default answers by reading your `package.json` and `git` configuration.

# E-Commerce with Product Recommendation System

Final Semester Project of Masters

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following packages:

```bash
pip install python-dotenv
pip install pandas
pip install flask
pip install flask_httpauth
pip install -U flask-cors
pip install pyodbc
pip install pymongo
pip install scipy
pip install --upgrade watchdog
pip install -U scikit-learn scipy matplotlib
```

```bash
pip install python-dotenv pandas flask flask_httpauth scipy pyodbc pymongo -U flask-cors -U scikit-learn scipy matplotlib --upgrade watchdog
```

## 🚀 Usage

```python
import foobar

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

# Sample Execution & Output

If run without command line arguments, using

```
./precisionEstimate
```

the following usage message will be displayed.

```
Usage: ./estimatePrecision.py num_execs [arbitrary precision]
```

If run using

```
./precisionEstimate 1000000
```

output _simliar_ to

```
           float|  3.7247|2.220446049250313e-16
 float-type-hint|  3.6731|2.220446049250313e-16
      Decimal-28| 31.8602|0.999999999999999999999999999
```

will be generated. Note that the `float` and `float-type-hint` lines may vary.

---

An optional precision command line argument can be supplied to change the
arbitrary precision used by the Python `decimal` module. For example:

```
./precisionEstimate 1000000 16
```

will generate output similar to

```
           float| 0.3979|2.220446049250313e-16
 float-type-hint| 0.4053|2.220446049250313e-16
      Decimal-16| 3.1643|0.999999999999999
```

## 👤 Author

**Srilekha Jannabhatla**

- Github: [@srilekha](https://github.com/srilekha)

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## 📝 License

[MIT](https://choosealicense.com/licenses/mit/)
