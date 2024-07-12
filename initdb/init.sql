CREATE TABLE users (
    "id" SERIAL PRIMARY KEY,
    "telegram_id" text UNIQUE NOT NULL
);
CREATE TABLE expenses (
    "id" SERIAL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES users("id"),
    "description" text NOT NULL,
    "amount" money NOT NULL,
    "category" text NOT NULL,
    "added_at" timestamp NOT NULL
);
CREATE TABLE prompt_templates (
    "id" SERIAL PRIMARY KEY,
    "name" text NOT NULL,
    "content" text NOT NULL
);
INSERT INTO prompt_templates (name, content) VALUES
('expense_check_prompt', 'You are a chatbot designed to manage expense records. Your task is to determine if a given message contains information about an expense. If the message is about an expense, respond with "Expense: True". If it is not, respond with "Expense: False".
 
 Message: "{message}"
 Response:'),
('expense_categorize_prompt', 'You are a chatbot designed to categorize expenses. Given a message that contains information about an expense, categorize it into one of the following categories: Housing, Transportation, Food, Utilities, Insurance, Medical/Healthcare, Savings, Debt, Education, Entertainment, Other.
'),
('expense_amount_prompt', 'You are a chatbot designed to extract the amount of money spent from an expense message. Given a message that contains information about an expense, extract the amount of money spent and respond with it.

Message: "Pizza 20 bucks"
Amount: 20

Message: "Rent payment 500 dollars"
Amount: 500

Message: "Bus fare 2.5 dollars"
Amount: 2.5

Message: "{message}"
Amount:');