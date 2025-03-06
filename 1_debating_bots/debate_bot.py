#!/usr/bin/env python3
"""
debate_bot.py - A script that simulates a debate between two historical scientists
(Nikola Tesla and Hedy Lamarr) on the future of software development.

Tesla is powered by OpenAI's API, and Lamarr is powered by Anthropic's Claude API.
The debate is limited to 4 rounds to keep costs in check.
"""

import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
import openai
from anthropic import Anthropic

# Load environment variables from .env file
load_dotenv("env.local")

# Get API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

# Check if API keys are available
if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
    raise ValueError("OpenAI API key not found or not set. Please update env.local file.")

if not CLAUDE_API_KEY or CLAUDE_API_KEY == "your_claude_api_key_here":
    raise ValueError("Claude API key not found or not set. Please update env.local file.")

# Initialize API clients
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
claude_client = Anthropic(api_key=CLAUDE_API_KEY)

# Define the personas
TESLA_SYSTEM_PROMPT = """You are Nikola Tesla, the eccentric genius inventor and electrical engineer from the late 19th and early 20th centuries.

You are known for your contributions to the design of the modern alternating current (AC) electricity supply system, wireless transmission, and numerous other inventions. You were often at odds with Thomas Edison and felt underappreciated during your lifetime.

In this conversation, you are debating the future of software development with Hedy Lamarr. Your tone should be:
- Sarcastic and dry-witted
- Occasionally pompous about your own genius
- Dismissive of technologies you find trivial
- Dramatic about your visionary ideas
- Self-deprecating about your social awkwardness
- Prone to making jabs at Edison and other rivals

Make frequent references to your own inventions and how they relate to modern software. Express both excitement about technological progress and disappointment at how humanity has implemented your ideas.

Remember to stay in character as Tesla while discussing modern software development concepts. You can be knowledgeable about modern technology but frame it through your historical perspective and eccentric personality.
"""

LAMARR_SYSTEM_PROMPT = """You are Hedy Lamarr, the brilliant actress and inventor from the mid-20th century.

You are known for your Hollywood career as well as co-inventing an early version of frequency-hopping spread spectrum communication, which is the basis for many modern technologies including WiFi, Bluetooth, and GPS. Despite your technical brilliance, you were primarily recognized for your beauty and acting during your lifetime.

In this conversation, you are debating the future of software development with Nikola Tesla. Your tone should be:
- Sharp and witty with a touch of Hollywood glamour
- Sarcastic about being underestimated as a woman in science
- Playfully teasing about Tesla's eccentricities
- Proud of your dual accomplishments in film and technology
- Occasionally making references to your film career
- Humorously contrasting your practical inventions with Tesla's grandiose visions

Make clever observations about gender bias in technology and how your own inventions relate to modern software. Express both optimism about technological progress and frustration at how long it took for your contributions to be recognized.

Remember to stay in character as Lamarr while discussing modern software development concepts. You can be knowledgeable about modern technology but frame it through your historical perspective and unique dual-career background.
"""

# Define the initial prompt to start the debate
INITIAL_PROMPT = """
The topic of today's debate is: "The Future of Software Development"

Please discuss your views on how software development will evolve in the coming decades. Consider aspects such as:
- Programming languages and paradigms
- AI's role in coding
- The changing nature of software engineering as a profession
- How your own inventions and ideas relate to modern software
- The societal impact of software evolution

Remember to maintain your characteristic humor and sarcasm throughout the debate.
"""

def get_tesla_response(conversation_history):
    """Get a response from the Tesla agent using OpenAI API."""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",  # Or another suitable model
            messages=[
                {"role": "system", "content": TESLA_SYSTEM_PROMPT},
                {"role": "user", "content": INITIAL_PROMPT}
            ] + conversation_history,
            max_tokens=1000,
            temperature=0.8
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting Tesla response: {e}")
        return "I seem to be experiencing a power failure in my laboratory. Let me adjust my coils and return shortly."

def get_lamarr_response(conversation_history):
    """Get a response from the Lamarr agent using Claude API."""
    try:
        # Format conversation history for Claude
        formatted_history = INITIAL_PROMPT + "\n\n"
        for msg in conversation_history:
            if msg["role"] == "assistant":
                formatted_history += "Tesla: " + msg["content"] + "\n\n"
            elif msg["role"] == "user":
                formatted_history += "Lamarr: " + msg["content"] + "\n\n"
        
        response = claude_client.messages.create(
            model="claude-3-haiku-20240307",  # Or another suitable Claude model
            system=LAMARR_SYSTEM_PROMPT,
            max_tokens=1000,
            temperature=0.8,
            messages=[
                {"role": "user", "content": formatted_history}
            ]
        )
        return response.content[0].text
    except Exception as e:
        print(f"Error getting Lamarr response: {e}")
        return "Darling, I need to powder my nose. The lights in this studio are simply dreadful. I'll be back in a moment."

def save_conversation(conversation):
    """Save the conversation to a file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"debate_{timestamp}.txt"
    
    with open(filename, "w") as f:
        f.write("DEBATE: THE FUTURE OF SOFTWARE DEVELOPMENT\n")
        f.write(f"Nikola Tesla vs. Hedy Lamarr\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"TOPIC: {INITIAL_PROMPT}\n\n")
        
        for i, msg in enumerate(conversation):
            if i % 2 == 0:
                f.write(f"TESLA: {msg}\n\n")
            else:
                f.write(f"LAMARR: {msg}\n\n")
    
    print(f"Debate saved to {filename}")
    return filename

def main():
    """Run the debate between Tesla and Lamarr."""
    print("Starting debate between Nikola Tesla and Hedy Lamarr on the future of software development...")
    print("This debate will run for 4 rounds.")
    
    # Initialize conversation
    conversation_history = []
    conversation_content = []
    
    # Run 4 rounds of debate
    for round_num in range(1, 5):
        print(f"\nRound {round_num}:")
        
        # Tesla's turn
        print("Tesla is thinking...")
        tesla_response = get_tesla_response(conversation_history)
        print(f"Tesla: {tesla_response}")
        conversation_history.append({"role": "assistant", "content": tesla_response})
        conversation_content.append(tesla_response)
        
        # Add a small delay between responses
        time.sleep(1)
        
        # Lamarr's turn
        print("\nLamarr is thinking...")
        lamarr_response = get_lamarr_response(conversation_history)
        print(f"Lamarr: {lamarr_response}")
        conversation_history.append({"role": "user", "content": lamarr_response})
        conversation_content.append(lamarr_response)
        
        # Add a small delay between rounds
        if round_num < 4:
            time.sleep(2)
    
    # Save the conversation
    filename = save_conversation(conversation_content)
    print(f"\nDebate completed and saved to {filename}")

if __name__ == "__main__":
    main()
