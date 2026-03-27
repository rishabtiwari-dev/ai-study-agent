import { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!text.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const res = await fetch(
        "https://ai-study-agent-1.onrender.com/study",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ text }),
        }
      );

      const data = await res.json();
      setResult(data);
    } catch (err) {
      alert("⚠️ Something went wrong!");
    }

    setLoading(false);
  };

  // 🔥 Copy feature
  const copyText = (text) => {
    navigator.clipboard.writeText(text);
    alert("Copied!");
  };

  return (
    <div className="app">
      <div className="container">

        {/* TITLE */}
        <div className="title">
          <span>🚀</span>
          <h1>AI Study Assistant</h1>
        </div>

        {/* TEXTAREA */}
        <textarea
          placeholder="Paste your study text here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        {/* BUTTON */}
        <button onClick={handleSubmit} disabled={loading}>
          {loading ? "🤖 Thinking..." : "Generate"}
        </button>

        {/* 🔥 LOADING UI */}
        {loading && (
          <div className="loader">
            <div className="spinner"></div>
            <p>AI is analyzing your content...</p>
          </div>
        )}

        {/* RESULTS */}
        {result && (
          <div className="results">

            {/* SUMMARY */}
            <div className="card">
              <div className="card-header">
                <h2>📌 Summary</h2>
                <button onClick={() => copyText(result.summary)}>📋</button>
              </div>
              <p>{result.summary}</p>
            </div>

            {/* EXPLANATION */}
            <div className="card">
              <div className="card-header">
                <h2>💡 Explanation</h2>
                <button onClick={() => copyText(result.simple_explanation)}>📋</button>
              </div>
              <p>{result.simple_explanation}</p>
            </div>

            {/* QUIZ */}
            <div className="card">
              <h2>❓ Quiz</h2>
              <ul>
                {result.quiz_questions?.map((q, i) => (
                  <li key={i}>{q}</li>
                ))}
              </ul>
            </div>

          </div>
        )}

      </div>
    </div>
  );
}

export default App;