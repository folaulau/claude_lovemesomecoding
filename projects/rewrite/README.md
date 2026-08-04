# Rewrite
- Currently lovemesomecoding.com is my website running on wordpress hosted on DreamHost for $25 a month. I want to migrate this over to my aws account to save money and improve UI/UX.

## Frontend project
- I want to host the frontend in aws s3 and deliver it via cloudfront.
- Use https://www.w3schools.com as a guide as I want my website to look like https://www.w3schools.com on the frontend.
- Use https://www.w3schools.com navbar designs.
- Use nextjs for the lovemesomecoding_frontend project so that pages are SEO-friendly and readable by Google search
- Bootstrap 5 for components and styling.
- look at this project /Users/folaukaveinga/Github/pitaconcrete.com which is a frontend that is using a backend i want to copy.
- /Users/folaukaveinga/Github/pitaconcrete.com is deployed to pitaconcrete.com which is hosted in our aws account.

## Backend project
- I want to use aws s3 as a backend database using json data structure.
- look at /Users/folaukaveinga/Github/backend-folaukaveinga project as an example.
- I am using chalice and deploy it to aws lambda but we can use other frameworks. 
- The goal is to deploy lovemesomecoding_backend into aws lambda like /Users/folaukaveinga/Github/backend-folaukaveinga
- Create backend admin pages where only admin users can login and use.
- After logging in, I should be able to create collections and posts. 
- pattern backend after wordpress to create collections / posts / comments.
- Posts and comments should be pull from the database which is s3 bucket for each page.