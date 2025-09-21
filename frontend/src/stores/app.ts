import { defineStore } from 'pinia'

interface GeneEntry {
  gene_name: string
  gene_entrez_id: string
  distance: number
  score: number | null
  gm_rank?: number
  pubcasefinder_rank?: number
  pubcasefinder_score?: number
  mean_rank?: number | null
  meta_rank?: number
}

interface SyndromeEntry {
  syndrome_name: string
  omim_id: number
  distance: number
  image_id: string
  subject_id: string
  score: number | null
  gm_rank?: number
  pubcasefinder_rank?: number
  pubcasefinder_score?: number
  mean_rank?: number | null
  meta_rank?: number
}

interface PatientEntry {
  subject_id: string
  gene_name: string
  gene_entrez_id: string
  distance: number
  image_id: string
  syndrome_name: string
  omim_id: number | string // Original composite value from GestaltMatcher
  score: number | null
  gm_rank?: number
  pubcasefinder_rank?: number
  pubcasefinder_score?: number
  mean_rank?: number | null
  meta_rank?: number
  // --- ADDED ---
  // Parsed IDs from the backend integrator
  numeric_omim_id?: number | null
  phenotypic_series_id?: string | null
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

