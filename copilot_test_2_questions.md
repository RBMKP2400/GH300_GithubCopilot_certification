### Domain: How GitHub Copilot works and handles data
### Question 1: A software engineer is working on a large backend application using GitHub Copilot in their IDE. They notice that Copilot provides highly relevant suggestions when working in smaller files, but the quality drops when editing lengthy code files with thousands of lines. What is the most likely reason for this variation in suggestion quality?
#### [ ] A. Copilot requires manual fine-tuning for each file size before providing accurate suggestions
#### [ ] B. The engineer’s IDE lacks the memory to process large files efficiently
#### [ ] C. GitHub Copilot has a limited context window, which restricts how much of the surrounding code it can consider at once
#### [ ] D. GitHub Copilot disables code completions automatically for files exceeding a certain number of lines

### Domain: GitHub Copilot plans and features
### Question 2: Which of the following are valid and commonly used commands while using GitHub Copilot in the CLI?
#### [ ] A. gh Copilot explain, gh Copilot suggest, gh Copilot extension list
#### [ ] B. Copilot.run, Copilot.info, Copilot.chat
#### [ ] C. gh codegen, gh audit, gh summarize
#### [ ] D. gh Copilot status, gh Copilot init, git Copilot deploy

### Domain: GitHub Copilot plans and features
### Question 3: You are configuring GitHub Copilot in the CLI for a smoother developer experience. Which of the following aliases can be set up to perform common actions like code suggestions and explanations? [Select Two]
#### [ ] A. “ghcs” - GitHub Copilot Suggest
#### [ ] B. “ghce” - GitHub Copilot Explain
#### [ ] C. “ghinit” - Initialize Copilot CLI
#### [ ] D. “ghshare” - Share Copilot responses with your colleagues
#### [ ] E. “ghrun” - Run Copilot commands in a build pipeline

### Domain: Prompt Crafting and Prompt Engineering
### Question 4: A project team frequently collaborates using GitHub Copilot Chat while developing a cloud-native application. During conversations, they notice that the AI assistant often tailors its responses based on previous messages in the same chat. The team finds it helpful and wonders how GitHub Copilot Chat uses chat history to improve its responses. Which of the following best explains how GitHub Copilot Chat uses chat history to improve its responses when a project team collaborates on a cloud-native application?
#### [ ] A. It uses recent messages in the current chat session to maintain context and provide more relevant answers
#### [ ] B. It permanently stores all previous chat conversations and uses them to retrain the model for future responses
#### [ ] C. It syncs chat history across user accounts to generate collective insights from team members’ past interactions
#### [ ] D. It connects to the user's GitHub activity history to automatically apply project-specific suggestions

### Domain: Prompt Crafting and Prompt Engineering
### Question 5: An SDET is trying to auto-generate unit tests for a Python function. However the suggestions are not consistent and sometimes look irrelevant for the required context. The expert realizes that the prompt which is being used is too vague: “Create Tests”. To improve the results, which of the following statements can be considered as the best ways to craft prompts to get the expected suggestions from GitHub Copilot. (SELECT THREE)
#### [ ] A. Start writing your code with a descriptive comment that explains the purpose of the code block
#### [ ] B. Include examples or expected outcomes to guide Copilot toward your strategy
#### [ ] C. Avoid overly generic statements like “generate function” or “Create Tests”, as they lack context
#### [ ] D. Use unrelated terms in your prompt to test Copilot’s ability to generate suggestions even on vague prompts
#### [ ] E. SDET should continue to use the vague prompts or the prompts that have almost no context as Copilot is smart enough to do everything on its own

### Domain: Developer use cases for AI
### Question 6: A Technology lead wants to present data-backed insights to leadership on how effectively their engineering team is using GitHub Copilot. They decide to leverage GitHub Copilot's Productivity API to collect detailed usage statistics across the team’s repositories. Which of the following metrics can the tech lead collect using the Productivity API to understand Copilot’s real impact? (SELECT THREE)
#### [ ] A. Average Daily Active Users of Copilot across the team
#### [ ] B. Total Acceptance Rate of Copilot-generated code suggestions
#### [ ] C. Number of Copilot-generated code lines manually modified after suggestion
#### [ ] D. Lines of Code Accepted from Copilot into the codebase
#### [ ] E. Number of production incidents caused by Copilot-generated code

