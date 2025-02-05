  # 🎵 Spotify Multi-Page Interactive Dashboard

A multi-page **Spotify Dashboard** built using **Dash**, **Plotly**, and **Python**. This project visualizes Spotify track, artist, and user behavior data using various interactive charts, including **radar charts**, **sunburst charts**, **treemaps**, and more. Designed with a Spotify-inspired aesthetic, this dashboard helps analyze data interactively and intuitively.

---

## 🌟 **Features**
- 🎨 **Spotify-Themed Design:** Custom colors, animations, and layouts styled to reflect Spotify’s UI.
- 📊 **Multiple Data Visualizations:** Dynamic radar charts, treemaps, sunburst charts, and gauge plots provide deep insights.
- 🌐 **Multi-Page Navigation:** Easily switch between pages for genre analysis, artist insights, and user behavior tracking.
- 📈 **Interactive Filters:** Use dropdowns, sliders, and more to explore the data from different perspectives.

---

## 🚀 **Getting Started**
Follow the steps below to get the project up and running.

### **1. Clone the Repository**
```bash
git clone [https://github.com/your-repo/spotify-dashboard.git](https://github.com/Hemaksh14/Spotify-Dashboard.git)
cd spotify-dashboard
```
### **2. Create a Virtual Environment (Optional but Recommended)**
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```
### **4. Run the Application**
```bash
python app.py
```
The app will run locally.

## **📂 Project Structure**
```bash
spotify-dashboard/
│
├── Data/
│   ├── spotify_tracks_dataset.csv
│   ├── spotify_dataset.csv
│   ├── Spotify_User_Behavior_Dataset.xlsx
│   └── simulated_collaborations.csv
│
├── app.py                   # Main Dash app
├── requirements.txt         # List of dependencies
└── README.md                # Documentation
```

📄 **Pages & Visualizations**
-----------------------------

### 🔰 **1. Landing Page**
- **Bubbles animation:** Welcome animation using floating Spotify-themed bubbles.
- **Navigation link:** Click “Enter Dashboard” to access the main sections.

---

### 🎨 **2. For Artists**
Gain insights into collaboration and track features using:

- **Radar Chart:** Compare track features across genres using attributes like danceability, energy, and acousticness.
- **Word Cloud:** View popular song titles based on their popularity scores.
- **Tree Map:** Explore average popularity across genres.
- **Collaboration Graph:** Visualize collaborations between artists, with filters for popularity and collaboration reach.

---

### 👥 **3. User Behavior Insights**
Understand user behavior patterns through:

- **Sunburst Chart:** Explore subscription plans and willingness to upgrade.
- **Polar Chart:** Analyze the preferred time slots for listening to music by different age groups.
- **Gauge Plot:** Measure user satisfaction with music recommendations and podcast variety.
- **Circle Pack Diagram:** Visualize user clustering based on behavior like favorite genres and subscription plans.

---

### 📊 **4. Genre Popularity Insights**
- **Sunburst Chart:** Analyze genre popularity and artists contributing to each genre.
- **Interactive Filters:** Filter by genres and control the number of genres displayed dynamically.

---

🖌 **Customization**
--------------------

You can customize this project by modifying the following:

- **Colors:** Located in the custom styles section of `app.py`.
- **Datasets:** Replace the CSV and Excel files with your data in the `Data/` folder.
- **Visualizations:** Edit or add new charts using **Dash** and **Plotly** components.

---

🔧 **Dependencies**
-------------------

- **Dash:** For building web-based, interactive dashboards.
- **Plotly:** For creating rich and interactive visualizations.
- **NetworkX:** For creating collaboration graphs.
- **Matplotlib:** For generating the word cloud.
- **Pandas:** For data manipulation and processing.

Install these dependencies using:
```bash
pip install -r requirements.txt
```
