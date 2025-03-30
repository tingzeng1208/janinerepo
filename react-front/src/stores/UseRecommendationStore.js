import { create } from 'zustand'
import axios from 'axios'

const useRecommendationStore = create((set) => ({
  recommendations: [],
  loading: false,
  error: null,

  fetchRecommendations: async (title) => {
    set({ loading: true, error: null })
    try {
      const res = await axios.post('http://localhost:5000/api/recommend', {
        title: title
      })
      const data = typeof res.data === "string" ? JSON.parse(res.data) : res.data
      set({ recommendations: data.recommendations, loading: false })
    } catch (err) {
      set({ error: err.message, loading: false })
    }
  }
}))

export default useRecommendationStore
