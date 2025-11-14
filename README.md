# Apache Jira Scraper & JSONL Dataset Builder

This project is a web scraping + data transformation pipeline that collects public issue data from Apache Jira (for 3 projects: SPARK, HADOOP, KAFKA) and converts it into a clean, structured JSONL dataset suitable for LLM training.
It includes:
Reliable Jira scraping
Pagination handlin
Retry + timeout logic
Error handling for 429, 5xx
JSON → JSONL transformation
Task generation (summarization + classification)
Large dataset links (stored on Google Drive)
This repository contains the full code + documentation to reproduce the dataset.
