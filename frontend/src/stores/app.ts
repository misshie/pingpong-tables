import { defineStore } from 'pinia'
interface GeneEntry {
  gene_name: string
  gene_entrez_id: string
  distance: number
  rank?: number
  score: number
  pubcasefinder_rank?: number
  pubcasefinder_score?: number
}

interface SyndromeEntry {
  syndrome_name: string
  omim_id: number
  distance: number
  image_id: string
  subject_id: string
  rank?: number
  score: number
  pubcasefinder_rank?: number
  pubcasefinder_score?: number
}

interface PatientEntry {
  subject_id: string
  gene_name: string
  gene_entrez_id: string
  distance: number
  image_id: string
  syndrome_name: string
  omim_id: number | string
  rank?: number
  score: number
  pubcasefinder_rank?: number
  pubcasefinder_score?: number
}

export interface AnalysisResult {
  model_version: string
  gallery_version: string
  suggested_genes_list: GeneEntry[]
  suggested_syndromes_list: SyndromeEntry[]
  suggested_patients_list: PatientEntry[]
  pubcasefinder?: any
}

export interface AppSettings {
  host: string
  port: string
  user: string
  password: string
}

export const useStore = defineStore('app', {
  state: () => ({
    host: 'https://localhost/',
    port: '443',
    user: 'your_username',
    password: 'your_password',
    locale: 'en-US',
    analysisResult: null as AnalysisResult | null,
    uploadedImage: null as string | null,
  }),

  getters: {
    predictApiUri: (state): string => {
      const baseUrl = `${state.host.replace(/\/$/, '')}:${state.port}`
      return `${baseUrl}/api/predict`
    },
  },

  actions: {
    setLocale (newLocale: string) {
      this.locale = newLocale
    },

    setUploadedImage (imageDataUrl: string) {
      this.uploadedImage = imageDataUrl
    },

    setAnalysisResult (result: AnalysisResult) {
      // Helper function to process each list
      const processList = (list: any[]): any[] => {
        if (!list || list.length === 0) {
          return [];
        }

        // 1. Add rank
        const rankedList = list.map((item, index) => ({
          ...item,
          rank: index + 1,
        }))

        // 2. Calculate score
        const distances = rankedList.map(item => item.distance)
        const min_dist = Math.min(...distances)
        const max_dist = Math.max(...distances)
        const range = max_dist - min_dist

        // Handle edge case where all distances are the same
        if (range === 0) {
          return rankedList.map(item => ({ ...item, score: 1 }))
        }

        return rankedList.map(item => ({
          ...item,
          score: 1 - (item.distance - min_dist) / range,
        }))
      }

      // Process each list in the result to add rank and score
      result.suggested_genes_list = processList(result.suggested_genes_list)
      result.suggested_syndromes_list = processList(result.suggested_syndromes_list)
      result.suggested_patients_list = processList(result.suggested_patients_list)

      this.analysisResult = result
    },

    clearAnalysisResult () {
      this.analysisResult = null
      this.uploadedImage = null
    },

    updateSettings (newSettings: AppSettings) {
      this.host = newSettings.host
      this.port = newSettings.port
      this.user = newSettings.user
      this.password = newSettings.password
    },
  },
})