### Domain: Privacy fundamentals and content exclusions
### Question 7: A security-focused software engineer is reviewing how GitHub Copilot can help avoid risky coding practices during development. The engineer wants to understand how Copilot provides warnings or suggestions that enhance code security. Which of the following statements accurately reflects GitHub Copilot’s capabilities in this area? (SELECT TWO)
#### [ ] A. GitHub Copilot automatically blocks any code pattern that matches a known CVE (Common Vulnerabilities and Exposures) from being written
#### [ ] B. GitHub Copilot can suggest safer alternatives when risky patterns like hardcoded credentials or SQL injections are detected
#### [ ] C. Copilot provides security warnings based on real-time static analysis and scanning of your codebase
#### [ ] D. Copilot’s ability to detect insecure code is based on its training data and pattern recognition, not active code scanning

### Domain: Privacy fundamentals and content exclusions
### Question 8: A technology-driven team at a large organisation has configured content exclusions in GitHub Copilot to prevent sensitive configuration files and internal libraries from influencing AI-generated code suggestions. However, one of the developers notices that despite excluding certain files, GitHub Copilot still appears to suggest code patterns that resemble internal logic. What are some reasons why GitHub Copilot’s content exclusions might not always work? (SELECT TWO)
#### [ ] A. Content exclusions are ignored when editing files in the GitHub web interface instead of an IDE like Visual Studio Code
#### [ ] B. In some IDEs, such as Visual Studio Code, semantic information from excluded files may still be inferred by Copilot if it's visible in non-excluded files
#### [ ] C. Copilot only honours exclusions configured at the enterprise level; organisation-level or repository-level exclusions are not supported
#### [ ] D. When developers interact with GitHub Copilot Chat using the “@github” participant in Visual Studio or VS Code, content exclusions may not be applied
#### [ ] E. If sensitive code is duplicated into a non-excluded file, Copilot may reference that content since it's now outside the excluded scope

### Domain: Privacy fundamentals and content exclusions
### Question 9: A QA Automation Lead is developing regression test cases for a newly released microservice. While working in their IDE, they notice GitHub Copilot isn't offering useful suggestions or sometimes, no suggestions at all. In such a scenario, which of the following actions can help improve Copilot's responses and encourage better code suggestions? (SELECT TWO)
#### [ ] A. Attempt to rewrite the initial comment or prompt with more descriptive intent, including function names and expected behaviour, along with the relevant examples
#### [ ] B. Continue typing the function body manually without changing anything, and expect Copilot to eventually catch up
#### [ ] C. Use inline comments or docstrings above the function to clarify what the function should achieve. Ensure that clear expectations are set in the form of comments
#### [ ] D. Disable and re-enable GitHub Copilot to reset its learning and start over from scratch
#### [ ] E. Switch to a different programming language, as Copilot is limited to one language at a time, like Python

### Domain: Developer use cases for AI
### Question 10: A developer is working on a performance-critical module and expects GitHub Copilot to suggest highly efficient algorithms based on industry best practices. However, after reviewing a few completions, the developer realizes the generated code, although functional, is not optimized for performance or readability. What does this scenario best illustrate about the limitations of using GitHub Copilot?
#### [ ] A. GitHub Copilot is designed to deliver production-ready, performance-optimized solutions with minimal developer input
#### [ ] B. GitHub Copilot automatically benchmarks its suggestions and improves them in real-time
#### [ ] C. GitHub Copilot rejects generating code for performance-critical systems due to liability concerns
#### [ ] D. GitHub Copilot may generate valid but suboptimal code, and developers are expected to apply judgment and refactor when necessary

