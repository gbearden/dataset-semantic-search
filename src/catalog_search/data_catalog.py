"""
Synthetic health dataset catalog (100 entries).

Covers: neuroimaging, genomics, EHR, clinical trials, longitudinal studies,
oncology, cardiovascular, metabolic, mental health, paediatrics, respiratory.

This corpus is designed so that the evaluation queries in tests/test_evaluation.py
have clearly correct answers, enabling precision/recall measurement.
"""

from __future__ import annotations

from .models import Dataset

SYNTHETIC_CATALOG: list[Dataset] = [
    # ── Neuroimaging / Alzheimer's ───────────────────────────────────────────
    Dataset(
        id="ADNI-001",
        title="Alzheimer's Disease Neuroimaging Initiative (ADNI)",
        description=(
            "Longitudinal multi-site study collecting MRI, PET, CSF biomarkers, "
            "and cognitive assessments in cognitively normal, MCI, and Alzheimer's "
            "disease participants."
        ),
        tags=["Alzheimer", "dementia", "MRI", "PET", "longitudinal", "neuroimaging"],
        modality=["MRI", "PET", "biomarker", "cognitive assessment"],
        conditions=["Alzheimer's disease", "mild cognitive impairment"],
        source="NIH NIA",
        study_type="observational",
        variables=["MMSE", "CDR", "hippocampal volume", "amyloid PET SUVR"],
    ),
    Dataset(
        id="OASIS-002",
        title="OASIS-3: Longitudinal Multimodal Neuroimaging Dataset",
        description=(
            "Retrospective compilation of MRI and PET data from the Charles F. and "
            "Joanne Knight ADRC covering >1000 participants across the adult lifespan "
            "including cognitively normal adults and those with Alzheimer's disease."
        ),
        tags=["neuroimaging", "MRI", "PET", "aging", "Alzheimer", "longitudinal"],
        modality=["MRI", "PET"],
        conditions=["Alzheimer's disease", "normal aging"],
        source="WUSTL Knight ADRC",
        study_type="observational",
        variables=["T1w", "FLAIR", "resting-state fMRI", "tau PET"],
    ),
    Dataset(
        id="HCP-003",
        title="Human Connectome Project (HCP)",
        description=(
            "High-resolution structural and functional MRI, diffusion MRI, and "
            "magnetoencephalography (MEG) data in healthy young adults to map "
            "human brain connectivity."
        ),
        tags=["connectome", "fMRI", "diffusion MRI", "brain connectivity", "neuroimaging"],
        modality=["MRI", "fMRI", "dMRI", "MEG"],
        conditions=["healthy controls"],
        source="NIH",
        study_type="observational",
        variables=["resting-state fMRI", "task fMRI", "DTI", "cortical thickness"],
    ),
    Dataset(
        id="ABIDE-004",
        title="Autism Brain Imaging Data Exchange (ABIDE)",
        description=(
            "Resting-state fMRI and structural MRI data from individuals with Autism "
            "Spectrum Disorder (ASD) and matched neurotypical controls aggregated "
            "across 24 international sites."
        ),
        tags=["autism", "ASD", "fMRI", "resting state", "neuroimaging", "brain"],
        modality=["fMRI", "MRI"],
        conditions=["autism spectrum disorder"],
        source="International multi-site",
        study_type="observational",
        variables=["functional connectivity", "gray matter volume"],
    ),
    Dataset(
        id="ENIGMA-005",
        title="ENIGMA Consortium MRI Meta-Analysis Dataset",
        description=(
            "Harmonised structural MRI measures (cortical thickness, subcortical volumes) "
            "across neuropsychiatric conditions from >40 000 participants in 43 countries."
        ),
        tags=["MRI", "cortical thickness", "meta-analysis", "neuroimaging", "brain morphometry"],
        modality=["MRI"],
        conditions=["schizophrenia", "bipolar disorder", "ADHD", "depression", "OCD"],
        source="ENIGMA Consortium",
        study_type="observational",
        variables=["cortical thickness", "subcortical volume", "surface area"],
    ),
    Dataset(
        id="UK-BB-006",
        title="UK Biobank Neuroimaging Sub-Study",
        description=(
            "Brain MRI (structural, functional, diffusion) in 100 000+ UK Biobank "
            "participants, linked to genetic, clinical, and lifestyle data."
        ),
        tags=["UK Biobank", "brain MRI", "population", "genetics", "imaging genetics"],
        modality=["MRI", "fMRI", "dMRI"],
        conditions=["population-based", "multiple chronic diseases"],
        source="UK Biobank",
        study_type="observational",
        variables=["white matter hyperintensities", "FA", "MD"],
    ),
    # ── Oncology / Cancer ────────────────────────────────────────────────────
    Dataset(
        id="TCGA-007",
        title="The Cancer Genome Atlas (TCGA)",
        description=(
            "Multi-omic profiling (genomics, transcriptomics, proteomics, epigenomics) "
            "of >20 000 primary cancer samples across 33 tumour types with linked "
            "clinical outcomes."
        ),
        tags=["cancer", "genomics", "RNA-seq", "mutation", "TCGA", "multi-omics"],
        modality=["genomics", "transcriptomics", "proteomics", "epigenomics"],
        conditions=["glioblastoma", "breast cancer", "lung cancer", "colorectal cancer"],
        source="NIH NCI",
        study_type="observational",
        variables=["somatic mutation", "copy number variation", "gene expression", "methylation"],
    ),
    Dataset(
        id="SEER-008",
        title="SEER Cancer Incidence and Survival Database",
        description=(
            "Population-based cancer registry data from 18 US geographic areas covering "
            "incidence, survival, and end-results for all major cancer types since 1973."
        ),
        tags=["cancer registry", "survival", "incidence", "epidemiology", "population"],
        modality=["registry", "EHR"],
        conditions=["all cancers", "breast cancer", "prostate cancer", "lung cancer"],
        source="NIH NCI SEER",
        study_type="observational",
        variables=["survival time", "stage", "grade", "treatment"],
    ),
    Dataset(
        id="TCIA-009",
        title="The Cancer Imaging Archive (TCIA) – LIDC-IDRI",
        description=(
            "CT images of the thorax with annotated lung nodules from 1010 cases. "
            "Expert radiologist annotations include nodule location, diameter, and "
            "malignancy rating."
        ),
        tags=["CT", "lung nodule", "radiology", "cancer imaging", "annotation"],
        modality=["CT", "imaging"],
        conditions=["lung cancer", "lung nodule"],
        source="NCI TCIA",
        study_type="observational",
        variables=["nodule diameter", "malignancy score", "CT HU"],
    ),
    Dataset(
        id="BRCA-010",
        title="METABRIC Breast Cancer Gene Expression Dataset",
        description=(
            "Gene expression microarray and copy-number data from ~2000 primary breast "
            "tumours with 20-year clinical follow-up, enabling molecular subtype analysis."
        ),
        tags=["breast cancer", "gene expression", "molecular subtypes", "survival"],
        modality=["genomics", "transcriptomics"],
        conditions=["breast cancer"],
        source="CRUK / METABRIC Consortium",
        study_type="observational",
        variables=["PAM50 subtype", "ER status", "overall survival", "copy number"],
    ),
    # ── Cardiovascular ───────────────────────────────────────────────────────
    Dataset(
        id="FHS-011",
        title="Framingham Heart Study (FHS) – Longitudinal Cohort",
        description=(
            "Multigenerational longitudinal cohort study tracking cardiovascular disease "
            "risk factors (blood pressure, cholesterol, smoking, diabetes) in Framingham, "
            "MA since 1948."
        ),
        tags=["cardiovascular", "heart disease", "longitudinal", "cohort", "risk factors"],
        modality=["EHR", "biomarker", "ECG"],
        conditions=["coronary artery disease", "hypertension", "stroke", "atrial fibrillation"],
        source="NIH NHLBI",
        study_type="observational",
        variables=["blood pressure", "cholesterol", "BMI", "ECG", "ejection fraction"],
    ),
    Dataset(
        id="MESA-012",
        title="Multi-Ethnic Study of Atherosclerosis (MESA)",
        description=(
            "Prospective study of subclinical cardiovascular disease in 6814 participants "
            "from six US communities including cardiac CT, MRI, and biomarker assessment."
        ),
        tags=["atherosclerosis", "cardiovascular", "cardiac CT", "MRI", "multi-ethnic"],
        modality=["CT", "MRI", "biomarker", "ECG"],
        conditions=["atherosclerosis", "subclinical CVD"],
        source="NIH NHLBI",
        study_type="observational",
        variables=["coronary artery calcium", "carotid IMT", "cardiac MRI", "CRP"],
    ),
    Dataset(
        id="UKBB-HEART-013",
        title="UK Biobank Cardiac MRI Dataset",
        description=(
            "Cardiac MRI of >50 000 UK Biobank participants with automated segmentation "
            "of cardiac chambers, enabling genome-wide association of cardiac structure."
        ),
        tags=["cardiac MRI", "heart", "GWAS", "imaging genetics", "ventricular volume"],
        modality=["MRI", "cardiac imaging"],
        conditions=["heart failure", "cardiomyopathy", "population-based"],
        source="UK Biobank",
        study_type="observational",
        variables=["LV volume", "ejection fraction", "myocardial mass"],
    ),
    Dataset(
        id="ACCORD-014",
        title="ACCORD: Action to Control Cardiovascular Risk in Diabetes",
        description=(
            "Randomised clinical trial testing intensive glycaemic, blood pressure, and "
            "lipid control on major cardiovascular outcomes in 10 251 type 2 diabetes "
            "participants."
        ),
        tags=["diabetes", "cardiovascular", "RCT", "glycaemic control", "blood pressure"],
        modality=["EHR", "biomarker"],
        conditions=["type 2 diabetes", "cardiovascular disease"],
        source="NIH NHLBI",
        study_type="interventional",
        variables=["HbA1c", "LDL cholesterol", "systolic BP", "MACE"],
    ),
    # ── Genomics / Genetics ──────────────────────────────────────────────────
    Dataset(
        id="GWAS-CAT-015",
        title="NHGRI-EBI GWAS Catalog",
        description=(
            "Curated collection of published genome-wide association studies across "
            "thousands of traits and diseases with variant-trait associations, "
            "effect sizes, and p-values."
        ),
        tags=["GWAS", "SNP", "genetics", "association", "variant"],
        modality=["genomics"],
        conditions=["multiple traits"],
        source="NHGRI / EBI",
        study_type="observational",
        variables=["OR", "p-value", "beta coefficient", "allele frequency"],
    ),
    Dataset(
        id="GTEx-016",
        title="Genotype-Tissue Expression (GTEx) Project",
        description=(
            "RNA-seq gene expression and genetic variant data across 54 human tissues "
            "from 948 post-mortem donors enabling eQTL mapping and tissue-specific "
            "regulatory analysis."
        ),
        tags=["RNA-seq", "eQTL", "gene expression", "tissue", "splicing"],
        modality=["transcriptomics", "genomics"],
        conditions=["normal tissue", "population variation"],
        source="NIH GTEx",
        study_type="observational",
        variables=["TPM", "eQTL effect size", "splice junction"],
    ),
    Dataset(
        id="ENCODE-017",
        title="ENCODE: Encyclopedia of DNA Elements",
        description=(
            "Functional genomics data (ChIP-seq, ATAC-seq, RNA-seq, Hi-C) from hundreds "
            "of cell lines and tissues characterising regulatory elements across the "
            "human genome."
        ),
        tags=["epigenomics", "ChIP-seq", "ATAC-seq", "regulatory elements", "chromatin"],
        modality=["genomics", "epigenomics"],
        conditions=["cell lines", "tissue"],
        source="NIH NHGRI ENCODE",
        study_type="observational",
        variables=["peak calls", "transcription factor binding", "histone marks"],
    ),
    Dataset(
        id="1KG-018",
        title="1000 Genomes Project Phase 3",
        description=(
            "Whole-genome sequencing of 2504 individuals from 26 global populations "
            "providing a reference haplotype panel for imputation and population genetics."
        ),
        tags=["whole genome sequencing", "population genetics", "haplotype", "SNP"],
        modality=["genomics", "WGS"],
        conditions=["healthy controls", "global populations"],
        source="1000 Genomes Consortium",
        study_type="observational",
        variables=["SNP", "indel", "structural variant", "allele frequency"],
    ),
    # ── EHR / Clinical Records ───────────────────────────────────────────────
    Dataset(
        id="MIMIC-019",
        title="MIMIC-IV: Medical Information Mart for Intensive Care",
        description=(
            "De-identified EHR data from >40 000 ICU admissions at Beth Israel Deaconess "
            "Medical Center including vital signs, lab results, medications, procedures, "
            "and clinical notes."
        ),
        tags=["EHR", "ICU", "critical care", "clinical notes", "NLP", "mortality"],
        modality=["EHR", "clinical notes", "time series"],
        conditions=["sepsis", "respiratory failure", "AKI", "cardiac arrest"],
        source="PhysioNet / BIDMC",
        study_type="observational",
        variables=["vital signs", "lab values", "ICD codes", "medications", "SOFA score"],
    ),
    Dataset(
        id="MIMIC-CXR-020",
        title="MIMIC-CXR: Chest X-ray Dataset with Radiology Reports",
        description=(
            "227 835 chest radiograph studies from 65 379 patients with structured and "
            "free-text radiology reports, enabling NLP and computer vision research "
            "in clinical imaging."
        ),
        tags=["chest X-ray", "radiology", "NLP", "CXR", "pneumonia", "clinical imaging"],
        modality=["X-ray", "imaging", "clinical notes"],
        conditions=["pneumonia", "pleural effusion", "cardiomegaly", "atelectasis"],
        source="PhysioNet / BIDMC",
        study_type="observational",
        variables=["CXR findings", "report labels", "DICOM metadata"],
    ),
    Dataset(
        id="OPTUM-021",
        title="Optum de-identified EHR Dataset",
        description=(
            "Real-world longitudinal EHR data from >100 million US patients including "
            "diagnoses, procedures, prescriptions, and lab results across outpatient and "
            "inpatient settings."
        ),
        tags=["EHR", "real-world data", "claims", "longitudinal", "US population"],
        modality=["EHR"],
        conditions=["multiple chronic conditions"],
        source="Optum",
        study_type="observational",
        variables=["ICD-10", "CPT", "NDC", "HbA1c", "eGFR"],
    ),
    # ── Diabetes / Metabolic ─────────────────────────────────────────────────
    Dataset(
        id="NHANES-022",
        title="NHANES: National Health and Nutrition Examination Survey",
        description=(
            "Cross-sectional survey combining interviews, physical examinations, and "
            "laboratory tests for a representative sample of the US non-institutionalised "
            "population since 1999."
        ),
        tags=["nutrition", "survey", "population", "dietary assessment", "biomarker"],
        modality=["survey", "biomarker", "physical exam"],
        conditions=["obesity", "diabetes", "hypertension", "nutrition deficiency"],
        source="CDC NCHS",
        study_type="observational",
        variables=["BMI", "waist circumference", "glucose", "HbA1c", "dietary recall"],
    ),
    Dataset(
        id="UKPDS-023",
        title="UK Prospective Diabetes Study (UKPDS)",
        description=(
            "Landmark RCT and observational follow-up examining the effects of intensive "
            "blood glucose control on complications in newly diagnosed type 2 diabetes "
            "patients over 20 years."
        ),
        tags=["diabetes", "RCT", "glycaemic control", "longitudinal", "complications"],
        modality=["EHR", "biomarker"],
        conditions=["type 2 diabetes"],
        source="Oxford / UKPDS",
        study_type="interventional",
        variables=["HbA1c", "fasting plasma glucose", "microvascular complications", "retinopathy"],
    ),
    Dataset(
        id="DPPOS-024",
        title="Diabetes Prevention Program Outcomes Study (DPPOS)",
        description=(
            "Long-term follow-up of the DPP RCT comparing metformin, lifestyle intervention, "
            "and placebo on progression from prediabetes to type 2 diabetes and "
            "cardiovascular events."
        ),
        tags=["diabetes prevention", "prediabetes", "metformin", "lifestyle", "RCT"],
        modality=["EHR", "biomarker"],
        conditions=["prediabetes", "type 2 diabetes"],
        source="NIH NIDDK",
        study_type="interventional",
        variables=["glucose tolerance", "HbA1c", "body weight", "diabetes incidence"],
    ),
    # ── Mental Health / Psychiatry ───────────────────────────────────────────
    Dataset(
        id="STAR-D-025",
        title="STAR*D: Sequenced Treatment Alternatives to Relieve Depression",
        description=(
            "Multi-level RCT in 4041 outpatients with non-psychotic major depression "
            "evaluating sequential antidepressant strategies (SSRIs, augmentation, "
            "switching)."
        ),
        tags=["depression", "antidepressant", "RCT", "MDD", "treatment-resistant"],
        modality=["EHR", "survey", "biomarker"],
        conditions=["major depressive disorder"],
        source="NIH NIMH",
        study_type="interventional",
        variables=["QIDS-SR", "HDRS", "remission rate", "time to response"],
    ),
    Dataset(
        id="PGC-026",
        title="Psychiatric Genomics Consortium (PGC) GWAS",
        description=(
            "Largest GWAS of psychiatric disorders combining data from >900 000 "
            "participants across schizophrenia, bipolar disorder, major depression, "
            "ADHD, and autism."
        ),
        tags=["schizophrenia", "bipolar", "depression", "GWAS", "genetics", "psychiatry"],
        modality=["genomics"],
        conditions=["schizophrenia", "bipolar disorder", "MDD", "ADHD", "ASD"],
        source="PGC",
        study_type="observational",
        variables=["SNP", "polygenic risk score", "OR", "p-value"],
    ),
    Dataset(
        id="ABCD-027",
        title="Adolescent Brain Cognitive Development (ABCD) Study",
        description=(
            "Longitudinal study of 11 875 US children from ages 9–10 with annual MRI, "
            "cognitive assessments, and surveys tracking brain development, substance "
            "use, and mental health."
        ),
        tags=["paediatric", "brain development", "MRI", "longitudinal", "mental health", "adolescent"],
        modality=["MRI", "fMRI", "cognitive", "survey"],
        conditions=["healthy development", "substance use", "ADHD", "anxiety"],
        source="NIH",
        study_type="observational",
        variables=["cortical thickness", "resting-state connectivity", "CBCL", "substance use"],
    ),
    # ── Respiratory / COVID-19 ───────────────────────────────────────────────
    Dataset(
        id="COG-UK-028",
        title="COVID-19 Genomics UK Consortium (COG-UK)",
        description=(
            "Whole-genome sequencing of >3 million SARS-CoV-2 samples from the UK "
            "enabling real-time tracking of variants of concern and transmission "
            "dynamics during the pandemic."
        ),
        tags=["COVID-19", "SARS-CoV-2", "whole genome sequencing", "variant", "surveillance"],
        modality=["genomics", "WGS"],
        conditions=["COVID-19"],
        source="COG-UK / NIHR",
        study_type="observational",
        variables=["lineage", "variant", "phylogenetic tree", "mutation profile"],
    ),
    Dataset(
        id="RECOVERY-029",
        title="RECOVERY Trial: COVID-19 Therapeutics",
        description=(
            "Adaptive platform RCT evaluating multiple COVID-19 treatments (dexamethasone, "
            "tocilizumab, baricitinib, remdesivir) in hospitalised patients in the UK."
        ),
        tags=["COVID-19", "RCT", "treatment", "dexamethasone", "mortality"],
        modality=["EHR", "biomarker"],
        conditions=["COVID-19", "ARDS"],
        source="University of Oxford / NIHR",
        study_type="interventional",
        variables=["28-day mortality", "mechanical ventilation", "hospital LOS", "CRP"],
    ),
    Dataset(
        id="SPIROMICS-030",
        title="SPIROMICS: Subpopulations and Intermediate Outcome Measures in COPD",
        description=(
            "Multi-centre longitudinal study with CT lung imaging, spirometry, "
            "and biomarkers in >2700 COPD and at-risk smokers to identify COPD subtypes."
        ),
        tags=["COPD", "spirometry", "CT", "lung", "smoking", "respiratory"],
        modality=["CT", "imaging", "spirometry", "biomarker"],
        conditions=["COPD", "emphysema", "chronic bronchitis"],
        source="NIH NHLBI",
        study_type="observational",
        variables=["FEV1", "FVC", "CT emphysema %", "exacerbation rate"],
    ),
    # ── Paediatrics ──────────────────────────────────────────────────────────
    Dataset(
        id="PEDS-IQ-031",
        title="Paediatric Imaging, Neurocognition, and Genetics (PING) Study",
        description=(
            "MRI, cognitive, and genetic data from 1493 typically developing children "
            "and adolescents (3–20 years) to characterise developmental trajectories "
            "of brain structure and function."
        ),
        tags=["paediatric", "brain development", "MRI", "genetics", "cognitive"],
        modality=["MRI", "cognitive", "genomics"],
        conditions=["typical development"],
        source="NIH",
        study_type="observational",
        variables=["cortical thickness", "white matter FA", "IQ", "SNP"],
    ),
    Dataset(
        id="CHD-032",
        title="Pediatric Heart Network: Congenital Heart Disease Registry",
        description=(
            "Registry and trial data from children with congenital heart disease including "
            "echocardiography, cardiac MRI, surgical outcomes, and neurodevelopmental "
            "follow-up."
        ),
        tags=["paediatric", "congenital heart disease", "cardiac MRI", "echocardiography", "surgery"],
        modality=["cardiac MRI", "echocardiography", "EHR"],
        conditions=["congenital heart disease", "Tetralogy of Fallot", "HLHS"],
        source="NIH NHLBI PHN",
        study_type="observational",
        variables=["RV volume", "oxygen saturation", "z-score", "neurodevelopment"],
    ),
    # ── Infectious Disease / Epidemiology ───────────────────────────────────
    Dataset(
        id="WHO-FLU-033",
        title="WHO FluNet Global Influenza Surveillance Data",
        description=(
            "Weekly influenza surveillance data from >100 countries including virus "
            "detections, subtyping, specimen counts, and ILI rates enabling global "
            "pandemic preparedness."
        ),
        tags=["influenza", "surveillance", "epidemiology", "pandemic", "virology"],
        modality=["surveillance", "virological"],
        conditions=["influenza A", "influenza B"],
        source="WHO Global Influenza Surveillance and Response System",
        study_type="observational",
        variables=["positive rate", "subtype H3N2/H1N1", "ILI incidence"],
    ),
    Dataset(
        id="MALARIAATLAS-034",
        title="Malaria Atlas Project (MAP) Global Parasite Rate Dataset",
        description=(
            "Geo-referenced Plasmodium falciparum and P. vivax parasite rate surveys "
            "and modelled prevalence maps used for global malaria burden estimation."
        ),
        tags=["malaria", "parasite rate", "GIS", "geospatial", "epidemiology", "Africa"],
        modality=["survey", "geospatial"],
        conditions=["malaria"],
        source="Malaria Atlas Project",
        study_type="observational",
        variables=["PfPR", "transmission intensity", "bed net coverage"],
    ),
    # ── Musculoskeletal / Orthopaedics ───────────────────────────────────────
    Dataset(
        id="OAI-035",
        title="Osteoarthritis Initiative (OAI) – Knee MRI Dataset",
        description=(
            "Longitudinal study with annual knee MRI (3T), X-ray, and clinical data "
            "from 4796 participants at risk for or with symptomatic knee osteoarthritis."
        ),
        tags=["osteoarthritis", "knee", "MRI", "X-ray", "cartilage", "musculoskeletal"],
        modality=["MRI", "X-ray"],
        conditions=["knee osteoarthritis"],
        source="NIH NIAMS",
        study_type="observational",
        variables=["cartilage volume", "KL grade", "WOMAC", "JSW"],
    ),
    Dataset(
        id="RSNA-BONE-036",
        title="RSNA Bone Age Dataset",
        description=(
            "12 611 paediatric hand X-rays from Stanford with expert bone age annotations "
            "used for AI model development and validation in paediatric radiology."
        ),
        tags=["X-ray", "bone age", "paediatric", "radiology", "AI", "hand"],
        modality=["X-ray", "imaging"],
        conditions=["bone age assessment"],
        source="RSNA / Stanford",
        study_type="observational",
        variables=["bone age (years)", "sex", "Greulich-Pyle annotation"],
    ),
    # ── Ophthalmology / Retinal ──────────────────────────────────────────────
    Dataset(
        id="EYEPACS-037",
        title="EyePACS Diabetic Retinopathy Screening Dataset",
        description=(
            "High-resolution retinal fundus photographs from 88 702 patients with "
            "expert graded diabetic retinopathy severity labels (0–4 scale) used for "
            "deep learning model development."
        ),
        tags=["diabetic retinopathy", "fundus", "retinal imaging", "AI", "diabetes", "eye"],
        modality=["fundus photography", "imaging"],
        conditions=["diabetic retinopathy"],
        source="EyePACS",
        study_type="observational",
        variables=["DR grade", "disc haemorrhage", "exudate", "neovascularisation"],
    ),
    Dataset(
        id="MAPLES-DR-038",
        title="MAPLES-DR: Multimodal Annotated Pathologies in Lesion-level Evaluation for DR",
        description=(
            "Retinal fundus and OCT images with pixel-level annotations of diabetic "
            "retinopathy lesions and diabetic macular oedema in 198 patients."
        ),
        tags=["OCT", "retinal imaging", "diabetic retinopathy", "lesion segmentation", "fundus"],
        modality=["OCT", "fundus photography"],
        conditions=["diabetic retinopathy", "diabetic macular oedema"],
        source="University of Montreal",
        study_type="observational",
        variables=["microaneurysm", "haemorrhage", "exudate", "neovascularisation", "oedema"],
    ),
    # ── Multimodal / Wearable ────────────────────────────────────────────────
    Dataset(
        id="APPLE-039",
        title="Apple Heart & Movement Study",
        description=(
            "Prospective study with continuous wearable sensor data (heart rate, activity, "
            "SpO2, ECG) from Apple Watch in >500 000 participants for cardiovascular "
            "and metabolic phenotyping."
        ),
        tags=["wearable", "heart rate", "ECG", "activity", "accelerometer", "mHealth"],
        modality=["wearable sensor", "ECG", "accelerometry"],
        conditions=["atrial fibrillation", "cardiovascular disease"],
        source="Apple / Brigham and Women's",
        study_type="observational",
        variables=["RR interval", "step count", "VO2 max estimate", "ECG waveform"],
    ),
    Dataset(
        id="PHYSIONET-040",
        title="PhysioNet MIMIC-III Waveform Database",
        description=(
            "Continuous high-resolution waveform recordings (ECG, ABP, SpO2, capnography) "
            "from 30 000 ICU patients linked to clinical data in MIMIC-III."
        ),
        tags=["waveform", "ICU", "ECG", "SpO2", "ABP", "physiological signals"],
        modality=["waveform", "physiological signals"],
        conditions=["critical illness"],
        source="PhysioNet / BIDMC",
        study_type="observational",
        variables=["heart rate variability", "arterial blood pressure", "SpO2"],
    ),
    # ── Additional entries to round out 100 ─────────────────────────────────
    Dataset(
        id="NLST-041",
        title="National Lung Screening Trial (NLST)",
        description=(
            "RCT comparing annual low-dose CT versus chest X-ray in 53 454 high-risk "
            "smokers demonstrating 20% reduction in lung cancer mortality with LDCT screening."
        ),
        tags=["lung cancer screening", "LDCT", "CT", "smoking", "RCT", "radiology"],
        modality=["CT", "X-ray"],
        conditions=["lung cancer"],
        source="NIH NCI",
        study_type="interventional",
        variables=["nodule detection", "lung cancer incidence", "all-cause mortality"],
    ),
    Dataset(
        id="PLCO-042",
        title="Prostate, Lung, Colorectal, Ovarian Cancer Screening Trial (PLCO)",
        description=(
            "RCT evaluating cancer screening modalities for four common cancers in "
            "155 000 US adults aged 55–74 with long-term follow-up."
        ),
        tags=["cancer screening", "prostate", "lung", "colorectal", "ovarian", "RCT"],
        modality=["imaging", "biomarker", "EHR"],
        conditions=["prostate cancer", "lung cancer", "colorectal cancer", "ovarian cancer"],
        source="NIH NCI",
        study_type="interventional",
        variables=["PSA", "CA-125", "flexible sigmoidoscopy", "CT"],
    ),
    Dataset(
        id="SPRINT-043",
        title="SPRINT: Systolic Blood Pressure Intervention Trial",
        description=(
            "RCT comparing intensive (<120 mmHg) versus standard (<140 mmHg) systolic "
            "blood pressure targets on cardiovascular events and mortality in 9361 "
            "non-diabetic adults at high cardiovascular risk."
        ),
        tags=["hypertension", "blood pressure", "RCT", "cardiovascular", "antihypertensive"],
        modality=["EHR", "biomarker"],
        conditions=["hypertension", "cardiovascular disease"],
        source="NIH NHLBI",
        study_type="interventional",
        variables=["systolic BP", "MACE", "eGFR", "albuminuria"],
    ),
    Dataset(
        id="MOBA-044",
        title="Norwegian Mother, Father, and Child Cohort Study (MoBa)",
        description=(
            "Pregnancy cohort with biobank samples, questionnaires, and linked registry "
            "data from >114 000 mother-child pairs studying determinants of childhood "
            "and maternal health."
        ),
        tags=["pregnancy", "cohort", "birth", "paediatric", "maternal health", "biobank"],
        modality=["biomarker", "survey", "registry"],
        conditions=["maternal health", "childhood disorders", "preeclampsia"],
        source="Norwegian Institute of Public Health",
        study_type="observational",
        variables=["gestational age", "birth weight", "folate", "inflammatory markers"],
    ),
    Dataset(
        id="GPRD-045",
        title="CPRD GOLD: Clinical Practice Research Datalink",
        description=(
            "Anonymised longitudinal primary care EHR data from >15 million UK patients "
            "linked to HES hospitalisation, ONS mortality, and cancer registry data."
        ),
        tags=["primary care", "EHR", "UK", "longitudinal", "pharmacoepidemiology"],
        modality=["EHR"],
        conditions=["multiple chronic diseases", "infectious diseases"],
        source="CPRD / MHRA",
        study_type="observational",
        variables=["Read codes", "prescriptions", "referrals", "BMI", "smoking status"],
    ),
    Dataset(
        id="MVPA-046",
        title="UK Biobank Accelerometry Dataset",
        description=(
            "Wrist-worn accelerometry data from >103 000 UK Biobank participants over "
            "7 days, enabling objective measurement of physical activity intensity, "
            "sedentary behaviour, and sleep."
        ),
        tags=["accelerometry", "physical activity", "sedentary behaviour", "sleep", "wearable"],
        modality=["accelerometry", "wearable sensor"],
        conditions=["population-based", "obesity", "type 2 diabetes"],
        source="UK Biobank",
        study_type="observational",
        variables=["MVPA minutes", "sedentary time", "sleep duration", "step count"],
    ),
    Dataset(
        id="BIOBANK-PROT-047",
        title="UK Biobank Olink Proteomics Dataset",
        description=(
            "Proximity extension assay proteomics measuring ~3000 plasma proteins in "
            ">54 000 UK Biobank participants, linked to genetic, imaging, and phenotypic data."
        ),
        tags=["proteomics", "plasma proteins", "biomarker", "Olink", "biobank"],
        modality=["proteomics"],
        conditions=["population-based", "multiple diseases"],
        source="UK Biobank",
        study_type="observational",
        variables=["protein NPX levels", "pQTL", "protein-disease associations"],
    ),
    Dataset(
        id="TEDDY-048",
        title="TEDDY: The Environmental Determinants of Diabetes in the Young",
        description=(
            "International prospective cohort following >8500 genetically at-risk children "
            "from birth examining environmental triggers (diet, microbiome, viral infections) "
            "for type 1 diabetes and coeliac disease."
        ),
        tags=["type 1 diabetes", "microbiome", "children", "autoimmune", "longitudinal", "diet"],
        modality=["biomarker", "genomics", "microbiome", "survey"],
        conditions=["type 1 diabetes", "coeliac disease", "islet autoimmunity"],
        source="NIH NIDDK",
        study_type="observational",
        variables=["islet autoantibodies", "HLA genotype", "16S rRNA", "dietary intake"],
    ),
    Dataset(
        id="MESA-AIR-049",
        title="MESA Air Pollution Sub-Study",
        description=(
            "Personal and ambient air pollution exposure estimates linked to MESA "
            "cardiovascular, CT, and MRI data examining long-term effects of PM2.5 "
            "and NO2 on cardiovascular and pulmonary health."
        ),
        tags=["air pollution", "PM2.5", "cardiovascular", "CT", "environmental epidemiology"],
        modality=["CT", "MRI", "biomarker", "environmental sensor"],
        conditions=["cardiovascular disease", "COPD", "atherosclerosis"],
        source="NIH NIEHS / EPA",
        study_type="observational",
        variables=["PM2.5 exposure", "NO2", "coronary artery calcium", "spirometry"],
    ),
    Dataset(
        id="ABCC-050",
        title="ACCORD Blood Pressure and Lipid Arms Sub-Study",
        description=(
            "Secondary analysis of the ACCORD trial examining brain MRI white matter "
            "lesions and cognitive outcomes in relation to intensive blood pressure and "
            "lipid therapy in diabetes."
        ),
        tags=["diabetes", "MRI", "white matter", "cognitive", "blood pressure", "lipid"],
        modality=["MRI", "cognitive", "EHR"],
        conditions=["type 2 diabetes", "white matter disease"],
        source="NIH NHLBI",
        study_type="interventional",
        variables=["white matter lesion volume", "cognitive score", "HbA1c", "LDL"],
    ),
    # Additional datasets to fill 50 more entries
    Dataset(
        id="NCBI-GEO-051",
        title="NCBI GEO: Gene Expression Omnibus",
        description=(
            "Public repository for high-throughput gene expression and other functional "
            "genomics data including microarray, sequencing, and ChIP-seq experiments "
            "across thousands of studies."
        ),
        tags=["gene expression", "microarray", "RNA-seq", "repository", "genomics"],
        modality=["transcriptomics", "genomics"],
        conditions=["multiple diseases", "cell lines"],
        source="NCBI",
        study_type="observational",
        variables=["gene expression", "fold change", "DESeq2 results"],
    ),
    Dataset(
        id="ARIC-052",
        title="Atherosclerosis Risk in Communities (ARIC) Study",
        description=(
            "Long-running US community-based study examining risk factors for atherosclerosis "
            "and cardiovascular disease in >15 000 adults from four US communities since 1987."
        ),
        tags=["cardiovascular", "atherosclerosis", "cohort", "longitudinal", "community"],
        modality=["EHR", "biomarker", "ECG", "ultrasound"],
        conditions=["coronary artery disease", "stroke", "atrial fibrillation"],
        source="NIH NHLBI",
        study_type="observational",
        variables=["carotid IMT", "LDL", "fibrinogen", "ECG intervals"],
    ),
    Dataset(
        id="BIOBANK-RETINA-053",
        title="UK Biobank Retinal OCT Dataset",
        description=(
            "Macular optical coherence tomography (OCT) scans from >67 000 UK Biobank "
            "participants enabling retinal biomarker discovery and disease screening."
        ),
        tags=["OCT", "retinal imaging", "biomarker", "macular", "eye"],
        modality=["OCT", "imaging"],
        conditions=["age-related macular degeneration", "glaucoma", "diabetic retinopathy"],
        source="UK Biobank",
        study_type="observational",
        variables=["retinal layer thickness", "drusen", "RNFL"],
    ),
    Dataset(
        id="CGAP-054",
        title="Cancer Genome Anatomy Project (CGAP) Gene Expression",
        description=(
            "Comprehensive gene expression profiling using SAGE and microarray for "
            "normal, pre-cancerous, and malignant tissues to characterise cancer transcriptomes."
        ),
        tags=["cancer", "gene expression", "SAGE", "transcriptome", "tumour"],
        modality=["transcriptomics"],
        conditions=["breast cancer", "ovarian cancer", "prostate cancer"],
        source="NIH NCI CGAP",
        study_type="observational",
        variables=["transcript count", "ESTs", "gene expression profile"],
    ),
    Dataset(
        id="FINRISK-055",
        title="FINRISK: Finnish Cardiovascular Risk Factor Survey",
        description=(
            "Population-based survey and cohort in Finland collecting cardiovascular "
            "risk factors, biobank samples, and follow-up data enabling gene-environment "
            "interactions and biomarker discovery."
        ),
        tags=["cardiovascular", "risk factors", "Finland", "biobank", "population"],
        modality=["biomarker", "survey"],
        conditions=["cardiovascular disease", "diabetes", "hypertension"],
        source="Finnish THL",
        study_type="observational",
        variables=["cholesterol", "C-reactive protein", "smoking", "physical activity"],
    ),
    Dataset(
        id="NSDUH-056",
        title="National Survey on Drug Use and Health (NSDUH)",
        description=(
            "Annual US survey measuring prevalence of substance use disorders, mental illness, "
            "and treatment receipt in the civilian non-institutionalised population aged 12+."
        ),
        tags=["substance use", "mental health", "survey", "opioid", "alcohol", "epidemiology"],
        modality=["survey"],
        conditions=["substance use disorder", "depression", "anxiety"],
        source="SAMHSA",
        study_type="observational",
        variables=["past-month use", "DSM criteria", "treatment access"],
    ),
    Dataset(
        id="AREDS-057",
        title="Age-Related Eye Disease Study (AREDS)",
        description=(
            "RCT and longitudinal cohort evaluating effects of antioxidant supplementation "
            "on progression of age-related macular degeneration (AMD) and cataract with "
            "fundus photography, OCT, and genetic data."
        ),
        tags=["AMD", "macular degeneration", "OCT", "fundus", "RCT", "antioxidant"],
        modality=["fundus photography", "OCT"],
        conditions=["age-related macular degeneration", "cataract"],
        source="NIH NEI",
        study_type="interventional",
        variables=["drusen area", "AMD progression", "visual acuity", "AREDS supplement"],
    ),
    Dataset(
        id="ICGC-058",
        title="International Cancer Genome Consortium (ICGC)",
        description=(
            "Whole-genome sequencing and multi-omic characterisation of primary cancer "
            "from >25 000 patients across 50 tumour types enabling pan-cancer driver "
            "discovery."
        ),
        tags=["cancer", "WGS", "somatic mutation", "pan-cancer", "tumour evolution"],
        modality=["genomics", "WGS", "transcriptomics"],
        conditions=["multiple cancer types"],
        source="ICGC International",
        study_type="observational",
        variables=["SNV", "SV", "CNV", "mutational signatures"],
    ),
    Dataset(
        id="NEMO-059",
        title="Neonatal Neuroimaging Dataset (NEMO)",
        description=(
            "Multi-site neonatal brain MRI dataset with T1, T2, and diffusion-weighted "
            "images from preterm and term infants with expert parcellations for brain "
            "segmentation algorithm development."
        ),
        tags=["neonatal", "brain MRI", "paediatric", "preterm", "segmentation"],
        modality=["MRI"],
        conditions=["preterm birth", "neonatal brain injury"],
        source="Multi-site consortium",
        study_type="observational",
        variables=["brain volume", "cortical surface area", "WM maturation"],
    ),
    Dataset(
        id="SLEEP-HEART-060",
        title="Sleep Heart Health Study (SHHS)",
        description=(
            "Multi-centre cohort with overnight polysomnography and cardiovascular "
            "follow-up to examine associations between sleep-disordered breathing "
            "and cardiovascular outcomes."
        ),
        tags=["sleep apnea", "polysomnography", "cardiovascular", "sleep", "cohort"],
        modality=["polysomnography", "EHR", "biomarker"],
        conditions=["obstructive sleep apnea", "cardiovascular disease", "hypertension"],
        source="NIH NHLBI",
        study_type="observational",
        variables=["AHI", "oxygen desaturation index", "sleep stage", "arousal index"],
    ),
    Dataset(
        id="MOABB-061",
        title="Mother of All BCI Benchmarks (MOABB) – EEG Dataset",
        description=(
            "Curated collection of electroencephalography (EEG) datasets for brain-computer "
            "interface research including motor imagery, P300, SSVEP tasks from hundreds "
            "of subjects."
        ),
        tags=["EEG", "brain-computer interface", "BCI", "motor imagery", "neuroimaging"],
        modality=["EEG"],
        conditions=["healthy controls", "motor disorders"],
        source="Open science / MOABB",
        study_type="observational",
        variables=["ERP", "power spectral density", "ERD/ERS"],
    ),
    Dataset(
        id="GBD-062",
        title="Global Burden of Disease (GBD) Study",
        description=(
            "Annual estimates of mortality, morbidity, and risk factors for 369 diseases "
            "and injuries in 204 countries from 1990 to present using systematic reviews "
            "and statistical modelling."
        ),
        tags=["global burden", "mortality", "disability", "DALY", "epidemiology", "risk factors"],
        modality=["registry", "survey", "modelled estimates"],
        conditions=["all diseases"],
        source="IHME / Lancet",
        study_type="observational",
        variables=["YLL", "YLD", "DALY", "attributable burden"],
    ),
    Dataset(
        id="BIOBANK-LIVER-063",
        title="UK Biobank Liver MRI Sub-Study",
        description=(
            "Abdominal MRI scans from >44 000 UK Biobank participants with liver iron "
            "concentration, liver fat fraction, and spleen measurements linked to genetic "
            "and metabolic data."
        ),
        tags=["liver", "MRI", "NAFLD", "steatosis", "iron", "abdominal imaging"],
        modality=["MRI", "abdominal imaging"],
        conditions=["NAFLD", "liver cirrhosis", "metabolic syndrome"],
        source="UK Biobank",
        study_type="observational",
        variables=["liver fat %", "liver iron concentration", "spleen volume"],
    ),
    Dataset(
        id="HUNT-064",
        title="HUNT: Trøndelag Health Study",
        description=(
            "Large population-based health survey in Norway since 1984 with biobank, "
            "imaging (ECG, spirometry, retinal photography), and extensive questionnaire "
            "data from >230 000 participants."
        ),
        tags=["population cohort", "Norway", "biobank", "cardiovascular", "longitudinal"],
        modality=["survey", "biomarker", "ECG", "spirometry"],
        conditions=["cardiovascular disease", "diabetes", "mental health"],
        source="NTNU Norway",
        study_type="observational",
        variables=["blood pressure", "grip strength", "spirometry", "HbA1c"],
    ),
    Dataset(
        id="TCIA-BRAIN-065",
        title="TCIA Brain Tumour Segmentation (BraTS) Dataset",
        description=(
            "Multi-modal MRI (T1, T1ce, T2, FLAIR) from glioblastoma and lower-grade "
            "glioma patients with expert ground-truth tumour segmentations for AI model "
            "benchmarking."
        ),
        tags=["brain tumour", "glioblastoma", "MRI", "segmentation", "AI benchmark", "FLAIR"],
        modality=["MRI"],
        conditions=["glioblastoma", "lower-grade glioma"],
        source="NCI TCIA / BraTS Challenge",
        study_type="observational",
        variables=["tumour volume", "enhancing tumour", "necrosis", "oedema"],
    ),
    Dataset(
        id="ABCD-SLEEP-066",
        title="ABCD Study Sleep & Circadian Sub-Analysis",
        description=(
            "Actigraphy, parental questionnaires, and resting-state fMRI data from "
            "the ABCD study examining relationships between sleep patterns and brain "
            "development in adolescents."
        ),
        tags=["sleep", "actigraphy", "adolescent", "brain development", "fMRI"],
        modality=["actigraphy", "fMRI", "survey"],
        conditions=["sleep disorders", "ADHD", "typical development"],
        source="NIH ABCD",
        study_type="observational",
        variables=["sleep efficiency", "wake-after-sleep-onset", "resting-state networks"],
    ),
    Dataset(
        id="DEAP-067",
        title="DEAP: Database for Emotion Analysis using Physiological Signals",
        description=(
            "Physiological signals (EEG, EMG, GSR, respiration, heart rate) and face "
            "video from 32 participants watching music videos with continuous emotion "
            "self-reports for affective computing research."
        ),
        tags=["EEG", "emotion", "physiological signals", "affective computing", "GSR"],
        modality=["EEG", "physiological signals", "video"],
        conditions=["emotion", "healthy controls"],
        source="Queen Mary University of London",
        study_type="observational",
        variables=["valence", "arousal", "dominance", "EEG power"],
    ),
    Dataset(
        id="CIBMTR-068",
        title="CIBMTR: Bone Marrow Transplant Outcomes Registry",
        description=(
            "Outcomes registry for allogeneic and autologous haematopoietic cell "
            "transplants from >500 transplant centres worldwide with >550 000 patients "
            "and longitudinal follow-up."
        ),
        tags=["bone marrow transplant", "haematopoietic", "registry", "survival", "GvHD"],
        modality=["EHR", "registry"],
        conditions=["leukaemia", "lymphoma", "aplastic anaemia", "graft-versus-host disease"],
        source="CIBMTR",
        study_type="observational",
        variables=["overall survival", "disease-free survival", "GvHD grade", "engraftment"],
    ),
    Dataset(
        id="ECOG-ACRIN-069",
        title="ECOG-ACRIN Cancer Research Group Clinical Trial Repository",
        description=(
            "Imaging (CT, MRI, PET) and clinical data from ECOG-ACRIN oncology "
            "clinical trials studying imaging biomarkers and AI-assisted response "
            "assessment in multiple cancer types."
        ),
        tags=["cancer imaging", "CT", "MRI", "PET", "clinical trial", "imaging biomarker"],
        modality=["CT", "MRI", "PET"],
        conditions=["lung cancer", "breast cancer", "lymphoma"],
        source="ECOG-ACRIN",
        study_type="interventional",
        variables=["RECIST response", "SUVmax", "tumour size", "progression-free survival"],
    ),
    Dataset(
        id="NIH-CHEST-070",
        title="NIH ChestX-ray14 Dataset",
        description=(
            "112 120 frontal-view chest X-ray images from 30 805 unique patients with "
            "14 disease labels mined from radiology reports using NLP, widely used for "
            "deep learning benchmark development."
        ),
        tags=["chest X-ray", "radiology", "deep learning", "classification", "NLP"],
        modality=["X-ray", "imaging"],
        conditions=["atelectasis", "pneumonia", "pleural effusion", "pneumothorax"],
        source="NIH Clinical Center",
        study_type="observational",
        variables=["disease label", "bounding box", "radiology report text"],
    ),
    Dataset(
        id="BIOBANK-DXA-071",
        title="UK Biobank DEXA Body Composition Dataset",
        description=(
            "Dual-energy X-ray absorptiometry (DEXA) scans from >10 000 UK Biobank "
            "participants providing whole-body and regional fat mass, lean mass, and "
            "bone mineral density measurements."
        ),
        tags=["DEXA", "body composition", "bone density", "adiposity", "musculoskeletal"],
        modality=["DEXA", "imaging"],
        conditions=["osteoporosis", "obesity", "sarcopenia"],
        source="UK Biobank",
        study_type="observational",
        variables=["fat mass", "lean mass", "BMD", "android/gynoid ratio"],
    ),
    Dataset(
        id="NGIAB-072",
        title="NextGen In Action: Paediatric Rare Disease Genomics",
        description=(
            "Whole-genome and exome sequencing of children with undiagnosed rare diseases "
            "through the Undiagnosed Diseases Network, with clinical phenotypes and "
            "variant interpretation data."
        ),
        tags=["rare disease", "WGS", "exome", "paediatric", "diagnosis", "variant"],
        modality=["WGS", "exome sequencing"],
        conditions=["undiagnosed rare diseases"],
        source="NIH Undiagnosed Diseases Network",
        study_type="observational",
        variables=["pathogenic variant", "HPO phenotype", "diagnostic yield"],
    ),
    Dataset(
        id="SEER-MEDIGAP-073",
        title="SEER-Medicare Linked Dataset",
        description=(
            "Linkage of SEER cancer registry data with Medicare claims for >2 million "
            "elderly cancer patients enabling real-world treatment pattern and "
            "outcomes analysis."
        ),
        tags=["cancer", "Medicare", "claims", "real-world", "elderly", "treatment patterns"],
        modality=["registry", "claims"],
        conditions=["breast cancer", "prostate cancer", "colorectal cancer", "lung cancer"],
        source="NIH NCI / CMS",
        study_type="observational",
        variables=["chemotherapy use", "radiation", "surgical resection", "survival"],
    ),
    Dataset(
        id="MIDUS-074",
        title="MIDUS: Midlife in the United States",
        description=(
            "Longitudinal survey study of US adults examining psychological, social, "
            "and biological factors affecting midlife health and development, including "
            "biomarker and neuroimaging sub-studies."
        ),
        tags=["midlife", "aging", "survey", "psychological", "longitudinal", "biomarker"],
        modality=["survey", "biomarker", "MRI"],
        conditions=["depression", "anxiety", "cardiovascular disease", "cancer"],
        source="NIH NIA",
        study_type="observational",
        variables=["well-being", "cortisol", "inflammation", "cognitive function"],
    ),
    Dataset(
        id="IBIS-075",
        title="Infant Brain Imaging Study (IBIS)",
        description=(
            "Longitudinal MRI study of infant siblings of children with autism from birth "
            "to 24 months examining early brain development and autism biomarkers."
        ),
        tags=["autism", "infant", "MRI", "brain development", "longitudinal", "paediatric"],
        modality=["MRI"],
        conditions=["autism spectrum disorder"],
        source="NIH NIMH",
        study_type="observational",
        variables=["brain volume", "cortical thickness", "ADOS", "Mullen scales"],
    ),
    Dataset(
        id="CALERIE-076",
        title="CALERIE: Comprehensive Assessment of Long-term Effects of Reducing Intake",
        description=(
            "RCT examining 25% caloric restriction over 2 years in healthy non-obese "
            "adults, measuring metabolic, cardiovascular, and ageing biomarkers including "
            "epigenetic clocks."
        ),
        tags=["caloric restriction", "aging", "metabolism", "RCT", "epigenetics"],
        modality=["biomarker", "epigenomics", "EHR"],
        conditions=["healthy aging"],
        source="NIH NIA",
        study_type="interventional",
        variables=["resting metabolic rate", "epigenetic age", "insulin sensitivity"],
    ),
    Dataset(
        id="PHENX-077",
        title="PhenX Toolkit: Standardised Phenotyping Measures",
        description=(
            "Consensus standard measures for 21 research domains enabling harmonised "
            "phenotyping across large NIH cohort studies for multi-study meta-analysis."
        ),
        tags=["phenotyping", "harmonisation", "survey", "biomarker", "standards"],
        modality=["survey", "biomarker"],
        conditions=["multiple domains"],
        source="NIH",
        study_type="observational",
        variables=["standardised measures", "protocol", "harmonised variables"],
    ),
    Dataset(
        id="RADLEX-078",
        title="RadLex Radiology Lexicon NLP Dataset",
        description=(
            "Annotated radiology reports with RadLex ontology terms supporting NLP "
            "information extraction for structured reporting across CT, MRI, X-ray, "
            "and ultrasound studies."
        ),
        tags=["NLP", "radiology reports", "ontology", "information extraction", "structured reporting"],
        modality=["clinical notes", "NLP"],
        conditions=["multiple conditions"],
        source="RSNA RadLex",
        study_type="observational",
        variables=["RadLex term", "report section", "finding", "impression"],
    ),
    Dataset(
        id="BIOBANK-PANCREAS-079",
        title="UK Biobank Pancreas MRI Sub-Study",
        description=(
            "Dixon-sequence MRI of the pancreas from >12 000 UK Biobank participants "
            "enabling automated pancreatic fat quantification and morphometry for "
            "diabetes and exocrine pancreatic disease research."
        ),
        tags=["pancreas", "MRI", "pancreatic fat", "diabetes", "abdominal imaging"],
        modality=["MRI"],
        conditions=["type 2 diabetes", "pancreatitis", "pancreatic cancer"],
        source="UK Biobank",
        study_type="observational",
        variables=["pancreatic fat fraction", "pancreas volume", "duct diameter"],
    ),
    Dataset(
        id="LLFS-080",
        title="Long Life Family Study (LLFS)",
        description=(
            "Family-based study of exceptional longevity and healthy ageing in >4800 "
            "participants from long-lived families in the US and Denmark with genomic, "
            "cognitive, and biomarker data."
        ),
        tags=["longevity", "aging", "genetics", "family study", "centenarians"],
        modality=["genomics", "biomarker", "cognitive"],
        conditions=["healthy aging", "longevity"],
        source="NIH NIA",
        study_type="observational",
        variables=["telomere length", "polygenic score", "cognitive function"],
    ),
    Dataset(
        id="MIMS-081",
        title="Mobile Insulin Titration Intervention (MITI) mHealth Dataset",
        description=(
            "Randomised trial of smartphone-based insulin titration in type 2 diabetes "
            "with continuous glucose monitoring and patient-reported outcomes collected "
            "via mobile app."
        ),
        tags=["mHealth", "diabetes", "insulin", "CGM", "mobile app", "RCT"],
        modality=["continuous glucose monitoring", "mHealth"],
        conditions=["type 2 diabetes"],
        source="NIH NIDDK",
        study_type="interventional",
        variables=["time in range", "HbA1c", "hypoglycaemia", "insulin dose"],
    ),
    Dataset(
        id="TCGA-IMAGING-082",
        title="TCGA Radiology Imaging Repository (TCGA-GBM CT/MRI)",
        description=(
            "Pre-operative CT and MRI from TCGA glioblastoma patients linked to genomic "
            "and survival data enabling radiogenomics and imaging-genomics association studies."
        ),
        tags=["glioblastoma", "MRI", "CT", "radiogenomics", "brain tumour", "cancer imaging"],
        modality=["MRI", "CT"],
        conditions=["glioblastoma"],
        source="NCI TCGA / TCIA",
        study_type="observational",
        variables=["tumour volume", "contrast enhancement", "IDH mutation", "MGMT methylation"],
    ),
    Dataset(
        id="GAP-083",
        title="Genetics of Asthma in Puerto Rico (GAP) Study",
        description=(
            "Genome-wide association study and biomarker dataset from Puerto Rican "
            "children with asthma examining genetic and environmental determinants "
            "of asthma severity and atopy."
        ),
        tags=["asthma", "GWAS", "paediatric", "atopy", "respiratory", "Puerto Rican"],
        modality=["genomics", "biomarker"],
        conditions=["asthma", "atopy", "allergic disease"],
        source="NIH NHLBI",
        study_type="observational",
        variables=["FEV1/FVC", "IgE", "eosinophil count", "SNP"],
    ),
    Dataset(
        id="BIOBANK-ECG-084",
        title="UK Biobank 12-Lead ECG Dataset",
        description=(
            "Resting 12-lead ECG recordings from >80 000 UK Biobank participants with "
            "automated interval measurements and genetic associations enabling ECG-GWAS."
        ),
        tags=["ECG", "electrocardiogram", "cardiac", "GWAS", "arrhythmia"],
        modality=["ECG"],
        conditions=["atrial fibrillation", "LVH", "arrhythmia", "population-based"],
        source="UK Biobank",
        study_type="observational",
        variables=["QRS duration", "QT interval", "PR interval", "heart rate"],
    ),
    Dataset(
        id="STRIDES-085",
        title="STRIDES: All of Us Research Program Cloud Dataset",
        description=(
            "NIH All of Us Research Program data in cloud including EHR, genomic, "
            "wearable, and survey data from >600 000 diverse US participants enabling "
            "precision medicine research."
        ),
        tags=["All of Us", "precision medicine", "EHR", "genomics", "diversity", "wearable"],
        modality=["EHR", "genomics", "wearable", "survey"],
        conditions=["multiple conditions", "rare diseases"],
        source="NIH All of Us",
        study_type="observational",
        variables=["SNP array", "WGS", "ICD codes", "medications", "Fitbit steps"],
    ),
    Dataset(
        id="PCOS-GWAS-086",
        title="Polycystic Ovary Syndrome (PCOS) International GWAS",
        description=(
            "Genome-wide association study of polycystic ovary syndrome in >10 000 "
            "cases and >100 000 controls identifying genetic loci related to "
            "reproductive and metabolic traits."
        ),
        tags=["PCOS", "GWAS", "reproductive health", "infertility", "metabolic"],
        modality=["genomics"],
        conditions=["polycystic ovary syndrome"],
        source="International PCOS Consortium",
        study_type="observational",
        variables=["SNP", "LH/FSH ratio", "testosterone", "AMH"],
    ),
    Dataset(
        id="MESA-SLEEP-087",
        title="MESA Sleep Ancillary Study",
        description=(
            "Polysomnography, actigraphy, and continuous oximetry in 2237 MESA "
            "participants examining associations of sleep characteristics with "
            "cardiovascular and metabolic outcomes."
        ),
        tags=["sleep", "polysomnography", "actigraphy", "cardiovascular", "MESA"],
        modality=["polysomnography", "actigraphy", "biomarker"],
        conditions=["sleep apnea", "insomnia", "cardiovascular disease"],
        source="NIH NHLBI",
        study_type="observational",
        variables=["AHI", "oxygen desaturation", "sleep staging", "actigraphy"],
    ),
    Dataset(
        id="CLINVAR-088",
        title="ClinVar: Clinical Variant Interpretation Database",
        description=(
            "Archive of genomic variants and their clinical significance classifications "
            "submitted by laboratories and researchers, with evidence supporting "
            "pathogenicity or benign interpretation."
        ),
        tags=["variant interpretation", "pathogenic", "germline", "clinical genetics", "VUS"],
        modality=["genomics"],
        conditions=["hereditary cancers", "rare Mendelian diseases", "cardiovascular genetics"],
        source="NCBI ClinVar",
        study_type="observational",
        variables=["ACMG classification", "variant effect", "condition", "evidence"],
    ),
    Dataset(
        id="CHESTCT-AI-089",
        title="RadImageNet: CT, MRI, Ultrasound Pretraining Dataset",
        description=(
            "Curated dataset of 1.35 million annotated radiology images across CT, MRI, "
            "and ultrasound modalities for pretraining radiology-specific deep learning "
            "foundation models."
        ),
        tags=["radiology AI", "pretraining", "CT", "MRI", "ultrasound", "deep learning"],
        modality=["CT", "MRI", "ultrasound"],
        conditions=["multiple conditions"],
        source="RadImageNet Consortium",
        study_type="observational",
        variables=["image label", "modality", "body part", "finding"],
    ),
    Dataset(
        id="PURE-090",
        title="Prospective Urban Rural Epidemiology (PURE) Study",
        description=(
            "Multinational longitudinal study in 21 countries across 5 continents "
            "examining cardiovascular risk factors, diet, and physical activity in "
            ">200 000 adults."
        ),
        tags=["cardiovascular", "diet", "physical activity", "global", "longitudinal", "risk factors"],
        modality=["survey", "biomarker", "EHR"],
        conditions=["cardiovascular disease", "diabetes", "hypertension"],
        source="McMaster University",
        study_type="observational",
        variables=["dietary recall", "blood pressure", "waist circumference", "MACE"],
    ),
    Dataset(
        id="MIMIC-ED-091",
        title="MIMIC-IV-ED: Emergency Department Dataset",
        description=(
            "De-identified EHR data from 448 972 emergency department visits including "
            "triage data, vital signs, diagnoses, and dispositions from Beth Israel "
            "Deaconess Medical Center."
        ),
        tags=["emergency department", "ED", "triage", "EHR", "acute care"],
        modality=["EHR"],
        conditions=["sepsis", "chest pain", "trauma", "dyspnea"],
        source="PhysioNet / BIDMC",
        study_type="observational",
        variables=["triage category", "vital signs", "ICD", "disposition", "LOS"],
    ),
    Dataset(
        id="OPAL-092",
        title="OPAL: Organoid Phenomics and AI Linked Dataset",
        description=(
            "High-content imaging of patient-derived intestinal organoids with matched "
            "WGS and transcriptomic data enabling drug response prediction and "
            "personalised medicine."
        ),
        tags=["organoid", "drug response", "microscopy", "WGS", "transcriptomics", "colorectal"],
        modality=["microscopy", "genomics", "transcriptomics"],
        conditions=["colorectal cancer", "IBD"],
        source="Sanger Institute",
        study_type="observational",
        variables=["drug IC50", "morphological features", "gene expression", "mutation"],
    ),
    Dataset(
        id="PAIN-IMAGING-093",
        title="OpenPain: Neuroimaging Repository for Chronic Pain",
        description=(
            "Structural and functional MRI, EEG, and psychophysical data from chronic "
            "pain patients (fibromyalgia, CRPS, low back pain) and matched controls "
            "for neural signature discovery."
        ),
        tags=["chronic pain", "fMRI", "MRI", "EEG", "fibromyalgia", "neuroimaging"],
        modality=["MRI", "fMRI", "EEG"],
        conditions=["fibromyalgia", "CRPS", "low back pain"],
        source="Multi-site / Open Science",
        study_type="observational",
        variables=["fMRI BOLD", "cortical thickness", "pain threshold", "questionnaire"],
    ),
    Dataset(
        id="CMR-PHENOME-094",
        title="CMR-Phenome: Cardiac MRI Phenome-Wide Association Study",
        description=(
            "Automated cardiac MRI phenotyping in 45 000 UK Biobank participants with "
            "genome-wide association enabling discovery of genetic determinants of "
            "cardiac structure and function."
        ),
        tags=["cardiac MRI", "GWAS", "imaging genetics", "heart failure", "phenome"],
        modality=["cardiac MRI"],
        conditions=["heart failure", "cardiomyopathy", "atrial fibrillation"],
        source="UK Biobank",
        study_type="observational",
        variables=["LV mass", "RV volume", "ejection fraction", "myocardial strain"],
    ),
    Dataset(
        id="DIAN-095",
        title="Dominantly Inherited Alzheimer Network (DIAN)",
        description=(
            "International longitudinal study of autosomal dominant Alzheimer's disease "
            "mutation carriers with MRI, PET amyloid/tau, CSF biomarkers, and cognitive "
            "assessments to characterise disease progression."
        ),
        tags=["Alzheimer", "familial", "dominantly inherited", "amyloid PET", "tau", "longitudinal"],
        modality=["MRI", "PET", "CSF biomarker", "cognitive"],
        conditions=["familial Alzheimer's disease", "PSEN1", "PSEN2", "APP mutation"],
        source="NIH NIA / DIAN Consortium",
        study_type="observational",
        variables=["amyloid PET SUVR", "tau PET", "hippocampal atrophy", "MMSE", "CDR"],
    ),
    Dataset(
        id="CARDIO-DL-096",
        title="EchoNet-Dynamic: Cardiac Echocardiography Dataset",
        description=(
            "10 030 apical-4-chamber echocardiography videos with expert measurements "
            "of ejection fraction and segmentation labels for deep learning model "
            "development in cardiac imaging."
        ),
        tags=["echocardiography", "echo", "cardiac", "AI", "deep learning", "ejection fraction"],
        modality=["echocardiography"],
        conditions=["heart failure", "cardiomyopathy"],
        source="Stanford / EchoNet",
        study_type="observational",
        variables=["LVEF", "end-systolic volume", "end-diastolic volume"],
    ),
    Dataset(
        id="BIOBANK-SPINE-097",
        title="UK Biobank Spine MRI Dataset",
        description=(
            "Sagittal T1/T2 MRI of the lumbar and cervical spine from >10 000 UK Biobank "
            "participants with automated disc and vertebral segmentation for back pain "
            "and osteoporosis research."
        ),
        tags=["spine", "MRI", "disc degeneration", "back pain", "osteoporosis", "musculoskeletal"],
        modality=["MRI"],
        conditions=["disc degeneration", "back pain", "osteoporosis"],
        source="UK Biobank",
        study_type="observational",
        variables=["disc height", "Modic change", "Pfirrmann grade", "vertebral BMD"],
    ),
    Dataset(
        id="NHANES-GENOME-098",
        title="NHANES-III Genetic Linkage Study",
        description=(
            "Genotyping of NHANES-III specimens enabling population-representative "
            "GWAS for common complex traits linked to nationally representative "
            "clinical and nutritional data."
        ),
        tags=["GWAS", "population genetics", "NHANES", "survey", "complex traits"],
        modality=["genomics", "survey", "biomarker"],
        conditions=["multiple complex traits"],
        source="CDC NCHS",
        study_type="observational",
        variables=["SNP array", "dietary intake", "nutrient levels", "BMI"],
    ),
    Dataset(
        id="IBRUTINIB-099",
        title="CLL RCT: Ibrutinib vs Chemoimmunotherapy in CLL",
        description=(
            "Phase 3 RCT comparing ibrutinib-based regimens versus standard "
            "chemoimmunotherapy in treatment-naive chronic lymphocytic leukaemia with "
            "genomic correlates of response."
        ),
        tags=["CLL", "leukaemia", "RCT", "ibrutinib", "BTK inhibitor", "genomics"],
        modality=["EHR", "genomics"],
        conditions=["chronic lymphocytic leukaemia"],
        source="Alliance/ECOG",
        study_type="interventional",
        variables=["PFS", "ORR", "TP53 mutation", "IGHV mutation status"],
    ),
    Dataset(
        id="MICROBIOME-HMP-100",
        title="Human Microbiome Project (HMP2) – Inflammatory Bowel Disease",
        description=(
            "Longitudinal multi-omic (metagenomics, metatranscriptomics, metabolomics, "
            "proteomics) profiling of the gut microbiome in IBD patients and controls "
            "from the iHMP."
        ),
        tags=["microbiome", "IBD", "metagenomics", "multi-omics", "gut", "longitudinal"],
        modality=["metagenomics", "metabolomics", "proteomics"],
        conditions=["Crohn's disease", "ulcerative colitis"],
        source="NIH HMP",
        study_type="observational",
        variables=["microbial abundance", "metabolite", "calprotectin", "disease activity"],
    ),
]
