import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.response.use(
  (res) => res.data,
  (err) => {
    console.error('[API Error]', err)
    return Promise.reject(err)
  }
)

export const metaApi = {
  getProvinces: () => api.get('/meta/provinces'),
  getSubjectCombinations: () => api.get('/meta/subject-combinations'),
  getCities: () => api.get('/meta/cities'),
  getMajorDirections: () => api.get('/meta/major-directions'),
  getCategories: () => api.get('/meta/categories'),
  getNewGaokaoProvinces: () => api.get('/meta/new-gaokao-provinces'),
  getAllSubjects: () => api.get('/meta/all-subjects'),
}

export const collegeApi = {
  list: (params = {}) => api.get('/colleges', { params }),
  detail: (id) => api.get(`/colleges/${id}`),
}

export const predictApi = {
  predictColleges: (userInput) => api.post('/predict/colleges', userInput),
  generatePlan: (userInput) => api.post('/plan/generate', userInput),
  exportPdf: (plan) =>
    axios.post('/api/plan/export-pdf', plan, {
      responseType: 'blob',
      timeout: 30000,
    }),
}

export const subjectApi = {
  analyze: (data) => api.post('/subject/analyze', data),
  compare: (data) => api.post('/subject/compare', data),
  getRequirement: (majorName, province) =>
    api.get(`/subject/requirement/${encodeURIComponent(majorName)}`, { params: { province } }),
}

export const majorApi = {
  list: (params = {}) => api.get('/majors', { params }),
  detail: (majorName) => api.get(`/majors/${encodeURIComponent(majorName)}`),
  compare: (majorNames) => api.post('/majors/compare', majorNames),
}

export default api
