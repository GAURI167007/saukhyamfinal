from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os

print("APP FILE IS RUNNING")

app = Flask(__name__)
app.secret_key = "saukhyam_secret_key_123" # Simple secret key for development


@app.route("/")
def home():
    return render_template("saukhyam.html")

@app.route("/ai_insights")
def ai_insights():
    return render_template("ai_insights.html")

@app.route("/contacts")
def contacts():
    return render_template("contacts.html")

@app.route("/appointments")
def appointments():
    data_file = "appointments.json"
    appointments_list = []
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            try:
                appointments_list = json.load(f)
            except json.JSONDecodeError:
                appointments_list = []
    # Reverse the list to show newest first
    appointments_list.reverse() 
    return render_template("appointments.html", appointments=appointments_list)

@app.route("/doctorsconnect", methods=["GET", "POST"])
def doctorsconnect():
    if request.method == "POST":
        # Extract form data
        speciality = request.form.get("speciality")
        mode = request.form.get("mode")
        date = request.form.get("date")
        time = request.form.get("time")
        concern = request.form.get("concern")

        # Create appointment record
        appointment = {
            "speciality": speciality,
            "mode": mode,
            "date": date,
            "time": time,
            "concern": concern
        }

        # Save to JSON file
        data_file = "appointments.json"
        if os.path.exists(data_file):
            with open(data_file, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        data.append(appointment)

        with open(data_file, "w") as f:
            json.dump(data, f, indent=4)

        flash("Request submitted successfully! We will connect you shortly.", "success")
        return redirect(url_for("doctorsconnect"))

    return render_template("doctorsconnect.html")

@app.route("/book_appointment", methods=["POST"])
def book_appointment():
    # Extract form data
    speciality = request.form.get("speciality", "General")
    mode = request.form.get("mode", "In-person")
    date = request.form.get("date")
    time = request.form.get("time")
    concern = request.form.get("concern", "Not specified")

    # Create appointment record
    appointment = {
        "speciality": speciality,
        "mode": mode,
        "date": date,
        "time": time,
        "concern": concern
    }

    # Save to JSON file
    data_file = "appointments.json"
    data = []
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

    data.append(appointment)

    with open(data_file, "w") as f:
        json.dump(data, f, indent=4)

    flash("Appointment booked successfully!", "success")
    return redirect(request.referrer or url_for('home'))

@app.route("/healthtrack")
def healthtrack():
    return render_template("healthtrack.html")

@app.route("/library")
def library():
    return render_template("library.html")

@app.route("/mentalhealth")
def mentalhealth():
    return render_template("mentalhealth.html")

@app.route("/shopping")
def shopping():
    return render_template("shopping.html")

@app.route("/subscription")
def subscription():
    return render_template("subscription.html")

@app.route("/pregnancy")
def pregnancy():
    return render_template("pregnancy.html")

@app.route("/postpregnancy")
def postpregnancy():
    return render_template("postpregnancy.html")

@app.route("/menstrual")
def menstrual():
    return render_template("menstrual.html")



@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").lower()
    
    # Retrieve conversation context from session
    context = session.get("chat_context", None)
    
    # Simulate thinking time (0.5 to 1.5 seconds)
    import time, random
    time.sleep(random.uniform(0.5, 1.5))

    response, new_context = get_ai_response(user_message, context)

    # Save new context to session
    session["chat_context"] = new_context
    return {"response": response}

def get_ai_response(message, context):
    msg = message.lower()
    
    # --- TOPIC: POSITIVE EMOTIONS (New) ---
    if "excited" in msg or "happy" in msg or "great" in msg or "good" in msg or "wonderful" in msg or "amazing" in msg:
        return "That's wonderful to hear! I'm so glad you're feeling good. Holding onto these positive moments is great for your mental well-being. What's making you feel this way?", "positive_vibes"

    # --- TOPIC: DATA INSIGHTS & METRICS ---
    if "hrv" in msg or "variability" in msg:
        return "I noticed your Heart Rate Variability (HRV) is a bit lower than usual. This often happens when you're tired or in the luteal phase of your cycle. It's your body's way of asking for a little extra rest. Maybe try a gentle yoga session or an early night today?", None

    elif "heart rate" in msg or "hr" in msg or "bpm" in msg:
        return "It looks like your resting heart rate is slightly elevated. You might be feeling a bit stressed or dehydrated. Please take a moment to breathe and have some water. If it stays high for a few days, it might be worth checking your iron levels, just to be safe.", None

    elif "score" in msg or "grade" in msg:
        return "Your health score is a reflection of how you've been doing lately. Remember, a 'Medium' or 'Low' score isn't a bad grade—it's just a gentle nudge to prioritize yourself today. You deserve to feel your best.", None

    elif "pattern" in msg or "trend" in msg:
        return "I've noticed a pattern where your energy tends to dip when your sleep drops below 6 hours. It's completely understandable. Try to be kind to yourself on those days, and maybe squeeze in a short nap if you can.", None

    # --- TOPIC: PHYSICAL SYMPTOMS ---
    elif "headache" in msg or "migraine" in msg:
        return "Headaches can be draining. Have you had enough water today? Sometimes dehydration or screen time is the culprit. A cool compress or resting in a dark room might help soothe it.", None

    elif "fever" in msg or "temperature" in msg or "hot" in msg:
        return "If you're feeling feverish, your body is fighting something off. Please prioritize rest and hydration. If your temperature goes above 102°F (39°C) or lasts more than a few days, seeing a doctor is best.", None

    elif "cold" in msg or "flu" in msg or "cough" in msg or "sneeze" in msg:
        return "I'm sorry you're feeling under the weather. Warm fluids like ginger tea or soup can be very comforting. Rest is your best medicine right now.", None

    elif "stomach" in msg or "nausea" in msg or "vomit" in msg or "digestion" in msg:
        return "Stomach discomfort is awful. Ginger or peppermint tea can settle nausea. Try sticking to plain foods like toast or rice for a bit. If pain is severe, please see a doctor.", None
        
    elif "dizzy" in msg or "lightheaded" in msg or "faint" in msg:
        return "Please sit or lie down immediately if you feel dizzy. It could be low blood sugar, dehydration, or low iron. Sip some water or juice slowly. If it happens often, a check-up is a good idea.", None

    elif "fatigue" in msg or "tired" in msg or "exhausted" in msg or "weary" in msg:
        return "Chronic fatigue can be a sign of anemia, thyroid issues, or just burnout. Listen to your body—rest isn't lazy, it's necessary. Have you had your iron levels checked recently?", None

    elif "back pain" in msg or "ache" in msg or "sore" in msg:
        return "Back pain is common, especially with stress or long sitting. Gentle stretching or a warm bath can work wonders. If it's sharp or persistent, physiotherapy might help.", None

    # --- TOPIC: WOMEN'S HEALTH ---
    elif "cramp" in msg or "pain" in msg and ("period" in msg or "menstrual" in msg):
        return "Period cramps can be so tough. A hot water bottle on your lower belly and some magnesium might help relax the muscles. Be gentle with yourself today.", None

    elif "pms" in msg or "moody" in msg or "irritated" in msg:
        return "PMS is real and valid. Your hormones are shifting, and it's okay to feel a bit off. Try to reduce caffeine and salt, and give yourself permission to rest.", None

    elif "spotting" in msg or "bleed" in msg:
        return "Spotting can happen for many reasons—ovulation, stress, or hormonal shifts. If it's heavy or accompanied by pain, tracking it and showing your doctor is a good plan.", None

    elif "cycle" in msg or "period" in msg or "late" in msg or "irregular" in msg:
        return "Cycles can vary with stress, diet, or travel. If it's consistently irregular, it might be worth discussing PCOD/PCOS with a specialist. Tracking helps find patterns.", None

    elif "menopause" in msg or "flash" in msg:
        return "Menopause is a major transition. Hot flashes and sleep changes are common. Cooling foods, layering clothes, and talking to others going through it can really help.", None
    
    elif "pregnancy" in msg or "baby" in msg:
        return "Pregnancy is a beautiful but demanding journey. Prioritize folic acid, protein, and rest. We have a dedicated Pregnancy section if you need specific trimester guides.", None

    # --- TOPIC: MENTAL HEALTH ---
    elif "anxiety" in msg or "anxious" in msg or "worry" in msg or "panic" in msg:
        return "Anxiety can feel overwhelming, like a wave. Try the 5-4-3-2-1 grounding technique: name 5 things you see, 4 you feel, 3 you hear... It helps bring you back to the present.", None
    
    elif "depress" in msg or "sad" in msg or "hopeless" in msg or "cry" in msg:
        return "I'm so sorry you're feeling this weight. You don't have to carry it alone. Reaching out to a trusted friend or therapist can be a lifeline. You matter.", None
    
    elif "stress" in msg or "overwhelmed" in msg or "burnout" in msg:
        return "You're carrying a lot. Remember, you can't pour from an empty cup. What is one small thing you can drop or delegate today to give yourself some breathing room?", None

    elif "lonely" in msg or "alone" in msg:
        return "Loneliness is a heavy feeling. Even though I'm an AI, I'm here listening. Connecting with a community or a hobby group can sometimes spark a little light.", None

    # --- TOPIC: LIFESTYLE & WELLNESS ---
    elif "sleep" in msg or "insomnia" in msg or "awake" in msg:
        return "Good sleep feels elusive sometimes. A cool, dark room and a 'brain dump' journal before bed can help quiet the mind. Have you tried 4-7-8 breathing?", None
    
    elif "diet" in msg or "food" in msg or "eat" in msg or "nutrition" in msg:
        return "Food is fuel, but it's also joy. Aim for a rainbow on your plate—colorful veggies provide antioxidants. And don't forget protein for sustained energy!", None
    
    elif "water" in msg or "hydrate" in msg or "drink" in msg:
        return "Hydration is your superpower! It helps meaningful focus, skin health, and energy. If plain water is boring, try adding a slice of lemon or cucumber.", None
    
    elif "exercise" in msg or "workout" in msg or "active" in msg:
        return "Movement is medicine. It doesn't have to be a gym session—a 20-minute dance in your room or a brisk walk counts! Do what makes your body feel good.", None

    # --- TOPIC: GREETINGS & EXTRAS ---
    elif "hello" in msg or "hi" in msg or "hey" in msg:
        return "Hello! I'm here to support you with symptom checks, wellness tips, or just a listening ear. How are you feeling right now?", "greeting"
    
    elif "thank" in msg or "thanks" in msg:
        return "You are so welcome. Take good care of yourself.", None
    
    elif "who are you" in msg or "what are you" in msg or "bot" in msg:
        return "I am your Saukhyam Personal Health Assistant. I'm here to listen, offer wellness tips, and help you understand your body and mind better.", None

    elif "help" in msg or "can you do" in msg:
        return "I can help you check your symptoms, offer tips for anxiety or sleep, or just chat if you're feeling lonely. If you need medical advice, please check the 'Doctors Connect' section.", None

    # --- CONTEXT: FOLLOW-UPS ---
    elif context == "positive_vibes":
        return "Thanks for sharing that joy with me! It's contagious. Is there anything else on your mind?", None
    elif context == "wellness_check_positive":
        return "I love hearing that! Focusing on the good moments builds resilience. Keep going!", None

    elif context == "greeting":
        return "Thanks for sharing. Whether it's a physical symptom or just a feeling, I'm here to help you navigate it.", None

    # --- FALLBACK ---
    return "I hear you. While I'm still learning about every specific condition, I want to support you. Could you tell me a bit more about what you're feeling? Or, for persistent symptoms, glancing at our 'Doctors Connect' page might be helpful.", "listening"

if __name__ == "__main__":
    print("STARTING FLASK SERVER")
    app.run(debug=True)