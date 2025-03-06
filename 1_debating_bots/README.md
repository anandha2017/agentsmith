# Historical Scientists Debate Bot

This project creates a simulated debate between two historical scientists - Nikola Tesla and Hedy Lamarr - on the future of software development. The debate is conducted with a humorous and sarcastic tone, with each scientist maintaining their unique personality and historical perspective.

## Features

- Tesla is powered by OpenAI's API (GPT-4o-mini)
- Lamarr is powered by Anthropic's Claude API (Claude-3-haiku)
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
   pip3 install -r requirements.txt
   ```
   
   Or install dependencies directly:
   ```
   pip3 install python-dotenv openai anthropic
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
python3 debate_bot.py
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

## Troubleshooting

If you encounter errors when running the script, try the following:

- **ModuleNotFoundError: No module named 'dotenv'**: Make sure you've installed the python-dotenv package with `pip3 install python-dotenv`
- **ModuleNotFoundError: No module named 'openai'**: Install the OpenAI package with `pip3 install openai`
- **ModuleNotFoundError: No module named 'anthropic'**: Install the Anthropic package with `pip3 install anthropic`
- **API key errors**: Ensure your API keys in env.local are valid and correctly formatted

If you're using a system with multiple Python installations, make sure to use the correct Python command (`python3` instead of `python`) and the corresponding pip command (`pip3` instead of `pip`).

## Example Output

The debate generates a humorous and sarcastic conversation between Tesla and Lamarr, with each character maintaining their unique personality while discussing modern software development concepts. The output is saved to a timestamped file (e.g., `debate_20250306_152426.txt`) and also printed to the console in real-time.

## License

[Include your license information here]
