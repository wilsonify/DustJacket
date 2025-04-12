# Contributing to DustJacket

Welcome! 

Thanks for your interest in contributing to **DustJacket**, 
a machine learning-driven toolkit for cleaning and enhancing Calibre metadata. 

Whether you're fixing a bug, writing code, enhancing documentation, or just filing an issue — every contribution matters.

This guide outlines how to get started, what you can contribute, and how to collaborate effectively.

---

## 💡 How You Can Contribute

We welcome all types of contributions:

- 🐞 Fix bugs or edge case failures
- 📚 Improve documentation and examples
- 🚀 Enhance model accuracy or efficiency
- 🧼 Refine data cleaning and normalization logic
- 🧪 Add tests to improve coverage
- 💡 Suggest or implement new features

No contribution is too small!

---

## Reporting and Working on Issues

Communication is key. here is how to create a new issue:

1. **Search existing issues** to avoid duplicates.
2. If the issue exists, **comment** that you're interested in working on it.
3. If the issue doesn’t exist, **create one** with:
   - A clear title and description
   - Steps to reproduce (for bugs)
   - Your intent to work on it (if applicable)

Example comment:

> I'm a beginner and would love to take a shot at fixing this. Any guidance is welcome!

---

## Local Development Setup

1. **Fork and clone** the repository:

```bash
git clone https://github.com/your-username/dustjacket.git
cd dustjacket
```

## Create and activate a virtual environment:

python -m venv venv

source venv/bin/activate        # On Windows: venv\Scripts\activate

## Install dependencies:

pip install -r requirements.txt

## Run tests to verify setup:

    pytest tests/

## 🌱 Making Your First Contribution

### Create a new branch:

```git checkout -b fix/issue-123-description```

Make your changes 
write clear commit messages:

```
git add .
git commit -m "Fix #123: Normalize author names using TF-IDF"
```

### Sync your fork before pushing:

git pull --rebase upstream main

### Push to your fork:

    git push origin fix/issue-123-description

### Open a Pull Request:

        Link the issue in the description (e.g., Closes #123)

        Clearly explain your changes

        Mention if you're a beginner — maintainers are happy to support!

# Code Style & Testing

Please follow these development conventions:

    Organize code in the code/, notebooks/, and tests/ directories.

    Write clear, consistent docstrings for all functions and classes.

    Add or update unit tests in the tests/ folder.

    Use pytest to run tests locally.

    Test coverage should include:

        Author clustering

        Genre classification

        Duplicate detection

# Licensing & Code of Conduct

By contributing, you agree that your contributions will be licensed under the MIT License.

We expect all contributors to follow our Code of Conduct to foster a welcoming and inclusive community.
🙌 Thank You!

We're grateful for your interest in DustJacket. 

Whether it's a typo fix or a new ML model, your effort matters. 

Don’t hesitate to reach out with questions, suggestions, or requests for feedback
