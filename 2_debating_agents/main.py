#!/usr/bin/env python3
"""
Two-Agent Debate System using AutoGen
This script creates a debate between two AI agents with distinct personalities.
"""

import os
import sys
import time
import json
import re
import datetime
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dotenv import load_dotenv

try:
    import autogen
except ImportError:
    print("AutoGen package not found. Installing...")
    os.system("pip install pyautogen")
    import autogen

# Set up argument parser
parser = argparse.ArgumentParser(description="Run a debate between two AI agents")
parser.add_argument("--topic", type=str, help="Override the debate topic")
parser.add_argument("--rounds", type=int, help="Override the number of debate rounds")
parser.add_argument("--output", type=str, help="Output file path for the debate")
args = parser.parse_args()

# Load environment variables from env.local
env_path = Path(__file__).parent / "env.local"
load_dotenv(dotenv_path=env_path)

# Get configuration values
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
DEBATE_ROUNDS = int(os.getenv("DEBATE_ROUNDS", "3"))
DEBATE_OUTPUT_PATH = os.getenv("DEBATE_OUTPUT_PATH", "")

# Override with command line arguments if provided
if args.rounds:
    DEBATE_ROUNDS = args.rounds
if args.output:
    DEBATE_OUTPUT_PATH = args.output

# Validate API keys
if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
    print("Error: OpenAI API key not found. Please set it in env.local")
    sys.exit(1)

if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY == "your_anthropic_api_key_here":
    print("Error: Anthropic API key not found. Please set it in env.local")
    sys.exit(1)

def load_text_file(file_path: str) -> str:
    """Load and return the contents of a text file."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error loading file {file_path}: {e}")
        sys.exit(1)

def parse_agent_config(config_text: str) -> Dict[str, Any]:
    """Parse the agent configuration from the text file."""
    config = {}
    
    # Extract name
    name_match = re.search(r'NAME:\s*(.*?)$', config_text, re.MULTILINE)
    if name_match:
        config['name'] = name_match.group(1).strip()
    
    # Extract universe
    universe_match = re.search(r'UNIVERSE:\s*(.*?)$', config_text, re.MULTILINE)
    if universe_match:
        config['universe'] = universe_match.group(1).strip()
    
    # Extract LLM configuration
    model_match = re.search(r'MODEL:\s*(.*?)$', config_text, re.MULTILINE)
    if model_match:
        config['model'] = model_match.group(1).strip()
    
    provider_match = re.search(r'PROVIDER:\s*(.*?)$', config_text, re.MULTILINE)
    if provider_match:
        config['provider'] = provider_match.group(1).strip()
    
    temp_match = re.search(r'TEMPERATURE:\s*(.*?)$', config_text, re.MULTILINE)
    if temp_match:
        config['temperature'] = float(temp_match.group(1).strip())
    
    tokens_match = re.search(r'MAX_TOKENS:\s*(.*?)$', config_text, re.MULTILINE)
    if tokens_match:
        config['max_tokens'] = int(tokens_match.group(1).strip())
    
    # Extract full sections for system message
    background_match = re.search(r'BACKGROUND:(.*?)(?=##|\Z)', config_text, re.DOTALL)
    if background_match:
        config['background'] = background_match.group(1).strip()
    
    # Get personality traits
    traits_section = re.search(r'## Personality Traits(.*?)(?=##|\Z)', config_text, re.DOTALL)
    if traits_section:
        traits_text = traits_section.group(1)
        traits = re.findall(r'-\s*(.*?)$', traits_text, re.MULTILINE)
        config['personality_traits'] = [trait.strip() for trait in traits]
    
    # Get debate style
    style_section = re.search(r'## Debate Style(.*?)(?=##|\Z)', config_text, re.DOTALL)
    if style_section:
        style_text = style_section.group(1)
        styles = re.findall(r'-\s*(.*?)$', style_text, re.MULTILINE)
        config['debate_style'] = [style.strip() for style in styles]
    
    return config

def parse_prompt(prompt_text: str) -> Dict[str, Any]:
    """Parse the initial prompt configuration."""
    prompt_config = {}
    
    # Extract topic
    topic_match = re.search(r'## Debate Topic\s*"(.*?)"', prompt_text, re.DOTALL)
    if topic_match:
        prompt_config['topic'] = topic_match.group(1).strip()
    
    # Extract context
    context_match = re.search(r'## Debate Context\s*(.*?)(?=##|\Z)', prompt_text, re.DOTALL)
    if context_match:
        prompt_config['context'] = context_match.group(1).strip()
    
    # Extract initial positions
    agent1_pos = re.search(r'- Agent 1.*?:(.*?)$', prompt_text, re.MULTILINE)
    if agent1_pos:
        prompt_config['agent1_position'] = agent1_pos.group(1).strip()
    
    agent2_pos = re.search(r'- Agent 2.*?:(.*?)$', prompt_text, re.MULTILINE)
    if agent2_pos:
        prompt_config['agent2_position'] = agent2_pos.group(1).strip()
    
    return prompt_config

def create_agent_config(agent_data: Dict[str, Any], prompt_data: Dict[str, Any], is_agent1: bool) -> Dict[str, Any]:
    """Create the configuration for an AutoGen agent."""
    # Determine which position to use
    position = prompt_data['agent1_position'] if is_agent1 else prompt_data['agent2_position']
    opponent = "Wonder Woman" if is_agent1 else "Black Widow"
    
    # Create system message
    system_message = f"""
