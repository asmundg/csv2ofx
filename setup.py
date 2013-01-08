from setuptools import find_packages, setup

setup(name='csv2ofx',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'csv2ofx-fokus = csv2ofx.fokus:main']})
