import os
import sys
import openai

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_changes(changed_files):
    print("Starting analysis of changed files...")
    print(f"Changed files: {changed_files}")

    report = "Impact Analysis Report\n"
    report += "======================\n"
    
    for file in changed_files.split():
        report += f"Changes in {file}:\n"
        print(f"Analyzing file: {file}")

        try:
            with open(file, 'r') as f:
                lines = f.readlines()
            print(f"Read {len(lines)} lines from {file}")
        except FileNotFoundError:
            report += f"File {file} not found.\n\n"
            print(f"File not found: {file}")
            continue
        
        # Extract and analyze added lines
        added_lines = [line[1:] for line in lines if line.startswith('+') and not line.startswith('+++')]
        print(f"Found {len(added_lines)} added lines in {file}")

        for line in added_lines:
            print(f"Analyzing line: {line.strip()}")
            try:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=f"Explain the following code change for black-box testing:\n\n{line}",
                    max_tokens=50
                )
                explanation = response.choices[0].text.strip()
                report += f"Code: {line}\nExplanation: {explanation}\n\n"
                print(f"Generated explanation: {explanation}")
            except Exception as e:
                report += f"Error generating explanation for {line}: {str(e)}\n\n"
                print(f"Error generating explanation for {line}: {str(e)}")

    with open("impact_analysis_report.txt", "w") as report_file:
        report_file.write(report)
    print("Analysis complete. Report written to impact_analysis_report.txt")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_changes.py <changed_files>")
        sys.exit(1)
    changed_files = sys.argv[1]
    print(f"Received changed files: {changed_files}")
    analyze_changes(changed_files)