

import random
import datetime

# ---------------------------------------------------------------
# Constants (named so there are no unexplained "magic values")
# ---------------------------------------------------------------
GAME_MIN = 1          # lowest number in the guessing game
GAME_MAX = 20         # highest number in the guessing game
GAME_ATTEMPTS = 5     # guesses allowed per game

QUOTES = [
    "The secret of getting ahead is getting started.",
    "Don't watch the clock; do what it does. Keep going.",
    "Small steps every day lead to big results.",
    "Mistakes are proof that you are trying.",
    "Dream big, start small, act now.",
]

JOKES = [
    "Why did the developer go broke? Because they used up all their cache.",
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "There are 10 types of people: those who understand binary and those who don't.",
    "I would tell you a UDP joke, but you might not get it.",
    "Why was the function sad? It didn't get any arguments.",
]

FACTS = [
    "Python is named after Monty Python, not the snake.",
    "The first computer bug was a real moth found in a computer in 1947.",
    "The perceptron, an early neural network unit, was introduced in 1958.",
    "The first 1 GB hard drive (1980) weighed over 200 kg.",
    "About 90% of the world's data was created in the last few years.",
]


# ---------------------------------------------------------------
# Greeting & name capture (FR-01, FR-02)
# ---------------------------------------------------------------
def get_user_name():
    """Ask for the user's name. Falls back to 'friend' if left blank."""
    name = input("Assistant: Hi! I'm Mini Alexa. What's your name?\nYou: ").strip()
    return name.title() if name else "Friend"


def build_greeting(name):
    """Return the welcome message that uses the stored name."""
    return f"Nice to meet you, {name}! Type 'help' to see what I can do."


# ---------------------------------------------------------------
# Date & time (FR-03, FR-04)
# ---------------------------------------------------------------
def get_current_time():
    """Return the current time, e.g. 'It's currently 3:45 PM.'"""
    now = datetime.datetime.now()
    return f"It's currently {now.strftime('%I:%M %p').lstrip('0')}."


def get_current_date():
    """Return today's date, e.g. 'Today is Sunday, 15 November 2026.'"""
    today = datetime.datetime.now()
    return f"Today is {today.strftime('%A, %d %B %Y')}."


# ---------------------------------------------------------------
# Calculator (FR-05)
# ---------------------------------------------------------------
def parse_expression(text):
    """
    Pull 'number operator number' out of text.
    Returns (a, op, b) or None if it can't be parsed.
    """
    # Remove the trigger words so only the maths is left
    for word in ("calculate", "calc", "what is", "what's"):
        text = text.replace(word, " ")
    # Put spaces around operators so "12+8" also works
    for op in "+-*/":
        text = text.replace(op, f" {op} ")
    parts = text.split()
    # Handle a negative first number like "-5 + 3"
    if len(parts) == 4 and parts[0] == "-":
        parts = ["-" + parts[1]] + parts[2:]
    if len(parts) != 3 or parts[1] not in ("+", "-", "*", "/"):
        return None
    try:
        return float(parts[0]), parts[1], float(parts[2])
    except ValueError:
        return None


def calculate(a, op, b):
    """Perform the arithmetic. Raises ZeroDivisionError on divide by zero."""
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    return a / b


def respond_calculator(text):
    """Handle a calculation request without ever crashing."""
    parsed = parse_expression(text)
    if parsed is None:
        entered = input("Assistant: What should I calculate? (e.g. 12 + 8)\nYou: ")
        parsed = parse_expression(entered.lower())
    if parsed is None:
        return "I couldn't read that. Try something like: calculate 12 + 8"
    a, op, b = parsed
    try:
        result = calculate(a, op, b)
    except ZeroDivisionError:
        return "I can't divide by zero - try a different number."
    # Show whole numbers without a trailing .0
    if result == int(result):
        result = int(result)
    else:
        result = round(result, 4)
    return f"The result is {result}"


# ---------------------------------------------------------------
# Quotes, jokes, facts (FR-06, FR-07, FR-08)
# ---------------------------------------------------------------
def get_random_quote():
    """Pick one random quote from QUOTES."""
    return random.choice(QUOTES)


def get_random_joke():
    """Pick one random joke from JOKES."""
    return random.choice(JOKES)


def get_random_fact():
    """Pick one random fact from FACTS."""
    return random.choice(FACTS)


# ---------------------------------------------------------------
# Number guessing game (FR-09)
# ---------------------------------------------------------------
def play_guessing_game():
    """Guessing game with limited attempts and higher/lower hints."""
    secret = random.randint(GAME_MIN, GAME_MAX)
    print(f"Assistant: I'm thinking of a number between {GAME_MIN} and "
          f"{GAME_MAX}. You have {GAME_ATTEMPTS} tries.")
    for attempt in range(1, GAME_ATTEMPTS + 1):
        raw = input(f"Guess #{attempt}: ").strip()
        try:
            guess = int(raw)
        except ValueError:
            print("That's not a whole number (this still uses up a try!).")
            continue
        if guess == secret:
            return f"Correct! You got it in {attempt} tries. Well done!"
        if guess < secret:
            print("Higher!")
        else:
            print("Lower!")
    return f"Out of tries! The number was {secret}. Type 'game' to play again."


