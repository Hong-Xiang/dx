from setuptools import setup

setup(name='dxpy',
      version='0.1',
      description='Duplicate components library python sub-library.',
      url='https://github.com/Hong-Xiang/dxl',
      author='Hong Xiang',
      author_email='hx.hongxiang@gmail.com',
      license='MIT',
      packages=[],
      install_requires=[
          'rx',
          'flask_restful',
          'flask_sqlalchemy',
          'graphviz',
          'fs'
      ],
      zip_safe=False)
