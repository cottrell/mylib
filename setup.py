from setuptools import setup, find_packages

setup(name='my-lib',
      version='0.2',
      description='Stuff. Now in a namespace "my". Alias to mylib for backwards compat if things are broken.',
      packages=['my.lib'],
      zip_safe=False)
