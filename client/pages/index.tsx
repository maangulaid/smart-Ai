import { useEffect, useState } from 'react';
import Link from 'next/link';

interface PredictionMap {
  [filename: string]: string;
}

export default function Home() {
  const [frames, setFrames] = useState<string[]>([]);
  const [predictions, setPredictions] = useState<PredictionMap>({});
  const [filter, setFilter] = useState<string>('All');
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [uploadInfo, setUploadInfo] = useState<string>('');

  const knownCategories = ['police car', 'construction', 'hazard', 'lane closure'];

  useEffect(() => {
    fetch('http://localhost:8000/frames-list')
      .then((res) => res.json())
      .then((data) => setFrames(data));

    fetch('http://localhost:8000/predictions')
      .then((res) => res.json())
      .then((data) => setPredictions(data));
  }, []);

  const handleUpload = async () => {
    if (!videoFile) return;

    const formData = new FormData();
    formData.append('file', videoFile);

    const response = await fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    setUploadInfo(`Uploaded: ${videoFile.name} (${videoFile.size} bytes)`);

    // Call /classify after upload
    await fetch('http://localhost:8000/classify', { method: 'POST' });

    // Refresh frames and predictions
    const [newFrames, newPreds] = await Promise.all([
      fetch('http://localhost:8000/frames-list').then(res => res.json()),
      fetch('http://localhost:8000/predictions').then(res => res.json())
    ]);

    setFrames(newFrames);
    setPredictions(newPreds);
  };

  const predictedLabels = Object.values(predictions);
  const availableCategories = new Set<string>();
  const otherCategories = new Set<string>();

  predictedLabels.forEach((label) => {
    if (knownCategories.includes(label.toLowerCase())) {
      availableCategories.add(label.toLowerCase());
    } else {
      otherCategories.add(label);
    }
  });

  const dropdownOptions = ['All', ...Array.from(availableCategories), 'Other'];

  const isFrameVisible = (filename: string): boolean => {
    const label = predictions[filename]?.toLowerCase();
    if (!label) return false;

    if (filter === 'All') return true;
    if (filter === 'Other') return !knownCategories.includes(label);
    return label === filter.toLowerCase();
  };

  return (
    <main style={{ background: '#111', minHeight: '100vh', color: 'white', padding: '2rem' }}>
      {/* Top nav bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 style={{ fontSize: '2rem' }}>📸 UrbanLens AI — Video Analysis</h1>
        <Link href="/LiveCCTVAnalyzer">
          <button style={{ padding: '0.5rem 1rem', background: '#0070f3', borderRadius: '6px', color: 'white' }}>
            🔍 Search by Area
          </button>
        </Link>
      </div>

      {/* Upload Section */}
      <section style={{ textAlign: 'center', marginTop: '3rem', marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>UrbanLens AI</h2>
        <p>Smart Video & Image Safety Analyzer</p>

        <input
          type="file"
          accept="video/*"
          onChange={(e) => setVideoFile(e.target.files?.[0] || null)}
          style={{
            marginTop: '1rem',
            padding: '0.5rem',
            background: '#000',
            color: 'white',
            borderRadius: '1rem',
          }}
        />
        <br />
        <button
          onClick={handleUpload}
          style={{
            marginTop: '1rem',
            padding: '0.5rem 1.5rem',
            background: 'transparent',
            border: '2px solid white',
            borderRadius: '1rem',
            color: 'white',
            cursor: 'pointer',
          }}
        >
          Analyze ▶
        </button>
        {uploadInfo && <p style={{ marginTop: '1rem', color: '#ccc' }}>{uploadInfo}</p>}
      </section>

      {/* Filter dropdown */}
      <div style={{ marginBottom: '1rem' }}>
        <label htmlFor="filter" style={{ marginRight: '1rem' }}>Filter by Category:</label>
        <select
          id="filter"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          style={{ padding: '0.5rem', borderRadius: '4px' }}
        >
          {dropdownOptions.map((option) => (
            <option key={option} value={option}>{option[0].toUpperCase() + option.slice(1)}</option>
          ))}
        </select>
      </div>

      {/* Frame grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '1rem' }}>
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
