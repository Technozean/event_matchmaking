Alright — here’s the **MySQL-optimized PRD** in `.md` format, keeping it beginner-friendly for a junior dev, Django + Tailwind, minimal dependencies, view-based functions, and OpenAI for querying event data.

---

# **Event Management & Networking Platform – MVP**

**Tech Stack:** Django (view-based functions), MySQL, Tailwind CSS, OpenAI API
**Dependencies:**

* `Django`
* `mysqlclient` (preferred) or `PyMySQL`
* `requests` (if needed for API calls)

---

## **1. Problem Statement**

When events are hosted, hosts and participants often lack visibility into **who is attending** and **what their background is**.
This limits networking opportunities, makes engagement harder, and underuses valuable attendee data.

---

## **2. Objective**

We want to build an event management platform that:

* Collects participant profiles before/during events.
* Allows structured Q\&A without interrupting sessions.
* Uses AI for **matchmaking** and **audience insights**.
* Lets users **query event data in natural language**.

---

## **3. Core MVP Features**

### **A. Event Creation & Registration**

* Host signs up and creates an event.
* Host adds **custom onboarding questions** (from templates or new).
* System generates **unique QR code** for participants.
* Participants scan code → fill registration form.

**Registration Form Fields**

* First Name, Last Name, Email (**mandatory**)
* Host-defined questions (**mandatory/optional**)

---

### **B. Host Questionnaire Templates**

* Pre-built templates for different event types (Tech Meetup, Startup Networking, HR & Talent, Education).
* Host can edit, add, remove questions.
* Question formats: **Multiple Choice, Short Text, Long Text, Rating Scale, Checkboxes**.

---

### **C. Participant Data Collection & Insights**

* Store all responses in **MySQL tables** (no Postgres-specific JSON queries).
* For filtering, **denormalize key fields**:

  * `skills` (comma-separated string)
  * `role`
  * `industry`
  * `experience_years`
  * `interests` (comma-separated string)
* AI-generated summaries:

  * Skill distribution
  * Industry spread
  * Seniority levels
  * Common interests

---

### **D. Public Q\&A Chat**

* Live Q\&A board during sessions.
* Participants post questions → others **upvote**.
* Host dashboard shows sorted questions by votes.

---

### **E. Participant Matchmaking**

* AI suggests participants with **similar skills, industry, interests**.
* Suggestions visible to both host & participants.

---

### **F. AI-Powered Event Data Chat**

* OpenAI API to query event data.
* **Hosts** can ask:

  * “Show all Python developers with 3+ years experience.”
  * “Which industries dominate this event?”
* **Participants** can ask:

  * “Who works in fintech?”
  * “How many share my interest in Web3?”

---

### **G. Smart Attendee Filtering**

* Host can prioritize certain attendees if event has a limit.
* Maintain **auto-managed waitlist**.

---

## **4. Models (MySQL-friendly)**

```python
from django.db import models

class Host(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)

class Event(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    qr_code_url = models.CharField(max_length=255, blank=True)

class OnboardingQuestion(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=50)  # MCQ, short_text, etc.
    is_mandatory = models.BooleanField(default=False)

class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField()
    skills = models.CharField(max_length=255, blank=True)  # comma-separated
    role = models.CharField(max_length=128, blank=True)
    industry = models.CharField(max_length=128, blank=True)
    experience_years = models.IntegerField(null=True, blank=True)
    interests = models.CharField(max_length=255, blank=True)

class QuestionResponse(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    question = models.ForeignKey(OnboardingQuestion, on_delete=models.CASCADE)
    answer = models.TextField()

class PublicQuestion(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    question_text = models.TextField()
    votes = models.IntegerField(default=0)
```

---

## **5. Views Approach**

* Use **view-based functions** (`views.py`) instead of DRF.
* Example:

```python
from django.shortcuts import render, redirect
from .models import Event

def create_event(request):
    if request.method == "POST":
        # Save event details
        ...
    return render(request, "create_event.html")
```

---

## **6. Tailwind Integration**

* Install Tailwind CSS locally.
* Use `npm` for building styles.
* Keep UI lightweight & responsive.

---

## **7. AI Query Handling**

* Create a helper function that fetches relevant DB data, formats it as text, and sends to **OpenAI API**.

```python
import openai

def query_event_data(prompt, data):
    openai.api_key = "YOUR_API_KEY"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a data assistant."},
                  {"role": "user", "content": prompt + "\n\nData:\n" + data}]
    )
    return response.choices[0].message["content"]
```

---

## **8. Success Metrics**

* % onboarding completion.
* No. of AI matchmaking connections.
* No. of questions posted/upvoted.
* Host satisfaction score.
