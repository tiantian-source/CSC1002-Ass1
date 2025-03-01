"""
CSC1002 - Console-Based Editor
Yitian Xu 124090767
"""

import re

"""Global variables"""
content = ""          # Current editor content
cursor_pos = 0        # Current cursor position (0-based index)
undo_stack = []       # Stack for undo operations (stores tuples of (content, cursor_pos))
last_valid_cmd = None # Last valid command for repeat (excluding undo/help)
show_cursor = False
pre_undo_cmd = None
pre_undo = False

"""ANSI escape codes for cursor highlighting"""
CURSOR_START = "\033[42m"
CURSOR_END = "\033[0m"

def save_state():
    """Save current state to undo stack"""
    global content, cursor_pos
    undo_stack.append((content, cursor_pos))
    
def show_help():
    """Display help menu"""
    help_text= """
? - display this help info
. - toggle row cursor on and off
h - move cursor left
l - move cursor right
^ - move cursor to beginning of the line
$ - move cursor to end of the line
w - move cursor to beginning of the next word
b - move cursor to beginning of previous word
i - insert <text> before cursor
a - append <text> after cursor
x - delete character at cursor
dw - delete word and tailing spaces at cursor
u - undo previous command
s - show content
q - quit program
"""
    print(help_text.strip())
    
def toggle_cursor():
    """Show cursor in green"""
    global show_cursor
    show_cursor = not show_cursor

def move_left(n=1):
    """Move cursor left by n characters"""
    global cursor_pos
    cursor_pos = max(0, cursor_pos - n)

def move_right(n=1):
    """Move cursor right by n characters"""
    global cursor_pos
    cursor_pos = min(len(content), cursor_pos + n)

def move_word_backward():
    """Move cursor to next word beginning"""
    global cursor_pos
        
    while cursor_pos <= len(content) and content[cursor_pos] != " ":
        cursor_pos += 1 
    while cursor_pos < len(content) and content[cursor_pos] == " ":
        cursor_pos += 1
      
def move_word_forward():
    """Move cursor to previous word beginning"""
    global cursor_pos
    
    """Find last word boundary before cursor"""
    if cursor_pos > 0 and content[cursor_pos - 1] == " ":
        cursor_pos -= 1
    while cursor_pos > 0 and content[cursor_pos - 1] != " ":
        cursor_pos -= 1
    while cursor_pos > 0 and content[cursor_pos - 1] == " ":
        cursor_pos -= 1
            
def execute_insert(text):
    """Insert text to the left of cursor"""
    global content, cursor_pos
    content = content[:cursor_pos] + text + content[cursor_pos:]
    cursor_pos = max(0, cursor_pos)
    """Cursor moves to start of inserted text"""

def execute_append(text):
    """Append text to the right of cursor"""
    global content, cursor_pos
    content = content[:cursor_pos+1] + text + content[cursor_pos+1:]
    cursor_pos += len(text) - 1

def delete_ch():
    global content,cursor_pos
    content = content[:cursor_pos] + content[cursor_pos+1:]
    
def delete_word():
    """Delete from cursor to next word or end"""
    global content, cursor_pos
    if cursor_pos >= len(content):
        return
    if cursor_pos >= len(content):
        return
    end = cursor_pos
    while end+1 < len(content) and content[end] == " " and content[end +1] == " ":
        end += 1
    while end < len(content) and re.match(r'\w', content[end]):
        end += 1
    while end < len(content) and re.match(r'[,.!?]', content[end]):
        end += 1
    while end < len(content) and content[end] == " ":
        end += 1
    content = content[:cursor_pos] + content[end:]




def handle_undo():
    """Undo last operation"""
    global content, cursor_pos, undo_stack,pre_undo_cmd,pre_undo
    if undo_stack:
        prev_state = undo_stack.pop()
        content, cursor_pos = prev_state
        pre_undo = True

def handle_repeat():
    """Repeat last valid command"""
    global last_valid_cmd, pre_undo_cmd,pre_undo
    target_cmd = pre_undo_cmd if pre_undo else last_valid_cmd
    if target_cmd and target_cmd not in ('u', '?','r',):
        parse_command(target_cmd)
        pre_undo = False

def show_content():
    """Show the present content"""
    global content
    return content

def display_content():
    """Display content with cursor highlighting"""
    if not content:
        return
    
    if cursor_pos >= len(content):
        if show_cursor:
            displayed = content + CURSOR_START + ' ' + CURSOR_END
        else:
            displayed = content 
    else:
        pre = content[:cursor_pos]
        if show_cursor :
            cur = CURSOR_START + content[cursor_pos] + CURSOR_END
        else:
            cur = content[cursor_pos]
        post = content[cursor_pos+1:]
        displayed = pre + cur + post
    print(displayed)
    
def parse_command(cmd):
    """Parse and execute user command"""
    global last_valid_cmd,pre_undo_cmd
    if cmd not in ('?',".",'h','l','^','$','w','b','dw','x','u','q','s','r') and  cmd[0]not in('i','a'):
        return True
    if cmd not in ('u', '?', 'r'):
        save_state()
    pre_undo_cmd = last_valid_cmd
    if cmd not in ('u','r'):
        last_valid_cmd = cmd         
           
    if cmd == "?":
        show_help()
        return False
    elif cmd == ".":
        toggle_cursor()
        return False
    elif cmd == "h":
        move_left()  
        return False
    elif cmd == "l":
        move_right() 
        return False
    elif cmd == "^":
        move_left(len(content))
        return False
    elif cmd == "$":
        move_right(len(content)-1)
        return False
    elif cmd == "w":
        move_word_backward()
        return False
    elif cmd == "b":
        move_word_forward()
        return False
    elif cmd[0] == "i":
        execute_insert(cmd[1:])
        return False
    elif cmd[0] == "a":
        execute_append(cmd[1:])
        return False
    elif cmd == "x":
        delete_ch()  
        return False
    elif cmd == "dw":
        delete_word()
        return False
    elif cmd == "u":
        handle_undo()
        return False
    elif cmd == "r":
        handle_repeat()
        return False
    elif cmd == "s":
        show_content()
        return False
    elif cmd == "q":
        None
        return False
    
        
def main():
    """Main program loop"""
    global last_valid_cmd
    while True:
        try:
            cmd = input(">")
            if not cmd:
                continue
                   
            if cmd == 'q':
                break
                
            if parse_command(cmd) == True:
                """Invalid command"""
                continue
                
            if cmd not in ('?', 'q'):
                display_content()
                
        except EOFError:
            break

if __name__ == "__main__":
    main()
