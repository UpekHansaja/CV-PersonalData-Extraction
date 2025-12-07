# QUICK START GUIDE

## 🚀 Get Started in 3 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure API Key
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your DeepSeek API key
# DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

Get your API key from: https://platform.deepseek.com/

### Step 3: Run the Extraction
```bash
python cv_extractor.py
```

When prompted, enter the full path to your CV folder:
```
Enter the path to the CV folder: /Users/yourname/Documents/cvs
```

## ✨ What Happens Next

1. The system scans the folder for CV files (PDF, DOCX, DOC, TXT)
2. For each CV, it:
   - Extracts the text content
   - Sends it to DeepSeek API for intelligent parsing
   - Extracts 13 key personal data fields
3. Saves all data to `extracted_data.csv`

## 📊 Output Example

You'll get a CSV file with columns like:
- filename, name, email, phone
- location, linkedin, github
- professional_summary, current_job_title
- current_company, years_experience
- education, institution

## ⚡ Performance

- **Per CV**: 5-10 seconds average
- **300 CVs**: ~25-50 minutes total
- **Real-time progress**: Console shows which CV is being processed
- **Cost-effective**: 90% cheaper than OpenAI/Claude

## 🔧 Advanced Usage

### Set Folder Path via Environment Variable
```bash
export CV_FOLDER_PATH="/path/to/cvs"
export OUTPUT_CSV_PATH="./results.csv"
python cv_extractor.py
```

### Use Python Directly
```python
from cv_extractor import CVExtractor

extractor = CVExtractor()
results = extractor.process_cv_folder("/path/to/cvs")
extractor.save_to_csv("output.csv")
```

## 📝 Logs

Check progress and errors in:
- **Console**: Real-time status
- **cv_extraction.log**: Detailed debug information

## ❓ Troubleshooting

**Q: "DEEPSEEK_API_KEY not set"**
A: Make sure your `.env` file has the key:
```bash
cat .env | grep DEEPSEEK_API_KEY
```

**Q: "No CV files found"**
A: Check your files are .pdf, .docx, .doc, or .txt in the specified folder

**Q: "JSON parsing error"**
A: Some CVs may be malformed. The system logs errors and continues with others.

**Q: How long will 300 CVs take?**
A: Approximately 25-50 minutes depending on file sizes and DeepSeek API response times.

**Q: How much will this cost?**
A: Significantly cheaper than OpenAI/Claude - typically 90% less expensive. Check [DeepSeek Pricing](https://platform.deepseek.com/pricing).

## 📞 Support

If you need help:
1. Check the README.md for detailed documentation
2. Review cv_extraction.log for error details
3. Verify your API key is valid at https://platform.deepseek.com/
4. Ensure CV files are readable

---

**Ready?** Run `python cv_extractor.py` and enter your CV folder path! 🎉

