# Triangle Rasterization & Shading

This project was developed as part of a university course in **Computer Graphics** and corresponds to the first assignment of the course, focusing on fundamental rendering techniques and triangle rasterization.

---

## 📌 Overview

The goal of this project is to implement a triangle rasterization pipeline and apply different shading techniques.

Given a set of vertices, triangle definitions, colors, and depth information, the system reconstructs a 2D image by:

- Filling triangles on a pixel grid
- Applying shading techniques (Flat & Gouraud)
- Handling depth ordering

---

## ✨ Features

- Triangle rasterization using scanline-based logic
- Linear interpolation between vectors(`vector_interp`) in order to use it for color computation in Gouraud Shading during scanline-based triangle filling
- Flat shading (constant color per triangle)
- Gouraud shading (smooth color interpolation)
- Depth-based triangle rendering
- Modular and reusable Python functions

---

## 🛠️ Technologies

- Python 3
- NumPy
- Matplotlib
- OpenCV

---

## 📂 Repository Structure

```
triangle-rasterization-and-shading
│
├── src/                    # Python source code
│ ├── demo_f.py
│ ├── demo_g.py
│ ├── f_shading.py
│ ├── g_shading.py
│ ├── render_img.py
│ ├── vector_interp.py
│ ├── compute_lines_triangle.py
│ └── sort_vertices.py
│
├── data/                   # Input data
│ └── hw1.npy
│
├── outputs/                # Generated images
│ ├── flat_shading.png
│ └── gouraud_shading.png
│
├── docs/                   # Documentation
│ ├── hw1_2024.pdf
│ └── report.pdf
│
├── README.md
└── .gitignore

```
---

## ⚙️ How to Run

### 1. Requirements

Make sure you have the following installed:

- Python 3.x  
- NumPy  
- Matplotlib  
- OpenCV  

You can install the required libraries using:

```bash
pip install numpy matplotlib opencv-python

```

### 2. Run the demos

Navigate to the src/ folder and run:

- python demo_f.py
- python demo_g.py

The demo scripts load the required input data internally and generate the final rendered images.
The required input data is provided in the data/ folder.

---

## 🧠 Key Concepts

- Triangle rasterization
- Scanline algorithms
- Linear interpolation
- Shading techniques (Flat & Gouraud)
- Depth sorting

---

## 📄 Notes

- The implementation focuses on algorithmic clarity, not real-time performance.
- Additional helper functions were implemented for better code organization.
- The project demonstrates rendering without using high-level graphics engines.
- OpenCV (cv2) is used for image post-processing (scaling and color format conversion) before saving the final output.