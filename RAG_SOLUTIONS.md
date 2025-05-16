# Solutions for Azure OpenAI Rate Limiting with Large PDFs

When uploading large PDF files (like your 800-page document) to LibreChat with Azure OpenAI embeddings, you may encounter rate limit errors due to the limitations of the S0 tier. This document provides two solutions to address this issue.

## Solution 1: Environment Variable Configuration

We've added several environment variables to the `.env` file to configure the OpenAI client and LangChain for better rate limiting handling:

```
# OpenAI Client Configuration for Rate Limiting
OPENAI_MAX_RETRIES=5
OPENAI_TIMEOUT=120
OPENAI_BATCH_SIZE=5
LANGCHAIN_TRACING=true
LANGCHAIN_PROJECT=librechat
LANGCHAIN_EMBEDDINGS_BATCH_SIZE=5

# Document Processing Configuration
DOCUMENT_CHUNK_SIZE=500
DOCUMENT_CHUNK_OVERLAP=50
DOCUMENT_BATCH_SIZE=5
```

These settings should help the RAG API handle large documents better by:
- Limiting batch sizes for embedding requests
- Adding retries with exponential backoff
- Increasing timeouts to allow for rate limit recovery
- Configuring smaller document chunks

After updating the `.env` file, we've restarted the RAG API service to apply these changes:

```bash
docker-compose restart rag_api
```

## Solution 2: Split Large PDFs Before Uploading

As an alternative solution, we've created a Python script (`split_pdf.py`) that splits large PDF files into smaller chunks before uploading them to LibreChat.

### Prerequisites

- Python 3.6 or higher
- PyPDF2 library (`pip install PyPDF2`)

### Usage

```bash
python split_pdf.py input.pdf --pages-per-chunk 50 --output-dir split_pdfs
```

This will split your large PDF into smaller PDFs with 50 pages each (you can adjust this number) and save them in the `split_pdfs` directory.

### Example

```bash
python split_pdf.py my_large_document.pdf --pages-per-chunk 40
```

This will create files like:
- `my_large_document_part_1.pdf` (pages 1-40)
- `my_large_document_part_2.pdf` (pages 41-80)
- And so on...

You can then upload these smaller PDFs to LibreChat one at a time, which should avoid hitting the rate limits.

## Recommended Approach

1. Try uploading your document with the new environment variable settings first.
2. If you still encounter rate limit errors, use the PDF splitting script to break your document into smaller chunks.
3. For very large documents (500+ pages), it's recommended to use the PDF splitting approach regardless, as it provides more control over the upload process.

## Troubleshooting

If you continue to experience rate limit errors:

1. Try reducing the `pages-per-chunk` value in the PDF splitting script (e.g., try 30 or 20 pages per chunk).
2. Increase the wait time between uploading each PDF chunk (e.g., wait 1-2 minutes between uploads).
3. Consider further adjusting the environment variables, particularly reducing `OPENAI_BATCH_SIZE` and `LANGCHAIN_EMBEDDINGS_BATCH_SIZE` to lower values.
