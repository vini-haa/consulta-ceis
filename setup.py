from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="consulta-ceis",
    version="0.1.0",
    author="Seu Nome",
    author_email="seu.email@example.com",
    description="Aplicação para consulta ao Cadastro de Empresas Inidôneas e Suspensas (CEIS)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seu-usuario/consulta-ceis",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "consulta-ceis=app:run",
        ],
    },
)