You are {agent_data['name']} from the {agent_data['universe']} universe.

Background: {agent_data['background']}

Your personality traits:
{chr(10).join(f"- {trait}" for trait in agent_data['personality_traits'])}

Your debate style:
{chr(10).join(f"- {style}" for style in agent_data['debate_style'])}

You are participating in a debate on the topic: "{prompt_data['topic']}"
Context: {prompt_data['context']}

Your position: {position}

Debate rules:
1. Maintain your character's voice and personality throughout.
2. Use humor and sarcasm in your responses.
3. Draw from your character's background and experiences.
4. Keep responses concise and impactful.
5. You are debating against {opponent}.
6. The debate will last for {DEBATE_ROUNDS} rounds.

Remember to stay in character at all times!
"""
    
    # Configure LLM settings based on provider
    if agent_data['provider'].lower() == 'openai':
        config = {
            "config_list": [{
                "model": agent_data['model'],
                "api_key": OPENAI_API_KEY,
                "temperature": agent_data['temperature'],
                "max_tokens": agent_data['max_tokens']
            }]
        }
    elif agent_data['provider'].lower() == 'anthropic':
        config = {
            "config_list": [{
                "model": agent_data['model'],
                "api_key": ANTHROPIC_API_KEY,
                "temperature": agent_data['temperature'],
                "max_tokens": agent_data['max_tokens']
            }]
        }
    else:
        raise ValueError(f"Unsupported provider: {agent_data['provider']}")
    
    return {
        "name": agent_data['name'],
        "system_message": system_message,
        "llm_config": config
    }

def save_debate(messages: List[Dict], filename: Optional[str] = None) -> str:
    """Save the debate to a file and return the filename."""
    if not filename:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"debate_{timestamp}.txt"
    
    # Create output directory if it doesn't exist
    if DEBATE_OUTPUT_PATH:
        os.makedirs(DEBATE_OUTPUT_PATH, exist_ok=True)
        filename = os.path.join(DEBATE_OUTPUT_PATH, filename)
    
    with open(filename, 'w') as f:
        f.write("=== AI AGENT DEBATE ===\n\n")
        for msg in messages:
            if msg.get('role') == 'system':
                continue
            f.write(f"[{msg.get('name', msg.get('role', 'unknown'))}]\n")
            f.write(f"{msg.get('content', '')}\n\n")
    
    print(f"Debate saved to {filename}")
    return filename

def main():
    """Main function to run the debate."""
    print("Loading agent configurations...")
    
    # Load agent configurations
    agent1_text = load_text_file(Path(__file__).parent / "agent1.txt")
    agent2_text = load_text_file(Path(__file__).parent / "agent2.txt")
    prompt_text = load_text_file(Path(__file__).parent / "initial_prompt.txt")
    
    # Parse configurations
    agent1_config = parse_agent_config(agent1_text)
    agent2_config = parse_agent_config(agent2_text)
    prompt_config = parse_prompt(prompt_text)
    
    # Override topic if provided
    if args.topic:
        prompt_config['topic'] = args.topic
    
    print(f"Debate topic: {prompt_config['topic']}")
    print(f"Number of rounds: {DEBATE_ROUNDS}")
    
    # Create agent configurations for AutoGen
    agent1_autogen_config = create_agent_config(agent1_config, prompt_config, True)
    agent2_autogen_config = create_agent_config(agent2_config, prompt_config, False)
    
    # Create the agents
    agent1 = autogen.ConversableAgent(
        name=agent1_autogen_config["name"],
        system_message=agent1_autogen_config["system_message"],
        llm_config=agent1_autogen_config["llm_config"],
        human_input_mode="NEVER"
    )
    
    agent2 = autogen.ConversableAgent(
        name=agent2_autogen_config["name"],
        system_message=agent2_autogen_config["system_message"],
        llm_config=agent2_autogen_config["llm_config"],
        human_input_mode="NEVER"
    )
    
    # Create a group chat with a custom termination function
    def is_termination_msg(message):
        """Check if we've reached the maximum number of rounds."""
        # Count the number of non-system messages
        message_count = sum(1 for msg in message["content"] if msg.get("role") != "system")
        # Each round consists of 2 messages (one from each agent)
        return message_count >= DEBATE_ROUNDS * 2
    
    # Create a group chat
    groupchat = autogen.GroupChat(
        agents=[agent1, agent2],
        messages=[],
        max_round=DEBATE_ROUNDS,
        speaker_selection_method="round_robin",
        allow_repeat_speaker=False,
    )
    
    # Create a group chat manager
    manager = autogen.GroupChatManager(
        groupchat=groupchat,
        llm_config=agent1_autogen_config["llm_config"],
        is_termination_msg=is_termination_msg
    )
    
    print("\nStarting debate...")
    print(f"{agent1.name} vs {agent2.name}")
    print("=" * 50)
    
    # Start the conversation with the debate topic
    initial_message = f"Welcome to our debate on: '{prompt_config['topic']}'. {agent1.name}, please start with your opening statement."
    
    # Run the debate
    agent1.initiate_chat(
        manager,
        message=initial_message
    )
    
    # Save the debate
    chat_history = agent1.chat_history
    save_debate(chat_history)
    
    print("Debate completed!")

if __name__ == "__main__":
    main()
