# Two-Agent Debate System

This project implements a debate system between two AI agents with distinct personalities using the AutoGen framework. The agents are configured to debate with humor and sarcasm, each taking on the persona of a superhero character.

## Features

- Two AI agents with distinct personalities (BlackWidow from Marvel and WonderWoman from DC)
- Configurable debate topics and number of rounds
- Humor and sarcasm-infused debates
- Easily modifiable agent personalities and LLM configurations
- Debate output saved to text files

## Prerequisites

- Python 3.8 or higher
- OpenAI API key (for gpt-4-mini)
- Anthropic API key (for Claude haiku)

## Installation

1. Clone this repository or navigate to the project directory.

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

### API Keys

1. Create a copy of `env.local` and rename it to `.env` (optional but recommended)
2. Add your API keys to the `.env` or `env.local` file:

```
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### Debate Configuration

You can modify the following configuration options in the `env.local` file:

- `DEBATE_ROUNDS`: Number of debate rounds (default: 3)
- `DEBATE_OUTPUT_PATH`: Directory to save debate outputs (optional)

### Agent Personalities

The agent personalities are defined in the following files:

- `agent1.txt`: Black Widow (Marvel) using gpt-4-mini
- `agent2.txt`: Wonder Woman (DC) using Claude haiku

You can modify these files to change the agent personalities, debate styles, or LLM configurations.

### Debate Topics

The initial debate topic and context are defined in `initial_prompt.txt`. You can modify this file to change the debate topic, context, or initial positions.

## Usage

Run the debate system with the default configuration:

```bash
python main.py
```

### Command Line Options

- `--topic`: Override the debate topic
- `--rounds`: Override the number of debate rounds
- `--output`: Specify an output file path for the debate

Example:

```bash
python main.py --topic "Is social media beneficial for society?" --rounds 5
```

## Customization

### Changing LLM Models

To use different LLM models, modify the `MODEL` field in the agent configuration files:

- For OpenAI models: Update the `MODEL` field in `agent1.txt`
- For Anthropic models: Update the `MODEL` field in `agent2.txt`

### Adding New Agents

To create new agent personalities:

1. Create a new agent configuration file (e.g., `agent3.txt`)
2. Follow the same format as the existing agent files
3. Modify the Python script to include the new agent

## Output

The debate will be saved to a text file in the current directory (or the specified output directory) with a timestamp in the filename, e.g., `debate_20250306_152426.txt`.

## Example

```
=== AI AGENT DEBATE ===

[Black Widow]
*adjusts microphone with a smirk* So, we're debating whether technology is making people smarter or dumber? Well, from what I've seen in my line of work, technology has created a generation of people who can't find their way home without GPS but think they're geniuses because they can Google the answer to trivia questions. I've infiltrated enough high-tech facilities to know that the same people developing "revolutionary" AI can't remember their own passwords. Stark might be the exception, but for every Tony Stark, there are millions scrolling mindlessly through cat videos while their critical thinking skills atrophy. Technology isn't enhancing intelligence—it's outsourcing it.

[Wonder Woman]
*smiles regally* How fascinating to hear such pessimism from someone whose team relies so heavily on Stark technology. *adjusts bracelet casually* In Themyscira, we've observed mankind for millennia, and I must say, this current technological revolution is quite remarkable. Yes, people may outsource memory to devices, but isn't that precisely what writing did thousands of years ago? The human mind is now free to solve greater problems. While you're concerned about people forgetting passwords, I'm witnessing children in remote villages accessing the knowledge of entire libraries through a single device. *with playful irony* Perhaps in your line of work, you only notice the weaknesses you can exploit rather than the potential being unlocked. Technology isn't making people dumber—it's elevating what humanity can achieve collectively.

...
```

## License

[MIT License](LICENSE)
