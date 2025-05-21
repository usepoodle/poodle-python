# Contributing to poodle-python

We love your input! We want to make contributing to poodle-python as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## We Develop with GitHub

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## We Use [Github Flow](https://docs.github.com/en/get-started/using-github/github-flow)

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Development Process

1. Clone the repository:

   ```bash
   git clone https://github.com/usepoodle/poodle-python.git
   cd poodle-python
   ```

2. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

3. Create a branch:

   ```bash
   git checkout -b feature/amazing-feature
   ```

4. Make your changes and test them:

   ```bash
   poetry run pytest
   poetry run flake8
   ```

5. Build the project to verify everything works:
   ```bash
   poetry build
   ```

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issue tracker](https://github.com/usepoodle/poodle-python/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/usepoodle/poodle-python/issues/new); it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can.
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Use a Consistent Coding Style

- Use Python for all new code.
- Follow PEP 8 guidelines.
- 4 spaces for indentation.
- Run `poetry run black .` and `poetry run flake8` to automatically format and check code.
- Write meaningful commit messages.

## License

By contributing, you agree that your contributions will be licensed under its MIT License.
