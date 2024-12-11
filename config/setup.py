import os
from setuptools import setup, find_packages

def read_requirements(file_path):
    """
    Read requirements from a file
    
    Args:
        file_path (str): Path to requirements file
    
    Returns:
        List of requirements
    """
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"Warning: Requirements file {file_path} not found")
        return []

def read_long_description(file_path='README.md'):
    """
    Read long description from README
    
    Args:
        file_path (str): Path to README file
    
    Returns:
        Long description string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Sports Prop Predictor - Machine Learning Sports Prediction Platform"

setup(
    name='sports-prop-predictor',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='Advanced Machine Learning Sports Prop Prediction Platform',
    long_description=read_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/sports-prop-predictor',
    packages=find_packages(exclude=['tests*', 'docs*']),
    install_requires=read_requirements('requirements.txt'),
    extras_require={
        'dev': read_requirements('dev_requirements.txt'),
        'test': read_requirements('test_requirements.txt')
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Sports/Recreation :: Data Analysis'
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'sports-prop-predictor=backend.cli:main',
            'train-model=ml_pipeline.model_training.prop_predictor_model:main'
        ]
    },
    keywords=[
        'machine-learning', 
        'sports-prediction', 
        'data-science', 
        'ai', 
        'prop-betting'
    ],
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/sports-prop-predictor/issues',
        'Source': 'https://github.com/yourusername/sports-prop-predictor'
    }
)