import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='django-rest-action-serializer',
    version='1.1.0',
    packages=setuptools.find_packages(),
    description='A Django app that provides a serializer mixin that allows You to customize the fields'
                'according to the action provided without the need to'
                'create other serializers.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Bruno Barreto Freitas',
    author_email='brunobarretofreitas@outlook.com',
    url='https://github.com/brunobarretofreitas/django-rest-action-serializer',
    download_url='https://github.com/brunobarretofreitas/django-rest-action-serializer/archive/master.zip',
    keywords='django django-rest-framework api serializer',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'Django', 'djangorestframework'
    ]
)