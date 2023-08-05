# Gradi.ai - Redefining Academic Assessment with AI

Automate the grading process, accelerate academic assessments, and elevate educational outcomes with the power of Gradi.ai !

Presentation Link: https://www.canva.com/design/DAFm1ReWkb0/wExqDD7LjFC6F7G23bQxsQ/edit?utm_content=DAFm1ReWkb0&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

## Problem Statement

-	Objective type paper correction is automatable but has not been extended to subjective type papers yet
-	Even after exams, students aren’t fully aware of their weaknesses and strengths
-	Also, students don’t really have a great idea on how to improve after tests

  
## Solution Idea

-	Automate the paper correction process for subjective type papers
-	Analyse student’s weaknesses using the exam paper
-	Suggest good study plans and topics to focus on more

  
## Planned Features

-	Gradi will use computer vision to read student answer sheets and correct each question based on keywords given by teachers
-	Gradi will give a grade for the student and analyse most common errors and point out weaknesses
-	Gradi will then create a personalized study plan for students with focus on weaknesses and strengths as per analysis

  
## Technical Architecture

-	Use Python and Streamlit to take answer sheet input and keyword input
-	Use EasyOCR API module to read question papers
-	Use Neural DB to retrieve references
-	Use openai api to compare answers with keywords and give grades
-	Use openai api again to find out weaknesses and provide study plan

  
## What’s out of scope

-	Cannot correct diagrams
-	Cannot understand equations due to the limitation of handprint module
-	Handwritten Text Reading is still in early stages of development
