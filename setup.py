from setuptools import setup, find_packages

setup(
    name='plant_monitor',
    version='0.0.0',
    description='Monitor Plant Health',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/cdbunker/PlantMonitor',
    author='Colin Bunker',
    author_email='cdbunker23@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pyyaml',

    ],
    extras_require={
        'client': [
            'smbus2',
        ],
        'receiver': [
            'flask',
            'plotly',
            'matplotlib',
        ],
    },
    entry_points={
        'console_scripts': [
            'client_app=plant_monitor.client_app:run',
            'receiver_app=plant_monitor.receiver_app:run',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
