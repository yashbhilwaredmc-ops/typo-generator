from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Your existing code
adjacent_keys = {
    'a': ['q', 'w', 's', 'z'],
    'b': ['v', 'g', 'h', 'n'],
    'c': ['x', 'd', 'f', 'v'],
    'd': ['s', 'e', 'r', 'f', 'c', 'x'],
    'e': ['w', 's', 'd', 'r'],
    'f': ['d', 'r', 't', 'g', 'v', 'c'],
    'g': ['f', 't', 'y', 'h', 'b', 'v'],
    'h': ['g', 'y', 'u', 'j', 'n', 'b'],
    'i': ['u', 'j', 'k', 'o'],
    'j': ['h', 'u', 'i', 'k', 'n', 'm'],
    'k': ['j', 'i', 'o', 'l', 'm'],
    'l': ['k', 'o', 'p'],
    'm': ['n', 'j', 'k'],
    'n': ['b', 'h', 'j', 'm'],
    'o': ['i', 'k', 'l', 'p'],
    'p': ['o', 'l'],
    'q': ['w', 'a'],
    'r': ['e', 'd', 'f', 't'],
    's': ['a', 'w', 'e', 'd', 'x', 'z'],
    't': ['r', 'f', 'g', 'y'],
    'u': ['y', 'h', 'j', 'i'],
    'v': ['c', 'f', 'g', 'b'],
    'w': ['q', 'a', 's', 'e'],
    'x': ['z', 's', 'd', 'c'],
    'y': ['t', 'g', 'h', 'u'],
    'z': ['a', 's', 'x']
}

def typo_variants(word):
    word = word.lower()
    variants = set()

    # Character omission
    for i in range(len(word)):
        variants.add(word[:i] + word[i+1:])

    # Character duplication
    for i in range(len(word)):
        variants.add(word[:i+1] + word[i] + word[i+1:])

    # Character transposition
    for i in range(len(word) - 1):
        swapped = list(word)
        swapped[i], swapped[i+1] = swapped[i+1], swapped[i]
        variants.add(''.join(swapped))

    # Keyboard adjacency substitution
    for i, char in enumerate(word):
        if char in adjacent_keys:
            for adj in adjacent_keys[char]:
                variants.add(word[:i] + adj + word[i+1:])

    return sorted(variants)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🔤 Typo Generator Tool</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Arial, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            .header p {
                opacity: 0.9;
                font-size: 1.1em;
            }
            .content {
                padding: 40px;
            }
            .input-group {
                margin-bottom: 30px;
            }
            label {
                display: block;
                margin-bottom: 10px;
                font-weight: 600;
                color: #333;
                font-size: 1.1em;
            }
            input[type="text"] {
                width: 100%;
                padding: 15px;
                border: 2px solid #e1e5e9;
                border-radius: 10px;
                font-size: 16px;
                transition: all 0.3s ease;
            }
            input[type="text"]:focus {
                outline: none;
                border-color: #4facfe;
                box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.1);
            }
            button {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                width: 100%;
            }
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            }
            .results {
                margin-top: 30px;
                display: none;
            }
            .results h3 {
                color: #333;
                margin-bottom: 15px;
                font-size: 1.3em;
            }
            .typo-list {
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                max-height: 400px;
                overflow-y: auto;
            }
            .typo-item {
                padding: 8px 12px;
                margin: 5px 0;
                background: white;
                border-radius: 6px;
                border-left: 4px solid #4facfe;
                font-family: 'Courier New', monospace;
            }
            .copy-btn {
                background: #28a745;
                margin-top: 15px;
                width: auto;
                padding: 10px 20px;
            }
            .stats {
                color: #666;
                font-style: italic;
                margin-bottom: 15px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔤 Typo Generator</h1>
                <p>Generate common typing mistakes for any keyword</p>
            </div>
            
            <div class="content">
                <div class="input-group">
                    <label for="keyword">Enter a keyword:</label>
                    <input type="text" id="keyword" placeholder="e.g., google, facebook, amazon" autofocus>
                </div>
                
                <button onclick="generateTypos()">Generate Typos</button>
                
                <div id="results" class="results">
                    <div class="stats" id="stats"></div>
                    <h3>Generated Variations:</h3>
                    <div class="typo-list" id="typoList"></div>
                    <button class="copy-btn" onclick="copyToClipboard()">📋 Copy All to Clipboard</button>
                </div>
            </div>
        </div>

        <script>
            function generateTypos() {
                const keyword = document.getElementById('keyword').value.trim();
                if (!keyword) {
                    alert('Please enter a keyword');
                    return;
                }

                fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ keyword: keyword })
                })
                .then(response => response.json())
                .then(data => {
                    const resultsDiv = document.getElementById('results');
                    const typoList = document.getElementById('typoList');
                    const stats = document.getElementById('stats');
                    
                    typoList.innerHTML = '';
                    stats.textContent = `Generated ${data.typos.length} variations for "${keyword}"`;
                    
                    data.typos.forEach(typo => {
                        const div = document.createElement('div');
                        div.className = 'typo-item';
                        div.textContent = typo;
                        typoList.appendChild(div);
                    });
                    
                    resultsDiv.style.display = 'block';
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error generating typos');
                });
            }

            function copyToClipboard() {
                const typoItems = document.querySelectorAll('.typo-item');
                const text = Array.from(typoItems).map(item => item.textContent).join('\\n');
                
                navigator.clipboard.writeText(text).then(() => {
                    alert('Copied to clipboard!');
                });
            }

            // Enter key support
            document.getElementById('keyword').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    generateTypos();
                }
            });
        </script>
    </body>
    </html>
    '''

@app.route('/generate', methods=['POST'])
def generate_typos():
    data = request.get_json()
    keyword = data.get('keyword', '')
    
    if not keyword:
        return jsonify({'error': 'No keyword provided'}), 400
    
    variations = typo_variants(keyword)
    
    return jsonify({
        'keyword': keyword,
        'typos': variations,
        'count': len(variations)
    })

if __name__ == '__main__':
    app.run(debug=True)