### Domain: Responsible AI
### Question 11: You are part of a data governance team tasked with reviewing enterprise-wide use of generative AI tools like Microsoft Copilot. A product manager has integrated Copilot into a customer support solution to draft email responses. What is the primary reason the output of the AI-generated emails should be validated before sending to customers?
#### [ ] A. AI-generated content may contain biased or culturally insensitive statements
#### [ ] B. AI tools sometimes struggle with grammar and sentence structure
#### [ ] C. The product manager is not qualified to review AI outputs independently
#### [ ] D. Customers are likely to reject machine-generated responses automatically

### Domain: Responsible AI
### Question 12: A multinational enterprise uses an AI tool to filter resumes for software engineering roles. Over time, HR observes that the shortlisted candidates are predominantly male from a specific region. What is the most likely root cause of this issue?
#### [ ] A. The tool lacks access to a sufficient number of resumes
#### [ ] B. The AI was trained on historical hiring data that may include human bias
#### [ ] C. The system uses incorrect formatting to evaluate candidate data
#### [ ] D. There is a conflict between regional compliance laws and the hiring workflow

### Domain: Responsible AI
### Question 13: Your healthcare startup is integrating an AI system for clinical data triage. To align with responsible AI practices, which of the following actions would best support ethical operations?
#### [ ] A. Avoid documenting development decisions to reduce legal exposure
#### [ ] B. Routinely fine-tune models without user consultation
#### [ ] C. Publish model limitations and ensure explainability of AI decisions
#### [ ] D. Prioritize fast delivery over model fairness and testing

### Domain: Responsible AI
### Question 14: Your team is building a credit scoring model for a digital bank. The model uses features like age, location, and profession. What is the best strategy to reduce the potential harm caused by bias or unfair predictions?
#### [ ] A. Remove all features from the dataset to ensure neutrality
#### [ ] B. Use the model as-is if it meets accuracy benchmarks
#### [ ] C. Conduct fairness audits and test the model on diverse groups
#### [ ] D. Let the business team manually adjust scores for underrepresented groups

### Domain: Responsible AI
### Question 15: Which of the following principles is most critical when designing and deploying ethical AI systems in customer-facing applications?
#### [ ] A. Maximizing profit through automation
#### [ ] B. Ensuring user consent and data privacy
#### [ ] C. Applying neural networks wherever possible
#### [ ] D. Deploying AI to reduce human resource requirements

### Domain: GitHub Copilot plans and features
### Question 16: A developer is new to GitHub Copilot Chat and opens Visual Studio Code. They want to understand what Copilot Chat can help with directly inside the IDE. What is the primary function of GitHub Copilot Chat within supported IDEs like VS Code?
#### [ ] A. Automatically commits and pushes code to GitHub repositories
#### [ ] B. Answers natural language coding questions and provides code suggestions inline
#### [ ] C. Analyzes repository security and generates pull request templates
#### [ ] D. Translates comments into different spoken languages

### Domain: GitHub Copilot plans and features
### Question 17: You’re advising a team on switching from GitHub Copilot Individual to Business. What features should they expect to gain in the Business plan? (Select Two)
#### [ ] A. Access to GitHub Copilot for CLI
#### [ ] B. IP indemnity for code suggestions
#### [ ] C. Organization-level usage controls
#### [ ] D. Free access to private GitHub Actions runners

### Domain: GitHub Copilot plans and features
### Question 18: An enterprise wants to automate billing insights and manage user licenses for Copilot Business. What REST API endpoint should the administrator use for subscription-level management?
#### [ ] A. /repos/:owner/:repo/hooks
#### [ ] B. /orgs/:org/copilot/billing
#### [ ] C. /users/:username/followers
#### [ ] D. /enterprises/:enterprise/settings

