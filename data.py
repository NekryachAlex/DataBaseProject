import json
import random

import psycopg2

def load_data(path):
    with open(path, 'r') as read_file:
        data = json.load(read_file)

    for university_class in data["Classes"]:
        classroom = university_class['Classroom']
        university_class['Classroom'] = data['Classrooms'][classroom]

    data = data['Classes']

    return data

def load_data_from_db(conn):
    conn = psycopg2.connect("dbname=postgres user=postgres password=16072003")
    cur1 = conn.cursor()
    cur2 = conn.cursor()
    data = []
    #save id of class for pushing it in future
    try:
        cur1.execute("select * from classes;")
        #extract classes
        row = cur1.fetchone()
        while row is not None:
           
            cur2.execute("select SubjectType from Subjects where SubjectId = %s", (row[4],))
            type = cur2.fetchone()

            cur2.execute("select GroupId from GroupsT where List = %s;", (row[2],))
            groupsColumn = cur2.fetchall()
            
            groups = []
            for group in groupsColumn:
                groups.append(group[0]) 


            cur2.execute("select Classrom from Classrooms where List = %s;", (row[1],))
            classroomsColumn = cur2.fetchall()
            classrooms = []
            for classroom in classroomsColumn:
                classrooms.append(classroom[0]) 

            data.append({"ClassId": row[0],"Subject": row[4], "Type": type[0], "Teacher": row[3], "Group": groups,\
                "Classroom": classrooms, "Duration": row[5]})
            
            row = cur1.fetchone()
        print(data)
        return data
    except Exception as e:
    
        print("Error occur1red. Rolling back changes.")
        conn.rollback()



def generate_chromosome(data):
    professors = {}
    classrooms = {}
    groups = {}
    subjects = {}

    new_data = []

    for single_class in data:
        professors[single_class['Teacher']] = [0] * 60
        for classroom in single_class['Classroom']:
            classrooms[classroom] = [0] * 60
        for group in single_class['Group']:
            groups[group] = [0] * 60
        subjects[single_class['Subject']] = {'L' : [], 'S' : [], 'W' : []}

    for single_class in data:
        new_single_class = single_class.copy()

        classroom = random.choice(single_class['Classroom'])
        day = random.randrange(0, 5)
     
        
        period = random.randrange(0, 13 - int(single_class['Duration']))
        new_single_class['Appointed_class'] = classroom
        time = 12 * day + period
        new_single_class['Appointed_time'] = time

        for i in range(time, time + int(single_class['Duration'])):
            professors[new_single_class['Teacher']][i] += 1
            classrooms[classroom][i] += 1
            for group in new_single_class['Group']:
                groups[group][i] += 1
        subjects[new_single_class['Subject']][new_single_class['Type']].append((time, new_single_class['Group']))

        new_data.append(new_single_class)

    return (new_data, professors, classrooms, groups, subjects)

def write_data(data, path):
    with open(path, 'w') as write_file:
        json.dump(data, write_file)


def write_data_to_db(data, conn):
    cur1 = conn.cursor()
    try:
        cur1.execute("TRUNCATE TABLE Timetable;")

        for classs in data:
            cur1.execute("Insert into Timetable (ClassId, Appointed_time, Classroom) values (%s, %s, %s);", (classs["ClassId"], classs["Appointed_time"], classs["Appointed_class"]))
        conn.commit()
    except Exception as e:
         print("Error occur1red. Rolling back changes.")
         conn.rollback()