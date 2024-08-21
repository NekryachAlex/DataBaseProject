# DataBaseProject
It is a simple course project. It includes working with the Postgresql data base. It just get data from data base and load it back. Also it can use json file.  
The purpose of the project is creating a timetable for university. Data for creating can be located in json file.   
-Data description:  
  The data consist of professors, classes, classrooms.    
  For the computing data is converted into chromosomes. A chromosome introduces current state of the timetable.   
  Classes are distributed in 60 cells: 5 days and 12 working hours in a day.  
-Algorithm description:  
  This algorithm always maintain two chromosomes. One is created from another using mutation. First chromosome is created randomly. The best fitted chromosome     is chosed and used for future computing. A       cost function is used for estimate chromosome.  
  There are several constraints: sequence of subjects (for example, lectures should be before laboratory works), overlap of classes, professors classrooms and     long gaps between classes.  
  Mutation chooses candidates violates constraints. If there are not such it choose randomly. After choosing it swaps two classes trying maintaint constraints.  
