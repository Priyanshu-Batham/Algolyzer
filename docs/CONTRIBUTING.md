# Contributing Guidelines

Thank you for considering contributing to Algolyzer! We appreciate your help in improving our project. Please follow the steps below to ensure a smooth and efficient contribution process.

1. Fork the Repository
    - Click the "Fork" button at the top of the repository page to create a copy in your GitHub account.

2. Clone the Forked Repository
    - Use the following command to clone your fork locally (replace `your-username` with your actual github username):

        ```bash
        git clone https://github.com/<your-username>/Algolyzer.git
        cd Algolyzer
        ```
## Setup project 
[Setup for Development](./setup_development.md)

## Creating a Feature Branch

1. Create and Switch to a New Branch
    - Name your branch based on the contribution, e.g., feature_authentication or fix_bug_123:

        ```bash
        git checkout -b feature_branch_name
        ```

2. Make Your Changes
    - Implement the feature, fix bugs, or update the documentation. Ensure your code adheres to the project's style and standards.

# Contributing for Quiz Data
1. Goto `localhost:8000/admin` and login using your **superuser** credentials.
2. Add your Topics and Questions in the `Topics` & `Questions` models under the `Quiz` tab.
3. Open the terminal and run
    ```bash 
    python manage.py dump_quiz
    ```


## Running Quality Checks

1. Format the Code
    - Run the provided script to ensure consistent formatting:

        ```bash
        ./run_qa_format
        ```

2. Run Tests
    - Navigate to the project directory and execute the test suite:

        ```bash
        python manage.py test
        ```

## Committing and Pushing Changes

1. Stage and Commit Changes
    - Add your changes and commit them with a descriptive message:

        ```bash
        git add .
        git commit -m "Add detailed commit message here"
        ```
2. Pre-Commit Hook
    - Note that a pre-commit hook will automatically run upon committing. If it fails, resolve the issues and commit again.

3. Push Your Branch
    - Push your branch to your forked repository:

        ```bash
        git push origin feature_branch_name
        ```

## Create an issue on GitHub

1. Before creating a pull request, create an issue on the [original repository](https://github.com/Priyanshu-Batham/Algolyzer/issues)
2. Remember to include as much information about your addition or fix.
3. Use appropriate labels for the issue.
4. Mention the maintainer for attention.
5. Patiently wait.
6. After maintainer approval, move on to open a pull request.

## Creating a Pull Request (PR)
1. Open a PR
    - Navigate to the original repository and open a PR from your branch.
    - Use a descriptive title and message, and reference any related issues (e.g., Fixes #issue_number).
    - Mention the Pull Request and

2. Address CI Pipeline Failures
    - If the PR fails the CI pipeline, review the logs, rectify the issues, and push the changes again.

3. Await Review
    - Be patient while the maintainers review your PR. Respond to feedback and make the required changes if needed.

4. Merge
    - Once approved, your PR will be merged into the main branch.

## Cleaning Up

- After a successful merge, you can clean up your local repository:

    ```bash
    git branch -D feature_branch_name
    git fetch --prune
    ```

## Additional Tips

- Modify the last commit if you need to make minor changes without creating a new commit.

    ```bash 
    git commit --amend
    ```

- Regularly sync your fork with the upstream repository:

    ```bash
    git fetch upstream
    git merge upstream/main
    ```