### Domain: GitHub Copilot plans and features
### Question 19: A developer is browsing a public repository on GitHub.com and notices an unfamiliar function in the code. They want to understand what it does without switching to their IDE. What is a key benefit of using GitHub Copilot Chat directly on GitHub.com in this scenario?
#### [ ] A. It allows users to modify repository secrets inline
#### [ ] B. It integrates issue tracking directly with calendar scheduling
#### [ ] C. It provides context-aware explanations of code blocks within the browser
#### [ ] D. It automatically merges pull requests across all forks

### Domain: GitHub Copilot plans and features
### Question 20: Which of the following represents a use case where GitHub Copilot Chat provides the most benefit?
#### [ ] A. Performing automated browser testing with Selenium
#### [ ] B. Explaining unfamiliar code snippets during onboarding
#### [ ] C. Scheduling sprint planning meetings
#### [ ] D. Exporting project analytics to Excel

### Domain: GitHub Copilot plans and features
### Question 21: A team notices GitHub Copilot Chat is taking longer to respond during heavy development hours. They want to improve its performance for faster, more relevant suggestions. Which of the following actions can help optimize Copilot Chat performance? (Select two)
#### [ ] A. Break down large files into smaller, modular components
#### [ ] B. Increase GPU power on the local development machine
#### [ ] C. Keep prompts short, specific, and focused
#### [ ] D. Enable GitHub Copilot Labs experimental features

### Domain: GitHub Copilot plans and features
### Question 22: Which of the following accurately reflects a known limitation of GitHub Copilot Chat?
#### [ ] A. Copilot Chat cannot explain code comments
#### [ ] B. It may generate insecure code if not reviewed carefully
#### [ ] C. Copilot Chat deletes temporary files after each session
#### [ ] D. Copilot Chat requires a GitHub Enterprise license to function

### Domain: GitHub Copilot plans and features
### Question 23: While working in VS Code, a developer receives a code suggestion from GitHub Copilot Chat. They want to see additional options before accepting. What can they do to explore alternative suggestions?
#### [ ] A. Use the /regenerate slash command
#### [ ] B. Enable autocomplete in GitHub Actions
#### [ ] C. Restart the IDE to reload the context
#### [ ] D. Use the browser version of GitHub Copilot Chat instead

### Domain: GitHub Copilot plans and features
### Question 24: You notice Copilot Chat frequently misunderstands your JavaScript prompts. You want to report this to help improve the model. How can you provide direct feedback to GitHub about this behavior?
#### [ ] A. Submit feedback via the “thumbs down” icon next to the response
#### [ ] B. Create a GitHub issue in the Copilot CLI repository
#### [ ] C. Send an email to GitHub support directly
#### [ ] D. Modify the source code of Copilot Chat and recompile

### Domain: GitHub Copilot plans and features
### Question 25: You’re training junior developers on how to get the best results from GitHub Copilot Chat. Which of the following are recommended best practices? (Select two)
#### [ ] A. Use clear and specific prompts for each coding request
#### [ ] B. Always accept the first suggestion provided
#### [ ] C. Regularly review Copilot-generated code for correctness and security
#### [ ] D. Use Copilot Chat to deploy production services

### Domain: GitHub Copilot plans and features
### Question 26: A developer wants to quickly summarize a block of code using Copilot Chat. Which slash command should they use to do this?
#### [ ] A. /summarize
#### [ ] B. /execute
#### [ ] C. /fix
#### [ ] D. /rewrite

### Domain: GitHub Copilot plans and features
### Question 27: You’re using GitHub Copilot Chat on GitHub.com and reviewing code in a public repository. Which of the following options are available to work with suggestions provided by Copilot Chat? (Select two)
#### [ ] A. Copy suggestions directly to your clipboard
#### [ ] B. Ask follow-up questions in the same chat thread
#### [ ] C. Run suggested code snippets in the browser
#### [ ] D. Trigger deployment pipelines from the suggestion window

