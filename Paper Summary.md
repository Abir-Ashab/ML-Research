## **Background of the Paper**

The paper introduces a **medical imaging dataset** made from brain scans of **67 patients**. These patients have either:

* **Primary brain tumors**: Called **High-Grade Gliomas (HGGs)**. These are brain cancers that start inside the brain.
* **Secondary brain tumors**: Called **Brain Metastases (BMs)**. These come from other body parts (like lung or breast cancer) and spread to the brain.

Now here's the challenge:
- On **MRI scans**, these two tumor types look very similar.
- But they need different treatments.
So, how do we tell them apart without surgery or biopsy? This is where AI and radiomics come in.

---

## **Radiomics**

Think of an MRI scan as an image. Just like computer vision extracts edges or textures from a photo, **radiomics** extracts **quantitative features** from MRI.

### Radiomic Features Include:

* **Shape**: Size, roundness, irregularity
* **Texture**: How "rough" or "smooth" an area is
* **Intensity**: How bright or dark a pixel is

Radiomics converts images into **numbers** that can be used by **machine learning models**.

---

## **Multiparametric MRI**

**MRI (Magnetic Resonance Imaging)** is like taking very detailed pictures of the brain.

But doctors don’t just take one kind of picture. They take **many types** using different settings. These are called **MRI sequences**.

This dataset includes four key MRI sequences:

| Sequence | Full Name                           | What It Shows                                                |
| -------- | ----------------------------------- | ------------------------------------------------------------ |
| T1       | T1-weighted                         | Shows anatomy and normal brain structure                     |
| T1-ce    | Contrast-enhanced T1                | Shows tumor "enhancement" using contrast agent (tumor edges) |
| T2       | T2-weighted                         | Shows water content, helps highlight tumors and swelling     |
| FLAIR    | Fluid-Attenuated Inversion Recovery | Removes fluid, highlights abnormal tissue like edema         |

Together, these give a **multiparametric** (multi-setting) view of brain tumors.

---

## **AI in Medical Imaging**

The idea is: Use **machine learning** to automatically:

* Detect tumors
* Segment (draw boundaries) around tumors
* Classify them as HGG or BM

In this paper, they used a **deep learning model** called **nnU-Net** to segment tumors.

**Segmentation** = "Find it and draw its outline"

In simple terms, **tumor segmentation** means “finding the exact location of a tumor in an MRI scan and outlining it pixel by pixel or voxel by voxel.” Imagine This: You are given a black-and-white photo of a forest and asked to:
* Find and color **only the trees** 
* Ignore the sky, grass, and animals

That’s **segmentation** — separating the part you're interested in (trees) from the rest (background).

In brain tumor segmentation:
* You are given an **MRI image** of the brain
* Your task is to **label only the tumor** (and sometimes its subregions)

In this paper, they segment two main tumor areas:

| Region                                    | What It Means                                                                   | Where It's Seen |
| ----------------------------------------- | ------------------------------------------------------------------------------- | --------------- |
| CE (Contrast-Enhancing)                   | The active, growing part of the tumor that lights up after contrast is injected | T1-ce images    |
| NCE (Non-Enhancing / FLAIR Abnormalities) | Edema or less active tumor areas                                                | FLAIR images    |

So, they create **two segmentation masks** for each patient:

* One for the CE region
* One for the NCE region



There are **two main ways** to do segmentation:

### 1. **Manual Segmentation**

* A doctor uses a tool like **ITK-SNAP** to draw outlines **by hand** on each MRI slice
* Very accurate, but **slow and time-consuming**

### 2. **Automated Segmentation**

* A **machine learning model** (like **nnU-Net**) is trained on examples
* It **learns how tumors look**, and then segments new images automatically
* Fast, but needs good training data


Imagine this simplified version of a brain image as a 2D matrix:

```text
[ 0 0 0 1 1 1 0 0 ]
[ 0 0 1 1 1 1 1 0 ]
[ 0 1 1 1 1 1 1 0 ]
[ 0 0 1 1 1 1 0 0 ]
```

* `1`s = tumor pixels
* `0`s = background/normal brain

This is the **segmentation mask**. We can overlay it on the original MRI image to visualize **where the tumor is**.


## **The MOTUM Dataset**

### Patients 

* **Total patients**: 67

  * **29** High-grade glioma (HGG)
  * **38** Brain metastases (BMs)
    → From Lung (20), Breast (10), Ovarian (4), Gastric (2), Melanoma (2)

All patients had:

* MRI scans
* Confirmed diagnosis from pathology
* Some had surgery or treatment information included

---

###  MRI Image Files

Each patient folder includes:

* **DICOM** and **NIfTI** files (medical image formats)
* 4 image types: FLAIR, T1, T1-ce, T2
* **Segmentation masks**:

  * CE (Contrast-enhancing tumor area)
  * NCE (Non-enhancing FLAIR abnormalities)
* Quality checked (only no or mild motion blur kept)

---

###  Tumor Segmentation

