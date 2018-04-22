# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# Create your models here.

class UserManager(models.Manager):
    def register(self, name, alias, email, password, confirm):
        errors = []
        if len(name) < 2:
            errors.append("Name must be 2 characters or more")

        if len(alias) < 2:
            errors.append("Alias must be 2 characters or more")

        if len(email) < 1:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(email):
            errors.append("Invalid email")
        else:
            usersMatchingEmail = User.objects.filter(email=email)
            if len(usersMatchingEmail) > 0:
                errors.append("Email already in use")


        if len(password) < 1:
            errors.append("Password is required")
        elif len(password) < 8:
            errors.append("Password must be 8 characters or more")

        if len(confirm) < 1:
            errors.append("Confirm Password is required")
        elif password != confirm:
            errors.append("Confirm Password must match Password")

        response = {
            "errors": errors,
            "valid": True,
            "user": None 
        }

        if len(errors) > 0:
            response["valid"] = False
            response["errors"] = errors
        else:
            response["user"] = User.objects.create(
                name=name,
                alias=alias,
                email=email.lower(),
                password=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            )

        return response

    def login(self, email, password):
        errors = []

        if len(email) < 1:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(email):
            errors.append("Invalid email")
        else:
            usersMatchingEmail = User.objects.filter(email=email)
            if len(usersMatchingEmail) == 0:
                errors.append("Unknown email")

        if len(password) < 1:
            errors.append("Password is required")
        elif len(password) < 8:
            errors.append("Password must be 8 characters or more")

        response = {
            "errors": errors,
            "valid": True,
            "user": None 
        }

        if len(errors) == 0:
            if bcrypt.checkpw(password.encode(), usersMatchingEmail[0].password.encode()):
                response["user"] = usersMatchingEmail[0]
            else:
                errors.append("Incorrect password")

        if len(errors) > 0:
            response["errors"] = errors
            response["valid"] = False

        return response

class AuthorManager(models.Manager):
	def addAuthor(self, author):
		errors=[]
		if len(author)<3:
			errors.append("Author must have a first and last name.")
		if len(errors)> 0:
			return {"valid": False, "errors": errors}
		else:
			Author.objects.create(name=name)
			return {"valid":True, "errors":errors}

class BookManager(models.Manager):
	def addBook(self, title, writer):
		errors=[]
		if len(title)<2:
			errors.append("Title must be longer than 3 characters")
		if len(errors)>0:
			return {"valid": False, "errors": errors}
		else:
			Book.objects.create(title=title, writer=writer)

class ReviewManager(models.Manager):
	def addReview(self, rating, description, reviewed_book, book_author, user):
		errors=[]
		if len(description)< 1:
			errors.append("There is no content in the review")
		if len(errors)>0:
			return {"valid":False, "errors":errors}
		else:
			Review.objects.create(
				rating=rating, 
				description= description,
				reviewed_book=title,
				book_author=author,
				user_id=user,
				)		


class User(models.Model):
    name = models.CharField(max_length=255) 
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
 		return "Users Object({}) {} {}>".format(self.id, self.name, self.alias)

    

class Author(models.Model):
	author=models.CharField(max_length=255)
	created_at= models.DateTimeField(auto_now_add=True)
	updated_at= models.DateTimeField(auto_now=True)	
	objects = AuthorManager()

	def __repr__(self):
 		return "Authors Object({}) {}>".format(self.id,self.author)


class Book(models.Model):
	title= models.CharField(max_length=255)
	writer=models.ForeignKey(Author, related_name="writer", default='0')
	created_at= models.DateTimeField(auto_now_add=True)
	updated_at= models.DateTimeField(auto_now=True)
	objects = BookManager()



class Review(models.Model):
	rating=models.IntegerField()
	description=models.CharField(max_length=255)
	reviewed_book=models.ForeignKey(Book,related_name="books")
	book_author= models.ForeignKey(Author, related_name="authors")
	user= models.ForeignKey(User, related_name="user")	
	created_at= models.DateTimeField(auto_now_add= True)
	updated_at= models.DateTimeField(auto_now=True)
	objects= ReviewManager

	def __repr__(self):
 		return "Review Object({}) {}>".format(self.id,self.user)









