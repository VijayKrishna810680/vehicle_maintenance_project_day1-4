import React, { useState } from 'react';

// Use environment variable for backend API URL
const API = process.env.REACT_APP_API_URL;

export default function Chat() {
  const [text, setText] = useState('');
  const [history, setHistory] = useState([]);

  async function send() {
    if (!text) return;

    const r = await fetch(API + '/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });

    const data = await r.json();

    setHistory(h => [...h, { you: text, bot: data.response }]);
    setText('');
  }

  return (
    <div>
      <div style={{ maxHeight: 300, overflow: 'auto', border: '1px solid #ddd', padding: 8 }}>
        {history.map((h, i) =>
          <div key={i}>
            <b>You:</b> {h.you}<br />
            <b>Bot:</b> {h.bot}
            <hr />
          </div>
        )}
      </div>
      <input
        value={text}
        onChange={e => setText(e.target.value)}
        style={{ width: '80%' }}
      />
      <button onClick={send}>Send</button>
    </div>
  );
}
