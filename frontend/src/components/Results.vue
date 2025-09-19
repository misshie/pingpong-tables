<script setup lang="ts">
  import type { VDataTable } from 'vuetify/components'
  import { ref } from 'vue'
  import { useI18n } from 'vue-i18n'
  import { useStore } from '@/stores/app'

  const store = useStore()
  const activeTab = ref('syndromes')
  const geneSearch = ref('')
  const syndromeSearch = ref('')
  const patientSearch = ref('')

  const { t } = useI18n()

  // Type definition for table headers
  type ReadonlyHeaders = VDataTable['$props']['headers']

  // Define headers for each data table
  const geneHeaders: ReadonlyHeaders = [
    { title: 'Rank', key: 'rank', sortable: false },
    { title: 'Gene Name', key: 'gene_name', sortable: true },
    { title: 'Entrez ID', key: 'gene_entrez_id', sortable: false },
    { title: 'Distance', key: 'distance', sortable: true },
    { title: 'Score', key: 'score', sortable: true, width: '150px' },
    { title: 'PCF Rank', key: 'pubcasefinder_rank', align: 'end' },
    { title: 'PCF Score', key: 'pubcasefinder_score', align: 'end' },
  ]

  const syndromeHeaders: ReadonlyHeaders = [
    { title: 'Rank', key: 'rank', sortable: false },
    { title: 'Syndrome Name', key: 'syndrome_name', sortable: true },
    { title: 'OMIM ID', key: 'omim_id', sortable: false },
    { title: 'Distance', key: 'distance', sortable: true },
    { title: 'Score', key: 'score', sortable: true, width: '150px' },
    { title: 'Image ID', key: 'image_id', sortable: false },
    { title: 'Subject ID', key: 'subject_id', sortable: false },
    { title: 'PCF Rank', key: 'pubcasefinder_rank', align: 'end' },
    { title: 'PCF Score', key: 'pubcasefinder_score', align: 'end' },
  ]

  const patientHeaders: ReadonlyHeaders = [
    { title: 'Rank', key: 'rank', sortable: false },
    { title: 'Subject ID', key: 'subject_id' },
    { title: 'Gene Name', key: 'gene_name' },
    { title: 'Syndrome Name', key: 'syndrome_name' },
    { title: 'Distance', key: 'distance' },
    { title: 'Score', key: 'score', sortable: true, width: '150px' },
    { title: 'OMIM iD', key: 'omim_id' },
    { title: 'Phenotypic Series', key: 'phenotypic_series', sortable: false },
    { title: 'PCF Rank', key: 'pubcasefinder_rank', align: 'end' },
    { title: 'PCF Score', key: 'pubcasefinder_score', align: 'end' },
  ]

  /**
   * Extracts the numeric OMIM ID from a composite string.
   * @param omimValue - The string from the data, e.g., "600123, PS123456"
   * @returns The numeric part, or null if not found.
   */
  function getNumericOmimId (omimValue: string | number | null): string | null {
    if (!omimValue) return null
    const parts = String(omimValue).split(',').map(p => p.trim())
    return parts.find(p => !p.startsWith('PS')) || null
  }
  /**
   * Extracts the Phenotypic Series ID from a composite string.
   * @param omimValue - The string from the data, e.g., "600123, PS123456"
   * @returns The PS part, or null if not found.
   */
  function getPhenotypicSeriesId (omimValue: string | number | null): string | null {
    if (!omimValue) return null
    const parts = String(omimValue).split(',').map(p => p.trim())
    return parts.find(p => p.startsWith('PS')) || null
  }

  // Helper function to format scores consistently.
  function formatScore (score: number | undefined | null) {
    return typeof score === 'number' ? score.toFixed(4) : '-'
  }
</script>

