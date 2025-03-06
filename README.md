# Historical Scientists Debate Bot

This project creates a simulated debate between two historical scientists - Nikola Tesla and Hedy Lamarr - on the future of software development. The debate is conducted with a humorous and sarcastic tone, with each scientist maintaining their unique personality and historical perspective.

## Features

- Tesla is powered by OpenAI's API (GPT-4)
- Lamarr is powered by Anthropic's Claude API
- The debate runs for exactly 4 rounds to keep costs in check
- The conversation is saved to a timestamped text file
- Both scientists maintain humorous, sarcastic personas throughout the debate

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Anthropic API key

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your API keys:
   - Rename `env.enviornment` to `env.local` if you haven't already
   - Edit `env.local` and replace the placeholder values with your actual API keys:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     CLAUDE_API_KEY=your_claude_api_key_here
     ```

## Usage

Run the debate bot:

```
python debate_bot.py
```

The script will:
1. Start a 4-round debate between Tesla and Lamarr
2. Print each response to the console as it's generated
3. Save the complete conversation to a timestamped file (e.g., `debate_20250603_151145.txt`)

## Customization

You can modify the following aspects of the debate:

- **Personas**: Edit the `TESLA_SYSTEM_PROMPT` and `LAMARR_SYSTEM_PROMPT` variables in `debate_bot.py`
- **Debate Topic**: Change the `INITIAL_PROMPT` variable
- **Models**: Adjust the model names in the `get_tesla_response` and `get_lamarr_response` functions
- **Response Length**: Modify the `max_tokens` parameter in the API calls
- **Creativity**: Adjust the `temperature` parameter (higher values = more creative responses)

## Notes

- The debate is limited to 4 rounds to keep API costs reasonable
- Error handling is included to gracefully handle API failures
- The conversation is formatted for easy reading in the saved file

## License

[Include your license information here]
