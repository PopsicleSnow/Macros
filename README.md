# UC Berkeley Dining Hall Macro Calculator 🍽️

A web application that helps UC Berkeley students track their macronutrient intake from campus dining halls and cafes. Calculate calories, protein, carbohydrates, fat, and sugar content from your meals with real-time menu data.

**🌐 Live Demo:** https://macros.kuljitu.com/

## 📋 Features

### Supported Dining Locations
- **Crossroads** - The largest dining hall on campus
- **Foothill** - Convenient dining for students in the hills
- **Cafe 3** - Quick meals and snacks
- **Clark Kerr** - Dining for Clark Kerr Campus residents
- **GBC** (Golden Bear Cafe) - Campus center dining
- **Browns** - Convenient campus dining option

### Nutrition Tracking
- ✅ **Calorie calculation** - Track your daily energy intake
- ✅ **Macronutrient breakdown** - Monitor protein, carbs, and fat
- ✅ **Sugar content** - Keep track of sugar consumption
- ✅ **Real-time menu data** - Always up-to-date with current offerings
- ✅ **Portion control** - Customize serving sizes for accurate tracking

## 🛠️ Technology Stack

- **Backend:** Python Flask
- **Database:** Google Cloud Firestore
- **Deployment:** Google App Engine
- **Data Source:** UC Berkeley Dining Menu APIs
- **Frontend:** HTML, CSS, JavaScript

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Google Cloud SDK (for deployment)
- Google Cloud Project with Firestore enabled

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Macros
   ```

2. **Set up virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Cloud credentials**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
   ```

5. **Run the application**
   ```bash
   python main.py
   ```
   
   The app will be available at `http://127.0.0.1:8080`

### Production Deployment

This application is designed to run on Google App Engine:

1. **Configure Google Cloud**
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Deploy to App Engine**
   ```bash
   gcloud app deploy
   ```

3. **Deploy cron jobs** (for automatic menu updates)
   ```bash
   gcloud app deploy cron.yaml
   ```

## 📁 Project Structure

```
Macros/
├── main.py              # Flask application and routes
├── locations.py         # Dining hall data fetching
├── query_firestore.py   # Database query operations
├── update_firestore.py  # Database update operations
├── menu.py             # Menu processing utilities
├── app.yaml            # App Engine configuration
├── cron.yaml           # Scheduled task configuration
├── requirements.txt    # Python dependencies
├── static/             # CSS, JS, images, and icons
├── templates/          # HTML templates
└── venv/              # Virtual environment (local)
```

## 🔧 Configuration

### Environment Variables
- `GOOGLE_APPLICATION_CREDENTIALS` - Path to Google Cloud service account key
- `GOOGLE_CLOUD_PROJECT` - Your Google Cloud project ID

### Firestore Collections
- `locations` - Available dining hall information
- `[location_name]` - Menu data for each dining hall

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on this repository
- Visit the live application at https://macros.kuljitu.com/

