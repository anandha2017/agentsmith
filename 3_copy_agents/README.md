# Bank Content Review System

A browser-based application for managing content creation and reviews for UK regulated banks using LLM integration.

## Features

- Bank selection from a predefined list of UK regulated banks
- Content input form with description and word count limit
- Content generation via Copywriter agent
- Display and editing of generated content
- Selection of reviewer agents for feedback
- Display of reviewer feedback with option to edit
- Content regeneration incorporating selected feedback
- Support for multiple LLM providers (Claude, OpenAI, DeepSeek)

## Project Structure

- `public/` - Static assets (HTML, CSS, JS)
- `src/` - Server code, routes, and controllers
- `config/` - Configuration files including bank information
- `agents/` - Agent definition files for each reviewer role

## Prerequisites

- Node.js (v16 or higher)
- npm (v8 or higher)
- API keys for Claude, OpenAI, and/or DeepSeek

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   cd 3_copy_agents
   npm install
   ```
3. Create a `.env.local` file based on the `env.environment` template:
   ```bash
   cp env.environment env.local
   ```
4. Edit `env.local` and add your API keys

## Running the Application

### Development Mode

```bash
npm run dev
```

This will start the development server with hot reloading at http://localhost:3000

### Production Mode

```bash
npm start
```

This will start the server in production mode at http://localhost:3000 (or the port specified in your environment variables)

## API Routes

- `GET /api/banks` - Fetch list of available banks
- `POST /api/generate` - Generate content using Copywriter agent
- `POST /api/review` - Submit content for review to selected agents
- `POST /api/regenerate` - Regenerate content with selected feedback

## LLM Provider Configuration

The application supports three LLM providers:
- Claude (Anthropic)
- OpenAI
- DeepSeek

You can switch between providers by:
1. Setting the appropriate API keys in your `.env.local` file
2. Changing the `LLM_PROVIDER` environment variable to `claude`, `openai`, or `deepseek`
3. Using the provider toggle in the web interface

## Agent Configuration

Each agent is defined in a JSON file in the `agents/` directory with:

### Core Structure
- **name**: Department/team name
- **role**: Primary responsibility
- **framework**: Regulatory/industry frameworks applied
- **checks**: List of validation criteria
- **instructions**: Detailed review guidance
- **prompt_template**: LLM interaction template
- **metadata**: Review process information

### Validation Frameworks
Agents reference specific regulations:
- FCA/PRA guidelines
- ISO standards
- UK legislation
- Industry best practices

### Compliance Checks
Standardized validation criteria across:
- Regulatory compliance
- Risk management
- Customer protection
- Data security

### Metadata
- `last_reviewed`: ISO date of last review
- `review_frequency`: Days between reviews
- `responsible_officer`: C-level accountable party

### Example Agent Configuration
```json
{
    "name": "Compliance Department",
    "role": "Verify FCA/PRA regulatory adherence",
    "regulatory_framework": {
        "FCA": ["COBS 4.2", "PRIN 2.1"],
        "PRA": ["SS35/15"]
    },
    "checks": [
        "Risk warning prominence",
        "Fair balance assessment",
        "Regulated entity identification"
    ],
    "metadata": {
        "last_reviewed": "2025-03-01",
        "review_frequency": 30,
        "responsible_officer": "Chief Compliance Officer"
    }
}
```

### Review Workflows
1. Content generation → 2. Agent selection → 3. Parallel reviews → 
4. Feedback consolidation → 5. Final approval