### Domain: How GitHub Copilot works and handles data
### Question 28: You’re using GitHub Copilot in Visual Studio Code while building a TypeScript project. As you start typing a function, Copilot instantly generates a code suggestion. Which of the following best describes the complete lifecycle of this suggestion?
#### [ ] A. User starts typing → Copilot builds a context → LLM generates a suggestion → User accepts or rejects it
#### [ ] B. GitHub Copilot scans the entire GitHub repo → Generates a prediction → Auto-inserts code
#### [ ] C. User requests help → Copilot uploads the entire project to OpenAI → Suggestion is generated
#### [ ] D. GitHub Copilot listens for keystrokes → Picks a random template → Suggests code without understanding
#### [ ] E. The user types → GitHub Copilot copies previous similar commits from the repo history and suggests code

### Domain: How GitHub Copilot works and handles data
### Question 29: When generating code suggestions, what sources of context does GitHub Copilot use to understand what to predict?
#### [ ] A. Global variables and API keys from your environment
#### [ ] B. Complete project history, including commit logs
#### [ ] C. File name, programming language, surrounding code, and comments
#### [ ] D. GitHub Issues and Pull Requests linked to the repository
#### [ ] E. Debug logs and terminal output during execution

### Domain: How GitHub Copilot works and handles data
### Question 30: You are writing a Python function with a clear docstring. How does GitHub Copilot use that information to build a prompt for code generation?
#### [ ] A. It combines your docstring, file name, and code near the cursor into a prompt sent to the LLM
#### [ ] B. It translates the docstring into another language and matches a function from Stack Overflow
#### [ ] C. It stores your code and searches GitHub for similar public functions
#### [ ] D. It compiles the entire file before sending it to the LLM

### Domain: How GitHub Copilot works and handles data
### Question 31: What kinds of input does GitHub Copilot Chat understand and process effectively?
#### [ ] A. Only code snippets and technical keywords
#### [ ] B. Purely Git commit messages and PR titles
#### [ ] C. Natural language queries, inline comments, and code context
#### [ ] D. Only file structure and variable names

### Domain: How GitHub Copilot works and handles data
### Question 32: Which statement best reflects how GitHub Copilot Individual handles your private code and suggestion data?
#### [ ] A. All code is automatically used to retrain the LLM
#### [ ] B. GitHub shares suggestions and private code with OpenAI without consent
#### [ ] C. GitHub commits your code history to external servers
#### [ ] D. Your data is only used to provide suggestions and shared for training only if telemetry is enabled

### Domain: How GitHub Copilot works and handles data
### Question 33: Which of the following are known limitations of GitHub Copilot and large language models (LLMs) in real-world programming? (Select 3)
#### [ ] A. Copilot may generate insecure code or introduce vulnerabilities
#### [ ] B. Copilot always understands business logic from natural language prompts
#### [ ] C. Copilot can hallucinate functions or APIs that don’t exist
#### [ ] D. Copilot automatically tests and validates its suggestions before presenting them
#### [ ] E. Copilot can produce syntactically correct but logically flawed code

### Domain: How GitHub Copilot works and handles data
### Question 34: Which of the following best explain how GitHub Copilot handles reasoning and calculations? (Select 3)
#### [ ] A. Copilot uses symbolic logic to perform step-by-step math calculations accurately
#### [ ] B. Copilot excels at language-based reasoning and summarizing code intent
#### [ ] C. Copilot is limited in performing accurate arithmetic or algorithmic calculations
#### [ ] D. Copilot predicts the next token based on patterns, not based on actual computation
#### [ ] E. Copilot uses external APIs to resolve mathematical expressions before suggesting answers

### Domain: How GitHub Copilot works and handles data
### Question 35: Which of the following statements are true regarding how GitHub Copilot Individual uses and shares user data? (Select TWO)
#### [ ] A. Copilot Individual uses user code to retrain the model by default
#### [ ] B. Copilot may collect telemetry data if the user consents
#### [ ] C. Copilot never shares any suggestion or usage data with GitHub
#### [ ] D. Users can opt out of sharing code snippets used for improving suggestions
#### [ ] E. Copilot suggestions are generated locally without contacting external servers

