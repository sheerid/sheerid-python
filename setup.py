from distutils.core import setup

setup(
    name='sheerid',
    version='0.5.0',
    author='SheerID, Inc.',
    author_email='developer@sheerid.com',
    packages=['sheerid', ],
    url='https://github.com/sheerid/sheerid-python',
    license='LICENSE.txt',
    description='Convenience wrapper to access the public SheerID verification API.',
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries',
    ],
)
