#!/usr/bin/env python3
"""
Multilingual Educational Assistant - Llama-Based AI Tutor
Teaches various subjects in multiple languages
Author: Pranay M
"""

import ollama
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.markdown import Markdown
from langdetect import detect
import json
import os

console = Console()

SUPPORTED_LANGUAGES = {
    "en": "English", "es": "Spanish", "fr": "French", "de": "German",
    "it": "Italian", "pt": "Portuguese", "zh": "Chinese", "ja": "Japanese",
    "ko": "Korean", "hi": "Hindi", "ar": "Arabic", "ru": "Russian"
}

SUBJECTS = {
    1: "Mathematics",
    2: "Physics", 
    3: "Chemistry",
    4: "Biology",
    5: "Computer Science",
    6: "History",
    7: "Geography",
    8: "Literature",
    9: "Economics",
    10: "Philosophy"
}

class MultilingualTutor:
    def __init__(self, model: str = "llama3.2"):
        self.model = model
        self.current_language = "en"
        self.current_subject = None
        self.conversation_history = []
        self.student_profile = {"level": "intermediate", "learning_style": "visual"}
        
    def set_language(self, lang_code: str):
        if lang_code in SUPPORTED_LANGUAGES:
            self.current_language = lang_code
            return True
        return False
    
    def set_subject(self, subject_id: int):
        if subject_id in SUBJECTS:
            self.current_subject = SUBJECTS[subject_id]
            return True
        return False
    
    def detect_language(self, text: str) -> str:
        try:
            detected = detect(text)
            return detected if detected in SUPPORTED_LANGUAGES else "en"
        except:
            return "en"
    
    def generate_lesson(self, topic: str) -> str:
        lang_name = SUPPORTED_LANGUAGES[self.current_language]
        prompt = f"""You are an expert {self.current_subject} tutor teaching in {lang_name}.
        
Create a comprehensive lesson on: {topic}

Structure your lesson as follows:
1. Introduction - What the student will learn
2. Key Concepts - Main ideas explained simply
3. Examples - Practical examples with step-by-step explanations
4. Practice Problems - 3 problems for the student to try
5. Summary - Key takeaways

Respond entirely in {lang_name}. Use clear, educational language appropriate for a {self.student_profile['level']} level student.
Adapt your teaching style for {self.student_profile['learning_style']} learners."""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    
    def explain_concept(self, concept: str) -> str:
        lang_name = SUPPORTED_LANGUAGES[self.current_language]
        prompt = f"""You are an expert {self.current_subject} tutor. A student asks about: {concept}

Explain this concept in {lang_name}:
1. Simple definition
2. Real-world analogy
3. Visual description (describe what it looks like)
4. Common misconceptions
5. How it connects to other concepts

Use clear language for a {self.student_profile['level']} level student."""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    
    def solve_problem(self, problem: str) -> str:
        lang_name = SUPPORTED_LANGUAGES[self.current_language]
        prompt = f"""You are an expert {self.current_subject} tutor helping solve a problem.

Problem: {problem}

Provide a detailed solution in {lang_name}:
1. Understand the problem - What are we asked to find?
2. Identify given information
3. Choose the approach/formula
4. Step-by-step solution with explanations
5. Final answer with verification
6. Tips for similar problems

Make sure each step is clear and educational."""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    
    def quiz_student(self, topic: str, num_questions: int = 5) -> dict:
        lang_name = SUPPORTED_LANGUAGES[self.current_language]
        prompt = f"""Create a quiz about {topic} in {self.current_subject}.

Generate {num_questions} multiple-choice questions in {lang_name}.

Return as JSON:
{{
    "questions": [
        {{
            "question": "Question text",
            "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
            "correct": "A",
            "explanation": "Why this is correct"
        }}
    ]
}}

Make questions appropriate for {self.student_profile['level']} level."""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        try:
            content = response['message']['content']
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(content[start:end])
        except:
            pass
        return {"questions": []}
    
    def translate_content(self, content: str, target_lang: str) -> str:
        target_name = SUPPORTED_LANGUAGES.get(target_lang, "English")
        prompt = f"""Translate the following educational content to {target_name}.
Maintain the educational tone and technical accuracy.
Preserve any formulas, equations, or special notation.

Content:
{content}

Provide only the translation, no additional commentary."""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    
    def adaptive_feedback(self, student_answer: str, correct_answer: str, topic: str) -> str:
        lang_name = SUPPORTED_LANGUAGES[self.current_language]
        prompt = f"""You are a supportive {self.current_subject} tutor providing feedback.

Topic: {topic}
Student's Answer: {student_answer}
Correct Answer: {correct_answer}

Provide encouraging, constructive feedback in {lang_name}:
1. Acknowledge what the student did correctly
2. Gently explain any errors
3. Provide hints for improvement
4. Suggest next steps for learning

Be supportive and motivating while being accurate."""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    
    def create_study_plan(self, goals: str, duration_weeks: int) -> str:
        lang_name = SUPPORTED_LANGUAGES[self.current_language]
        prompt = f"""Create a personalized {self.current_subject} study plan in {lang_name}.

Student Goals: {goals}
Duration: {duration_weeks} weeks
Level: {self.student_profile['level']}
Learning Style: {self.student_profile['learning_style']}

Create a detailed weekly plan including:
1. Weekly objectives
2. Topics to cover
3. Recommended resources
4. Practice exercises
5. Milestones and checkpoints

Make it realistic and achievable."""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    
    def interactive_chat(self, message: str) -> str:
        detected_lang = self.detect_language(message)
        if detected_lang != self.current_language:
            self.current_language = detected_lang
        
        self.conversation_history.append({"role": "user", "content": message})
        
        lang_name = SUPPORTED_LANGUAGES[self.current_language]
        system_prompt = f"""You are a helpful, patient {self.current_subject} tutor.
Respond in {lang_name}. Be encouraging and educational.
Level: {self.student_profile['level']}
Previous context: {len(self.conversation_history)} messages exchanged."""

        messages = [{"role": "system", "content": system_prompt}] + self.conversation_history[-10:]
        
        response = ollama.chat(model=self.model, messages=messages)
        assistant_message = response['message']['content']
        
        self.conversation_history.append({"role": "assistant", "content": assistant_message})
        return assistant_message