1. **Manual annotation** using **ITK-SNAP** tool for first 30 patients.
2. Used these to **train a 2D deep learning model (nnU-Net)**.
3. Applied model to the remaining 37 patients.
4. Doctors **visually checked and corrected** the segmentations.

They avoided 3D models due to:

* **Slice thickness of 5mm** (2D quality better)
* **Small dataset size**

**Dice Score** (a measure of segmentation accuracy):

* NCE (non-enhancing area): **0.902**
* CE (contrast-enhancing tumor): **0.587**


### Clinical Data

Also included:

* **Age, sex**
* **Tumor origin** (lung, breast, etc.)
* **Surgery info**
* **Immunohistochemistry** results
* **Molecular data** (where available)

This adds **context** to the image data — super useful for **training models** that combine imaging + clinical info.

---

### Dataset Organization (Structure)

* Stored in **BIDS format** (common in neuroimaging)
* For each subject (e.g., `sub-0001/`):

  ```
  sub-0001/
    anat/
      sub-0001_T1.nii.gz
      sub-0001_FLAIR.nii.gz
      ...
    derivatives/
      segmentations/
      radiomics_features/
  clinical_data.csv
  ```

---

### Preprocessing Pipeline

1. **Skull stripping**: Remove non-brain parts of image using **HD-BET**
2. **Co-registration**: Align all image sequences using **FSL**
3. **Convert DICOM to NIfTI**
4. **Check quality**
5. **Segmentation**
6. **Feature extraction**: Using **PyRadiomics**

---
## **Dice Score**

The **Dice Score**, or Dice Similarity Coefficient (DSC), is a commonly used evaluation metric for segmentation tasks. Dice Score tells you how much the predicted tumor region overlaps with the **true (ground truth) tumor region** drawn by a doctor.

### Dice Score Formula:

$$
\text{Dice Score} = \frac{2 \times |A \cap B|}{|A| + |B|}
$$

Where:

* **A** = Ground truth pixels (drawn by a doctor)
* **B** = Predicted pixels (output of the AI model)
* **|A ∩ B|** = Number of pixels that both A and B got correct (overlap)
* **|A| + |B|** = Total pixels in each region

---

### Dice Score Values:

| Dice Score | Interpretation                  |
| ---------- | ------------------------------- |
| 1.0        | Perfect overlap (AI = Doctor)   |
| 0.8–0.9    | Very good overlap               |
| 0.5–0.7    | Moderate overlap                |
| 0–0.4      | Poor segmentation               |

---

### Dice Scores in This Paper

| Region                            | Dice Score | Meaning                                |
| --------------------------------- | ---------- | -------------------------------------- |
| **NCE (Non-Enhancing Edema)**     | **0.902**  | Very high overlap — model did great!   |
| **CE (Contrast-Enhancing Tumor)** | **0.587**  | Moderate performance — model struggled |

---

### Why Did the Model Perform Better on NCE Than CE

#### 1. **Size of Regions**

* **NCE areas (edema)** are **larger** and easier to detect.
* **CE areas** are often **small, irregular, and patchy**, making it harder for the model to catch every part.

#### 2. **Visual Contrast**

* **Edema in FLAIR images** appears as **bright and well-defined**.
* **Enhancing tumors in T1-ce** might be **blurred**, mixed with blood vessels, or have **less clear boundaries**.

#### 3. **Training Data Limitation**

* Only 30 subjects had manual masks for training
* Small data size can limit how well the model generalizes, especially for **complex areas like CE**

In tumor segmentation:

* A **high Dice Score** means the model’s outline is reliable → usable in clinical practice
* A **low Dice Score** means we may need more training data, better preprocessing, or improved models
---

## **Radiomic Feature Extraction**

Using **PyRadiomics**, they extracted **110 features** per tumor.

Feature groups:

* **Shape**: 16 features (volume, surface area, compactness)
* **Intensity**: 18 features (mean, median, std. dev.)
* **Texture**:

  * GLCM (gray-level co-occurrence matrix): 24
  * GLRLM (run-length): 16
  * GLSZM (size zone): 16
  * NGTDM (tone difference): 5
  * GLDM (dependence): 14

These features can be used to:

* Train classifiers (e.g., SVM, Random Forest)
* Predict tumor type or survival

---

## **Uses of the dataset**

As a beginner in this field, you can:

1. **Visualize brain MRIs** with Python (e.g., `nibabel`, `matplotlib`)
2. **Explore segmentation** by overlaying masks
3. **Extract radiomics features** using PyRadiomics
4. **Train simple classifiers** (e.g., scikit-learn) on tumor types
5. **Try nnU-Net** to segment new images
6. Build tools to assist radiologists in diagnosis

---

## Dataset and Tools Links

* Dataset: [https://doi.gin.g-node.org/10.12751/g-node.tvzqc5](https://doi.gin.g-node.org/10.12751/g-node.tvzqc5)
* Code: [https://github.com/hongweilibran/MOTUM](https://github.com/hongweilibran/MOTUM)
* Segmentation Docker: [https://hub.docker.com/repository/docker/branhongweili/motum\_seg](https://hub.docker.com/repository/docker/branhongweili/motum_seg)

---
