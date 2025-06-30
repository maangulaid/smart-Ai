import { useState } from 'react';

export default function LiveCCTVAnalyzer() {
  const [zipCode, setZipCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState<any>(null);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    if (!zipCode) {
      setError('Please enter a ZIP code');
      return;
    }

    setLoading(true);
    setError('');
    setSummary(null);

    try {
      const res = await fetch('http://localhost:8000/analyze-location', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ zip_code: zipCode })
      });

      const data = await res.json();
      setSummary(data);
    } catch (err) {
      console.error(err);
      setError('Failed to analyze location');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ padding: '2rem', background: '#111', minHeight: '100vh', color: 'white' }}>
      <h1 style={{ fontSize: '2rem', marginBottom: '1rem' }}>📍 Analyze Area by ZIP Code</h1>

      <div style={{ marginBottom: '1rem' }}>
        <input
          type="text"
          value={zipCode}
          onChange={(e) => setZipCode(e.target.value)}
          placeholder="Enter ZIP code"
          style={{ padding: '0.5rem', borderRadius: '4px', marginRight: '1rem' }}
        />
        <button
          onClick={handleSubmit}
          style={{ padding: '0.5rem 1rem', borderRadius: '4px', backgroundColor: '#0070f3', color: 'white', border: 'none' }}
        >
          Analyze
        </button>
      </div>

      {error && <p style={{ color: 'red' }}>{error}</p>}
      {loading && <p>Analyzing CCTV feeds around {zipCode}...</p>}

      {summary && (
        <div style={{ marginTop: '2rem' }}>
          <h2>🚨 Detected Situations</h2>
          {Object.keys(summary).length === 0 ? (
            <p>No major issues found in this area.</p>
          ) : (
            <ul>
              {Object.entries(summary).map(([location, details]: any) => (
                <li key={location} style={{ marginBottom: '1rem' }}>
                  <strong>{location}</strong>: {details.join(', ')}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </main>
  );
}
