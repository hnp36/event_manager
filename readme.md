# Assignment 10 

## Closed Issues (Bug Fixes)

1. **Bug #1:**[Added last_login field to UserResponse schema](https://github.com/hnp36/event_manager/issues/1)
  # description
    Fixed inconsistent example values for email and password between the LoginRequest and UserCreate schemas in Swagger UI, which was causing confusion during testing. Synchronized the example data across both schemas, added an automated test to enforce their consistency, and cleaned up the test fixtures accordingly.

2. **Bug #2:**[In Tests, Missing fixtures for user_token, admin_token, and manager_token](https://github.com/hnp36/event_manager/issues/2)
  # description
  ISSUE:
Tests were failing because they tried to use token fixtures (user_token, admin_token, and manager_token) that were not defined in your conftest.py file. When pytest runs your tests, it looks for fixtures with those names but cannot find them, which results in errors.

How I Resolved It:

I added three new fixtures at the end of your conftest.py file to create authentication tokens:

user_token: generates a token for a verified user
admin_token: generates a token for an admin user
manager_token: generates a token for a manager user
Each token fixture is now connected to its corresponding user fixture. For instance, the admin_token is linked to the admin_user. I used the create_access_token function from your JWT service to generate properly formatted tokens that include the user ID and role. Additionally, I updated the login_request_data fixture to use "username" instead of "email" to align with the requirements of your login endpoint. This change follows the common OAuth2 practice of allowing the username field to accept an email address.

3. **Bug #3:**[SMTPServerDisconnected: Connection unexpectedly closed](https://github.com/hnp36/event_manager/issues/3)
  # description
  Issue:
The application tried to send an email using the SMTP server, but the server closed the connection before the message could be sent.

smtplib.SMTPServerDisconnected: Connection unexpectedly closed

Possible Reason:
There could be a problem with the SMTP settings, such as the hostname, port, or password. Additionally, there may be an issue with the credentials needed to authenticate the SMTP session.

4. **Bug #4:**[Duplicate entries in the UserListResponse Swagger example](https://github.com/hnp36/event_manager/issues/4)
  # description
The example dictionary within the UserListResponse schema contained duplicate fields such as "bio" and "role," which resulted in invalid JSON and confusing Swagger documentation.

I removed the duplicates and revised the example block to align with the actual UserResponse schema. Additionally, I added the missing field "is_professional." I have confirmed that all test cases continue to pass.

5. **Bug #5:**[Unclear Error message for the login page ](https://github.com/hnp36/event_manager/issues/5)
  # description
I observed that the error messages were unclear when users entered incorrect login details or had their accounts locked. To improve this, I revised the login process to display clearer messages, such as “Incorrect email or password” for failed attempts and “Account locked” after too many tries. This helps users easily understand the issue.



## Docker Image

[Docker Image](Docker.png)

## Test-Coverage

[Test-Cov](Test-Cov.png)

## Reflection

Working through these bug fixes gave me valuable experience in technical problem-solving and collaboration within a development team. I improved my understanding of how schemas and example values affect API documentation, particularly with tools like Swagger. Initially, inconsistencies between schemas caused confusion during testing, but aligning example data and automating checks helped me see how small mismatches impact usability.

Resolving token-related fixture errors emphasized the importance of robust, reusable test infrastructure and clarified the role of OAuth2 standards in FastAPI. Furthermore, I learned about the significance of clear communication and documentation. Bugs such as SMTP disconnection and unclear login error messages highlighted the need for better configuration management and user-friendly error reporting.

This experience underscored how attention to detail—like fixing duplicate Swagger fields—can enhance API quality. Moving forward, I aim to incorporate more automated tests and clearer feedback loops in development and code review processes.


# Event Manager Company: Software QA Analyst/Developer Onboarding Assignment

Welcome to the Event Manager Company! As a newly hired Software QA Analyst/Developer and a student in software engineering, you are embarking on an exciting journey to contribute to our project aimed at developing a secure, robust REST API that supports JWT token-based OAuth2 authentication. This API serves as the backbone of our user management system and will eventually expand to include features for event management and registration.

## Assignment Objectives

1. **Familiarize with REST API functionality and structure**: Gain hands-on experience working with a REST API, understanding its endpoints, request/response formats, and authentication mechanisms.

2. **Implement and refine documentation**: Critically analyze and improve existing documentation based on issues identified in the instructor videos. Ensure that the documentation is up-to-date and accurately reflects the current state of the software.

3. **Engage in manual and automated testing**: Develop comprehensive test cases and leverage automated testing tools like pytest to push the project's test coverage towards 90%. Gain experience with different types of testing, such as unit testing, integration testing, and end-to-end testing.

