# 📚 Cambridge Distributed Systems and Security Reading Group

This repository builds and deploys the website for the Distributed Systems and Security Reading Group at the Department of Computer Science and Technology, University of Cambridge. The website is here: https://cambridge-security-reading-group.github.io/

[![Build and deploy GitHub page](https://github.com/cambridge-security-reading-group/cambridge-security-reading-group.github.io/actions/workflows/pages-build-and-deploy.yml/badge.svg)](https://github.com/cambridge-security-reading-group/cambridge-security-reading-group.github.io/actions/workflows/pages-build-and-deploy.yml)


## Local setup

To build and test the website locally, you need to have [uv installed](https://docs.astral.sh/uv/). Other Python environments may work, but this is the one we use. Then follow the standard steps:

```
git clone git@github.com:cambridge-security-reading-group/cambridge-security-reading-group.github.io.git
cd cambridge-security-reading-group.github.io
uv run --install
watch -n 1 uv run main.py
```


## Deployment

Edit and test the website locally, then commit and push your changes. The GitHub Actions workflow will automatically build and deploy the website to GitHub Pages. The logic for this is in the [`.github/workflows/pages-build-and-deploy.yml`](.github/workflows/pages-build-and-deploy.yml) file.