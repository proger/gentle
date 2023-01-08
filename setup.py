from setuptools import setup
from gentle import __version__

setup(
    app=['serve.py'],
    data_files=[],
    options={'py2app': {
        'argv_emulation': False,
        'resources': 'k3,m3,ffmpeg,www,exp'
    }},
    name='gentle-uk',
    version=__version__,
    description='Robust yet lenient forced-aligner for Ukrainian built on Kaldi.',
    url='http://lowerquality.com/gentle',
    author='Robert M Ochshorn',
    license='MIT',
    packages=['gentle'],
    install_requires=['twisted', 'uk'],
    test_suite='tests',
)
