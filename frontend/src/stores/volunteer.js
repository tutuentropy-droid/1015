import { defineStore } from 'pinia'
import { metaApi, collegeApi, predictApi } from '../api'

export const useVolunteerStore = defineStore('volunteer', {
  state: () => ({
    provinces: [],
    subjectCombinations: [],
    cities: [],
    majorDirections: [],
    categories: [],

    userInput: {
      province: '',
      score: 0,
      rank: 0,
      subject_combination: '',
      acceptable_cities: [],
      target_major_directions: [],
      accept_adjustment: true,
      volunteer_count: 10,
    },

    collegeList: [],
    collegeDetail: null,

    predictions: [],
    volunteerPlan: null,

    compareList: [],
    maxCompare: 5,

    loading: {
      meta: false,
      colleges: false,
      detail: false,
      predict: false,
      plan: false,
      pdf: false,
    },
  }),

  getters: {
    reachColleges: (state) => state.predictions.filter((p) => p.category === '冲'),
    stableColleges: (state) => state.predictions.filter((p) => p.category === '稳'),
    safeColleges: (state) => state.predictions.filter((p) => p.category === '保'),
    isInCompare: (state) => (id) => state.compareList.some((c) => c.id === id),
    compareCount: (state) => state.compareList.length,
  },

  actions: {
    async loadMeta() {
      if (this.provinces.length) return
      this.loading.meta = true
      try {
        const [p, s, c, m, cat] = await Promise.all([
          metaApi.getProvinces(),
          metaApi.getSubjectCombinations(),
          metaApi.getCities(),
          metaApi.getMajorDirections(),
          metaApi.getCategories(),
        ])
        this.provinces = p
        this.subjectCombinations = s
        this.cities = c
        this.majorDirections = m
        this.categories = cat
      } finally {
        this.loading.meta = false
      }
    },

    async fetchColleges(params = {}) {
      this.loading.colleges = true
      try {
        this.collegeList = await collegeApi.list(params)
      } finally {
        this.loading.colleges = false
      }
    },

    async fetchCollegeDetail(id) {
      this.loading.detail = true
      try {
        this.collegeDetail = await collegeApi.detail(id)
      } finally {
        this.loading.detail = false
      }
    },

    setUserInput(partial) {
      this.userInput = { ...this.userInput, ...partial }
    },

    resetUserInput() {
      this.userInput = {
        province: '',
        score: 0,
        rank: 0,
        subject_combination: '',
        acceptable_cities: [],
        target_major_directions: [],
        accept_adjustment: true,
        volunteer_count: 10,
      }
      this.predictions = []
      this.volunteerPlan = null
    },

    async predictColleges() {
      if (!this.userInput.province || !this.userInput.score || !this.userInput.rank) {
        throw new Error('请填写省份、分数和位次')
      }
      this.loading.predict = true
      try {
        this.predictions = await predictApi.predictColleges(this.userInput)
        return this.predictions
      } finally {
        this.loading.predict = false
      }
    },

    async generatePlan() {
      if (!this.userInput.province || !this.userInput.score || !this.userInput.rank) {
        throw new Error('请填写省份、分数和位次')
      }
      this.loading.plan = true
      try {
        this.volunteerPlan = await predictApi.generatePlan(this.userInput)
        return this.volunteerPlan
      } finally {
        this.loading.plan = false
      }
    },

    async exportPdf() {
      if (!this.volunteerPlan) return
      this.loading.pdf = true
      try {
        const res = await predictApi.exportPdf(this.volunteerPlan)
        const blob = new Blob([res.data], { type: 'application/pdf' })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `志愿填报方案_${this.userInput.province}_${this.userInput.score}分.pdf`
        link.click()
        window.URL.revokeObjectURL(url)
      } finally {
        this.loading.pdf = false
      }
    },

    addToCompare(college) {
      if (this.compareList.length >= this.maxCompare) {
        return { success: false, message: `最多对比${this.maxCompare}所院校` }
      }
      if (this.isInCompare(college.id)) {
        return { success: false, message: '该院校已在对比列表中' }
      }
      this.compareList.push(college)
      return { success: true, message: '已添加成功' }
    },

    removeFromCompare(id) {
      const idx = this.compareList.findIndex((c) => c.id === id)
      if (idx >= 0) {
        this.compareList.splice(idx, 1)
      }
    },

    clearCompare() {
      this.compareList = []
    },

    toggleCompare(college) {
      if (this.isInCompare(college.id)) {
        this.removeFromCompare(college.id)
        return { added: false, message: '已移除对比' }
      } else {
        return this.addToCompare(college)
      }
    },
  },
})
