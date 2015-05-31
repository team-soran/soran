from setuptools import find_package, setup


install_requires = [
  'flask == 0.10.1', 'flask-script == 2.0.5', 'sqlalchemy == 0.9.8',
  'alembic == 0.7.4', 'itsdangerous == 0.24', 'bcrypt == 1.1.0',
  'html5lib >= 0.999, < 1.0',
  'wtforms >= 2.0.2, < 2.1.0',
  'flask-wtf >= 0.11',
  'libsass >= 0.7.0, < 0.8.0',
  'iso8601 >= 0.1.10, < 0.2.0',
  'typeannotations >= 0.1.0',
]


tests_require = [
    'pytest >= 2.7.0, < 2.8.0',
]


docs_require = [
    'sphinx == 1.2.3',
]


setup(
    name='soran',
    version='0.0.1',
    author='team-soran',
    author_email='hyojun@admire.kr',
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'docs': docs_require,
        'tests': tests_require,
    },
    entry_points='''
        [console_scripts]
        soran = soran.cli:main
    '''
)