4. **Explore and debug issues**: Dive deep into the codebase to investigate and resolve issues related to user profile updates and OAuth token generation. Utilize debugging tools, interpret error messages, and trace the flow of execution to identify the root cause of problems.

5. **Collaborate effectively**: Experience the power of collaboration using Git for version control and GitHub for code reviews and issue tracking. Work with issues, branches, create pull requests, and merge code while following best practices.

## Setup and Preliminary Steps

1. **Fork the Project Repository**: Fork the [project repository](https://github.com/yourusername/event_manager) to your own GitHub account. This creates a copy of the repository under your account, allowing you to work on the project independently.

2. **Clone the Forked Repository**: Clone the forked repository to your local machine using the `git clone` command. This creates a local copy of the repository on your computer, enabling you to make changes and run the project locally.

3. **Verify the Project Setup**: Follow the steps in the instructor video to set up the project using [Docker](https://www.docker.com/). Docker allows you to package the application with all its dependencies into a standardized unit called a container. Verify that you can access the API documentation at `http://localhost/docs` and the database using [PGAdmin](https://www.pgadmin.org/) at `http://localhost:5050`.

## Testing and Database Management

1. **Explore the API**: Use the Swagger UI at `http://localhost/docs` to familiarize yourself with the API endpoints, request/response formats, and authentication mechanisms. Swagger UI provides an interactive interface to explore and test the API endpoints.

2. **Run Tests**: Execute the provided test suite using pytest, a popular testing framework for Python. Running tests ensures that the existing functionality of the API is working as expected. Note that running tests will drop the database tables, so you may need to manually drop the Alembic version table using PGAdmin and re-run migrations to ensure a clean state.

3. **Increase Test Coverage**: To enhance the reliability of the API, aim to increase the project's test coverage to 90%. Write additional tests for various scenarios and edge cases to ensure that the API handles different situations correctly.

## Collaborative Development Using Git

1. **Enable Issue Tracking**: Enable GitHub issues in your repository settings. [GitHub Issues](https://guides.github.com/features/issues/) is a powerful tool for tracking bugs, enhancements, and other tasks related to the project. It allows you to create, assign, and prioritize issues, facilitating effective collaboration among team members.

2. **Create Branches**: For each issue or task you work on, create a new branch with a descriptive name using the `git checkout -b` command. Branching allows you to work on different features or fixes independently without affecting the main codebase. It enables parallel development and helps maintain a stable main branch.

3. **Pull Requests and Code Reviews**: When you have completed work on an issue, create a [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) to merge your changes into the main branch. Pull requests provide an opportunity for code review, where your team members can examine your changes, provide feedback, and suggest improvements. Code reviews help maintain code quality, catch potential issues, and promote knowledge sharing among the team.

## Specific Issues to Address

In this assignment, you will identify, document, and resolve five specific issues related to:

1. **Username validation**: Investigate and resolve any issues related to username validation. This may involve handling special characters, enforcing length constraints, or ensuring uniqueness. Proper username validation is essential to maintain data integrity and prevent potential security vulnerabilities.

2. **Password validation**: Ensure that password validation follows security best practices, such as enforcing minimum length, requiring complexity (e.g., a mix of uppercase, lowercase, numbers, and special characters), and properly hashing passwords before storing them in the database. Robust password validation protects user accounts and mitigates the risk of unauthorized access.

3. **Profile field edge cases**: Test and handle various scenarios related to updating profile fields. This may include updating the bio and profile picture URL simultaneously or individually. Consider different combinations of fields being updated and ensure that the API handles these cases gracefully. Edge case testing helps uncover potential issues and ensures a smooth user experience.

Additionally, you will resolve a sixth issue demonstrated in the instructor video. These issues will test various combinations and scenarios to simulate real-world usage and potential edge cases. By addressing these specific issues, you will gain experience in identifying and resolving common challenges in API development.

## Submission Requirements

To complete this assignment, submit the following:

1. **GitHub Repository Link**: Ensure that your repository is well-organized and includes:
  - Links to five closed issues, each with accompanying test code and necessary application code modifications.
  - Each issue should be well-documented, explaining the problem, the steps taken to resolve it, and the outcome. Proper documentation helps others understand your work and facilitates future maintenance.
  - All issues should be merged into the main branch, following the Git workflow and best practices.

2. **Updated README**: Replace the existing README with:
  - Links to the closed issues, providing easy access to your work.
  - Link to project image deployed to Dockerhub.
  - A 2-3 paragraph reflection on what you learned from this assignment, focusing on both technical skills and collaborative processes. Reflect on the challenges you faced, the solutions you implemented, and the insights you gained. This reflection helps solidify your learning and provides valuable feedback for improving the assignment in the future.

## Grading Rubric

| Criteria                                                                                                                | Points |
|-------------------------------------------------------------------------------------------------------------------------|--------|
| Resolved 5 issues related to username validation, password validation, and profile field edge cases                      | 30     |
| Resolved the issue demonstrated in the instructor video                                                                 | 20     |
| Increased test coverage to 90% by writing comprehensive test cases                                                      | 20     |
| Followed collaborative development practices using Git and GitHub (branching, pull requests, code reviews)              | 15     |
| Submitted a well-organized GitHub repository with clear documentation, links to closed issues, and a reflective summary | 15     |
| **Total**                                                                                                               | **100**|

## Resources and Documentation

- **Instructor Videos and Important Links**:
 - [Introduction to REST API with Postgres](https://youtu.be/dgMCSND2FQw) - This video provides an overview of the REST API you'll be working with, including its structure, endpoints, and interaction with the PostgreSQL database.
 - [Assignment Instructions](https://youtu.be/TFblm7QrF6o) - Detailed instructions on your tasks, guiding you through the assignment step by step.
 - [Git Command Reference I created and some explanation for collaboration with git](git.md)
 - [Docker Commands and Running The Tests in the Application](docker.md)
 - Look at the code comments:
    - [Test Configuration and Fixtures](tests/conftest.py)
    - [API User Routes](app/routers/user_routes.py)
    - [API Oauth Routes - Connection to HTTP](app/routers/oauth.py)
    - [User Service - Business Logic - This implements whats called the service repository pattern](app/services/user_service.py)
    - [User Schema - Pydantic models](app/schemas/user_schemas.py)
    - [User Model - SQl Alchemy Model ](app/models/user_model.py)
    - [Alembic Migration - this is what runs to create the tables when you do alembic upgrade head](alembic/versions/628adcb2d60e_initial_migration.py)
    - See the tests folder for all the tests

 - API Documentation: `http://localhost/docs` - The Swagger UI documentation for the API, providing information on endpoints, request/response formats, and authentication.
 - Database Management: `http://localhost:5050` - The PGAdmin interface for managing the PostgreSQL database, allowing you to view and manipulate the database tables.

- **Code Documentation**:
 The project codebase includes docstrings and comments explaining various concepts and functionalities. Take the time to read through the code and understand how different components work together. Pay attention to the structure of the code, the naming conventions used, and the purpose of each function or class. Understanding the existing codebase will help you write code that is consistent and integrates well with the project.

- **Additional Resources**:
 - [SQLAlchemy Library](https://www.sqlalchemy.org/) - SQLAlchemy is a powerful SQL toolkit and Object-Relational Mapping (ORM) library for Python. It provides a set of tools for interacting with databases, including query building, database schema management, and data serialization. Familiarize yourself with SQLAlchemy's documentation to understand how it is used in the project for database operations.
 - [Pydantic Documentation](https://docs.pydantic.dev/latest/) - Pydantic is a data validation and settings management library for Python. It allows you to define data models with type annotations and provides automatic validation, serialization, and deserialization. Consult the Pydantic documentation to understand how it is used in the project for request/response validation and serialization.
 - [FastAPI Framework](https://fastapi.tiangolo.com/) - FastAPI is a modern, fast (high-performance) Python web framework for building APIs. It leverages Python's type hints and provides automatic API documentation, request/response validation, and easy integration with other libraries. Explore the FastAPI documentation to gain a deeper understanding of its features and how it is used in the project.
 - [Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/index.html) - Alembic is a lightweight database migration tool for usage with SQLAlchemy. It allows you to define and manage database schema changes over time, ensuring that the database structure remains consistent across different environments. Refer to the Alembic documentation to learn how to create and apply database migrations in the project.

These resources will provide you with a solid foundation to understand the tools, technologies, and concepts used in the project. Don't hesitate to explore them further and consult the documentation whenever you encounter challenges or need clarification.

## Conclusion

This assignment is designed to challenge you, help you grow as a developer, and prepare you for the real-world responsibilities of a Software QA Analyst/Developer. By working on realistic issues, collaborating with your team, and focusing on testing and quality assurance, you will gain valuable experience that will serve you throughout your career.

Remember, the goal is not just to complete the assignment but to embrace the learning journey. Take the time to understand the codebase, ask questions, and explore new concepts. Engage with your team members, seek feedback, and learn from their experiences. Your dedication, curiosity, and willingness to learn will be the key to your success in this role.

We are excited to have you on board and look forward to seeing your contributions to the project. Your fresh perspective and skills will undoubtedly make a positive impact on our team and the quality of our software.

If you have any questions or need assistance, don't hesitate to reach out to your mentor or team lead. We are here to support you and ensure that you have a rewarding and enriching experience.

Once again, welcome to the Event Manager Company! Let's embark on this exciting journey together and create something remarkable.

Happy coding and happy learning!
