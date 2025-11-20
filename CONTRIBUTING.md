# Contributing Guide

Thank you for considering a contribution to this project!  We encourage contributions and aim to make the process as smooth as possible.  The following guidelines will help you get started.

## Getting started

1. **Fork the repository** and clone your fork locally.
2. Create a new branch for your change: `git checkout -b feature/my-change`.
3. Make your changes, ensuring that you follow the existing coding style and best practices.
4. Write tests where appropriate and ensure all existing tests continue to pass.
5. Commit your changes and push the branch to your fork.
6. Open a pull request against the `main` branch of this repository.  In your PR description, explain the rationale for the change and include any relevant context or issue references.

## Code style

This project uses the following conventions:

- **Black** for code formatting.  Please run `black` on Python files before committing.
- **Flake8** for linting.  Aim to fix any lint warnings unless specifically justified.
- **pytest** for tests.  New features should include tests where appropriate.

## Commit messages

Write clear and descriptive commit messages.  A typical format might include:

```
feat(api): add POST /orders endpoint

Adds a new endpoint for creating orders and records order metrics.
```

## Reporting issues

If you encounter a bug or have an enhancement request, please open an issue.  When reporting bugs, include a minimal reproduction case and any relevant logs or error messages.

## Community standards

This project adheres to a Code of Conduct in order to foster a welcoming and respectful community.  By participating you agree to abide by its terms.

We appreciate your effort to improve the project and look forward to your contribution!
