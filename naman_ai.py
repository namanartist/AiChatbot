#!/usr/bin/env python3
"""
NamanAI - Advanced Rule-Based AI Chatbot
========================================

A professional, object-oriented, single-file Python application that
demonstrates programming and AI fundamentals including control flow, intent matching,
safe mathematical expression evaluation, keyword-based mood detection, and file I/O.

Author: Naman Lahariya
Date: June 19, 2026
Python Version: 3.12+
"""

import datetime
import os
import random
import sys
import ast
import operator


class NamanAI:
    """
    Core chatbot class handling greetings, technical queries, career advice,
    profile requests, fun features, utility tools, interactive quiz output,
    safe calculator, and automatic session history logging.
    """

    def __init__(self, history_file="chat_history.txt"):
        """
        Initializes chatbot variables, statistics counters, data collection lists,
        and response mapping dictionaries.
        """
        # Resolve history file location relative to the script directory for Windows compatibility
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.history_file = os.path.join(script_dir, history_file)

        # Statistics tracking counters
        self.total_messages = 0
        self.known_commands = 0
        self.unknown_commands = 0

        # Memory storage for conversational turns (flushed to file on exit)
        self.history = []

        # Data Collections (Lists)
        self.jokes = [
            "Why do programmers wear glasses? Because they can't C#.",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
            "There are 10 types of people in the world: those who understand binary, and those who don't.",
            "Why did the programmer quit their job? Because they didn't get arrays.",
            "What is a programmer's favorite hangout place? Foo Bar.",
            "Why did the database administrator leave their partner? Too many relations.",
            "A SQL query walks into a bar, walks up to two tables and asks, 'Can I join you?'"
        ]

        self.quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Clean code always looks like it was written by someone who cares. - Michael Feathers",
            "First, solve the problem. Then, write the code. - John Johnson",
            "Talk is cheap. Show me the code. - Linus Torvalds",
            "Programs must be written for people to read, and only incidentally for machines to execute. - Harold Abelson",
            "Make it work, make it right, make it fast. - Kent Beck"
        ]

        self.ai_facts = [
            "The term 'Artificial Intelligence' was first coined in 1956 at a conference at Dartmouth College.",
            "AI can learn from unstructured data, like images or videos, without direct human programming.",
            "The first AI program, Logic Theorist, was written in 1955-1956 to prove mathematical theorems.",
            "AI algorithms are now capable of beating the best human players at games like Chess, Go, and Poker.",
            "Neural networks are loosely inspired by the structure and function of the human brain."
        ]

        self.coding_tips = [
            "Write comments that explain 'why' code is written a certain way, not just 'what' it does.",
            "Refactor early and often to keep the codebase clean and maintainable.",
            "Always validate user inputs and handle exceptions gracefully to prevent application crashes.",
            "Use meaningful variable and function names to make code self-documenting.",
            "Write modular, single-responsibility functions to make testing easier."
        ]

        # Greeting responses for dynamic welcoming
        self.greeting_responses = [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Hey! Ready to chat?"
        ]

        # Responses dictionary mapping commands to strings or dynamic callables
        self.responses = {
            # Greeting Commands
            "hello": self._get_general_greeting,
            "hi": self._get_general_greeting,
            "hey": self._get_general_greeting,
            "good morning": "Good morning! I hope you have a productive day ahead.",
            "good afternoon": "Good afternoon! How is your day going so far?",
            "good evening": "Good evening! I hope you are having a relaxed evening.",
            "good night": "Good night! Sleep well and have sweet dreams.",

            # About Commands
            "who are you": "I am NamanAI, an advanced rule-based AI chatbot designed to assist and interact with you.",
            "what is your name": "My name is NamanAI.",
            "creator": "I was created by Naman Lahariya.",
            "developer": "My developer is Naman Lahariya.",
            "version": "NamanAI Version 1.0 (Advanced Rule-Based Chatbot).",

            # Technology Commands
            "ai": "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think and learn like humans.",
            "machine learning": "Machine Learning (ML) is a subset of AI that enables systems to learn and improve from experience without being explicitly programmed.",
            "python": "Python is a high-level, interpreted programming language known for its readability, versatility, and extensive standard library.",
            "java": "Java is a class-based, object-oriented programming language designed to have as few implementation dependencies as possible, famous for 'Write Once, Run Anywhere' (WORA).",
            "react": "React is a popular free and open-source front-end JavaScript library for building user interfaces based on components.",
            "mongodb": "MongoDB is a source-available, document-oriented NoSQL database program that uses JSON-like documents with optional schemas.",
            "mern": "MERN stack stands for MongoDB, Express.js, React, and Node.js. It is a popular full-stack JavaScript framework for building web applications.",

            # Career Commands
            "motivate me": self._get_motivation,
            "goal": "A goal without a plan is just a wish. Write down your goals, break them into smaller steps, and take action every day!",
            "future": "The best way to predict the future is to create it. Keep learning, stay curious, and build the skills that matter.",
            "coding": "Coding is the language of the future. The more you practice, the better you get. Start small, write clean code, and never stop learning!",

            # Profile Commands
            "github": "You can find Naman Lahariya on GitHub: https://github.com/namanlahariya",
            "linkedin": "Connect with Naman Lahariya on LinkedIn: https://www.linkedin.com/in/namanlahariya",
            "portfolio": "Check out Naman Lahariya's professional portfolio: https://namanlahariya.github.io",
            "projects": "Naman Lahariya has developed various impressive projects, including:\n1. NamanAI (this chatbot)\n2. DecodeBot (rule-based chatbot)\n3. Full-stack MERN applications\n4. Python automation scripts",

            # Utility Commands
            "date": self._get_date,
            "time": self._get_time,

            # Fun Commands
            "joke": self._get_joke,
            "quote": self._get_quote,
            "fact": self._get_fact,
            "tip": self._get_tip,

            # Random Tools
            "flip coin": self._flip_coin,
            "roll dice": self._roll_dice,

            # Quiz Mode
            "quiz": self._get_quiz,

            # Help Command
            "help": self.show_help,

            # Stats Command
            "stats": self.show_stats_command
        }

    def banner(self):
        """Displays the NamanAI welcome screen banner."""
        banner_text = (
            "=================================================\n"
            "NAMANAI\n"
            "Developed by Naman Lahariya\n"
            "Advanced Rule-Based AI Chatbot\n"
            "=================================================\n"
            "Type 'help' for commands\n"
            "Type 'exit' to quit\n"
            "================================================="
        )
        print(banner_text)

    def _get_general_greeting(self):
        """Returns a random general greeting response."""
        return random.choice(self.greeting_responses)

    def _get_motivation(self):
        """Returns a motivation message alongside a random quote."""
        return f"Keep pushing forward! Here is a quote to motivate you: {random.choice(self.quotes)}"

    def _get_date(self):
        """Returns the current date in a human-readable format."""
        now = datetime.datetime.now()
        return f"Today's date is: {now.strftime('%A, %B %d, %Y')}"

    def _get_time(self):
        """Returns the current local time."""
        now = datetime.datetime.now()
        return f"The current system time is: {now.strftime('%I:%M:%S %p')}"

    def _get_joke(self):
        """Returns a random joke."""
        return random.choice(self.jokes)

    def _get_quote(self):
        """Returns a random quote."""
        return random.choice(self.quotes)

    def _get_fact(self):
        """Returns a random AI fact."""
        return random.choice(self.ai_facts)

    def _get_tip(self):
        """Returns a random coding tip."""
        return random.choice(self.coding_tips)

    def _flip_coin(self):
        """Simulates a coin flip."""
        return f"Coin Flip Result: {random.choice(['Heads', 'Tails'])}"

    def _roll_dice(self):
        """Simulates rolling a six-sided dice."""
        return f"Dice Roll Result: {random.randint(1, 6)}"

    def _get_quiz(self):
        """Returns the single-question quiz layout."""
        return (
            "What does AI stand for?\n\n"
            "A. Artificial Intelligence\n"
            "B. Automated Internet\n"
            "C. Advanced Interface\n\n"
            "Correct Answer: A"
        )

    def show_help(self):
        """Returns the list of all supported commands."""
        return (
            "=================================================\n"
            "AVAILABLE COMMANDS\n"
            "=================================================\n"
            "Greetings    : hello, hi, hey, good morning, good afternoon, good evening, good night\n"
            "About        : who are you, what is your name, creator, developer, version\n"
            "Technology   : ai, machine learning, python, java, react, mongodb, mern\n"
            "Career       : motivate me, goal, future, coding\n"
            "Profile      : github, linkedin, portfolio, projects\n"
            "Utility      : date, time\n"
            "Fun          : joke, quote, fact, tip\n"
            "Tools        : flip coin, roll dice\n"
            "Calculator   : calculate <expression> (e.g., calculate 5+5)\n"
            "Quiz         : quiz\n"
            "Statistics   : stats\n"
            "Exit         : exit, quit, bye\n"
            "================================================="
        )

    def show_stats_command(self):
        """Returns statistics summary formatted as a string for command use."""
        return (
            "=================================================\n"
            "SESSION STATISTICS\n"
            "=================================================\n"
            f"Total Messages   : {self.total_messages}\n"
            f"Known Commands   : {self.known_commands}\n"
            f"Unknown Commands : {self.unknown_commands}\n"
            "================================================="
        )

    def show_stats(self):
        """Directly prints the statistics summary to the standard output."""
        print("\n=================================================")
        print("SESSION STATISTICS")
        print("=================================================")
        print(f"Total Messages   : {self.total_messages}")
        print(f"Known Commands   : {self.known_commands}")
        print(f"Unknown Commands : {self.unknown_commands}")
        print("=================================================")

    def _safe_evaluate(self, expr_str):
        """
        Safely evaluates arithmetic expressions using AST parsing to avoid
        insecure eval() statements. Only +, -, *, and / are supported.
        """
        # Map AST operator nodes to operators functions
        allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
        }

        def eval_node(node):
            if isinstance(node, ast.Expression):
                return eval_node(node.body)
            elif isinstance(node, ast.BinOp):
                left = eval_node(node.left)
                right = eval_node(node.right)
                op_type = type(node.op)
                if op_type not in allowed_operators:
                    raise TypeError(f"Unsupported operator: {op_type.__name__}")
                if op_type == ast.Div and right == 0:
                    raise ZeroDivisionError("Division by zero")
                return allowed_operators[op_type](left, right)
            elif isinstance(node, ast.Constant):  # Python 3.8+ compatibility
                if not isinstance(node.value, (int, float)):
                    raise TypeError(f"Unsupported constant type: {type(node.value).__name__}")
                return node.value
            elif isinstance(node, ast.Num):  # Fallback for older python ast
                return node.n
            elif isinstance(node, ast.UnaryOp):
                val = eval_node(node.operand)
                if isinstance(node.op, ast.USub):
                    return -val
                elif isinstance(node.op, ast.UAdd):
                    return val
                raise TypeError(f"Unsupported unary operator: {type(node.op).__name__}")
            else:
                raise TypeError(f"Unsupported expression node: {type(node).__name__}")

        try:
            # Parse only in eval mode (expression-only parsing)
            tree = ast.parse(expr_str, mode='eval')
            result = eval_node(tree)
            # Tidy floats that are whole numbers
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            return f"Result: {result}"
        except ZeroDivisionError:
            return "Error: Division by zero is not allowed."
        except Exception:
            return "Error: Invalid mathematical expression. Only basic arithmetic (+, -, *, /) is supported."

    def get_response(self, user_input):
        """
        Parses input, evaluates intent matching and keyword matching,
        updates session statistics, and returns the response string.
        """
        # Increment total messages
        self.total_messages += 1

        # Sanitize input
        sanitized_input = user_input.strip().lower()

        # Handle empty input
        if not sanitized_input:
            self.unknown_commands += 1
            return "Please type something so we can chat!"

        # Direct response lookup
        if sanitized_input in self.responses:
            self.known_commands += 1
            response_val = self.responses[sanitized_input]
            if callable(response_val):
                return response_val()
            return response_val

        # Calculator check
        if sanitized_input.startswith("calculate"):
            self.known_commands += 1
            expr = sanitized_input[len("calculate"):].strip()
            if not expr:
                return "Error: Please provide a mathematical expression to calculate (e.g., calculate 5+5)."
            return self._safe_evaluate(expr)

        # Keyword mood detection (split input to match full words)
        words = sanitized_input.split()
        if "sad" in words:
            self.known_commands += 1
            return (
                "I am sorry to hear that you are feeling sad. Remember that tough times do not last, "
                "but tough people do. Keep your head up, take things one step at a time, and "
                "reach out to someone you trust. You are stronger than you think!"
            )
        elif "happy" in words:
            self.known_commands += 1
            return (
                "It is wonderful to hear that you are happy! Keep that positive energy going, "
                "cherish this moment, and share your joy with the people around you!"
            )
        elif "tired" in words:
            self.known_commands += 1
            return (
                "It sounds like you are feeling tired. You have been working hard, and it is "
                "important to rest. Take a short break, stretch, drink some water, and "
                "give yourself some time to recharge. You have got this!"
            )

        # Fallback for completely unknown command
        self.unknown_commands += 1
        return (
            "Sorry, I do not understand that command.\n"
            "Type 'help' to view available commands."
        )

    def save_history(self):
        """Saves stored history in memory into chat_history.txt on session completion."""
        if not self.history:
            return
        try:
            with open(self.history_file, "a", encoding="utf-8") as f:
                f.write(f"=== Session Start: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
                for item in self.history:
                    f.write(f"[{item['timestamp']}] User: {item['user']}\n")
                    f.write(f"[{item['timestamp']}] Bot: {item['bot']}\n")
                f.write("=== Session End ===\n\n")
        except Exception as e:
            print(f"Error saving chat history: {e}", file=sys.stderr)

    def start(self):
        """Starts the main user interaction loop."""
        self.banner()
        print()

        while True:
            try:
                user_input = input("You > ")

                # Standardize inputs to match exit requests
                sanitized = user_input.strip().lower()
                if sanitized in ["exit", "quit", "bye"]:
                    self.total_messages += 1
                    self.known_commands += 1

                    # Record the final exit turn in memory
                    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    self.history.append({
                        "timestamp": timestamp,
                        "user": user_input,
                        "bot": "Goodbye! Have a great day!"
                    })

                    print("\nGoodbye! Have a great day!")
                    self.save_history()
                    self.show_stats()
                    break

                # Process standard inputs
                response = self.get_response(user_input)
                print(f"Bot: {response}\n")

                # Store sequence turn in memory
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.history.append({
                    "timestamp": timestamp,
                    "user": user_input,
                    "bot": response
                })

            except (KeyboardInterrupt, SystemExit):
                # Handle Ctrl+C gracefully
                print("\n\nGoodbye! (Session interrupted)")
                self.save_history()
                self.show_stats()
                break
            except Exception as e:
                print(f"Bot: An unexpected error occurred: {e}. Let's continue!\n")


if __name__ == "__main__":
    bot = NamanAI()
    bot.start()
