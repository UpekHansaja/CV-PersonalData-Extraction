# CV Personal Data Extraction System

An intelligent system to extract personal information from bulk CVs (300+) using DeepSeek API and save the data to a CSV file.

## Features

- **Multi-format Support**: Processes PDF, DOCX, DOC, and TXT files
- **AI-Powered Extraction**: Uses DeepSeek API for accurate data extraction
- **Batch Processing**: Handles 300+ CVs efficiently with progress tracking
- **Comprehensive Data Extraction**: Extracts 13 key fields from each CV
- **Error Handling**: Robust error handling with detailed logging
- **CSV Export**: Automatic export to CSV with all extracted data

## Extracted Data Fields

1. **Name** - Full name of the candidate
2. **Email** - Email address
3. **Phone** - Mobile/Phone number
4. **Location** - City and Country
5. **LinkedIn** - LinkedIn profile URL
6. **GitHub** - GitHub profile URL
7. **Professional Summary** - Brief professional objective/summary
8. **Current Job Title** - Most recent job title
9. **Current Company** - Most recent/current employer
10. **Years Experience** - Total years of experience
11. **Education** - Highest degree obtained
12. **Institution** - University/School name
13. **Filename** - Source CV filename

## Prerequisites

- Python 3.8+
- DeepSeek API key
- CVs in PDF, DOCX, DOC, or TXT format

## Installation

1. **Clone/Navigate to the project**
```bash
cd CV-PersonalData-Extraction
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
```

4. **Add your DeepSeek API key to `.env`**
```
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

Get your API key from: https://platform.deepseek.com/

## Usage

### Method 1: Using Environment Variables

```bash
export CV_FOLDER_PATH="/path/to/your/cvs"
export OUTPUT_CSV_PATH="./extracted_data.csv"
python cv_extractor.py
```

### Method 2: Interactive Mode

```bash
python cv_extractor.py
# Enter the CV folder path when prompted
```

### Method 3: Direct Python Usage

```python
from cv_extractor import CVExtractor

# Initialize
extractor = CVExtractor()

# Process CVs
results = extractor.process_cv_folder("/path/to/cvs")

# Save to CSV
extractor.save_to_csv("output.csv")
```

## Example Output

The script generates a CSV file with the following structure:

| filename | name | email | phone | location | linkedin | github | professional_summary | current_job_title | current_company | years_experience | education | institution |
|----------|------|-------|-------|----------|----------|--------|----------------------|-------------------|-----------------|-------------------|-----------|-------------|
| cv1.pdf | John Doe | john@email.com | +1-555-0100 | New York, USA | linkedin.com/in/... | github.com/... | Experienced software engineer... | Senior Developer | Tech Corp | 8 | Bachelor | MIT |

## Configuration

### Environment Variables (.env)

```ini
# Required
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Optional
CV_FOLDER_PATH=/path/to/cvs  # Can be provided interactively
OUTPUT_CSV_PATH=./extracted_data.csv  # Default if not set
```

## Logging

The system generates two logs:
- **Console Output**: Real-time progress and status
- **cv_extraction.log**: Detailed logs for debugging

Example log output:
```
2025-01-06 10:30:45,123 - INFO - Found 300 CV files to process
2025-01-06 10:30:47,456 - INFO - Processing [1/300] cv_001.pdf
2025-01-06 10:30:52,789 - INFO - ✓ Extracted data from cv_001.pdf
2025-01-06 10:31:15,234 - INFO - Data saved to extracted_data.csv
2025-01-06 10:31:15,234 - INFO - Total records: 287
```

## Performance Notes

- **Processing Speed**: ~5-10 seconds per CV (depending on file size and API response time)
- **300 CVs**: ~25-50 minutes total
- **API Rate Limits**: Respectful of OpenAI API rate limits
- **Memory**: Efficient streaming of results, minimal memory footprint

## Error Handling

The system handles various errors gracefully:
- Unsupported file formats - Skipped with warning
- Corrupted files - Logged and skipped
- Extraction failures - Logged with details
- API errors - Logged with details
- Missing fields - Stored as null/empty in CSV

## Troubleshooting

### "DEEPSEEK_API_KEY environment variable not set"
- Ensure you've created `.env` file with your API key
- Run: `export DEEPSEEK_API_KEY=your_key_here`
- Verify your key is valid: https://platform.deepseek.com/

### "Folder not found"
- Verify the folder path is correct
- Use absolute paths: `/full/path/to/folder`

### "No CV files found"
- Check file extensions are: `.pdf`, `.docx`, `.doc`, `.txt`
- Ensure files are in the specified folder (not in subfolders)

### JSON parsing errors
- Some CVs may have unusual formatting
- These are logged; the process continues with other CVs
- Check `cv_extraction.log` for details

### "Invalid API key"
- Verify your OpenAI API key is correct
- Check key hasn't been revoked: https://platform.openai.com/api-keys
- Ensure sufficient API credits

## API Costs

This system uses DeepSeek API. Estimated costs:
- Average CV: ~2,000 tokens (input) + 150 tokens (output)
- 300 CVs: ~675,000 tokens total
- Cost: Significantly lower than OpenAI/Claude (typically 90% cheaper)
- Check [DeepSeek Pricing](https://platform.deepseek.com/pricing) for current rates

## Limitations

- Files larger than 4000 characters are truncated for processing
- Batch processing is sequential (not parallel) to respect API limits
- Some hand-written or scanned CVs may not extract well
- OCR is not included; PDFs must be text-based
- Requires active internet connection for API calls

## Future Enhancements

- [ ] Add parallel processing with rate limiting
- [ ] Include OCR for scanned documents
- [ ] Custom field extraction templates
- [ ] Data validation and deduplication
- [ ] Web UI for easier file upload
- [ ] Database export options (MongoDB, PostgreSQL)
- [ ] Skill extraction and categorization
- [ ] Support for multiple resume formats

## License

MIT

## Support

For issues or questions:
1. Check the README.md for detailed documentation
2. Review cv_extraction.log for error details
3. Verify your DeepSeek API key is valid
4. Ensure CV files are readable
5. Check [DeepSeek Documentation](https://platform.deepseek.com/docs) for API issues

