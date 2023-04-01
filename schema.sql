CREATE DATABASE IF NOT EXISTS cs353hw4db;
USE cs353hw4db;

DROP TABLE User;
DROP TABLE Task;
DROP TABLE TaskType;

CREATE TABLE User(
	id int,
    password varchar(255),
    username varchar(255),
    email varchar(255),
    primary key (id)
);

CREATE TABLE Task(
	id int,
    title varchar(255),
    description text,
    status varchar(255),
    deadline datetime,
    creation_time datetime,
    done_time datetime,
    user_id int,
    task_type varchar(255),
    primary key (id)
);

CREATE TABLE TaskType(
	type varchar(255),
    primary key (type)
);

INSERT INTO User VALUES( 
	'1',
    'pass123',
    'user1',
    'user1@example.com'
 );
 
 INSERT INTO User VALUES(
	'2',
    'password',
    'user2',
    'user2@example.com'
 );
 
 INSERT INTO TaskType VALUES(
	'Health'
 );
 
 INSERT INTO TaskType VALUES(
	'Job'
 );
 
 INSERT INTO TaskType VALUES(
	'Lifestyle'
 );
 
 INSERT INTO TaskType VALUES(
	'Family'
 );
 
 INSERT INTO TaskType VALUES(
	'Hobbies'
 );
 
 INSERT INTO Task VALUES(
	'1',
    'Go for a walk',
    'Walk for at least 30 mins',
    'Done',
    '2023-03-20 17:00:00',
    '2023-03-15 10:00:00',
    '2023-03-20 10:00:00',
    '1',
    'Health'
 );
 
 INSERT INTO Task VALUES(
	'2',
    'Clean the house',
    'Clean the whole house',
    'Done',
    '2023-03-18 12:00:00',
    '2023-03-14 09:00:00',
    '2023-03-18 17:00:00',
    '1',
    'Lifestyle'
 );
 
  INSERT INTO Task VALUES(
	'3',
    'Submit report',
    'Submit quarterly report',
    'Todo',
    '2023-04-12 17:00:00',
    '2023-03-21 10:00:00',
    null,
    '1',
    'Job'
 );
 
  INSERT INTO Task VALUES(
	'4',
    'Call Mom',
    'Call Mom and wish her',
    'Todo',
    '2023-04-06 11:00:00',
    '2023-03-23 12:00:00',
    null,
    '1',
    'Family'
 );
 
  INSERT INTO Task VALUES(
	'5',
    'Gym workout',
    'Do weight training for an hour',
    'Done',
    '2023-03-19 14:00:00',
    '2023-03-12 10:00:00',
    '2023-03-19 11:00:00',
    '1',
    'Health'
 );
 
 INSERT INTO Task VALUES(
	'6',
    'Play guitar',
    'Learn new song for an hour',
    'Todo',
    '2023-04-05 20:00:00',
    '2023-03-20 14:00:00',
    null,
    '2',
    'Hobbies'
 );
 
  INSERT INTO Task VALUES(
	'7',
    'Book flights',
    'Book flights for summer vacation',
    'Done',
    '2023-03-16 09:00:00',
    '2023-03-13 13:00:00',
    '2023-03-16 11:00:00',
    '2',
    'Lifestyle'
 );
 
  INSERT INTO Task VALUES(
	'8',
    'Write a blog post',
    'Write about recent project',
    'Todo',
    '2023-04-11 17:00:00',
    '2023-03-22 09:00:00',
    null,
    '2',
    'Job'
 );
 
 INSERT INTO Task VALUES(
	'9',
    'Grocery shopping',
    'Buy groceries for the week',
    'Todo',
    '2023-04-05 18:00:00',
    '2023-03-31 10:00:00',
    null,
    '2',
    'Family'
 );
 
 INSERT INTO Task VALUES(
	'10',
    'Painting',
    'Paint a landscape for 2 hours',
    'Done',
    '2023-03-23 15:00:00',
    '2023-03-18 14:00:00',
    '2023-03-23 16:00:00',
    '2',
    'Hobbies'
 );



