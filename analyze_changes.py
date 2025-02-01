import os
import sys
import subprocess
import openai

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_changed_lines(file):
    """Get the changed lines in a file using git diff."""
    try:
        result = subprocess.run(
            ["git", "diff", "HEAD^", "HEAD", "--", file],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error getting diff for {file}: {e}")
        return ""

def analyze_changes(changed_files):
    print("Starting analysis of changed files...")
    print(f"Changed files: {changed_files}")

    report = "Impact Analysis Report\n"
    report += "======================\n"
    
    for file in changed_files.split():
        report += f"Changes in {file}:\n"
        print(f"Analyzing file: {file}")

        changed_lines = get_changed_lines(file)
        if not changed_lines:
            report += f"No changes found in {file}.\n\n"
            print(f"No changes found in {file}.")
            continue
        
        print(f"Changed lines in {file}:\n{changed_lines}")

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    # {"role": "system", "content": "You are an assistant that explains code changes for black-box testing."},
                    {"role": "user", "content": f"Explain the impact of the following code changes for black-box testing:\n\n{changed_lines}"}
                ],
                max_tokens=150
            )
            explanation = response.choices[0].message['content'].strip()
            report += f"Changed Lines:\n{changed_lines}\nExplanation:\n{explanation}\n\n"
            print(f"Generated explanation: {explanation}")
        except Exception as e:
            report += f"Error generating explanation for changes in {file}: {str(e)}\n\n"
            print(f"Error generating explanation for changes in {file}: {str(e)}")

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