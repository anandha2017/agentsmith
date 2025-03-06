# Project Requirements Summary

This document summarizes the requirements for the Two-Agent Debate System project.

## Core Requirements

1. **Environment Setup**
   - Create an `env.local` file for API keys
   - Support for OpenAI and Anthropic API keys
   - Make LLM configurations easily modifiable for future updates

2. **Agent Personalities**
   - Create `agent1.txt` for a female Marvel character (Black Widow)
     - Tie this agent to gpt-4-mini OpenAI LLM
   - Create `agent2.txt` for a female DC character (Wonder Woman)
     - Tie this agent to Claude haiku LLM
   - Ensure both agent configurations are easily modifiable

3. **Debate Configuration**
   - Cap the debate at 3 rounds by default
   - Make the number of rounds configurable
   - Create an initial prompt in a separate file (`initial_prompt.txt`)
   - Set the debate style to humor and sarcasm

4. **Implementation**
   - Write the Python code under the `2_debating_agents` directory
   - Use the AutoGen framework for agent implementation
   - Create a README.md file with execution instructions

## Additional Details

- **Agent 1 (Black Widow)**
  - Marvel Universe character
  - Uses OpenAI's gpt-4-mini model
  - Personality traits include dry wit, intelligence, and pragmatism

- **Agent 2 (Wonder Woman)**
  - DC Universe character
  - Uses Anthropic's Claude haiku model
  - Personality traits include nobility, wisdom, and diplomatic skills

- **Debate Format**
  - Initial topic: "Is technology making people smarter or dumber?"
  - Black Widow argues technology makes people less capable
  - Wonder Woman argues technology expands human potential
  - Debate style emphasizes humor and sarcasm
  - Each agent has 3 turns by default (configurable)

- **Technical Implementation**
  - Python script loads configurations from text files
  - Uses AutoGen's ConversableAgent and GroupChat
  - Saves debate output to a text file
  - Command-line options for overriding topic and rounds

## File Structure

```
2_debating_agents/
├── env.local              # API keys and configuration
├── agent1.txt             # Black Widow personality (Marvel, gpt-4-mini)
├── agent2.txt             # Wonder Woman personality (DC, Claude haiku)
├── initial_prompt.txt     # Debate topic and context
├── main.py                # Python implementation
├── README.md              # Execution instructions
└── memory.md              # This summary file
```

This project creates a humorous and sarcastic debate between two superheroines from rival universes, with easily modifiable configurations for personalities, topics, and LLM settings.
