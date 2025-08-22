#!/usr/bin/env python3
"""
Simple web interface for the AI Password Generator
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from password_generator import PasswordGenerator


class PasswordHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.generator = PasswordGenerator()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/index.html':
            self.serve_html()
        elif self.path.startswith('/generate'):
            self.handle_generate()
        elif self.path.startswith('/analyze'):
            self.handle_analyze()
        else:
            self.send_error(404)
    
    def serve_html(self):
        """Serve the main HTML page"""
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Password Generator</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { background: #f5f5f5; padding: 20px; border-radius: 10px; margin: 10px 0; }
        .result { background: #e8f5e8; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .password { font-family: monospace; font-size: 18px; font-weight: bold; color: #2c5aa0; }
        .strength { font-weight: bold; }
        .strong { color: green; }
        .medium { color: orange; }
        .weak { color: red; }
        button { background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #45a049; }
        input, select { padding: 8px; margin: 5px; border: 1px solid #ddd; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>🔐 AI Password Generator</h1>
    
    <div class="container">
        <h2>Generate Password</h2>
        <form id="generateForm">
            <label>Pattern:</label>
            <select name="pattern">
                <option value="secure">Secure (16 chars, all types)</option>
                <option value="memorable">Memorable (words + numbers)</option>
                <option value="simple">Simple (8 chars, basic)</option>
                <option value="complex">Complex (20 chars, maximum security)</option>
            </select><br><br>
            
            <label>Count:</label>
            <input type="number" name="count" value="1" min="1" max="10"><br><br>
            
            <button type="submit">Generate Password</button>
        </form>
        <div id="generateResult"></div>
    </div>
    
    <div class="container">
        <h2>Analyze Password</h2>
        <form id="analyzeForm">
            <label>Password to analyze:</label><br>
            <input type="text" name="password" placeholder="Enter password to analyze" style="width: 300px;"><br><br>
            <button type="submit">Analyze Strength</button>
        </form>
        <div id="analyzeResult"></div>
    </div>

    <script>
        document.getElementById('generateForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(e.target);
            const params = new URLSearchParams(formData);
            
            fetch('/generate?' + params.toString())
                .then(response => response.json())
                .then(data => {
                    let html = '';
                    data.passwords.forEach((item, index) => {
                        html += `<div class="result">
                            <div>Password ${index + 1}: <span class="password">${item.password}</span></div>
                            <div class="strength ${item.analysis.strength.toLowerCase()}">
                                Strength: ${item.analysis.strength} (${item.analysis.score}/${item.analysis.max_score})
                            </div>
                        </div>`;
                    });
                    document.getElementById('generateResult').innerHTML = html;
                });
        });
        
        document.getElementById('analyzeForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(e.target);
            const params = new URLSearchParams(formData);
            
            fetch('/analyze?' + params.toString())
                .then(response => response.json())
                .then(data => {
                    let feedback = '';
                    if (data.feedback.length > 0) {
                        feedback = '<br>Suggestions:<ul>';
                        data.feedback.forEach(item => {
                            feedback += `<li>${item}</li>`;
                        });
                        feedback += '</ul>';
                    }
                    
                    document.getElementById('analyzeResult').innerHTML = `
                        <div class="result">
                            <div class="strength ${data.strength.toLowerCase()}">
                                Strength: ${data.strength} (${data.score}/${data.max_score})
                            </div>
                            ${feedback}
                        </div>`;
                });
        });
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def handle_generate(self):
        """Handle password generation"""
        try:
            query = urlparse(self.path).query
            params = parse_qs(query)
            
            pattern = params.get('pattern', ['secure'])[0]
            count = int(params.get('count', ['1'])[0])
            
            passwords = []
            for _ in range(min(count, 10)):  # Limit to 10 passwords
                password = self.generator.generate_pattern_password(pattern)
                analysis = self.generator.analyze_password_strength(password)
                passwords.append({
                    'password': password,
                    'analysis': analysis
                })
            
            response = {'passwords': passwords}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def handle_analyze(self):
        """Handle password analysis"""
        try:
            query = urlparse(self.path).query
            params = parse_qs(query)
            
            password = params.get('password', [''])[0]
            if not password:
                raise ValueError("No password provided")
            
            analysis = self.generator.analyze_password_strength(password)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(analysis).encode())
            
        except Exception as e:
            self.send_error(500, str(e))


def main():
    """Start the web server"""
    port = 8000
    server = HTTPServer(('localhost', port), PasswordHandler)
    print(f"🌐 AI Password Generator Web Interface")
    print(f"Server running at: http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
        server.shutdown()


if __name__ == "__main__":
    main()
