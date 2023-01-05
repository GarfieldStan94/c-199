import socket
from threading import Thread
import random 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = "127.0.0.1"
port = 5000

server.bind((ip_address, port))
server.listen()
list_of_clients = []

question = [

    "How high is Mt Everest?\n a. 2 KM\n b. 8.8 KM\n c. 7.9 KM\n d. 4.3 KM", 
    "Who was the first U.S. President\n a. Teddy Roosevelt\n b. Chester A. Arthur\n c. Alexander Hamilton\n d. George Washington",
    "What is 3 x 9\n a. 12\n b. 6\n c. 48\n d. 27",
    "What day is Valentine's Day\n a. February 4th\n b. March 13th\n c. February 14th\n d. May 18th"
]

answers = [
    "B",
    "D",
    "D",
    "C"
]

def get_random_question_answers (con):

  random_index = random.randint(0,len(question) - 1)
  random_question = question[random_index] 
  random_answer = answers[random_index] 
  con.send(random_question.encode('utf-8')) 
  return random_index, random_question, random_answer  

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
def remove_question(index):
    question.pop(index)
    answers.pop(index)
def clientThread(con, addr):
    score = 0
    con.send("Welcome to this Quiz!".encode('utf-8'))
    index, ques, answer = get_random_question_answers(con)
    while True:
        try:
            message = con.recv(2048).decode('utf-8')
            if message:
                if message.upper() == answer:
                    score += 1
                    con.send(f"Correct answer, your score is {score}\n".encode ("UTF-8")) 
                else: con.send(f"Incorrect answer, your score is {score}\n".encode ("UTF-8"))      
                remove_question(index)
                index, ques, answer = get_random_question_answers(con)
            else:
                remove(con)
        except:
            continue

while True:
    con, addr = server.accept ()
    list_of_clients.append(con)
    print (addr [0]+" connected")
    
    new_thread = Thread (target = clientThread, args= (con, addr))
    new_thread.start()