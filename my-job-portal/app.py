import requests
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "career_hub_secret_key"

# --- ADZUNA API CREDENTIALS (Updated) ---
ADZUNA_APP_ID = "8e4b4cbe"
ADZUNA_API_KEY = "52a697152c900c4e8c391e563cae6855"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/jobs')
def jobs():
    # URL se 'title' nikalna (e.g., /jobs?title=Python)
    query = request.args.get('title')
    
    # Agar query khali hai (pehle baar load hone par), toh 'Software' dikhao
    # Agar user ne kuch likha hai, toh wahi search karo
    search_term = query if query else "Software Engineer"
    
    location = "Lucknow"
    
    # API Call
    url = f"https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {
        'app_id': ADZUNA_APP_ID,
        'app_key': ADZUNA_API_KEY,
        'results_per_page': 8,
        'what': search_term, # Yahan search_term jayega
        'where': location,
        'content-type': 'application/json'
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        live_jobs = []
        # 'for' wali line 'live_jobs' ke bilkul niche honi chahiye
        for result in data.get('results', []):
            # 'append' wali line 'for' ke andar honi chahiye (thoda aage)
            live_jobs.append({
                "title": result.get('title'),
                "company": result.get('company', {}).get('display_name', 'Verified Recruiter'),
                "loc": result.get('location', {}).get('display_name', 'Lucknow'),
                "link": result.get('redirect_url'),
                "desc": result.get('description', '')[:120] + "..."
            })
    except Exception as e:
        print(f"Error: {e}")
        live_jobs = []

    return render_template('jobs.html', jobs=live_jobs)
@app.route('/analyzer')
def analyzer():
    return render_template('analyzer.html')

@app.route('/tracking')
def tracking():
    # Dummy data for tracking (Isse aap baad mein database se connect kar sakte hain)
    applications = [
        {"job": "Python Developer", "status": "Under Review", "date": "2026-05-01"},
        {"job": "Web Designer", "status": "Applied", "date": "2026-05-04"}
    ]
    return render_template('tracking.html', apps=applications)

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get("message", "").lower()
    
    # Simple AI Logic for Bot
    if "track" in user_msg or "application" in user_msg:
        reply = "Aapki last application 'Python Developer' ke liye abhi 'Under Review' status mein hai."
    elif "analyze" in user_msg or "resume" in user_msg:
        reply = "Resume analyzer page par jayein aur apna PDF upload karein taaki hum score nikaal sakein."
    elif "java" in user_msg or "python" in user_msg:
        reply = f"Maine Lucknow mein kuch naye {user_msg} jobs dekhi hain, please Jobs page check karein."
    elif "hi" in user_msg or "hello" in user_msg:
        reply = "Hello! Main Career Hub AI Assistant hoon. Main aapki kya madad kar sakta hoon?"
    else:
        reply = "Main samajh nahi paya, kya aap career ya job se juda kuch aur puchna chahte hain?"
    
    return jsonify({"reply": reply})

@app.route('/logout')
def logout():
    session.clear()  # Saara login data clear ho jayega
    return redirect('/')  # User ko wapas login page par bhej dega
if __name__ == '__main__':
    # Debug mode ON rakha hai taaki errors turant dikhen
    app.run(debug=True)
