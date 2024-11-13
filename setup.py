from setuptools import find_packages, setup

setup(
    name="zira",
    version="1.0.3",
    author="Shayan Sadeghi",
    author_email="ShayanSadeghi1996@gmail.com",
    description="Async logging system with local caching and syncing system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ShayanSadeghi/zira",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "motor>=3.6.0",
        "python-dotenv>=1.0.1",
    ],
    keywords=["log", "event-logger", "logger", "monitor"],
)
