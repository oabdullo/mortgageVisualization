# 🚀 Deployment Guide - Mortgage Calculator

This guide will help you deploy your Streamlit mortgage calculator to free hosting platforms.

## 🌟 Recommended Free Hosting Options

### 1. **Streamlit Community Cloud** (Recommended)
- **Free tier**: Unlimited apps, 1GB RAM, 1 CPU
- **Best for**: Streamlit apps specifically
- **URL**: https://share.streamlit.io

#### Steps:
1. Push your code to GitHub
2. Go to https://share.streamlit.io
3. Sign in with GitHub
4. Click "New app"
5. Select your repository: `oabdullo/mortgageVisualization`
6. Set main file path: `app.py`
7. Click "Deploy!"

### 2. **Heroku** (Alternative)
- **Free tier**: 550-1000 dyno hours/month
- **Best for**: General web apps

#### Steps:
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Deploy: `git push heroku main`

### 3. **Railway** (Modern Alternative)
- **Free tier**: $5 credit monthly
- **Best for**: Easy deployment

#### Steps:
1. Go to https://railway.app
2. Connect GitHub
3. Select your repository
4. Deploy automatically

## 📁 Required Files (Already Created)

✅ `app.py` - Main Streamlit application
✅ `requirements.txt` - Python dependencies
✅ `Procfile` - Heroku deployment config
✅ `runtime.txt` - Python version
✅ `setup.sh` - Heroku setup script
✅ `.streamlit/config.toml` - Streamlit configuration

## 🔧 Local Testing

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Visit: http://localhost:8501

## 🚀 Quick Deploy to Streamlit Community Cloud

1. **Commit and push your changes:**
   ```bash
   git add .
   git commit -m "Add Streamlit web app"
   git push origin main
   ```

2. **Deploy to Streamlit:**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Repository: `oabdullo/mortgageVisualization`
   - Branch: `main`
   - Main file path: `app.py`
   - Click "Deploy!"

3. **Your app will be live at:**
   `https://your-app-name.streamlit.app`

## 🎯 Features of the Web App

- **Interactive Input**: Home price and down payment sliders
- **Real-time Calculations**: Instant loan comparisons
- **Beautiful Charts**: Plotly visualizations
- **Responsive Design**: Works on mobile and desktop
- **Data Export**: Download CSV files
- **Multiple Loan Options**: 15, 20, and 30-year terms

## 🔧 Customization

### Change Default Values
Edit `data/sample_loans.json`:
```json
{
  "home_price": 500000,
  "down_payment": 100000,
  "sample_loans": [...]
}
```

### Add More Loan Options
Add to `sample_loans` array:
```json
{
  "name": "25-Year @ 5.8%",
  "annual_rate": 0.058,
  "years": 25
}
```

### Customize Styling
Edit the CSS in `app.py` or modify `.streamlit/config.toml`

## 🐛 Troubleshooting

### Common Issues:

1. **Import Error**: Make sure all files are in the repository
2. **Port Error**: Check Procfile format
3. **Memory Error**: Reduce data size or upgrade hosting plan
4. **Slow Loading**: Optimize charts or reduce data points

### Debug Commands:
```bash
# Check requirements
pip check

# Test imports
python -c "import streamlit, plotly, pandas"

# Run with debug
streamlit run app.py --logger.level=debug
```

## 📊 Performance Tips

1. **Limit Data**: Only load necessary data
2. **Cache Results**: Use `@st.cache_data` for expensive calculations
3. **Optimize Charts**: Reduce data points for better performance
4. **Lazy Loading**: Load data only when needed

## 🔒 Security Notes

- No sensitive data is stored
- All calculations are client-side
- No user authentication required
- Safe for public deployment

## 📈 Monitoring

- **Streamlit Cloud**: Built-in analytics
- **Heroku**: Use Heroku metrics
- **Railway**: Built-in monitoring

## 🎉 Success!

Once deployed, your mortgage calculator will be available worldwide at your chosen URL!

Share it with friends, family, or on social media to help others make informed mortgage decisions.