# ---------------------------------------------------------------
# AI concept demos (FR-13, FR-14)
# ---------------------------------------------------------------
def recommend_activity():
    """
    AI CONCEPT - Rule-based decision / simple decision tree.
    The current hour is the input "feature"; the if/elif chain acts like
    the branches of a decision tree that outputs a "class" (an activity).
    """
    hour = datetime.datetime.now().hour
    if 5 <= hour < 9:
        return "Good morning! How about breakfast and a short walk?"
    if 9 <= hour < 12:
        return "Great time to focus - try your most important task now."
    if 12 <= hour < 14:
        return "It's lunchtime! Time for a proper meal."
    if 14 <= hour < 18:
        return "Afternoon slump? Have a snack and do some light coding."
    if 18 <= hour < 22:
        return "Evening: relax, have dinner, or review what you learned today."
    return "It's late - time to rest. Sleep helps your brain learn!"


def neuron(inputs, weights, bias):
    """
    DL CONCEPT - Artificial neuron (perceptron).
    1. Multiply each input by its weight and add them up (weighted sum).
    2. Add the bias.
    3. Apply a step activation function: output 1 if sum > 0, else 0.
    """
    weighted_sum = sum(x * w for x, w in zip(inputs, weights))
    total = weighted_sum + bias
    return 1 if total > 0 else 0, total


def perceptron_demo():
    """
    Forward propagation demo: inputs -> weights/bias -> activation -> output.
    Weights are FIXED (no training), so this is not machine learning yet.
    Example question: "Should I go outside?" using 3 yes(1)/no(0) inputs.
    """
    weights = [0.6, 0.3, 0.4]   # how important each input is
    bias = -0.7                 # how hard it is to say "yes"
    questions = ["Is the weather good? (0-1)", "Do you have free time? (0-1)",
                 "Are your friends going? (0-1)"]
    print("Assistant: Perceptron demo - decide 'Should I go outside?'")
    print(f"Weights are fixed at {weights} and bias is {bias}.")
    inputs = []
    for q in questions:
        try:
            inputs.append(float(input(f"{q}: ")))
        except ValueError:
            return "Please enter numbers like 0 or 1 - try 'perceptron' again."
    output, total = neuron(inputs, weights, bias)
    # Optional hidden layer: feed the first neuron's output into a second one
    final, _ = neuron([output], [1.0], -0.5)
    answer = "Yes, go outside!" if final == 1 else "Better stay in."
    return (f"Weighted sum + bias = {round(total, 2)} -> step activation "
            f"output = {output}.\n(Hidden layer output = {final}) {answer}")


# ---------------------------------------------------------------
# Help menu (FR-10)
# ---------------------------------------------------------------
def print_help():
    """Show every supported command."""
    return (
        "Here is what I can do:\n"
        " - time        show current time\n"
        " - date        show current date\n"
        " - calculate   do a calculation (e.g. calculate 12 + 8)\n"
        " - joke        tell a joke\n"
        " - quote       motivational quote\n"
        " - fact        random fact\n"
        " - game        play number guessing game\n"
        " - recommend   rule-based activity suggestion\n"
        " - perceptron  single neuron demo\n"
        " - hello       say hi\n"
        " - exit        quit the assistant"
    )


# ---------------------------------------------------------------
# Routing: keyword detection -> intent -> function
# ---------------------------------------------------------------
def respond(text, name):
    """
    AI CONCEPT - Intent recognition by keyword / pattern matching.
    Returns (reply, should_exit).
    """
    text = text.lower().strip()           # normalize
    words = set(text.replace("?", " ").replace("!", " ").split())

    if words & {"exit", "quit", "bye"}:
        return f"Goodbye, {name}! Have a great day.", True
    if "help" in words:
        return print_help(), False
    if words & {"hello", "hi", "hey"}:
        return f"Hello, {name}! How can I help?", False
    if "time" in words:
        return get_current_time(), False
    if "date" in words or "today" in words:
        return get_current_date(), False
    if words & {"calculate", "calc"} or parse_expression(text):
        return respond_calculator(text), False
    if words & {"quote", "motivate", "motivation"}:
        return get_random_quote(), False
    if words & {"joke", "funny"}:
        return get_random_joke(), False
    if "fact" in words:
        return get_random_fact(), False
    if words & {"game", "guess"}:
        return play_guessing_game(), False
    if words & {"recommend", "suggest", "activity"}:
        return f"Here's a suggestion for you, {name}: {recommend_activity()}", False
    if words & {"perceptron", "neuron"}:
        return perceptron_demo(), False
    return "I'm not sure I understood that - type 'help' to see what I can do.", False


def main():
    """Main loop: input -> normalize -> route -> print."""
    print("=" * 43)
    print("   MINI ALEXA - VIRTUAL ASSISTANT")
    print("=" * 43)
    name = get_user_name()
    print(f"Assistant: {build_greeting(name)}")

    while True:
        try:
            text = input("You: ")
            reply, done = respond(text, name)
            print(f"Assistant: {reply}")
            if done:
                break
        except (KeyboardInterrupt, EOFError):
            print(f"\nAssistant: Goodbye, {name}!")
            break
        except Exception as error:  # last-resort safety net (FR-12)
            print(f"Assistant: Oops, something went wrong ({error}). "
                  "Let's keep going.")
    print("=" * 43)


if __name__ == "__main__":
    main()
