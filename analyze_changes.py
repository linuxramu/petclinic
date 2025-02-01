import os
import sys
import openai

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_changes(changed_files):
    report = "Impact Analysis Report\n"
    report += "======================\n"
    
    for file in changed_files.split():
        report += f"Changes in {file}:\n"
        with open(file, 'r') as f:
            lines = f.readlines()
        
        # Extract and analyze added lines
        added_lines = [line[1:] for line in lines if line.startswith('+') and not line.startswith('+++')]
        for line in added_lines:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Explain the following code change for black-box testing:\n\n{line}",
                max_tokens=50
            )
            explanation = response.choices[0].text.strip()
            report += f"Code: {line}\nExplanation: {explanation}\n\n"

    with open("impact_analysis_report.txt", "w") as report_file:
        report_file.write(report)

if __name__ == "__main__":
    changed_files = sys.argv[1]
    analyze_changes(changed_files)