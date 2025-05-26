# DevOps Workflow: CI/CD & GitOps

This document details the automated pipelines and practices used for the OmniRAG project, demonstrating a robust DevOps workflow.

## 1. Core Application CI/CD Pipeline (e.g., `ci.yml`, `deploy-dev-gitops.yml`)

... (explain your core application pipelines here) ...

## 2. LaTeX Requirements Document Automation (`.github/workflows/build-latex-requirements.yml`)

### Purpose
This workflow automates the compilation of the formal OmniRAG Requirements Specification (written in LaTeX) into a PDF document. It ensures that the latest, version-controlled PDF is always available directly in the repository, reflecting any changes to its source files.

### Triggers
This pipeline is triggered automatically on:
* `push` events to the `main` branch if any files within `docs/requirements/` (specifically `.tex`, `.bib`, `.sty`, `.cls`, or image files) are modified.
* `pull_request` events targeting the `main` branch, if `.tex` files in `docs/requirements/` are changed.
This targeted triggering optimizes resource usage by only running when relevant documentation source is updated.

### Workflow Steps

#### Job: `build_pdf`
This job runs on an `ubuntu-latest` runner and has `contents: write` permissions, allowing it to push changes back to the repository.

1.  **Checkout repository:**
    * Uses `actions/checkout@v4` to clone the repository, making all files available for the workflow. The `GITHUB_TOKEN` is used for authentication.

2.  **Compile LaTeX Requirements Specification:**
    * Utilizes the `xu-cheng/latex-action@v2` to perform the LaTeX compilation.
    * `root_file: omnirag_requirements_spec.tex` specifies the main file.
    * `working_directory: docs/requirements/` tells the compiler to operate from within this directory, ensuring all included files (like images or custom styles) are found correctly. The compiled `omnirag_requirements_spec.pdf` will be generated in this directory.

3.  **Commit and Push Compiled PDF:**
    * Configures the Git user as `github-actions[bot]`.
    * Stages the `omnirag_requirements_spec.pdf` file for commit.
    * Commits the changes with a message including `[skip ci]`. This tag is crucial; it prevents other CI workflows from triggering recursively due to this automated commit, avoiding infinite loops.
    * Pushes the changes to the `main` branch, ensuring the repository holds the latest PDF version.

### Output & Accessibility
The compiled `omnirag_requirements_spec.pdf` is located directly in the `docs/requirements/` folder of the `main` branch. This PDF can be linked from the main web documentation on `anpham.me` or accessed directly via the GitHub repository.
