# Contributing to HUMMBL Unified Tier Framework

Thank you for your interest in contributing to the HUMMBL Unified Tier Framework! This document provides guidelines for contributing to this project.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Contribution Types](#contribution-types)
- [Getting Started](#getting-started)
- [Submission Guidelines](#submission-guidelines)
- [Style Guidelines](#style-guidelines)
- [Review Process](#review-process)
- [Recognition](#recognition)

---

## 📜 Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

---

## 🤝 How Can I Contribute?

We welcome several types of contributions:

### ✅ Accepted Contributions

1. **Documentation Improvements**
   - Typo corrections and grammar fixes
   - Clarification of ambiguous sections
   - Additional examples and use cases
   - Translation improvements

2. **Issue Reporting**
   - Bug reports (errors, inconsistencies)
   - Documentation gaps or unclear sections
   - Broken links or references
   - Accessibility issues

3. **Use Case Examples**
   - Real-world application case studies
   - Domain-specific examples
   - Success stories and lessons learned
   - Problem assessment walkthroughs

4. **Empirical Validation Data**
   - Tier classification validation studies
   - Base-N effectiveness measurements
   - Model application tracking data
   - User feedback and outcome data

5. **Translations**
   - Framework translations to other languages
   - Glossary translations
   - Example translations

### ❌ Not Accepted Without Prior Discussion

1. **Structural Changes**
   - Major reorganization of sections
   - Changes to tier definitions or scoring methodology
   - Modifications to Base-N architecture
   - Alterations to proprietary components

2. **New Framework Components**
   - Additional tiers or classification systems
   - New scoring methodologies
   - Alternative architectures

**For major changes, please open an issue first to discuss your proposal.**

---

## 📝 Contribution Types

### Type 1: Documentation Fixes (Low Barrier)

**What:** Typos, grammar, formatting, broken links  
**Process:** Direct pull request  
**Review Time:** 1-3 days  
**Example:** "Fixed typo in Section 4.2"

### Type 2: Content Enhancements (Medium Barrier)

**What:** Additional examples, clarifications, use cases  
**Process:** Issue discussion → Pull request  
**Review Time:** 1-2 weeks  
**Example:** "Added healthcare industry case study to Section 7"

### Type 3: Empirical Data (High Barrier)

**What:** Validation studies, research data, measurements  
**Process:** Detailed proposal → Review → Integration  
**Review Time:** 2-4 weeks  
**Example:** "Tier classification validation study with N=50 problems"

### Type 4: Translations (Medium-High Barrier)

**What:** Framework translations to other languages  
**Process:** Translation proposal → Review → Integration  
**Review Time:** 2-3 weeks  
**Example:** "Spanish translation of complete framework"

---

## 🚀 Getting Started

### 1. Fork the Repository

```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/hummbl-unified-tier-framework.git
cd hummbl-unified-tier-framework
```


### 2. Create a Branch

```bash
# Create a descriptive branch name
git checkout -b fix/typo-section-4
# or
git checkout -b feat/healthcare-case-study
# or
git checkout -b docs/clarify-tier-scoring
```

**Branch Naming Convention:**
- `fix/` - Bug fixes, typo corrections
- `feat/` - New features, examples, case studies
- `docs/` - Documentation improvements
- `trans/` - Translations
- `data/` - Empirical data contributions

### 3. Make Your Changes

- Edit the relevant files
- Follow the [Style Guidelines](#style-guidelines)
- Test your changes (check links, formatting, etc.)

### 4. Commit Your Changes

```bash
git add .
git commit -m "fix: correct typo in wickedness scoring section"
```

**Commit Message Format:**
```text
<type>: <short description>

[optional body]

[optional footer]
```

**Types:**
- `fix:` - Bug fixes
- `feat:` - New features
- `docs:` - Documentation changes
- `style:` - Formatting changes
- `refactor:` - Code restructuring
- `test:` - Test additions
- `chore:` - Maintenance tasks

### 5. Push and Create Pull Request

```bash
git push origin fix/typo-section-4
```

Then create a pull request on GitHub.

---

## 📤 Submission Guidelines

### Pull Request Checklist

Before submitting a pull request, ensure:

- [ ] **Description:** Clear description of what changed and why
- [ ] **Issue Reference:** Link to related issue (if applicable)
- [ ] **Testing:** Changes have been tested (links work, formatting correct)
- [ ] **Style:** Follows project style guidelines
- [ ] **Attribution:** Proper attribution maintained
- [ ] **License:** Agreement to license terms
- [ ] **Scope:** Changes are focused and minimal

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (typo, broken link, etc.)
- [ ] Documentation improvement
- [ ] New example or case study
- [ ] Empirical data contribution
- [ ] Translation

## Related Issue
Closes #[issue number]

## Testing
How were these changes tested?

## Checklist
- [ ] I have read the CONTRIBUTING guidelines
- [ ] My changes follow the project style
- [ ] I have tested my changes
- [ ] I have maintained proper attribution
- [ ] I agree to the license terms
```


---

## 🎨 Style Guidelines

### Markdown Formatting

1. **Headings:**
   - Use ATX-style headings (`#`, `##`, `###`)
   - Include space after `#`
   - Don't skip heading levels

2. **Lists:**
   - Use `-` for unordered lists
   - Use `1.` for ordered lists
   - Include blank line before and after lists

3. **Links:**
   - Use descriptive link text
   - Format: `[Link Text](URL)`
   - Verify all links work

4. **Code Blocks:**
   - Use fenced code blocks with language specification
   - Format: ` ```language`
   - Indent consistently

5. **Emphasis:**
   - Use `**bold**` for strong emphasis
   - Use `*italic*` for mild emphasis
   - Use `code` for technical terms

### Content Style

1. **Clarity:**
   - Write clearly and concisely
   - Define technical terms
   - Provide examples where helpful

2. **Consistency:**
   - Match existing terminology
   - Follow established patterns
   - Maintain consistent tone

3. **Attribution:**
   - Credit sources appropriately
   - Maintain existing attributions
   - Follow citation format

### Examples

**Good:**
```markdown
### 1.2 Tier 1: Simple Problems (0-9 points)

**Definition:**
Problems with few variables, clear cause-effect relationships, and well-established solution methods.

**Examples:**
- Fixing a flat tire
- Balancing a checkbook
```


**Bad:**
```markdown
### Tier 1
Simple problems are easy to solve.
Examples: flat tire, checkbook
```


---

## 🔍 Review Process

### Timeline

1. **Initial Review:** 1-3 days for triage
2. **Detailed Review:** 1-2 weeks for content review
3. **Revisions:** As needed based on feedback
4. **Final Approval:** 1-3 days after revisions
5. **Merge:** Upon approval

### Review Criteria

Reviewers will assess:

- ✅ **Accuracy:** Information is correct and well-sourced
- ✅ **Clarity:** Content is clear and understandable
- ✅ **Consistency:** Matches existing style and terminology
- ✅ **Attribution:** Proper credits maintained
- ✅ **Scope:** Changes are focused and appropriate
- ✅ **Quality:** Professional quality and formatting

### Feedback

- Reviewers may request changes
- Be responsive to feedback
- Engage constructively in discussion
- Revise as needed

### Approval

- Requires approval from project maintainers
- May require multiple review rounds
- Final decision rests with HUMMBL

---

## 🏆 Recognition

### Contributor Recognition

Contributors will be recognized in:

1. **CHANGELOG.md:** Listed in version release notes
2. **Contributors Section:** Added to README (for significant contributions)
3. **Acknowledgments:** Mentioned in framework documentation (for major contributions)

### Contribution Levels

- **Bronze:** 1-5 accepted contributions
- **Silver:** 6-15 accepted contributions
- **Gold:** 16+ accepted contributions or major empirical data

---

## 📞 Questions?

### Where to Ask

- **General Questions:** Open a GitHub Discussion
- **Bug Reports:** Open a GitHub Issue
- **Feature Proposals:** Open a GitHub Issue with `[Proposal]` prefix
- **Security Issues:** See [SECURITY.md](SECURITY.md)
- **Private Inquiries:** Contact via GitLab

### Response Time

- **Issues:** 1-3 days for initial response
- **Pull Requests:** 1-3 days for initial review
- **Discussions:** 1-5 days for response

---

## 📜 License Agreement

By contributing, you agree that:

1. Your contributions will be licensed under the same license as the project
2. You have the right to submit the contributions
3. You understand and accept the proprietary nature of certain components
4. You will maintain proper attribution requirements

See [LICENSE.md](LICENSE.md) for complete terms.

---

## 🙏 Thank You!

Thank you for contributing to the HUMMBL Unified Tier Framework. Your contributions help improve problem-solving methodologies for practitioners, researchers, and learners worldwide.

**Questions?** Open an issue or discussion on GitHub.

---

**Maintained by HUMMBL, LLC**  
**Last Updated:** November 1, 2025
