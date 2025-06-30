import React from "react";

"use client";

import { useEffect, useState } from "react";

export default function FrameGallery() {
  const [frames, setFrames] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchFrames = async () => {
      try {
        const res = await fetch("http://localhost:8000/frames-list");
        if (!res.ok) throw new Error("Failed to fetch frames");
        const data = await res.json();
        setFrames(data);
      } catch (err: any) {
        setError(err.message || "Something went wrong");
      } finally {
        setLoading(false);
      }
    };

    fetchFrames();
  }, []);

  return (
    <div style={{ padding: "20px", color: "#f2f2f2" }}>
      <h2 style={{ fontSize: "1.5rem", marginBottom: "1rem" }}>
        🖼 Extracted Frame Gallery
      </h2>

      {loading && <p>Loading frames...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "15px",
        }}
      >
        {frames.map((filename) => (
          <img
            key={filename}
            src={`http://localhost:8000/frames/${filename}`}
            alt={filename}
            style={{
              width: "200px",
              borderRadius: "12px",
              boxShadow: "0 0 10px rgba(0,0,0,0.5)",
              border: "1px solid #ccc",
            }}
          />
        ))}
      </div>
    </div>
  );
}
