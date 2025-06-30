import { useEffect, useState } from 'react';

interface PredictionMap {
  [filename: string]: string;
}

export default function Gallery() {
  const [frames, setFrames] = useState<string[]>([]);
  const [predictions, setPredictions] = useState<PredictionMap>({});
  const [filter, setFilter] = useState<string>('All');

  // Fetch data once
  useEffect(() => {
    fetch('http://localhost:8000/frames-list')
      .then((res) => res.json())
      .then((data) => setFrames(data));

    fetch('http://localhost:8000/predictions')
      .then((res) => res.json())
      .then((data) => setPredictions(data));
  }, []);

  // Dynamic dropdown options based on current predictions
  const labels = Object.values(predictions).map((l) => l.toLowerCase());
  const labelCount: Record<string, number> = {};

  labels.forEach((label) => {
    labelCount[label] = (labelCount[label] || 0) + 1;
  });

  // Show only common categories, collapse the rest into "Other"
  const sortedLabels = Object.entries(labelCount)
    .sort((a, b) => b[1] - a[1])
    .map(([label]) => label);

  const visibleOptions = sortedLabels.slice(0, 5);
  const dropdownOptions = ['All', ...visibleOptions, 'Other'];

  const isFrameVisible = (filename: string): boolean => {
    const label = predictions[filename]?.toLowerCase();
    if (!label) return false;
    if (filter === 'All') return true;
    if (filter === 'Other') return !visibleOptions.includes(label);
    return label === filter.toLowerCase();
  };

  return (
    <main style={{ background: '#111', minHeight: '100vh', color: 'white', padding: '2rem' }}>
      <h1 style={{ fontSize: '2rem', marginBottom: '1rem' }}>📸 Classified Frames</h1>

      {/* Dropdown Filter */}
      <div style={{ marginBottom: '1rem' }}>
        <label htmlFor="filter" style={{ marginRight: '1rem' }}>Filter by Category:</label>
        <select
          id="filter"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          style={{ padding: '0.5rem', borderRadius: '4px' }}
        >
          {dropdownOptions.map((option) => (
            <option key={option} value={option}>
              {option[0].toUpperCase() + option.slice(1)}
            </option>
          ))}
        </select>
      </div>

      {/* Gallery */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))',
        gap: '1rem'
      }}>
        {frames.filter(isFrameVisible).map((filename) => (
          <div key={filename} style={{ background: '#222', padding: '1rem', borderRadius: '8px' }}>
            <img
              src={`http://localhost:8000/frames/${filename}`}
              alt={filename}
              style={{ width: '100%', borderRadius: '4px' }}
            />
            <p style={{ marginTop: '0.5rem', fontSize: '0.9rem', color: '#ccc' }}>
              <strong>Prediction:</strong> {predictions[filename] || 'Loading...'}
            </p>
          </div>
        ))}
      </div>
    </main>
  );
}
