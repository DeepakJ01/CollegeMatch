# 🎓 CollegeMatch - Maharashtra Engineering College Finder

A web application built with **FastAPI** to help students find the best engineering colleges in Maharashtra based on their CET scores, preferences, and category.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)
![Pandas](https://img.shields.io/badge/Pandas-1.3+-orange.svg)

---

## 🧠 Overview

This FastAPI-based web application allows students to:
- Enter their CET scores and category
- View a list of colleges in Maharashtra they may be eligible for
- Make informed decisions based on cutoffs and preferences

---

## 📁 Project Structure

## CollegeMatch/
#### ├── pycache/ - Python cache (ignored)
#### ├── venv/ - Virtual environment (ignored)
#### ├── final_output.csv - College dataset 
#### ├── index.html - Frontend interface
#### └── main.py - Backend server

---

## ⚙️ Setup Instructions

### 1. Create Virtual Environment

python -m venv venv

### 2. Activate Virtual Environment
For Windows:
.\venv\Scripts\activate

### 3. Install Dependencies

pip install fastapi pandas uvicorn

### 4. Run the Application

uvicorn main:app --reload

### 5. Access the Application
Open your browser and visit:
http://127.0.0.1:8000

## 📌 Important Notes
### 📊 Dataset Requirement:

Ensure final_output.csv is in the same directory as main.py

This file must contain the college data for the app to function properly
