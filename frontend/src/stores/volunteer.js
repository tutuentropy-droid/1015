import { defineStore } from 'pinia'
import { metaApi, collegeApi, predictApi, subjectApi, majorApi } from '../api'

export const useVolunteerStore = defineStore('volunteer', {
  state: () => ({
    provinces: [],
    subjectCombinations: [],
    cities: [],
    majorDirections: [],
    categories: [],
    allSubjects: [],
    newGaokaoProvinces: [],

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

    subjectAnalysisResult: null,
    subjectCompareResult: null,
    favoriteColleges: [],

    majorList: [],
    majorCompareList: [],
    maxMajorCompare: 3,
    majorCompareResult: null,

    loading: {
      meta: false,
      colleges: false,
      detail: false,
      predict: false,
      plan: false,
      pdf: false,
      subjectAnalysis: false,
      subjectCompare: false,
      majors: false,
      majorCompare: false,
    },
  }),

  getters: {
    reachColleges: (state) => state.predictions.filter((p) => p.category === '冲'),
    stableColleges: (state) => state.predictions.filter((p) => p.category === '稳'),
    safeColleges: (state) => state.predictions.filter((p) => p.category === '保'),
    isInCompare: (state) => (id) => state.compareList.some((c) => c.id === id),
    compareCount: (state) => state.compareList.length,
    isFavorite: (state) => (id) => state.favoriteColleges.some((c) => c.id === id),
    favoriteCount: (state) => state.favoriteColleges.length,
    isMajorInCompare: (state) => (name) => state.majorCompareList.some((m) => m.name === name),
    majorCompareCount: (state) => state.majorCompareList.length,
  },

  actions: {
    async loadMeta() {
      if (this.provinces.length) return
      this.loading.meta = true
      try {
        const [p, s, c, m, cat, subs, ngp] = await Promise.all([
          metaApi.getProvinces(),
          metaApi.getSubjectCombinations(),
          metaApi.getCities(),
          metaApi.getMajorDirections(),
          metaApi.getCategories(),
          metaApi.getAllSubjects(),
          metaApi.getNewGaokaoProvinces(),
        ])
        this.provinces = p
        this.subjectCombinations = s
        this.cities = c
        this.majorDirections = m
        this.categories = cat
        this.allSubjects = subs
        this.newGaokaoProvinces = ngp
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

    async analyzeSubjects(subjects, province, collegeIds = []) {
      this.loading.subjectAnalysis = true
      try {
        this.subjectAnalysisResult = await subjectApi.analyze({
          subjects,
          province,
          college_ids: collegeIds,
        })
        return this.subjectAnalysisResult
      } finally {
        this.loading.subjectAnalysis = false
      }
    },

    async compareSubjectCombinations(combinations, province, collegeIds = []) {
      this.loading.subjectCompare = true
      try {
        this.subjectCompareResult = await subjectApi.compare({
          combinations,
          province,
          college_ids: collegeIds,
        })
        return this.subjectCompareResult
      } finally {
        this.loading.subjectCompare = false
      }
    },

    toggleFavorite(college) {
      if (this.isFavorite(college.id)) {
        this.removeFavorite(college.id)
        return { added: false, message: '已取消收藏' }
      } else {
        this.favoriteColleges.push(college)
        return { added: true, message: '已加入收藏' }
      }
    },

    removeFavorite(id) {
      const idx = this.favoriteColleges.findIndex((c) => c.id === id)
      if (idx >= 0) {
        this.favoriteColleges.splice(idx, 1)
      }
    },

    async fetchMajors(params = {}) {
      if (this.majorList.length) return this.majorList
      this.loading.majors = true
      try {
        this.majorList = await majorApi.list(params)
        return this.majorList
      } finally {
        this.loading.majors = false
      }
    },

    addMajorToCompare(major) {
      if (this.majorCompareList.length >= this.maxMajorCompare) {
        return { success: false, message: `最多对比${this.maxMajorCompare}个专业` }
      }
      if (this.isMajorInCompare(major.name)) {
        return { success: false, message: '该专业已在对比列表中' }
      }
      this.majorCompareList.push(major)
      return { success: true, message: '已添加成功' }
    },

    removeMajorFromCompare(majorName) {
      const idx = this.majorCompareList.findIndex((m) => m.name === majorName)
      if (idx >= 0) {
        this.majorCompareList.splice(idx, 1)
      }
    },

    clearMajorCompare() {
      this.majorCompareList = []
      this.majorCompareResult = null
    },

    toggleMajorCompare(major) {
      if (this.isMajorInCompare(major.name)) {
        this.removeMajorFromCompare(major.name)
        return { added: false, message: '已移除对比' }
      } else {
        return this.addMajorToCompare(major)
      }
    },

    async compareMajors() {
      if (this.majorCompareList.length < 2) {
        throw new Error('请至少选择 2 个专业')
      }
      this.loading.majorCompare = true
      try {
        const names = this.majorCompareList.map((m) => m.name)
        this.majorCompareResult = await majorApi.compare(names)
        return this.majorCompareResult
      } finally {
        this.loading.majorCompare = false
      }
    },
  },
})
