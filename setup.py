from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
    name="atss",
    version="0.2.3",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'atss=atss.cli:main',
        ],
    },
    classifiers=[
    'Programming Language :: Python :: 3.13',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
    ],
    author="platon17",
    description="Library for analyzing acrostic texts for hidden messages",
    long_description=readme(),
    long_description_content_type='text/markdown',
    
)
