# Interactive Quiz System

This directory contains an interactive quiz system for self-assessment across all Spark Code Practice labs.

## Usage

Run the interactive quiz system:

```bash
python quizzes/interactive_quiz.py
```

## Features

- **7 Individual Lab Quizzes**: Test your knowledge on each lab topic
- **Comprehensive Quiz**: Test all labs in one session
- **Immediate Feedback**: Get instant feedback on your answers
- **Detailed Explanations**: Learn from detailed explanations for each question
- **Difficulty Levels**: Questions marked as Easy, Medium, or Hard
- **Score Tracking**: Track your progress across all labs

## Quiz Topics

1. **Lab 1**: Spark Fundamentals
   - DataFrame vs RDD
   - Transformations vs Actions
   - Lazy Evaluation
   - Spark Architecture
   - SparkSession

2. **Lab 2**: Data Loading & Transformation
   - File Formats (Parquet, CSV, JSON)
   - Schema Inference
   - Null Handling
   - Data Transformations
   - Type Casting

3. **Lab 3**: Advanced DataFrame Operations
   - Join Types
   - Broadcast Joins
   - Window Functions
   - Ranking Functions
   - Complex Data Types

4. **Lab 4**: Spark SQL & Optimization
   - Catalyst Optimizer
   - Adaptive Query Execution (AQE)
   - Predicate Pushdown
   - Common Table Expressions (CTE)
   - Query Hints

5. **Lab 5**: Spark Streaming Fundamentals
   - Structured Streaming
   - Window Operations
   - Watermarking
   - Output Modes
   - Checkpoints

6. **Lab 6**: Machine Learning with MLlib
   - MLlib Overview
   - Feature Engineering
   - Pipelines
   - Classification vs Regression
   - Hyperparameter Tuning

7. **Lab 7**: Production Deployment
   - Docker Deployment
   - Kubernetes
   - Monitoring
   - CI/CD
   - High Availability

## Running the Quiz

1. Navigate to the spark-code-practice directory
2. Run the quiz script:
   ```bash
   python quizzes/interactive_quiz.py
   ```
3. Select a quiz from the menu
4. Answer questions by entering the number of your choice
5. Review explanations for each answer
6. Check your score at the end

## Integration with Labs

The quiz questions are designed to complement the lab materials:
- After completing a lab, take the corresponding quiz to reinforce learning
- Use quiz explanations to review concepts you found challenging
- Track your progress across all labs to identify areas for improvement

## Adding New Questions

To add new questions to the quiz system:

1. Edit `quizzes/interactive_quiz.py`
2. Add questions to the appropriate method (e.g., `_get_lab1_questions()`)
3. Follow the Question dataclass structure:
   ```python
   Question(
       question="Your question here",
       options=["Option 1", "Option 2", "Option 3", "Option 4"],
       correct_answer=0,  # Index of correct answer (0-based)
       explanation="Explanation of why this is correct",
       difficulty="Easy/Medium/Hard"
   )
   ```

## Requirements

- Python 3.7+
- No additional dependencies required (uses only standard library)

## Tips for Success

- Take quizzes after completing each lab
- Review the explanations for incorrect answers
- Retake quizzes periodically to reinforce learning
- Use the comprehensive quiz to test overall knowledge
- Combine quizzes with practice exercises for thorough preparation