### Domain: Testing with GitHub Copilot
### Question 36: You are working on a backend application and want to write unit tests for a newly developed function. Your team is using GitHub Copilot Chat to speed up development and improve test coverage. You want to understand how GitHub Copilot Chat can assist in generating effective unit test cases during development. What is the primary benefit of using GitHub Copilot Chat for writing unit tests?
#### [ ] A. It provides test code snippets based on your existing functions, suggests inputs, expected outputs, and assertions, and even helps identify boundary and edge cases
#### [ ] B. It manually writes all test cases without requiring any user input or context
#### [ ] C. It only proposes possible input and output combinations but doesn’t write full test cases
#### [ ] D. It executes all unit tests automatically and provides real-time test results

### Domain: Testing with GitHub Copilot
### Question 37: You are working on a project in Visual Studio Code (VS Code) and want to manage your unit tests efficiently. You’ve installed a test framework extension (e.g., Jest, Mocha, Pytest) and now want to view, run, debug, and manage your test cases from a centralized UI. Which built-in feature of Visual Studio Code provides this functionality?
#### [ ] A. To write new code snippets for unit tests
#### [ ] B. To run and debug unit tests, view the results of test runs, and manage test cases in the workspace
#### [ ] C. To generate test cases based on the code context
#### [ ] D. To automatically fix failing tests

### Domain: Privacy fundamentals and content exclusions
### Question 38: You are reviewing unit testing best practices and want to ensure that functions handle input validation effectively. What is the primary purpose of generating assertions related to function input parameters?
#### [ ] A. To enhance the performance of the function
#### [ ] B. To prevent invalid data from being processed by the function
#### [ ] C. To check if the function returns the expected output
#### [ ] D. To document the function’s expected inputs

### Domain: Prompt Crafting and Prompt Engineering
### Question 39: You are learning how to write effective prompts for GitHub Copilot to get high-quality code suggestions. While most prompt engineering principles improve Copilot’s response accuracy, one of the following is NOT considered a principle of effective prompt engineering.
#### [ ] A. Clarity: Focus on a single, well-defined task
#### [ ] B. Verbosity: Provide extensive and detailed descriptions
#### [ ] C. Specificity: Use clear and explicit instructions
#### [ ] D. Surround: Utilize descriptive filenames and keep related files open

### Domain: Developer use cases for AI
### Question 40: As a developer contributing to a cross-functional team, you’re asked to maintain project documentation. What is the main goal of project documentation in a software development lifecycle?
#### [ ] A. To deliver technical implementation details meant solely for the backend developers
#### [ ] B. To summarize the project features for end-users in a marketing document
#### [ ] C. To communicate the purpose, boundaries, and key decisions about the project to all stakeholders
#### [ ] D. To record commit timestamps and development milestones across sprints

### Domain: Developer use cases for AI
### Question 41: You’re collaborating on a large development project and want to ensure your code is easy for other team members to understand and maintain. What is the key benefit of writing inline code documentation?
#### [ ] A. It makes the code more challenging for others to interpret
#### [ ] B. It improves readability and maintainability, helping developers quickly understand the logic
#### [ ] C. It inflates the codebase unnecessarily
#### [ ] D. It demonstrates advanced syntax and complexity in the developer’s skills

### Domain: Developer use cases for AI
### Question 42: A developer is writing a function in Visual Studio Code. GitHub Copilot begins suggesting code completions based on the current input. How does GitHub Copilot decide which suggestions to generate?
#### [ ] A. It uses a random selection from common coding patterns
#### [ ] B. It considers the programming language used, regardless of context
#### [ ] C. It bases suggestions on the current context and code written in the editor
#### [ ] D. It evaluates how long the current code snippet is

