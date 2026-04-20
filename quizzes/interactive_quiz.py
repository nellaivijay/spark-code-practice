"""
Interactive Quiz System for Spark Code Practice

Run this script to test your knowledge across all labs.
Usage: python quizzes/interactive_quiz.py
"""

import json
from typing import List, Dict, Tuple
from dataclasses import dataclass
import sys


@dataclass
class Question:
    """Represents a quiz question"""
    question: str
    options: List[str]
    correct_answer: int
    explanation: str
    difficulty: str


class QuizManager:
    """Manages interactive quizzes"""
    
    def __init__(self):
        self.quizzes = {
            "lab1": self._get_lab1_questions(),
            "lab2": self._get_lab2_questions(),
            "lab3": self._get_lab3_questions(),
            "lab4": self._get_lab4_questions(),
            "lab5": self._get_lab5_questions(),
            "lab6": self._get_lab6_questions(),
            "lab7": self._get_lab7_questions()
        }
        self.scores = {}
    
    def _get_lab1_questions(self) -> List[Question]:
        """Lab 1: Spark Fundamentals questions"""
        return [
            Question(
                question="What is the main difference between DataFrame and RDD in Spark?",
                options=[
                    "DataFrame is immutable, RDD is mutable",
                    "DataFrame has schema and optimizations, RDD is low-level",
                    "DataFrame can only handle structured data, RDD handles unstructured",
                    "There is no difference"
                ],
                correct_answer=1,
                explanation="DataFrames have schema information and benefit from the Catalyst optimizer for better performance, while RDDs are lower-level distributed collections without schema.",
                difficulty="Easy"
            ),
            Question(
                question="Which of the following is a transformation operation in Spark?",
                options=[
                    "count()",
                    "collect()",
                    "filter()",
                    "show()"
                ],
                correct_answer=2,
                explanation="filter() is a transformation (lazy evaluation), while count(), collect(), and show() are actions that trigger execution.",
                difficulty="Easy"
            ),
            Question(
                question="What does lazy evaluation mean in Spark?",
                options=[
                    "Spark never executes code",
                    "Spark delays execution until an action is called",
                    "Spark executes code immediately",
                    "Spark only executes on the driver"
                ],
                correct_answer=1,
                explanation="Lazy evaluation means Spark builds a logical plan and only executes it when an action is called, allowing for optimization.",
                difficulty="Medium"
            ),
            Question(
                question="Which component of Spark is responsible for resource management and job scheduling?",
                options=[
                    "Driver",
                    "Executor",
                    "Cluster Manager",
                    "Worker Node"
                ],
                correct_answer=2,
                explanation="The Cluster Manager is responsible for resource management and job scheduling across the cluster.",
                difficulty="Medium"
            ),
            Question(
                question="What is the purpose of the SparkSession in PySpark?",
                options=[
                    "To create RDDs only",
                    "To manage Spark applications and provide entry point",
                    "To store data in memory",
                    "To handle SQL queries only"
                ],
                correct_answer=1,
                explanation="SparkSession is the entry point for programming Spark and provides methods for creating DataFrames, reading data, and executing SQL queries.",
                difficulty="Easy"
            )
        ]
    
    def _get_lab2_questions(self) -> List[Question]:
        """Lab 2: Data Loading & Transformation questions"""
        return [
            Question(
                question="Which file format is most efficient for Spark workloads?",
                options=[
                    "CSV",
                    "JSON",
                    "Parquet",
                    "Text"
                ],
                correct_answer=2,
                explanation="Parquet is a columnar storage format that provides efficient compression and encoding, making it ideal for Spark workloads.",
                difficulty="Easy"
            ),
            Question(
                question="What is schema inference in Spark?",
                options=[
                    "Creating a schema manually",
                    "Automatically detecting data types from the data",
                    "Ignoring schema information",
                    "Converting schema to XML"
                ],
                correct_answer=1,
                explanation="Schema inference automatically detects the data types of columns by reading a sample of the data.",
                difficulty="Medium"
            ),
            Question(
                question="How do you handle null values in a DataFrame?",
                options=[
                    "Using dropna() or fillna()",
                    "Only using dropna()",
                    "Only using fillna()",
                    "Null values cannot be handled"
                ],
                correct_answer=0,
                explanation="You can handle null values using dropna() to remove them or fillna() to replace them with default values.",
                difficulty="Easy"
            ),
            Question(
                question="What is the difference between select() and withColumn()?",
                options=[
                    "They are the same",
                    "select() adds columns, withColumn() removes columns",
                    "select() chooses columns, withColumn() adds/modifies columns",
                    "select() is for filtering, withColumn() is for selection"
                ],
                correct_answer=2,
                explanation="select() is used to choose specific columns from the DataFrame, while withColumn() is used to add or modify columns.",
                difficulty="Medium"
            ),
            Question(
                question="Which method is used to change the data type of a column?",
                options=[
                    "cast()",
                    "convert()",
                    "transform()",
                    "changeType()"
                ],
                correct_answer=0,
                explanation="cast() is used to change the data type of a column in Spark DataFrames.",
                difficulty="Easy"
            )
        ]
    
    def _get_lab3_questions(self) -> List[Question]:
        """Lab 3: Advanced DataFrame Operations questions"""
        return [
            Question(
                question="Which join type returns all rows from both DataFrames with NULLs where there are no matches?",
                options=[
                    "Inner join",
                    "Left join",
                    "Right join",
                    "Outer join"
                ],
                correct_answer=3,
                explanation="Outer join (full outer join) returns all rows from both DataFrames, filling with NULLs where there are no matches.",
                difficulty="Medium"
            ),
            Question(
                question="What is a broadcast join in Spark?",
                options=[
                    "A join that broadcasts results to all executors",
                    "A join optimization for small tables",
                    "A join that uses radio frequency",
                    "A join type for streaming"
                ],
                correct_answer=1,
                explanation="Broadcast join is an optimization where the smaller table is sent to all executors to avoid shuffling data.",
                difficulty="Medium"
            ),
            Question(
                question="What is the purpose of window functions in Spark?",
                options=[
                    "To create new windows in the UI",
                    "To perform calculations across a set of rows related to the current row",
                    "To join multiple DataFrames",
                    "To filter data based on windows"
                ],
                correct_answer=1,
                explanation="Window functions allow you to perform calculations across a set of rows related to the current row, such as ranking or running totals.",
                difficulty="Medium"
            ),
            Question(
                question="Which window function assigns a unique sequential number to each row within a partition?",
                options=[
                    "rank()",
                    "dense_rank()",
                    "row_number()",
                    "percent_rank()"
                ],
                correct_answer=2,
                explanation="row_number() assigns a unique sequential number to each row within a partition, without gaps.",
                difficulty="Easy"
            ),
            Question(
                question="What is the difference between rank() and dense_rank()?",
                options=[
                    "They are the same",
                    "rank() has gaps, dense_rank() has no gaps",
                    "dense_rank() has gaps, rank() has no gaps",
                    "rank() is for numbers, dense_rank() is for strings"
                ],
                correct_answer=1,
                explanation="rank() leaves gaps in ranking when there are ties, while dense_rank() does not leave gaps.",
                difficulty="Hard"
            )
        ]
    
    def _get_lab4_questions(self) -> List[Question]:
        """Lab 4: Spark SQL & Optimization questions"""
        return [
            Question(
                question="What is the Catalyst Optimizer in Spark?",
                options=[
                    "A tool for optimizing Python code",
                    "Spark's query optimization engine",
                    "A visualization tool",
                    "A machine learning library"
                ],
                correct_answer=1,
                explanation="The Catalyst Optimizer is Spark's query optimization engine that transforms logical plans into optimized physical plans.",
                difficulty="Medium"
            ),
            Question(
                question="What is Adaptive Query Execution (AQE) in Spark?",
                options=[
                    "A method for adaptive learning",
                    "Runtime optimization of query plans",
                    "A type of join",
                    "A data format"
                ],
                correct_answer=1,
                explanation="AQE optimizes query plans at runtime based on runtime statistics, improving performance.",
                difficulty="Hard"
            ),
            Question(
                question="What is predicate pushdown?",
                options=[
                    "Pushing predicates down to the data source",
                    "Pushing data to the driver",
                    "A type of join",
                    "A machine learning technique"
                ],
                correct_answer=0,
                explanation="Predicate pushdown is an optimization where filters are pushed down to the data source level to reduce data transfer.",
                difficulty="Medium"
            ),
            Question(
                question="What is a Common Table Expression (CTE) in SQL?",
                options=[
                    "A temporary table for a single query",
                    "A permanent table",
                    "A view",
                    "A function"
                ],
                correct_answer=0,
                explanation="A CTE is a temporary result set that can be referenced within a single SQL statement.",
                difficulty="Medium"
            ),
            Question(
                question="Which configuration enables AQE in Spark?",
                options=[
                    "spark.sql.optimizer.enabled",
                    "spark.sql.adaptive.enabled",
                    "spark.aqe.enabled",
                    "spark.query.adaptive"
                ],
                correct_answer=1,
                explanation="spark.sql.adaptive.enabled is the configuration to enable Adaptive Query Execution.",
                difficulty="Hard"
            )
        ]
    
    def _get_lab5_questions(self) -> List[Question]:
        """Lab 5: Spark Streaming Fundamentals questions"""
        return [
            Question(
                question="What is Structured Streaming in Spark?",
                options=[
                    "A method for streaming video",
                    "A high-level API for stream processing",
                    "A type of join",
                    "A data format"
                ],
                correct_answer=1,
                explanation="Structured Streaming is a high-level API for stream processing built on the Spark SQL engine.",
                difficulty="Easy"
            ),
            Question(
                question="What is the difference between tumbling and sliding windows?",
                options=[
                    "They are the same",
                    "Tumbling windows are non-overlapping, sliding windows can overlap",
                    "Sliding windows are non-overlapping, tumbling windows can overlap",
                    "Tumbling windows are for time, sliding windows for count"
                ],
                correct_answer=1,
                explanation="Tumbling windows are non-overlapping, fixed-size windows, while sliding windows can overlap.",
                difficulty="Medium"
            ),
            Question(
                question="What is watermarking in Structured Streaming?",
                options=[
                    "Adding watermarks to images",
                    "Handling late data in streaming",
                    "A type of join",
                    "A security feature"
                ],
                correct_answer=1,
                explanation="Watermarking is used to handle late-arriving data in streaming by tracking the event time.",
                difficulty="Medium"
            ),
            Question(
                question="Which output mode only outputs new rows since the last trigger?",
                options=[
                    "Append mode",
                    "Complete mode",
                    "Update mode",
                    "Latest mode"
                ],
                correct_answer=0,
                explanation="Append mode only outputs new rows since the last trigger, suitable for non-aggregation queries.",
                difficulty="Medium"
            ),
            Question(
                question="What is the purpose of checkpoints in Structured Streaming?",
                options=[
                    "To check data quality",
                    "To recover from failures",
                    "To monitor performance",
                    "To optimize queries"
                ],
                correct_answer=1,
                explanation="Checkpoints save the state of the streaming query to enable recovery from failures.",
                difficulty="Easy"
            )
        ]
    
    def _get_lab6_questions(self) -> List[Question]:
        """Lab 6: Machine Learning with MLlib questions"""
        return [
            Question(
                question="What is MLlib in Spark?",
                options=[
                    "A library for machine learning",
                    "A type of data format",
                    "A visualization tool",
                    "A streaming library"
                ],
                correct_answer=0,
                explanation="MLlib is Spark's machine learning library providing scalable algorithms for classification, regression, clustering, and more.",
                difficulty="Easy"
            ),
            Question(
                question="What is the purpose of VectorAssembler in MLlib?",
                options=[
                    "To create vectors from columns",
                    "To assemble data from files",
                    "To visualize vectors",
                    "To convert vectors to arrays"
                ],
                correct_answer=0,
                explanation="VectorAssembler combines multiple columns into a single vector column, which is required for most MLlib algorithms.",
                difficulty="Medium"
            ),
            Question(
                question="What is a Pipeline in MLlib?",
                options=[
                    "A data flow tool",
                    "A sequence of stages for ML workflows",
                    " A type of join",
                    "A visualization"
                ],
                correct_answer=1,
                explanation="A Pipeline is a sequence of stages (transformers and estimators) that streamline ML workflows.",
                difficulty="Medium"
            ),
            Question(
                question="What is the difference between classification and regression?",
                options=[
                    "They are the same",
                    "Classification predicts categories, regression predicts continuous values",
                    "Regression predicts categories, classification predicts continuous values",
                    "Classification is for training, regression is for testing"
                ],
                correct_answer=1,
                explanation="Classification predicts discrete categories/classes, while regression predicts continuous numerical values.",
                difficulty="Easy"
            ),
            Question(
                question="What is hyperparameter tuning?",
                options=[
                    "Tuning hyperparameters for better performance",
                    "Tuning model parameters",
                    "Tuning data quality",
                    "Tuning Spark configuration"
                ],
                correct_answer=0,
                explanation="Hyperparameter tuning involves finding the optimal hyperparameters (configuration settings) for a model to improve performance.",
                difficulty="Hard"
            )
        ]
    
    def _get_lab7_questions(self) -> List[Question]:
        """Lab 7: Production Deployment questions"""
        return [
            Question(
                question="What is the main benefit of containerizing Spark applications with Docker?",
                options=[
                    "Better performance",
                    "Consistent environments and easy deployment",
                    "Lower cost",
                    "Better security only"
                ],
                correct_answer=1,
                explanation="Docker provides consistent environments across development, testing, and production, making deployment easier and more reliable.",
                difficulty="Easy"
            ),
            Question(
                question="What is Kubernetes used for in Spark deployment?",
                options=[
                    "Data storage",
                    "Container orchestration and scaling",
                    "Machine learning",
                    "Streaming"
                ],
                correct_answer=1,
                explanation="Kubernetes is used for container orchestration, managing and scaling Spark containers in production.",
                difficulty="Medium"
            ),
            Question(
                question="What is the purpose of monitoring in production Spark applications?",
                options=[
                    "To watch the application run",
                    "To detect issues and ensure performance",
                    "To stop the application",
                    "To change the code"
                ],
                correct_answer=1,
                explanation="Monitoring helps detect issues, track performance metrics, and ensure the application runs smoothly in production.",
                difficulty="Easy"
            ),
            Question(
                question="What is CI/CD in the context of Spark applications?",
                options=[
                    "Continuous Integration and Continuous Deployment",
                    "Code Integration and Code Deployment",
                    "Continuous Improvement and Continuous Development",
                    "Code Integration and Continuous Development"
                ],
                correct_answer=0,
                explanation="CI/CD automates the integration, testing, and deployment of code changes, improving development velocity and quality.",
                difficulty="Medium"
            ),
            Question(
                question="What is high availability in Spark?",
                options=[
                    "Making Spark available at high cost",
                    "Ensuring the system remains operational despite failures",
                    "Running Spark on high-end hardware",
                    "Making Spark available only during business hours"
                ],
                correct_answer=1,
                explanation="High availability ensures Spark applications continue to operate even when components fail, often through redundancy and failover mechanisms.",
                difficulty="Medium"
            )
        ]
    
    def display_menu(self) -> str:
        """Display the quiz menu and get user selection"""
        print("\n" + "="*60)
        print("   SPARK CODE PRACTICE - INTERACTIVE QUIZ SYSTEM")
        print("="*60)
        print("\nAvailable Quizzes:")
        print("1. Lab 1: Spark Fundamentals")
        print("2. Lab 2: Data Loading & Transformation")
        print("3. Lab 3: Advanced DataFrame Operations")
        print("4. Lab 4: Spark SQL & Optimization")
        print("5. Lab 5: Spark Streaming Fundamentals")
        print("6. Lab 6: Machine Learning with MLlib")
        print("7. Lab 7: Production Deployment")
        print("8. All Labs (Comprehensive)")
        print("0. Exit")
        print("="*60)
        
        choice = input("\nSelect a quiz (0-8): ").strip()
        return choice
    
    def run_quiz(self, lab_key: str) -> Tuple[int, int]:
        """Run a quiz for a specific lab"""
        questions = self.quizzes[lab_key]
        correct = 0
        total = len(questions)
        
        print(f"\n{'='*60}")
        print(f"   QUIZ: {lab_key.upper().replace('LAB', 'Lab ')}")
        print(f"   Total Questions: {total}")
        print(f"{'='*60}\n")
        
        for i, question in enumerate(questions, 1):
            print(f"\nQuestion {i}/{total} [{question.difficulty}]")
            print(f"\n{question.question}\n")
            
            for j, option in enumerate(question.options, 1):
                print(f"  {j}. {option}")
            
            while True:
                try:
                    answer = int(input(f"\nYour answer (1-{len(question.options)}): "))
                    if 1 <= answer <= len(question.options):
                        break
                    print("Invalid choice. Please try again.")
                except ValueError:
                    print("Please enter a number.")
            
            if answer == question.correct_answer + 1:
                print("\n✓ Correct!")
                correct += 1
            else:
                print(f"\n✗ Incorrect. The correct answer is: {question.correct_answer + 1}")
            
            print(f"\nExplanation: {question.explanation}")
            print("-"*60)
        
        return correct, total
    
    def run_all_quizzes(self) -> Dict[str, Tuple[int, int]]:
        """Run all quizzes and return results"""
        results = {}
        for lab_key in self.quizzes.keys():
            print(f"\n{'='*60}")
            print(f"Starting {lab_key.upper().replace('LAB', 'Lab ')} Quiz...")
            print(f"{'='*60}")
            input("Press Enter to continue...")
            
            correct, total = self.run_quiz(lab_key)
            results[lab_key] = (correct, total)
        
        return results
    
    def display_summary(self, results: Dict[str, Tuple[int, int]]):
        """Display summary of quiz results"""
        print("\n" + "="*60)
        print("   QUIZ SUMMARY")
        print("="*60)
        
        total_correct = 0
        total_questions = 0
        
        for lab_key, (correct, total) in results.items():
            percentage = (correct / total) * 100 if total > 0 else 0
            print(f"\n{lab_key.upper().replace('LAB', 'Lab ')}: {correct}/{total} ({percentage:.1f}%)")
            total_correct += correct
            total_questions += total
        
        overall_percentage = (total_correct / total_questions) * 100 if total_questions > 0 else 0
        print(f"\n{'='*60}")
        print(f"OVERALL: {total_correct}/{total_questions} ({overall_percentage:.1f}%)")
        print("="*60)
        
        if overall_percentage >= 90:
            print("\n🎉 Excellent! You have a strong understanding of Spark!")
        elif overall_percentage >= 70:
            print("\n👍 Good job! Keep practicing to improve further.")
        elif overall_percentage >= 50:
            print("\n📚 You're on the right track. Review the labs for improvement.")
        else:
            print("\n💪 Keep learning! Review the labs and try again.")
    
    def run(self):
        """Main quiz loop"""
        while True:
            choice = self.display_menu()
            
            if choice == "0":
                print("\nThank you for using the Spark Code Practice Quiz System!")
                break
            
            if choice == "8":
                results = self.run_all_quizzes()
                self.display_summary(results)
            elif choice in [str(i) for i in range(1, 8)]:
                lab_key = f"lab{choice}"
                correct, total = self.run_quiz(lab_key)
                percentage = (correct / total) * 100 if total > 0 else 0
                print(f"\n{'='*60}")
                print(f"Result: {correct}/{total} ({percentage:.1f}%)")
                print(f"{'='*60}")
            else:
                print("Invalid choice. Please try again.")


def main():
    """Main entry point"""
    quiz_manager = QuizManager()
    quiz_manager.run()


if __name__ == "__main__":
    main()
