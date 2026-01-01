# 🌍 Multilingual Educational Assistant

**AI-Powered Tutor for Multiple Subjects & Languages**

Author: Pranay M

## Overview

A Llama-based AI tutor that teaches various subjects in 12+ languages. Features adaptive learning, interactive quizzes, personalized study plans, and step-by-step problem solving.

## Features

- **12 Languages**: English, Spanish, French, German, Italian, Portuguese, Chinese, Japanese, Korean, Hindi, Arabic, Russian
- **10 Subjects**: Mathematics, Physics, Chemistry, Biology, Computer Science, History, Geography, Literature, Economics, Philosophy
- **Adaptive Learning**: Adjusts to student level and learning style
- **Interactive Quizzes**: Auto-generated multiple-choice questions
- **Problem Solving**: Step-by-step solutions with explanations
- **Study Plans**: Personalized weekly learning schedules
- **Real-time Translation**: Convert content between languages
- **Chat Interface**: Natural conversation with your tutor

## Installation

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull Llama model
ollama pull llama3.2

# Install Python dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Menu Options

1. **Set Language** - Choose your preferred teaching language
2. **Select Subject** - Pick the subject to study
3. **Generate Lesson** - Create comprehensive lessons on any topic
4. **Explain Concept** - Get detailed explanations with analogies
5. **Solve Problem** - Step-by-step problem solutions
6. **Take Quiz** - Test your knowledge with auto-generated quizzes
7. **Study Plan** - Create personalized weekly study schedules
8. **Interactive Chat** - Have a conversation with your tutor
9. **Translate Content** - Translate educational content
10. **Set Profile** - Update learning level and style

## Example

```python
from main import MultilingualTutor

tutor = MultilingualTutor()
tutor.set_language("es")  # Spanish
tutor.set_subject(1)  # Mathematics

# Generate a lesson
lesson = tutor.generate_lesson("Pythagorean Theorem")
print(lesson)

# Take a quiz
quiz = tutor.quiz_student("Algebra", num_questions=5)
```

## License

MIT License
