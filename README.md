# Agentic Data Generator

A Python command-line tool that generates synthetic CSV datasets
from sample data using OpenRouter.

The application first analyzes the sample dataset, then generates
new rows in batches and validates their row and column counts.

## Requirements

- Docker Desktop
- An OpenRouter API key
- A sample CSV containing a header row

## Setup

1. Clone this repository and open its directory.
2. Create a `.env` file containing:

   ```env
   OPENROUTER_API_KEY=your_key_here
   ```

3. Create an `app/data` directory and place your sample CSV inside it.

## Run with Docker

Build the image:

```powershell
docker build -t agentic-data-generator .
```

Run from the project directory in PowerShell:

```powershell
docker run --rm -it --env-file .env -v "${PWD}\app\data:/app/data" agentic-data-generator
```

Enter the CSV filename, including its extension, and the desired
number of generated rows when prompted.

The generated dataset is saved to `app/data/new_dataset.csv`.

## Project files

- `agents.py`: CSV handling, analysis, generation, and validation
- `prompts.py`: Instructions used for analysis and generation
- `Dockerfile`: Container configuration
- `requirements.txt`: Python dependencies
- `.env.example`: Required environment variable template

## Limitations

- Generated content should be reviewed before use.
- Validation checks CSV structure, not factual accuracy or uniqueness.
- Each run overwrites `new_dataset.csv`.
- Requests depend on OpenRouter model availability and rate limits.