import React, { useState } from 'react'
import useRecommendationStore from '../stores/UseRecommendationStore'

const Recommendation = () => {
  const [title, setTitle] = useState('')
  const { recommendations, fetchRecommendations, loading, error } = useRecommendationStore()

  const handleSubmit = (e) => {
    e.preventDefault()
    fetchRecommendations(title)
  }

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Movie Recommender</h1>
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

      <ul>
        {recommendations.map((movie, index) => (
          <li key={index}>{movie}</li>
        ))}
      </ul>
    </div>
  )
}

export default Recommendation
