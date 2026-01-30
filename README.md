# GH-300 GitHub Copilot — Practice Tests

This repository contains **two simulation preparatory tests** for the **GH-300 (GitHub Copilot) certification**.

You take each test by marking your selected answer(s) in the questions Markdown file, and then generating a grading report that summarizes your results **per domain** and appends the full **explanations**.

## How to Take a Test

1. Open one of the question files:
	- `copilot_test_1_questions.md`
	- `copilot_test_2_questions.md`

2. For each question, mark the correct option(s) by changing the checkbox to an `x`:
	- Example: change `#### [ ] B. ...` to `#### [x] B. ...`

	Notes:
	- Some questions are multi-select; mark **all** correct options.
	- Upper/lowercase both work (`x` or `X`).

3. Save the file after you finish the test:
	- In VS Code: `Ctrl + S`

## Generate the Report

After you finish marking answers, run the report generator with the test number (1 or 2):

```bash
python3 generate_report.py 1
```

or:

```bash
python3 generate_report.py 2
```

This will generate:

- `copilot_test_1_report.md` (or `copilot_test_2_report.md`) in the repository root.

The report includes:

- Overall totals (answered, unanswered, correct, incorrect)
- A breakdown **by domain**, including which questions were incorrect/unanswered
- An appended `## Explanations` section containing the full explanations for each question

## Files Layout (Reference)

- Questions (what you edit): `copilot_test_X_questions.md` (repo root)
- Answer keys: `docs/copilot_test_X_answers.md`
- Explanations: `docs/copilot_test_X_explanations.md`
- Generated report: `copilot_test_X_report.md` (repo root)

