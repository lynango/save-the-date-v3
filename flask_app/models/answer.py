from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import question
from flask_app.models import user

class Answer:
    db_name = "save_the_date"

    def __init__(self,db_data):
        self.id = db_data['id']
        self.answer = db_data['answer']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.creator = None

# Create an answer
    @classmethod
    def save(cls,data):
        query = """
        INSERT INTO answers (answer, user_id, question_id) 
        VALUES (%(answer)s,%(user_id)s,%(question_id)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

# Retrieve all answers
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM answers;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        answers = []
        for row in results:
            answers.append( cls(row) )
        return answers

# Retrieve all answers with questions
    @classmethod
    def get_all_answers_with_creator(cls):
        query = """
                SELECT * FROM questions
                JOIN answers ON answers.question_id = questions.id
                JOIN users ON questions.user_id = users.id
                ORDER BY questions.id ASC;
                """
        results = connectToMySQL(cls.db_name).query_db(query)
        for result in results:
            print("*************", result)
        all_answers = []
        for row in results:
            one_answer = cls(row)
            all_answers.append(one_answer)
        return all_answers

# Retrieve all answers by question_id
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM answers WHERE question_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        print("**********RESULTS = ",results)
        answersList = []
        for result in results:
            answer = cls(result)
            answersList.append(answer)
        return answersList

# Update answer
    @classmethod
    def update(cls, data):
        query = "UPDATE answers SET answer=%(answer)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

# Delete answer
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM answers WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)