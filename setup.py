from setuptools import setup, find_packages

setup(name='my-lib',
      version='0.2',
      description='Stuff. Now in a namespace "my". Alias to myoldlib for backwards compat if things are broken.',
      packages=['my.oldlib'],
      zip_safe=False)

setup(name='myoldlib',
      version='0.2',
      description='Stuff. Now in a namespace "my". Alias to myoldlib for backwards compat if things are broken.',
      packages=['myoldlib'],
      zip_safe=False)
