import setuptools
setuptools.setup(
    name="pde",
    version="0.0.1",
    url="https://github.com/OpenChemE/Process-Dynamics-Engine",
    author="Siang Lim",
    author_email="siang@alumni.ubc.ca",
    description="A simulator for process control models described by transfer functions or state space representations",
    long_description=open('README.md').read(),
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
