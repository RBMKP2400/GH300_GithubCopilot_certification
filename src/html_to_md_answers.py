import re
import html
import sys

def clean_html(raw_html):
    if not raw_html: return ""
    # Remove HTML tags
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    # Unescape HTML entities
    cleantext = html.unescape(cleantext)
    # Collapse whitespace
    cleantext = re.sub(r'\s+', ' ', cleantext).strip()
    return cleantext

def extract_answers(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []

    blocks = re.split(r'<div class="white-box review-answer".*?>', content, flags=re.DOTALL)
    
    answers = []
    
    # Skip the first block as it is content before the first match
    for i, block in enumerate(blocks[1:]):
        # 1. Extract Question Number
        q_num_match = re.search(r'Question\s+(\d+)', block, re.IGNORECASE)
        q_num = int(q_num_match.group(1)) if q_num_match else i + 1

        # 2. Extract Options and check for correctness
        ans_block_match = re.search(r'<div class="answer.*?">(.*?)</div>', block, re.DOTALL)
        
        correct_options = []
        
        if ans_block_match:
            li_matches = re.findall(r'<li(.*?)>(.*?)</li>', ans_block_match.group(1), re.DOTALL)
            
            for attrs, content in li_matches:
                # Check if this option is correct
                # Criteria: 'right' in class attribute OR '<span>right</span>' or '<span>correct</span>' in content
                is_correct = False
                if 'right' in attrs.lower(): # e.g. class="selected right"
                    is_correct = True
                
                # Check inner spans just in case
                if re.search(r'<span>(right|correct)</span>', content, re.IGNORECASE):
                    is_correct = True
                    
                if is_correct:
                    # Extract the letter (A., B., etc.)
                    # The content usually starts with "A. some text..."
                    clean_content = clean_html(content)
                    match_letter = re.match(r'^([A-Z])\.', clean_content)
                    if match_letter:
                        correct_options.append(match_letter.group(1))

        # Check fallback: "Correct Answer: X" in explanation
        if not correct_options:
            exp_match = re.search(r'Correct Answers?:\s*([A-Z](?:(?:,\s*|\s+and\s+)[A-Z])*)', block, re.IGNORECASE)
            if exp_match:
                # Parse "A, B and E" string
                content_str = exp_match.group(1).replace(' and ', ', ')
                chars = re.split(r',\s*', content_str)
                correct_options = [c.strip() for c in chars]

        correct_options.sort()
        answers.append({
            'number': q_num,
            'correct_choices': correct_options
        })

    # Sort by question number to be safe
    answers.sort(key=lambda x: x['number'])
    return answers

def to_markdown(answers):
    md_output = ""
    for ans in answers:
        if ans['correct_choices']:
            choices_str = ", ".join(ans['correct_choices'])
            md_output += f"{ans['number']}. {choices_str}\n"
        else:
            md_output += f"{ans['number']}. \n"
    return md_output

def main():
    input_file = "questions.html"
    output_file = "answers.md"
    
    print(f"Reading from {input_file}...")
    answers = extract_answers(input_file)
    
    if not answers:
        print("No answers found.")
        return

    print(f"Found {len(answers)} questions with answers.")
    
    markdown_content = to_markdown(answers)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
        
    print(f"Successfully exported to {output_file}")

if __name__ == "__main__":
    main()
