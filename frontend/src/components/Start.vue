<script setup lang="ts">
  import { useI18n } from 'vue-i18n'

  const { t } = useI18n()

  // Main Links
  const mainLinks = [
    {
      href: 'https://www.gestaltmatcher.org/',
      icon: 'mdi-home-variant-outline',
      title: 'Project Homepage',
      subtitle: 'Visit the main project website.',
    },
    {
      href: 'https://en.wikipedia.org/wiki/GestaltMatcher',
      icon: 'mdi-wikipedia',
      title: 'Wikipedia Article',
      subtitle: 'Read more on Wikipedia.',
    },
    {
      href: 'https://db.gestaltmatcher.org/',
      icon: 'mdi-database-search-outline',
      title: 'GestaltMatcher Database',
      subtitle: 'Explore the project database.',
    },
    {
      href: 'https://pubcasefinder.dbcls.jp/?lang=en',
      icon: 'mdi-book-search-outline',
      title: 'PubCaseFinder',
      subtitle: 'Search System for Rare Genetic Diseases.',
    },
  ]

  // Related Resources
  const resources = [
    {
      href: 'https://github.com/misshie/pingpong-tables',
      icon: 'mdi-github',
      title: 'piNGPong tables Repository',
    },
  ]

  // Publications
  const publications = [
    {
      title: 'Next-generation phenotyping integrated in a national framework for patients with ultrarare disorders improves genetic diagnostics and yields new molecular findings',
      authors: 'Schmidt, Axel; et al.',
      journal: 'Nature Genetics. 56 (8): 1644–1653',
      year: 2024,
      doi: '10.1038/s41588-024-01836-1',
    },
    {
      title: 'GestaltMatcher Database - A global reference for facial phenotypic variability in rare human diseases',
      authors: 'Lesmann, Hellen; et al.',
      journal: 'medRxiv',
      year: 2024,
      doi: '10.1101/2023.06.06.23290887',
    },
    {
      title: 'Improving Deep Facial Phenotyping for Ultra-rare Disorder Verification Using Model Ensembles',
      authors: 'Hustinx, Alexander; et al.',
      journal: 'WACV',
      year: 2023,
      doi: '10.1109/WACV56688.2023.00499',
      pdfUrl: 'https://openaccess.thecvf.com/content/WACV2023/papers/Hustinx_Improving_Deep_Facial_Phenotyping_for_Ultra-Rare_Disorder_Verification_Using_Model_WACV_2023_paper.pdf',
    },
    {
      title: 'Few-Shot Meta-Learning for Recognizing Facial Phenotypes of Genetic Disorders',
      authors: 'Sümer, Ömer; et al.',
      journal: 'Studies in Health Technology and Informatics. Vol. 302',
      year: 2023,
      doi: '10.3233/SHTI230312',
    },
    {
      title: 'GestaltMatcher facilitates rare disease matching using facial phenotype descriptors',
      authors: 'Hsieh, Tzung-Chien; et al.',
      journal: 'Nature Genetics. 54 (3): 349–357',
      year: 2022,
      doi: '10.1038/s41588-021-01010-x',
    },
  ]
</script>

<template>
  <v-container class="fill-height" style="max-width: 900px;">
    <v-responsive class="align-center text-center fill-height">
      <!-- Logo and Title -->
      <v-img
        class="mb-4 mx-auto"
        height="150"
        src="@/assets/piNGPongTables.png"
        style="max-width: 600px;"
      />
      <!---- <h1 class="text-h4 font-weight-bold">piNGPong tables</h1> -->
      <div class="text-body-1 font-weight-light mt-2 mb-6">
        Next-Generation Phenotyping with AI and FAIR data
      </div>

      <!-- Call to Action -->
      <v-card
        class="py-4 mb-8"
        color="tertiary"
        prepend-icon="mdi-rocket-launch-outline"
        rounded="lg"
        variant="tonal"
      >
        <template #title>
          <h2 class="text-h5 font-weight-bold">
            {{ t('startPage.getStarted') }}
          </h2>
        </template>
        <template #subtitle>
          <div class="text-subtitle-1">
            <span v-html="t('startPage.pressAnalysis')" />
          </div>
        </template>
      </v-card>

      <!-- Main Links -->
      <v-row class="mb-4">
        <v-col v-for="link in mainLinks" :key="link.href" cols="12" md="6">
          <v-card
            append-icon="mdi-open-in-new"
            class="py-4 text-left"
            :href="link.href"
            :prepend-icon="link.icon"
            rel="noopener noreferrer"
            rounded="lg"
            :subtitle="link.subtitle"
            target="_blank"
            :title="link.title"
            variant="outlined"
          />
        </v-col>
      </v-row>

      <v-divider class="my-6" />

      <!-- Related Resources -->
      <div class="text-left mb-6">
        <h3 class="text-h6 font-weight-medium mb-2">Related Resources</h3>
        <v-list bg-color="transparent" lines="one">
          <v-list-item
            v-for="resource in resources"
            :key="resource.title"
            :href="resource.href"
            rel="noopener noreferrer"
            rounded="lg"
            target="_blank"
          >
            <template #prepend>
              <v-icon class="mr-4" :icon="resource.icon" />
            </template>
            <v-list-item-title>{{ resource.title }}</v-list-item-title>
            <template #append>
              <v-icon icon="mdi-open-in-new" size="small" />
            </template>
          </v-list-item>
        </v-list>
      </div>

      <!-- Publications -->
      <div class="text-left">
        <h3 class="text-h6 font-weight-medium mb-2">Publications</h3>
        <v-list bg-color="transparent" lines="three">
          <v-list-item
            v-for="(pub, i) in publications"
            :key="i"
            class="mb-2"
            rounded="lg"
            variant="tonal"
          >
            <v-list-item-title class="font-weight-bold mb-1" style="white-space: normal;">
              {{ pub.title }}
            </v-list-item-title>
            <v-list-item-subtitle style="white-space: normal;">
              {{ pub.authors }} ({{ pub.year }})<br><em>{{ pub.journal }}</em>
            </v-list-item-subtitle>

            <template #append>
              <div class="d-flex flex-column ga-2">
                <v-btn
                  v-if="pub.doi"
                  :href="`https://doi.org/${pub.doi}`"
                  icon="mdi-book-open-variant"
                  rel="noopener noreferrer"
                  size="small"
                  target="_blank"
                  variant="text"
                />
                <v-btn
                  v-if="pub.pdfUrl"
                  :href="pub.pdfUrl"
                  icon="mdi-file-pdf-box"
                  rel="noopener noreferrer"
                  size="small"
                  target="_blank"
                  variant="text"
                />
              </div>
            </template>
          </v-list-item>
        </v-list>
      </div>
      <div class="py-12" />
    </v-responsive>
  </v-container>
</template>
