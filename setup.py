import setuptools

setuptools.setup(
	name="TP-RequestFlows",
	version="2024.2.12",
	author="TP Cyber Security",
	license="MIT",
	author_email="tpcybersec2023@gmail.com",
	description="",
	long_description=open("README.md").read(),
	long_description_content_type="text/markdown",
	install_requires=open("requirements.txt").read().split(),
	url="https://github.com/truocphan/TP-RequestFlows",
	classifiers=[
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: Implementation :: Jython"
	],
	keywords=["TPCyberSec", "TP-RequestFlows", "Request Flows"],
	packages=["TP_RequestFlows"],
)