def display_menu():
    table = Table(title="🌍 Multilingual Educational Assistant", show_header=True)
    table.add_column("Option", style="cyan", width=6)
    table.add_column("Feature", style="green")
    table.add_column("Description", style="white")
    
    table.add_row("1", "Set Language", "Choose your preferred language")
    table.add_row("2", "Select Subject", "Pick a subject to study")
    table.add_row("3", "Generate Lesson", "Create a lesson on any topic")
    table.add_row("4", "Explain Concept", "Get detailed explanation")
    table.add_row("5", "Solve Problem", "Step-by-step problem solving")
    table.add_row("6", "Take Quiz", "Test your knowledge")
    table.add_row("7", "Study Plan", "Create personalized study plan")
    table.add_row("8", "Interactive Chat", "Chat with your tutor")
    table.add_row("9", "Translate Content", "Translate to another language")
    table.add_row("10", "Set Profile", "Update your learning profile")
    table.add_row("0", "Exit", "Close the application")
    
    console.print(table)


def main():
    console.print(Panel.fit(
        "[bold blue]🌍 Multilingual Educational Assistant[/bold blue]\n"
        "[green]AI-Powered Tutor for Multiple Subjects & Languages[/green]\n"
        "[dim]Author: Pranay M[/dim]",
        border_style="blue"
    ))
    
    tutor = MultilingualTutor()
    
    while True:
        display_menu()
        choice = Prompt.ask("\n[cyan]Select option[/cyan]", default="0")
        
        if choice == "0":
            console.print("[yellow]Goodbye! Keep learning! 📚[/yellow]")
            break
            
        elif choice == "1":
            console.print("\n[bold]Available Languages:[/bold]")
            for code, name in SUPPORTED_LANGUAGES.items():
                console.print(f"  {code}: {name}")
            lang = Prompt.ask("Enter language code", default="en")
            if tutor.set_language(lang):
                console.print(f"[green]✓ Language set to {SUPPORTED_LANGUAGES[lang]}[/green]")
            else:
                console.print("[red]Invalid language code[/red]")
                
        elif choice == "2":
            console.print("\n[bold]Available Subjects:[/bold]")
            for sid, name in SUBJECTS.items():
                console.print(f"  {sid}: {name}")
            subject_id = IntPrompt.ask("Select subject", default=1)
            if tutor.set_subject(subject_id):
                console.print(f"[green]✓ Subject set to {tutor.current_subject}[/green]")
            else:
                console.print("[red]Invalid subject[/red]")
                
        elif choice == "3":
            if not tutor.current_subject:
                console.print("[yellow]Please select a subject first (option 2)[/yellow]")
                continue
            topic = Prompt.ask("Enter topic for the lesson")
            with console.status("[bold green]Generating lesson..."):
                lesson = tutor.generate_lesson(topic)
            console.print(Panel(Markdown(lesson), title="📚 Lesson", border_style="green"))
            
        elif choice == "4":
            if not tutor.current_subject:
                console.print("[yellow]Please select a subject first (option 2)[/yellow]")
                continue
            concept = Prompt.ask("Enter concept to explain")
            with console.status("[bold green]Explaining concept..."):
                explanation = tutor.explain_concept(concept)
            console.print(Panel(Markdown(explanation), title="💡 Explanation", border_style="blue"))
            
        elif choice == "5":
            if not tutor.current_subject:
                console.print("[yellow]Please select a subject first (option 2)[/yellow]")
                continue
            problem = Prompt.ask("Enter the problem to solve")
            with console.status("[bold green]Solving problem..."):
                solution = tutor.solve_problem(problem)
            console.print(Panel(Markdown(solution), title="🔢 Solution", border_style="cyan"))
            
        elif choice == "6":
            if not tutor.current_subject:
                console.print("[yellow]Please select a subject first (option 2)[/yellow]")
                continue
            topic = Prompt.ask("Enter quiz topic")
            num_q = IntPrompt.ask("Number of questions", default=5)
            with console.status("[bold green]Generating quiz..."):
                quiz = tutor.quiz_student(topic, num_q)
            
            score = 0
            for i, q in enumerate(quiz.get("questions", []), 1):
                console.print(f"\n[bold]Question {i}:[/bold] {q['question']}")
                for opt in q['options']:
                    console.print(f"  {opt}")
                answer = Prompt.ask("Your answer (A/B/C/D)").upper()
                if answer == q['correct']:
                    score += 1
                    console.print("[green]✓ Correct![/green]")
                else:
                    console.print(f"[red]✗ Incorrect. Correct: {q['correct']}[/red]")
                console.print(f"[dim]{q['explanation']}[/dim]")
            
            console.print(f"\n[bold]Final Score: {score}/{len(quiz.get('questions', []))}[/bold]")
            
        elif choice == "7":
            if not tutor.current_subject:
                console.print("[yellow]Please select a subject first (option 2)[/yellow]")
                continue
            goals = Prompt.ask("What are your learning goals?")
            weeks = IntPrompt.ask("Duration in weeks", default=4)
            with console.status("[bold green]Creating study plan..."):
                plan = tutor.create_study_plan(goals, weeks)
            console.print(Panel(Markdown(plan), title="📅 Study Plan", border_style="magenta"))
            
        elif choice == "8":
            if not tutor.current_subject:
                console.print("[yellow]Please select a subject first (option 2)[/yellow]")
                continue
            console.print("[dim]Type 'exit' to leave chat[/dim]")
            while True:
                message = Prompt.ask("\n[cyan]You[/cyan]")
                if message.lower() == 'exit':
                    break
                with console.status("[bold green]Thinking..."):
                    response = tutor.interactive_chat(message)
                console.print(f"\n[green]Tutor:[/green] {response}")
                
        elif choice == "9":
            content = Prompt.ask("Enter content to translate")
            console.print("\n[bold]Target Languages:[/bold]")
            for code, name in SUPPORTED_LANGUAGES.items():
                console.print(f"  {code}: {name}")
            target = Prompt.ask("Target language code", default="es")
            with console.status("[bold green]Translating..."):
                translated = tutor.translate_content(content, target)
            console.print(Panel(translated, title="🌐 Translation", border_style="yellow"))
            
        elif choice == "10":
            level = Prompt.ask("Your level (beginner/intermediate/advanced)", default="intermediate")
            style = Prompt.ask("Learning style (visual/auditory/reading/kinesthetic)", default="visual")
            tutor.student_profile = {"level": level, "learning_style": style}
            console.print("[green]✓ Profile updated[/green]")
        
        console.print("\n" + "="*50)


if __name__ == "__main__":
    main()
