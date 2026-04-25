

# Create your views here.
import random,os
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Response


# ── Helpers ───────────────────────────────────────────────────────────────────

WRONG_DATE_MESSAGES = [
    "Nice try… but you're not her 😏",
    "Unauthorized human detected 🚫",
    "Access denied. Are you even Anuska? 🤔",
    "Hmm… that doesn't seem right 👀",
    "Wrong answer! Did you guess? 😂",
    "404: You Not Found in the list 🙅",
    "This is a top-secret mission. Try again 🕵️",
]

REJECTION_TAUNTS = [
    "She said no again 💀 Still sending emails tho 😅",
    "Another rejection logged. Respect the grind 🙏",
    "Statistically, she has to say yes eventually… right? 📊",
]





def save_response(request, step_name, answer):
    session_key = request.session.session_key or ""
    Response.objects.create(
        step_name=step_name,
        answer=answer,
        session_key=session_key,
    )


# ── Views ─────────────────────────────────────────────────────────────────────

def login_view(request):
    request.session.flush()

    error = None

    if request.method == 'POST':
        day = request.POST.get('day', '').strip()
        month = request.POST.get('month', '').strip().lower()

        print("LOGIN INPUT:", day, month)

        if day == '17' and month in {'september', 'sep', '9', '09'}:
            
            request.session.flush()  # reset session
            request.session['authenticated'] = True
            request.session['rejection_count'] = 0

            print("SESSION SET:", request.session.items())

            return redirect('step2')  # direct URL

        else:
            error = random.choice(WRONG_DATE_MESSAGES)

    return render(request, 'invite/login.html', {'error': error})

def welcome_view(request):
    print("WELCOME SESSION:", request.session.items())

    if not request.session.get('authenticated'):
        return redirect('/')

    return render(request, 'invite/welcome.html')


def step2_view(request):
    if not request.session.get('authenticated'):
        return redirect('login')

    if request.method == 'POST':
        answer = request.POST.get('answer')
        save_response(request, 'Library Question', answer)

        if answer == 'yes':
            send_web3_email(request.session.session_key)  # 🔥 SEND MAIL
            return redirect('success_library')
        else:
            return redirect('loading')

    return render(request, 'invite/step2.html')


def loading_view(request):
    """Fake loading screen between steps."""
    if not request.session.get('authenticated'):
        return redirect('login')
    next_step = request.GET.get('next', 'step3')
    return render(request, 'invite/loading.html', {'next_step': next_step})


def step3_view(request):
    if not request.session.get('authenticated'):
        return redirect('login')

    if request.method == 'POST':
        answer = request.POST.get('answer')
        save_response(request, 'Persuasion 1', answer)

        if answer == 'yes':
            send_web3_email(request.session.session_key)  # 🔥 SEND MAIL
            return redirect('success_library')
        else:
            request.session['rejection_count'] = request.session.get('rejection_count', 0) + 1
            return redirect('loading')

    return render(request, 'invite/step3.html')

def step4_view(request):
    if not request.session.get('authenticated'):
        return redirect('login')

    if request.method == 'POST':
        answer = request.POST.get('answer')
        save_response(request, 'Persuasion 2', answer)

        if answer == 'yes':
            send_web3_email(request.session.session_key)  # 🔥 SEND MAIL
            return redirect('success_library')
        else:
            request.session['rejection_count'] = request.session.get('rejection_count', 0) + 1
            return redirect('loading')

    return render(request, 'invite/step4.html')


def step5_view(request):
    """Step 5: Coffee fallback."""
    if not request.session.get('authenticated'):
        return redirect('login')

    if request.method == 'POST':
        answer = request.POST.get('answer')
        save_response(request, 'Coffee Plan B', answer)
        if answer == 'yes':
            return redirect('success_coffee')
        else:
            count = request.session.get('rejection_count', 0) + 1
            request.session['rejection_count'] = count
            return redirect('final_rejection')

    return render(request, 'invite/step5.html')

def success_library_view(request):
    if not request.session.get('authenticated'):
        return redirect('login')

    save_response(request, 'Final Answer', 'ACCEPTED — Library 📚')

    send_web3_email(request.session.session_key)  # 🔥
    print("🔥 SUCCESS LIBRARY HIT")

    return render(request, 'invite/success_library.html')

def success_coffee_view(request):
    if not request.session.get('authenticated'):
        return redirect('login')

    save_response(request, 'Final Answer', 'ACCEPTED — Coffee ☕')

    send_web3_email(request.session.session_key)  # 🔥

    return render(request, 'invite/success_coffee.html')


def final_rejection_view(request):
    if not request.session.get('authenticated'):
        return redirect('login')

    count = request.session.get('rejection_count', 1)
    taunt = random.choice(REJECTION_TAUNTS)

    save_response(request, 'Final Answer', f'REJECTED (×{count}) 💀')

    send_web3_email(request.session.session_key)  # 🔥

    return render(request, 'invite/final_rejection.html', {
        'rejection_count': count,
        'taunt': taunt,
    })


def logout_view(request):
    request.session.flush()
    return redirect('login')


import requests

def send_web3_email(session_key):
    try:
        print("🔥 WEB3 FUNCTION CALLED")

        responses = Response.objects.filter(session_key=session_key)

        message = "📊 Full Response Summary:\n\n"
        for r in responses:
            message += f"{r.step_name} → {r.answer}\n"

        data = {
            "access_key": os.getenv("WEB3FORMS_KEY"),
            "subject": "Anuska Invite Response 💌",
            "from_name": "Invite App",
            "message": message,
            "email": "praprasanna0310@gmail.com"
        }

        res = requests.post("https://api.web3forms.com/submit", data=data)
        print("🔥 WEB3 RESPONSE:", res.text)   # 👈 IMPORTANT

    except Exception as e:
        print("WEB3 ERROR:", e)