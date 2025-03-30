import React, { useState } from 'react'
import useRecommendationStore from '../stores/UseRecommendationStore'

const Recommendation  = () => {
  const [title, setTitle] = useState('')
  const {
    movieRecommendations,
    songRecommendations,
    message,
    loading,
    error,
    fetchRecommendations
  } = useRecommendationStore()

  const handleSubmit = (e) => {
    e.preventDefault()
    if (title.trim()) {
      fetchRecommendations(title)
    }
  }

  return (
    <div style={{ padding: '2rem' }}>
      <h1>🎬 Movie & 🎵 Song Recommender</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={title}
          placeholder="Enter movie title"
          onChange={(e) => setTitle(e.target.value)}
        />
        <button type="submit">Get Recommendations</button>
      </form>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {message && <p><strong>{message}</strong></p>}

      <div style={{ marginTop: '2rem' }}>
        <h2>🎬 Movie Recommendations</h2>
        <ul>
          {movieRecommendations.map((movie, idx) => (
            <li key={idx}>{movie}</li>
          ))}
        </ul>

        <h2>🎵 Song Recommendations</h2>
        <ul>
          {songRecommendations.map((song, idx) => (
            <li key={idx}>{song}</li>
          ))}
        </ul>
      </div>
    </div>
  )
}

export default Recommendation
