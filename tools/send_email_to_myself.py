#!/usr/bin/env python3
import os
import re
import smtplib
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

CSS_STYLES = """
<style>
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f6f8fa; color: #24292f; line-height: 1.6; }
h1 { color: #1f2328; font-size: 24px; border-bottom: 1px solid #d0d7de; padding-bottom: 12px; margin-top: 0; }
h2 { color: #1f2328; font-size: 20px; margin-top: 32px; padding-bottom: 8px; border-bottom: 1px solid #d0d7de; }
h3 { color: #1f2328; font-size: 16px; margin-top: 24px; }
p { margin: 12px 0; }
table { border-collapse: collapse; width: 100%; margin: 16px 0; font-size: 14px; }
th, td { border: 1px solid #d0d7de; padding: 10px 12px; text-align: left; }
th { background: #f6f8fa; font-weight: 600; }
tr:nth-child(even) { background: #f6f8fa; }
code { background: #f6f8fa; padding: 2px 6px; border-radius: 4px; font-size: 13px; }
pre { background: #f6f8fa; padding: 16px; border-radius: 6px; overflow-x: auto; }
blockquote { border-left: 4px solid #0969da; margin: 16px 0; padding-left: 16px; color: #57606a; }
a { color: #0969da; text-decoration: none; }
a:hover { text-decoration: underline; }
hr { border: none; border-top: 1px solid #d0d7de; margin: 24px 0; }
ul, ol { padding-left: 24px; }
li { margin: 4px 0; }
strong { color: #1f2328; }
.metadata { color: #57606a; font-size: 14px; margin-bottom: 20px; }
</style>
"""

def load_dotenv():
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        env_file = parent / ".env"
        if env_file.exists():
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k, v = k.strip(), v.strip().strip('"\'')
                    if k and k not in os.environ:
                        os.environ[k] = v
            break

def md_to_html(md_content, title=None, css=None):
    # Protect fenced code blocks from markdown transformation
    code_blocks = []
    def stash_code_block(match):
        lang = match.group(1) or ""
        code = match.group(2)
        code = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        placeholder = f"\x00CODEBLOCK{len(code_blocks)}\x00"
        code_blocks.append(f'<pre><code class="language-{lang}">{code}</code></pre>' if lang else f'<pre><code>{code}</code></pre>')
        return placeholder

    html = re.sub(r'```(\w*)\n(.*?)```', stash_code_block, md_content, flags=re.DOTALL)

    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)

    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', html)

    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)

    html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*</li>\n?)+', r'<ul>\g<0></ul>\n', html)

    html = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)

    html = re.sub(r'^---$', r'<hr>', html, flags=re.MULTILINE)

    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

    def convert_table(match):
        table_content = match.group(0)
        lines = table_content.strip().split('\n')
        html_table = '<table>\n'
        for i, line in enumerate(lines):
            if re.match(r'^[\|\-\:\s]+$', line):
                continue
            cells = [c.strip() for c in line.split('|')]
            cells = [c for c in cells if c]  # drop empty from leading/trailing |
            if not cells:
                continue
            tag = 'th' if i == 0 else 'td'
            row = ''.join(f'<{tag}>{c}</{tag}>' for c in cells)
            html_table += f'<tr>{row}</tr>\n'
        html_table += '</table>'
        return html_table

    html = re.sub(r'(\|.+\|\n)+', convert_table, html)

    html = re.sub(r'\n\n', '</p><p>', html)
    html = '<p>' + html + '</p>'
    html = re.sub(r'<p>(<h[123]>.*?</h[123]>)</p>', r'\1', html, flags=re.DOTALL)
    html = re.sub(r'<p>(<ul>.*?</ul>)</p>', r'\1', html, flags=re.DOTALL)
    html = re.sub(r'<p>(<table>.*?</table>)</p>', r'\1', html, flags=re.DOTALL)
    html = re.sub(r'<p>(<hr>)</p>', r'\1', html)

    # Restore code blocks
    for i, block in enumerate(code_blocks):
        html = html.replace(f"\x00CODEBLOCK{i}\x00", block)
    
    title_html = f'<title>{title}</title>' if title else ''
    css_html = css if css else CSS_STYLES
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{title_html}
{css_html}
</head>
<body>
{html}
</body>
</html>"""

def send_email(subject, body, to_addr=None, cc_addr=None, is_html=False):
    load_dotenv()
    
    username = os.getenv("GMAIL_USERNAME")
    password = os.getenv("GMAIL_APP_PASSWORD")
    if not to_addr:
        to_addr = os.getenv("GMAIL_RECIPIENTS", "<your-email>")
    
    if not username or not password:
        print("Error: GMAIL_USERNAME and GMAIL_APP_PASSWORD must be set in .env")
        return False

    msg = MIMEMultipart("alternative")
    msg["From"] = username
    msg["To"] = to_addr
    if cc_addr:
        msg["Cc"] = cc_addr
    
    msg["Subject"] = subject
    if is_html:
        msg.attach(MIMEText(body, "html", "utf-8"))
    else:
        msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(username, password)
            recipients = [to_addr]
            if cc_addr:
                recipients.append(cc_addr)
            server.send_message(msg, username, recipients)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send an email to myself using Gmail.")
    parser.add_argument("subject", help="Email subject")
    parser.add_argument("body", help="Email body (or use --file)")
    parser.add_argument("--to", help="Recipient email address (default: GMAIL_RECIPIENTS env var)")
    parser.add_argument("--cc", help="CC email address (optional)", default="")
    parser.add_argument("--html", action="store_true", help="Send body as HTML")
    parser.add_argument("--file", "-f", help="Read body from file (markdown will be converted to HTML)")
    parser.add_argument("--css", help="Path to custom CSS file for HTML styling")
    args = parser.parse_args()
    
    css_styles = CSS_STYLES
    if args.css and Path(args.css).exists():
        with open(args.css, "r", encoding="utf-8") as f:
            css_styles = f"<style>{f.read()}</style>"
    
    body = args.body
    is_html = args.html
    
    if args.file:
        file_path = Path(args.file)
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            if file_path.suffix.lower() == ".md":
                body = md_to_html(content, title=args.subject, css=css_styles)
                is_html = True
            else:
                body = content
        else:
            print(f"Error: File not found: {args.file}")
    
    if send_email(args.subject, body, args.to, args.cc, is_html):
        print("Email sent successfully!")
    else:
        exit(1)