### Domain: Developer use cases for AI
### Question 43: You are working in Visual Studio Code with GitHub Copilot enabled. While typing a function, Copilot generates multiple suggestions to complete your code block.As a developer, how can you review these options and select the most appropriate one?
#### [ ] A. Copilot adds all suggestions to the editor automatically
#### [ ] B. Only the top suggestion is preserved, and the rest are discarded
#### [ ] C. Copilot benchmarks each suggestion and inserts the best-performing one based on test runs
#### [ ] D. You can use arrow keys or tab navigation to browse through and pick your preferred suggestion

### Domain: Developer use cases for AI
### Question 44: An enterprise uses GitHub Copilot in a private repo setting. How can Copilot enhance productivity and align with company-specific standards?
#### [ ] A. It adapts to internal best practices and policies to provide contextual suggestions and coding help
#### [ ] B. It generates suggestions solely from public repositories
#### [ ] C. It provides random snippets of code to speed up development
#### [ ] D. It avoids using the organization’s codebase to maintain privacy

### Domain: Prompt Crafting and Prompt Engineering
### Question 45: You’re building an AI assistant that classifies user requests using large language models (LLMs). You are evaluating the use of zero-shot and few-shot prompting. Which of the following statements accurately reflect key differences between zero-shot and few-shot learning? (Select two options)
#### [ ] A. Zero-shot prompting is better suited for models that have not been fine-tuned
#### [ ] B. Few-shot prompting introduces more tokens, potentially increasing cost and latency
#### [ ] C. Zero-shot prompting uses labeled examples to guide the model toward specific outputs
#### [ ] D. Few-shot prompting allows the model to learn from examples and improve response relevance
#### [ ] E. Few-shot prompting does not affect the model’s context or performance

### Domain: Testing with GitHub Copilot
### Question 46: You are reviewing a unit test written by a team member. The test is clearly divided into three sections: Setting up the test environment, Calling the method under test, Verifying the results. What is the main purpose of using the Arrange-Act-Assert (AAA) pattern in unit testing?
#### [ ] A. It helps define the order of code execution in the application logic
#### [ ] B. It serves as a format for auto-generating test documentation
#### [ ] C. It determines how tests are built and executed by the test runner
#### [ ] D. It separates unit tests into clear steps: setup, execution, and result verification

### Domain: Prompt Crafting and Prompt Engineering
### Question 47: A developer is curious about how GitHub Copilot understands their code prompts and produces accurate code suggestions. What mechanism allows Copilot to provide contextually relevant responses?
#### [ ] A. It depends solely on the data it was trained on, without incorporating user-specific context
#### [ ] B. It applies methods like zero-shot, one-shot, and few-shot prompting to generate relevant suggestions
#### [ ] C. It needs manual fine-tuning for every new task to perform effectively
#### [ ] D. It is unable to adjust its responses based on user behavior or input context

### Domain: Testing with GitHub Copilot
### Question 48: Your team lead wants to enforce consistent usage of GitHub Copilot across the development team within your GitHub organization. Which of the following options allow administrators to control how Copilot suggestions work across repositories?
#### [ ] A. Enforce Copilot policies via organization-level configuration
#### [ ] B. Limit suggestions only to open-source repositories
#### [ ] C. Allow users to control organization-wide Copilot settings
#### [ ] D. Configure Copilot via repository secrets in .env files

### Domain: Privacy fundamentals and content exclusions
### Question 49: You want to generate a boilerplate unit test for a new function using GitHub Copilot. How can you prompt Copilot to suggest a valid test stub aligned with best practices?
#### [ ] A. Use keyboard shortcuts without writing any code context
#### [ ] B. Paste code from another project
#### [ ] C. Write a comment that starts with “// Generate test for…”
#### [ ] D. Include irrelevant function names to confuse the model

### Domain: Privacy fundamentals and content exclusions
### Question 50: Sometimes GitHub Copilot may not offer suggestions or may return irrelevant code. What should a developer do in such scenarios to improve suggestion quality?
#### [ ] A. Avoid adding comments or filenames
#### [ ] B. Close the editor and restart GitHub
#### [ ] C. Ignore Copilot and write code manually
#### [ ] D. Add inline comments that describe the task explicitly
