from setuptools import setup

# may work with older versions of pip, should find out.
setup(name='requiremensfinder',
      version='0.01',
      py_modules=['requirementsfinder'],
      install_requires=['pip>=6.1.1', 'argparse'],
      author='James P Robinson Jr',
      author_email="JamesPRobinsonJr@gmail.com",
      entry_points={
          "console_scripts": [
              "requirementsfinder=requirementsfinder:main",
          ],
      },
      license='MIT',
      classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 2.7",
    ],
      )
