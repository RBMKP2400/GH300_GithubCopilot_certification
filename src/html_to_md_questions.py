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

def extract_questions(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []

    # Use regex split with capturing parentheses to keep the delimiter (the div tag)
    # This allows us to extract attributes from the div
    parts = re.split(r'(<div class="white-box review-answer"[^>]*?>)', content, flags=re.DOTALL)
    
    questions = []
    
    # The split results in [preamble, tag, content, tag, content, ...]
    # We iterate over the pairs of tag and content
    for i in range(1, len(parts), 2):
        tag = parts[i]
        block = parts[i+1]

        # 0. Extract Domain
        domain_match = re.search(r'data-domain="([^"]*)"', tag)
        domain = domain_match.group(1) if domain_match else "Unknown Domain"

        # 1. Extract Question Number
        q_num_match = re.search(r'Question\s+(\d+)', block, re.IGNORECASE)
        # Use loop index // 2 + 1 for fallback numbering since i jumps by 2
        block_index = (i - 1) // 2
        q_num = q_num_match.group(1) if q_num_match else f"Unknown-{block_index+1}"

        # 2. Extract Question Text
        que_block_match = re.search(r'<div class="que">(.*?)</div>', block, re.DOTALL)
        q_text = "No question text found"
        if que_block_match:
            raw_que = que_block_match.group(1)
            # Remove the domain/category span which is inside the que block
            raw_que = re.sub(r'<span class="que-category">.*?</span>', '', raw_que, flags=re.DOTALL)
            q_text = clean_html(raw_que)

        # 3. Extract Options
        options = []
        ans_block_match = re.search(r'<div class="answer\s*">(.*?)</div>', block, re.DOTALL)
        if ans_block_match:
            # Find all content inside <li> tags
            li_matches = re.findall(r'<li.*?>(.*?)</li>', ans_block_match.group(1), re.DOTALL)
            
            for li_content in li_matches:
                # Remove span content entirely if it's just "right" or similar markers
                li_content = re.sub(r'<span>(right|correct)</span>', '', li_content, flags=re.IGNORECASE)
                li_content = re.sub(r'<span.*?>.*?</span>', '', li_content, flags=re.DOTALL) 
                
                opt_text = clean_html(li_content)
                if opt_text:
                    options.append(opt_text)

        questions.append({
            'domain': domain,
            'number': q_num,
            'text': q_text,
            'options': options
        })

    return questions

def to_markdown(questions):
    md_output = ""
    for q in questions:
        md_output += f"### Domain: {q['domain']}\n"
        md_output += f"### Question {q['number']}: {q['text']}\n"
        for opt in q['options']:
            md_output += f"#### [ ] {opt}\n"
        md_output += "\n"
    return md_output

def main():
    input_file = "questions.html"
    output_file = "questions.md"
    
    print(f"Reading from {input_file}...")
    questions = extract_questions(input_file)
    
    if not questions:
        print("No questions found.")
        return

    print(f"Found {len(questions)} questions.")
    
    markdown_content = to_markdown(questions)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
        
    print(f"Successfully exported to {output_file}")

if __name__ == "__main__":
    main()