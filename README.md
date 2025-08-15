HR Bot


Introduction
This project is a serverless HR chatbot designed to streamline common employee requests and inquiries. Built on the AWS Lex platform, the bot uses natural language processing (NLP) to automate interactions for tasks such as submitting leave requests, checking vacation balances, and retrieving company policy information.
The primary goal of this bot is to improve operational efficiency by offloading repetitive questions from human HR staff, allowing them to focus on more complex tasks. The bot's logic is powered by AWS Lambda, which securely processes and responds to user intents.


Features

Leave Management: Allows employees to submit leave requests and check their leave balance.

Policy Lookup: Provides quick access to common company policies and documentation.

FAQs: Integrates with Amazon Kendra to provide intelligent and accurate answers to frequently asked questions.

Secure & Scalable: Leverages AWS's serverless architecture for a secure, highly scalable, and cost-effective solution.



Technology Stack

Amazon Lex: For building the conversational interface and managing user intents.

Amazon Kendra: For intelligent search and FAQ-based responses.

AWS Lambda: For the serverless backend logic that handles the bot's functionality.

Python: The programming language used to write the Lambda function.

Git & GitHub: For version control and project hosting.


Setup and Installation
To set up and run this bot, you will need an AWS account.

Clone the Repository:
Clone this repository to your local machine using the following command:
git clone https://github.com/Lipsha-Dash/HRBot.git

Create and Configure the AWS Lambda Function:
In the AWS Management Console, navigate to the Lambda service.
Create a new Lambda function.
Choose Python as the runtime.
Copy the Python code from this repository's source files into your Lambda function.
Configure the necessary permissions for the function to interact with other AWS services.

Build and Deploy the Amazon Lex Bot:
In the AWS Management Console, navigate to the Amazon Lex service.
Create a new bot.
Define the intents (e.g., SubmitLeaveRequest, CheckLeaveBalance, GetPolicy).
For each intent, configure it to fulfill with your Lambda function.
Build and publish the bot, creating an alias (e.g., ProdAlias) to manage your production version.

Integrate with Amazon Kendra:
Set up an Amazon Kendra index and data source containing your FAQ documents.
Configure a new intent in your Lex bot (e.g., FAQIntent) to use Kendra for fulfilling requests.

Usage

Once the bot is deployed, you can interact with it through any channel you have integrated (e.g., a test console, a website, or a messaging platform like Slack or Facebook Messenger).
Here are some example phrases you can use:

"I want to request a leave."

"What is my leave balance?"

"Tell me about the sick leave policy."

"Check my PTO balance"

Contact
For questions or feedback, feel free to open an issue in this repository.
