from setuptools import setup, find_packages
setup(name='dxl-dxpy',
      version='0.7.1',
      description='Duplicate components library python library.',
      url='https://github.com/Hong-Xiang/dxl',
      author='Hong Xiang',
      author_email='hx.hongxiang@gmail.com',
      license='MIT',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests", "dxpy.tests"]),
      install_requires=[
          'rx',
          'flask_restful',
          'flask_sqlalchemy',
          'graphviz',
          'fs',
          'apscheduler',
          'ruamel.yaml',
          'arrow'
      ],
      scripts=['bin/dxpy'],
      zip_safe=False)
