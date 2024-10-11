from setuptools import setup, find_packages

setup(name='hl7utils',
      version='0.0.1',
      description='helper functions for working with HL7 messages',
      url='https://github.com/PennMedicineVision/hl7-utils',
      author='Jeffrey Duda',
      author_email='jeff.duda@gmail.com',
      license='APACHE 2.0',
      packages=find_packages('src'),
      package_dir={'':'src'},
      zip_safe=False)
