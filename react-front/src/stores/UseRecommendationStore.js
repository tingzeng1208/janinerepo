import { create } from 'zustand'
import axios from 'axios'

const useRecommendationStore = create((set) => ({
  movieRecommendations: [],
  songRecommendations: [],
  message: null,
  loading: false,
  error: null,

  fetchRecommendations: async (title) => {
    set({ loading: true, error: null, message: null })
    try {
      const res = await axios.post('http://localhost:5000/api/recommend', {
        title: title
      })

      console.log(res.data) // Log the response data
      const data = typeof res.data === "string" ? JSON.parse(res.data) : res.data

      set({
        movieRecommendations: data.recommendations || [],
        songRecommendations: data.songs || [],
        message: data.message || null,
        loading: false
      })
    } catch (err) {
      set({ error: err.message, loading: false })
    }
  }
}))

export default useRecommendationStore
