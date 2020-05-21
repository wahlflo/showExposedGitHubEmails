import setuptools

with open('README.md', mode='r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()


setuptools.setup(
    name="exposed_github_user_emails_scanner",
    version="1.0.3",
    author="Florian Wahl",
    author_email="florian.wahl.developer@gmail.com",
    description="A cli script to find exposed email addresses of one GitHub user in his or her public repositories.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wahlflo/showExposedGitHubEmails",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
       'cli-formatter>=1.1.0',
       'requests'
    ],
    entry_points={
        "console_scripts": [
            "showExposedGitHubEmails=github_exposed_email_crawler.script:main",
        ],
    }
)