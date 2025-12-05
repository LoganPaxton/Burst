## 🤝 Contributing to Burst

We welcome contributions of all kinds! Whether you are fixing bugs, improving documentation, writing new test cases, or proposing new language features, your help is valuable.

Please take a moment to review this document to ensure the contribution process is as smooth as possible for everyone.

---

## 🐞 Reporting Bugs

If you find a bug in the compiler or runtime, please check the existing issues before submitting a new one.

1.  **Search Issues:** Check the Issues tab to see if the bug has already been reported.
2.  **Create a New Issue:** If it's a new bug, open a new issue and include:
    * **A Clear Title:** Summarizing the problem (e.g., "Compiler crashes on multi-line string interpolation").
    * **Steps to Reproduce:** The shortest code snippet in Burst that triggers the bug.
    * **Expected Behavior:** What the code *should* do.
    * **Actual Behavior:** What the code *actually* does (e.g., stack trace, error message, incorrect output).

## 🚀 Proposing Enhancements (New Features)

We encourage ideas for new features or language syntax improvements!

1.  **Open a Discussion:** Before writing any code for a major feature, please open an issue to discuss your idea with the maintainers. This helps us ensure the feature aligns with Burst's philosophy of simplicity and static typing.
2.  **Scope the Change:** Explain the problem your feature solves and how it integrates with the existing syntax (e.g., proposing a `while` loop implementation).

---

## 🛠️ Contribution Guidelines (Pull Requests)

Ready to contribute code? Follow these steps to ensure your Pull Request (PR) can be merged quickly:

1.  **Fork the Repository:** Fork the main Burst repository to your GitHub account.
2.  **Create a Branch:** Create a new branch for your specific fix or feature. Use a descriptive name (e.g., `bug/fix-include-path` or `feat/add-while-loop`).
3.  **Code Standards:**
    * Ensure your changes are consistent with the existing codebase (especially in `compiler.py` and `tokenizer.py`).
    * Include clear docstrings or comments for complex logic.
    * **Keep it Focused:** PRs should ideally focus on a single feature or bug fix.
4.  **Add Tests:**
    * For bug fixes, add a failing test case that passes with your fix.
    * For new features, add corresponding test files (e.g., in the `tests/` directory) that demonstrate the feature works correctly.
5.  **Submit the PR:**
    * Target the `main` branch of the original repository.
    * Reference any related issues (e.g., `Fixes #123`).
    * Describe the changes made and why they are necessary.

## ✍️ Documentation and Examples

If you are just improving the `README.md`, writing clearer comments in the source code, or creating new examples in the `tests/` directory, you can submit a PR directly without a prior issue, as long as the changes are clear and helpful.

Thank you for contributing to Burst!
