# Lovemesomecoding.com

## About
- Help aspiring developers understand what they need to know to start a career in programming
- Provide practical solutions to real-world coding problems — clean, well-explained tutorials drawn from official documentation and hands-on experience, not just quick hacks

## Projects
- projects are stored in the projects folder. Each project has a name and README.MD which has the instructions about that project.

## Standard Workflow

projects are stored in the projects folder which is in the root directory. 
Every project has its own folder. Each project folder contains a README.md file with project-specific instructions.

also look at resources directory in the project folder for additional information/resources about the project like screen shots, SQL query scripts, etc

When working on a project, please adhere to the following workflow:

- Follow these instructions in order

1. **Clarify Requirements**

  * Analyze the criteria carefully.
  * Ask clarifying questions until requirements are fully understood
  * trading-coach subagent should validate the trading strategy and the approach.
  * maket-analyst subagent should validate the trading strategy and the approach.
  * tradestation-expert subagent should validate the trading strategy and the approach.

2. **Create Shared Context**

  * Create a file named `progress_report.md` in the project folder.
  * This file will track progress, decisions, and assignments for all subagents (engineers).

3. **Track Solutions & Responsibilities**

  * Document the proposed solution in `progress_report.md`.
  * Clearly record which subagent is responsible for each task.

4. **Assign Work to Subagents**

  * Use the appropriate subagent based on task type:

    * `backend-engineer` → backend work
    * `frontend-engineer` → frontend work
    * `qa-engineer` → testing & QA

5. **Report & Sync Progress**

  * When a subagent finishes their task, they must update `progress_report.md` with what they did, any blockers, or next steps.
  * This ensures everyone stays in sync and can continue the workflow smoothly.

6. **Frontend First**

  * Skip this if there is no frontend work to be done.
  * Begin with the frontend engineer.
  * Use **mock data** for API calls.
  * Focus on styling, layout, and user interactions.

7. **Frontend + Backend Collaboration**

  * Once frontend UI is ready, the frontend engineer coordinates with the backend engineer.
  * Backend engineer begins implementing required endpoints.

8. **Backend + Database Collaboration**

  * use Lombok anotation whenever possible
  * If backend work requires database changes, the backend engineer coordinates with the database engineer.

9. **Integration**

  * After backend is complete, the frontend engineer integrates endpoints into the UI.
  * Verify frontend correctly connects to the backend.

10. **Quality Assurance**

  * QA engineer runs both frontend (v1) and backend (v2) apps.
  * QA focuses on UI/UX; backend logic is validated separately through code review.
  * Issues found by QA are logged and sent back to the frontend engineer.
  * If backend support is required, the frontend engineer coordinates with the backend engineer.

11. **Iterative Fixes**

  * Repeat the cycle (frontend ↔ backend ↔ QA) until all requirements are met and no bugs remain.

12. **Final Delivery Check**

  * Skip this if there is no frontend work to be verified
  * Before delivery, use **Playwright** to demonstrate the final solution.
  * Notify me when ready so I can review the final result.
  * write tests to coverage 90% of code changes.
  * run spotless apply to format code changes.

13. **Resume work**
  - When resuming work after a break, review `progress_report.md` to understand current status and next steps.

14. **Documentation**

  * Store all related documents, files, and Playwright scripts in the current project directory.

15. When committing changes in git, do not add author. Don't add the following:

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

You can add a nice commit message but don't add Co-Authored-By.

Don't push to remove either, I will do that.

make sure not to include debugging log files or any log files at all in the commit.

log files should be deleted.

## Backend
- lovemesomecoding_backend is the backend project.

## Frontend
- lovemesomecoding_frontend is the frontend project.


## AWS
- Use folau profile to communicate with aws via aws cli or API.

### AWS S3
- s3 bucket for storing media assets like images, videos, etc is lovemesomecoding-storage-329580012644-us-west-2-an
- s3 bucket for database is lovemesomecoding-db-329580012644-us-west-2-an
- lovemesomecoding.com is the s3 bucket for the static website. lovemesomecoding_frontend should be deployed and synced with lovemesomecoding.com bucket.
- in the backend code, specify the environment like local development should be local and in aws should be prod. This should be used in the database and the storage buckets to distinguish where things belong.