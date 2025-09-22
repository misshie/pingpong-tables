# **piNGPong tables**

*Next-Generation Phenotyping powered by GestaltMatcher and PubCaseFinder*

<img src="./assets/piNGPongTables.png" width="80%" alt="pingpon tables" />

### **Table of Contents**

1. [Introduction](#introduction)
2. [For End-Users (Installation & Usage)](#for-end-users-installation--usage)  
3. [For Developers](#for-end-users-installation--usage)
4. [Technology Stack](#for-end-users-installation--usage)
5. [License](#for-end-users-installation--usage)  
6. [Acknowledgements](#acknowledgements)  
7. [Author](#author)
8. [References](#references)

### **Introduction**

**piNGPong tables** is a web-based application designed to support the diagnosis of rare diseases.
It integrates facial phenotype analysis from images with clinical information (HPO IDs) to provide
a comprehensive view for clinical geneticists and medical researchers.

The application leverages the analytical power of GestaltMatcher for image-based predictions
and complements it with data from PubCaseFinder for HPO-based queries, offering a multi-faceted
approach to next-generation phenotyping.

***piNGPong tables, GestaltMatcher, PubCaseFiner, and external information sources are intended for research and educational purposes only***.

### **For End-Users (Installation & Usage)**

This section provides instructions for users who want to run the application.
No front-end development environment is required.

#### **Prerequisites**

* Docker and Docker Compose must be installed on your system.

#### **1. Get the Application**

Download latest release zip file and unzip.

#### **2. Place Trained Models**

Due to ethical reasons the pretrained models are not made available publicly. \
Once access has been granted to GMDB, the pretrained model weights can be requested as well.

Save the following files in `backend/saved_models/`
1. `Resnet50_Final.pth` (for the face alignment)
2. `glint360k_r50.onnx` (base pre-trained model for model a)
3. `glint360k_r100.onnx` (base pre-trained model for model b)

Trained models by GestaltMatcher Database in `backend/data`
1. `s1_glint360k_r50_512d_gmdb__v1.1.0_bs64_size112_channels3_last_model.pth` (model 1 for the encoding)
2. `s2_glint360k_r100_512d_gmdb__v1.1.0_bs128_size112_channels3_last_model.pth` (model 2 for the encoding)

Gellery Encodings by GestaltMatcher Database in `backend/data/gellery_encodings`
1. `GMDB_gallery_encodings_20082024_v1.1.0_service.pkl`

You need to place the separately distributed clinical data files into the backend/ directory.
 Copy your data and saved\_models directories to the specified location.

The final structure should look like this:

```
pingpong-tables/  
└── backend/  
    ├── data/          <-- Place your data directory here  
    ├── saved_models/  <-- Place your models directory here
    └── ... (other backend files)
```

#### **3. Build and Run the Application**

Navigate to the backend directory and use Docker Compose to build and start the services.

```
cd backend  
docker compose build  
docker compose up -d     # without `-d`, you can watch logs on console.
```

The initial startup may take about 90 seconds as the API service loads the models.

#### **4. Access the Application**

Once the startup process is complete, open your web browser and navigate to:  
`https://localhost`

**Security Warning on First Access**

When you first access *piNGPong tables*, your browser may show a potential security warning due to our use of a self-signed certificate.

This is a normal and expected behavior. To proceed, please click on the button labeled "Advanced" or "Proceed to..." and accept the certificate.

### **For Developers**

This section is for developers who wish to contribute to the project.

#### **Initial Setup**

1. **Frontend Dependencies:**
```
   cd frontend  
   npm install
```

2. Backend Data:  
   Follow step 2 in the "For End-Users" section to place the required clinical data in the backend/ directory.

#### **Running in Development Mode**

1. **Start Frontend Dev Server:**
```
   cd frontend  
   npm run dev
```

2. Start Backend API Server:  
```
   In a separate terminal:  
   cd backend  
   docker compose up --build
```

   The frontend will now be available at http://localhost:3000 with hot-reloading enabled,
   and it will communicate with the API server running inside Docker.

#### **Building the Frontend**

To build the production-ready frontend and copy it to the backend's static directory,
run the provided script from the project root:

`./build-frontend.sh`

### **Technology Stack**

* **Frontend:** Vue.js 3, TypeScript, Vuetify, Pinia
* **Backend:** Python 3, FastAPI  
* **Infrastructure:** Docker, Docker Compose, Nginx

### **License**

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License**.
See the [LICENSE.md](https://www.google.com/search?q=./LICENSE.md) file for full details.

### **Acknowledgements**

The backend service of this project is based on the work of
[GestaltMatcher](https://www.gestaltmatcher.org/) with their [repository](https://github.com/igsb/GestaltMatcher-Arc/).
The backend service utilze the API of PubCaseFinder. See also [detailed description](https://pubcasefinder.dbcls.jp/api). The authoe is grateful for their foundational contributions to the field.

### **Author**

* **Hiroyuki Mishima** (三嶋 博之)*
*Department of Human Genetics, Atomic Bomb Disease Institute, Nagasaki University*  
* [Research Map Profile](https://researchmap.jp/misshie?lang=en)

## References
### GestaltMatcher
1. **GestaltMatcher**: Hsieh, T.-C. et al. (2022). GestaltMatcher facilitates rare disease matching using facial phenotype descriptors. Nature Genetics, 54(3), 349-357. [https://www.nature.com/articles/s41588-021-01010-x](https://www.nature.com/articles/s41588-021-01010-x)
2. **GestaltMatcher-Arc**: Hustinx, A. et al. (2023). Improving deep facial phenotyping for ultra-rare disorder verification using model ensembles. 2023 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV). doi:[10.1109/wacv56688.2023.00499](https://openaccess.thecvf.com/content/WACV2023/papers/Hustinx_Improving_Deep_Facial_Phenotyping_for_Ultra-Rare_Disorder_Verification_Using_Model_WACV_2023_paper.pdf)
3. **GestaltMatcher Database**: Lesmann, H. et al. (2024). GestaltMatcher Database - A global reference for facial phenotypic variability in rare human diseases. medRxiv. doi:[10.1101/2023.06.06.23290887](https://www.medrxiv.org/content/10.1101/2023.06.06.23290887v3)

### PubCaseFinder
1. Shin, J., Fujiwara, T., Saitsu, H., & Yamaguchi, A. (2025).Ontology-based expansion of virtual gene panels to improve diagnostic efficiency for rare genetic diseases. BMC medical informatics and decision making, 25(Suppl 1), 59. doi:[10.1186/s12911-025-02910-2](https://doi.org/10.1186/s12911-025-02910-2)
2. Fujiwara, T., Shin, J. M., & Yamaguchi, A. (2022). Advances in the development of PubCaseFinder, including the new application programming interface and matching algorithm. Human mutation, 10.1002/humu.24341. Advance online publication. doi:[10.1002/humu.24341](https://doi.org/10.1002/humu.24341)
3. Yamaguchi, A., Shin, J. M., & Fujiwara, T. (2021, December). Gene Ranking based on Paths from Phenotypes to Genes on Knowledge Graph. In The 10th International Joint Conference on Knowledge Graphs (pp. 131-134). doi:[10.1145/3502223.3502240](https://doi.org/10.1145/3502223.3502240)
4. Fujiwara, T., Yamamoto, Y., Kim, J. D., Buske, O., & Takagi, T. (2018). PubCaseFinder: A case-report-based, phenotype-driven differential-diagnosis system for rare diseases. The American Journal of Human Genetics, 103(3), 389-399. doi:[10.1016/j.ajhg.2018.08.003](https://doi.org/10.1016/j.ajhg.2018.08.003)
