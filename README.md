[![Github Actions Workflow](https://github.com/DiogoCarapito/insulin_calculator/actions/workflows/main.yaml/badge.svg)](https://github.com/DiogoCarapito/insulin_calculator/actions/workflows/main.yaml)

# Insulin Calculator
This is a insulin dose calculator webapp live at []() using streamlit. 
This is a project that started when I was in Endocrinology. By that time I was learnig about DevOps concepts like CI/CD, so I decided to excercise them with a real world problem.

## Problem: 
Calculating the right dose of Inslin for Type 1 Diabetes Mellitus commes with a set of challanges.

Models help claculate the right dose for each situation and meal. Simpler models tend to be easyer to implement, but the more complex are more accurate    

There are many variables to take into account:
- actual glycemia
- glycemia tendency
- target glicemia
- sensibility factor
- carbohydrates equivalency
- carbohydrates intake (as grams or as food)

The calculations involve simple addition and multiplication, but it's quite tedious repeating at least 3 times a day, every day.

## Solution

This streamlit app calculates the dose of insulin taking unto account the variabrls mentioned before.
It computes and explains the calculation.
Carbohydrates intake can be calculated froma list of food with the carbohydrates composition