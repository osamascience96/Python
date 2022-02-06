# Django

## Introduction
>The Django Framework is build upon the ***MVC*** Design Pattern. It is one of the most famous design pattern that is used many other frameworks and easy to implement.
>The ***MVC*** stands for Model-View-Controller, where all these entities communicate with each other in terms of data and also loosely coupled. Each entity knows its role best in terms of seperation of concerns.

## Data Models
***Models*** in django is a great abstration in django framework. When we *query* the database we dont directly take data from the database as we use **SQL language** that is also an abstraction to perfrom CRUD on db schema.
But python build more abstraction for us to have so that we don't have to bother about the complex sql queries as well, mainly as a developer we can focus on the project goal.
> So the point of the matter is that What is ***ORM***?
> The **ORM** stands for Object Relational Mapper that is used by django to map the django objects to the SQL to perform the CRUD to database schema.

![ORM Mapper Image](ORM_Django_basic_image.png)


***What are Migrations in Django?***
> Migrations is a method in Django that is used to **"apply the changes based on the changes that you have made in your models"**. For instance if you change add a field, or delete a specific model or other operations related to CRUD.
> So we can easily focus on this by focusing on the simple flow of migration procedures that is mostly done.

**Example**
If i make any changes in the model, that would surely reflect on to our database but in order to do that, after making changes we have to create new migrations on the queue that fill applied when we migrate the following changes

**General Steps**
1. Make changes in the model
2. makemigrations
3. migrate
 
So in general, after making the changes in model, you make new migrations, that will be migrated by you to apply the changes to the database.

**More on Migrations:**   
> When we make migrations on any app, each migration we make is stored in the django_migrations table in the database to keep the record of each migration, we performed. Now, while performing the migrations, we first make new migrations and that is stored in the migrations folder(not yet applied in the database structure), so the first one is stored in **001_initial.py** and then what we do either add any attribute so it is stored based on the migrations indexing going on in the project, **n_[modelname]_[attributeadded].py**, here *n* is the number of migrations being added like 002, 003, 004 etc and the model name is always mentioned there and the the last one is the name of the new attribute being updated in the schema of the table in the database. So when we migrate, we apply th following changes, now during the procedure when the structure is getting changed, the schema of the table is updated based on the migrations stored in the migration table and then the migrations table to store the record of the migration performed on the table. And when we delete the table, we see the migration stored in the migration folder is like this one **n_delete_[modelname].py**. Even this migration is also stored in the table. So weather if we delete the delete migration and then apply the migrations, the django is going to look in the models and based on it, it is going be recovered again and you cannot get rid of this delete migration, until you come up with a new migration for the table.

