import { useState } from 'react';

export default function LiveCCTVAnalyzer() {
  const [location, setLocation] = useState('');
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState<any>(null);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!location.trim()) {
      setError('Please enter a valid ZIP code or address.');
      return;
    }
    setError('');
    setLoading(true);
    setSummary(null);

    try {
      const res = await fetch('http://localhost:8000/analyze-location', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ location })
      });

      if (!res.ok) throw new Error('Failed to fetch analysis.');

      const data = await res.json();
      setSummary(data.summary);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ padding: '2rem', background: '#111', minHeight: '100vh', color: 'white' }}>
      <h1 style={{ fontSize: '2rem', marginBottom: '1rem' }}>🌐 Live CCTV Location Analyzer</h1>

      <div style={{ marginBottom: '1rem' }}>
        <input
          type="text"
          placeholder="Enter ZIP code or address"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          style={{ padding: '0.5rem', width: '300px', borderRadius: '4px' }}
        />
        <button
          onClick={handleAnalyze}
          style={{ marginLeft: '1rem', padding: '0.5rem 1rem', backgroundColor: '#444', color: 'white', border: 'none', borderRadius: '4px' }}
        >
          Analyze
        </button>
      </div>

      {loading && <p>Analyzing CCTV feeds...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {summary && (
        <div>
          <h2 style={{ marginTop: '2rem' }}>🛑 Road Issues Detected:</h2>
          <ul>
            {Object.entries(summary).map(([street, incidents]) => (
              <li key={street}>
                <strong>{street}:</strong> {Array.isArray(incidents) ? incidents.join(', ') : incidents}
              </li>
            ))}
          </ul>
        </div>
      )}
    </main>
  );
}
