
import re

input_path = '/Users/guru/Melanoma Detection Using Convolutional Neural Network (CNN)/static/css/aos.css'

with open(input_path, 'r') as f:
    css = f.read()

# 1. Ensure basic spacing around braces and semicolons
# Add space before opening brace if missing, and newline after
css = css.replace('{', ' {\n')
# Add newline after semicolon
css = css.replace(';', ';\n')
# Add newline before closing brace, and two newlines after (to separate rules)
css = css.replace('}', '\n}\n\n')

# 2. Iterate line by line to handle indentation and selector lists
lines = css.split('\n')
output_lines = []
indent_level = 0

for line in lines:
    line = line.strip()
    if not line:
        continue
        
    # Decrease indent for closing brace
    if line.startswith('}'):
        indent_level = max(0, indent_level - 1)
        
    # Add comma separation for selectors if they are on the same line (heuristic)
    # But usually minified css has commas. We want `sel1, sel2 {` -> `sel1,\nsel2 {` ? 
    # Maybe just keeping them on one line or wrapping is fine. 
    # For now, let's just respect the brace indentation.
    
    # Indent the line
    current_indent = '  ' * indent_level
    output_lines.append(current_indent + line)
    
    # Increase indent for opening brace
    if line.endswith('{'):
        indent_level += 1

final_css = '\n'.join(output_lines)

# 3. Some cleanup
# Ensure proper spacing after colon
# Regex to match colon not followed by space, excluding inside quotes or urls if possible.
# Simple approximation: replace all ':' with ': ' then fix double spaces
final_css = final_css.replace(':', ': ')
final_css = final_css.replace('  ', ' ') # this might hurt indentation, wait.
# Actually, the indentation uses spaces. 
# Let's use a regex for the colon fix only.
final_css = re.sub(r':(?!\s)', ': ', final_css)

# Fix possible ':  '
final_css = final_css.replace(':  ', ': ')

# Re-establish indentation that might have been messed up (the previous step didn't mess indent because it's at start of line, but let's be careful)
# Actually, the previous step works on the whole string. 
# `  property: value` -> `  property: value` (nothing changes if space exists)
# `  property:value` -> `  property: value`
# `  ` (indent) -> `  ` (no colon)

# One specific fix for aos.css specific selectors like `[data-aos][data-aos]`
# The commas in selectors: `sel1,sel2 {` -> `sel1, sel2 {`
final_css = final_css.replace(',', ', ')
# Fix double spaces again if any created
final_css = final_css.replace('  ', ' ')
# Wait, replacing double space with single space might ruin indentation (2 spaces).
# Let's revert the double space fix and handle indentation separately.

# Rerun indentation logic on the cleaned string is safer.

# Redo the logic in a cleaner way:
lines = final_css.split('\n')
final_lines = []
indent_level = 0
for line in lines:
    line = line.strip()
    if not line:
        continue
    
    if line.startswith('}'):
        indent_level = max(0, indent_level - 1)
        
    final_lines.append(('  ' * indent_level) + line)
    
    if line.endswith('{'):
        indent_level += 1

final_css = '\n'.join(final_lines)

with open(input_path, 'w') as f:
    f.write(final_css)
