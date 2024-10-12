from setuptools import find_packages,setup

setup(
    name='mcqgenrator',
    version='0.0.1',
    author='yeswanth chowdary',
    author_email='bgotti@hawk.iit.edu',
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2","langchain_community","langchain-openai"],
    packages=find_packages()
)