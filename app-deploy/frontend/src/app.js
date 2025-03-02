import React, { useState } from 'react';

function App() {
    const [inputText, setInputText] = useState('');
    const [translatedText, setTranslatedText] = useState('');
    const [language, setLanguage] = useState('en');

    // Function to handle translation
    const translateText = async () => {
        const response = await fetch(`/translate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: inputText, target_language: language }),
        });
        const data = await response.json();
        setTranslatedText(data.translatedText);
    };

    return (
        <div className="App">
            <h1>AI Translator</h1>

            <div>
                <textarea
                    id="input-text"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    placeholder="Enter text to translate"
                />
            </div>

            <div>
                <select
                    id="language-select"
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                >
                    <option value="en">English</option>
                    <option value="es">Spanish</option>
                    <option value="fr">French</option>
                    <option value="de">German</option>
                    {/* Add other languages as needed */}
                </select>
            </div>

            <button onClick={translateText}>Translate</button>

            <div>
                <h2>Translated Text:</h2>
                <p id="translated-text">{translatedText}</p>
            </div>
        </div>
    );
}

export default App;