<template>
  <v-container fluid>
    <v-row v-if="store.uploadedImage" class="mb-4" justify="center">
      <v-col cols="auto">
        <v-card
          elevation="2"
          width="150"
        >
          <v-img
            alt="Uploaded analysis image"
            aspect-ratio="1"
            cover
            :src="store.uploadedImage"
          />
        </v-card>
      </v-col>
    </v-row>

    <v-card>
      <!-- Display Metadata -->
      <v-card-text class="d-flex justify-space-between text-caption py-2">
        <span>Model Version: {{ store.analysisResult?.model_version }}</span>
        <span>Gallery Version: {{ store.analysisResult?.gallery_version }}</span>
      </v-card-text>
      <v-divider />

      <v-tabs
        v-model="activeTab"
        bg-color="tertiary"
      >
        <v-tab value="syndromes">{{ t('resultsPage.tabs.syndromes') }} ({{ store.analysisResult?.suggested_syndromes_list?.length || 0 }})</v-tab>
        <v-tab value="genes">{{ t('resultsPage.tabs.genes') }} ({{ store.analysisResult?.suggested_genes_list?.length || 0 }})</v-tab>
        <v-tab value="patients">{{ t('resultsPage.tabs.patients') }} ({{ store.analysisResult?.suggested_patients_list?.length || 0 }})</v-tab>
      </v-tabs>

      <v-card-text>
        <v-window v-model="activeTab">
          <!-- ---------------------- GENES Tab --------------- -->
          <v-window-item value="genes">
            <v-text-field
              v-model="geneSearch"
              class="mb-4"
              density="compact"
              flat
              hide-details
              :label="t('resultsPage.search.genes')"
              prepend-inner-icon="mdi-magnify"
              single-line
              variant="solo-filled"
            />
            <v-data-table
              v-if="store.analysisResult?.suggested_genes_list"
              class="elevation-1"
              density="compact"
              :headers="geneHeaders"
              :items="store.analysisResult.suggested_genes_list"
              :items-per-page="15"
              :search="geneSearch"
            >
              <!-- Slot for Distance (displays only the number) -->
              <template #item.distance="{ item }">
                {{ item.distance.toFixed(4) }}
              </template>
              <!-- Slot for Score (displays the progress bar) -->
              <template #item.score="{ item }">
                <v-progress-linear
                  color="blue-grey"
                  height="10"
                  :model-value="item.score * 100"
                  rounded
                />
              </template>

              <!-- Slot for Entrez ID (link from gene_entrez_id to NCBI -->
              <template #item.gene_entrez_id="{ item }">
                <a
                  v-if="item.gene_entrez_id"
                  class="text-decoration-none"
                  :href="`https://www.ncbi.nlm.nih.gov/gene/${item.gene_entrez_id}`"
                  rel="noopener noreferrer"
                  target="_blank"
                >
                  {{ item.gene_entrez_id }}
                  <v-icon class="ml-1" icon="mdi-open-in-new" size="x-small" />
                </a>
              </template>

              <template #item.pubcasefinder_rank="{ item }">
                {{ item.pubcasefinder_rank ?? '-' }}
              </template>

              <template #item.pubcasefinder_score="{ item }">
                {{ formatScore(item.pubcasefinder_score) }}
              </template>
            </v-data-table>
          </v-window-item>

          <!-- ---------------- SYNDROMES Tab ------------ -->
          <v-window-item value="syndromes">
            <v-text-field
              v-model="syndromeSearch"
              class="mb-4"
              density="compact"
              flat
              hide-details
              :label="t('resultsPage.search.syndromes')"
              prepend-inner-icon="mdi-magnify"
              single-line
              variant="solo-filled"
            />
            <v-data-table
              v-if="store.analysisResult?.suggested_syndromes_list"
              class="elevation-1"
              density="compact"
              :headers="syndromeHeaders"
              :items="store.analysisResult.suggested_syndromes_list"
              :items-per-page="15"
              :search="syndromeSearch"
            >
              <!-- Slot for OMIM ID -->
              <template #item.omim_id="{ item }">
                <a :href="`https://omim.org/entry/${item.omim_id}`" rel="noopener noreferrer" target="_blank">
                  {{ item.omim_id }}
                </a>
              </template>
              <!-- Slot for Distance -->
              <template #item.distance="{ item }">
                {{ item.distance.toFixed(4) }}
              </template>
              <!-- New Slot for Score -->
              <template #item.score="{ item }">
                <v-progress-linear
                  color="blue-grey"
                  height="10"
                  :model-value="item.score * 100"
                  rounded
                />
              </template>

              <template #item.pubcasefinder_rank="{ item }">
                {{ item.pubcasefinder_rank ?? '-' }}
              </template>

              <template #item.pubcasefinder_score="{ item }">
                {{ formatScore(item.pubcasefinder_score) }}
              </template>

            </v-data-table>
          </v-window-item>

          <!-- ----------------------- PATIENTS Tab ---------------------- -->
          <v-window-item value="patients">
            <v-text-field
              v-model="patientSearch"
              class="mb-4"
              density="compact"
              flat
              hide-details
              :label="t('resultsPage.search.patients')"
              prepend-inner-icon="mdi-magnify"
              single-line
              variant="solo-filled"
            />
            <v-data-table
              v-if="store.analysisResult?.suggested_patients_list"
              class="elevation-1"
              density="compact"
              :headers="patientHeaders"
              :items="store.analysisResult.suggested_patients_list"
              :items-per-page="15"
              :search="patientSearch"
            >
              <!-- Slot for OMIM ID -->
              <template #item.omim_id="{ item }">
                <a
                  v-if="getNumericOmimId(item.omim_id)"
                  :href="`https://omim.org/entry/${getNumericOmimId(item.omim_id)}`"
                  rel="noopener noreferrer"
                  target="_blank"
                >
                  {{ getNumericOmimId(item.omim_id) }}
                </a>
              </template>

              <!-- Slot for Phenotypic Series -->
              <template #item.phenotypic_series="{ item }">
                <a
                  v-if="getPhenotypicSeriesId(item.omim_id)"
                  :href="`https://www.omim.org/phenotypicSeries/${getPhenotypicSeriesId(item.omim_id)}`"
                  rel="noopener noreferrer"
                  target="_blank"
                >
                  {{ getPhenotypicSeriesId(item.omim_id) }}
                </a>
              </template>

              <!-- Slot for Distance -->
              <template #item.distance="{ item }">
                {{ item.distance.toFixed(4) }}
              </template>

              <!-- Slot for Score -->
              <template #item.score="{ item }">
                <v-progress-linear
                  color="blue-grey"
                  height="10"
                  :model-value="item.score * 100"
                  rounded
                />
              </template>

              <template #item.pubcasefinder_rank="{ item }">
                {{ item.pubcasefinder_rank ?? '-' }}
              </template>

              <template #item.pubcasefinder_score="{ item }">
                {{ formatScore(item.pubcasefinder_score) }}
              </template>

            </v-data-table>
          </v-window-item>
        </v-window>
      </v-card-text>
    </v-card>
  </v-container>
</template>
