import React, { useState } from 'react';
 
function App() {
    const [inputText, setInputText] = useState('');
    const [translatedText, setTranslatedText] = useState('');
    const [language, setLanguage] = useState('en');
    const [detectedLanguage, setDetectedLanguage] = useState('');
 
    // Function to handle translation and language detection
    const translateText = async () => {
        const response = await fetch('/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: inputText, target_language: language }),
        });
 
        const data = await response.json();
        // Check if the response contains translated text and detected language
        if (data.translatedText) {
            setDetectedLanguage(data.detectedLanguage); // Set the detected language
            setTranslatedText(data.translatedText); // Set the translated text
        } else {
            setTranslatedText("Error in translation");
        }
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
<h2>Detected Language: {detectedLanguage}</h2>  {/* Display Detected Language */}
<h2>Translated Text:</h2>
<p id="translated-text">{translatedText}</p>
</div>
</div>
    );
}
 
export default App;
