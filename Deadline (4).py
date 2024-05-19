import json
import g4f
from tkinter import *
from tkinter import ttk
import tkinter as stk
import sys

root = Tk()
root.geometry("400x600")
root.titile = "Бэймакс-тест"
frm = ttk.Frame(root, padding=10)
frm.pack()
question_id = 0


def clear_screen():
    global root, frm
    for widget in root.winfo_children():
        widget.destroy()
    frm = ttk.Frame(root, padding=10)
    frm.pack()

def gpt_request():
	text = open("text.txt", "rb").read().decode("utf-8")
	args = open("args.txt", "rb") .read().decode("utf-8")
	cont = f"{text} \n | {args}"
	chat_completion = g4f.ChatCompletion.create(
    	model=g4f.models.gpt_35_turbo,
    	messages=[{"role": "user", "content": cont}],
	)
	return dict(json.loads(chat_completion))
	
def gpt_request_full():
	text = open("text.txt", "r").read()
	args = open("arg_full.txt", "r") .read()
	cont = f"{text} \n | {args}"
	chat_completion = g4f.ChatCompletion.create(
    	model=g4f.models.gpt_35_turbo,
    	messages=[{"role": "user", "content": cont}],
	)
	return dict(json.loads(chat_completion))


def render_first():
	global root, frm
	ttk.Label(frm, text="Начать тест на знание 'Город героев'").pack(side=TOP)
	ttk.Button(frm, text="Поехали!", command=start).pack(anchor="center")

	
def start():
	global frm, root, questions
	while True:
		clear_screen()
		loading = ttk.Label(frm, text="Выполняется запрос...")
		loading.pack()
		frm.update()
		try:
			questions = gpt_request()
		except Exception:
			continue
		clear_screen()
		loading = ttk.Label(frm, text="готово")
		loading.pack()
		frm.update()
		if checker():
			render_question()
			break
				
	
def render_question():
    global root, frm, var, questons, question_id
    clear_screen()
    scroll_bar = ttk.Scrollbar(frm)
    scroll_bar.pack(side=stk.RIGHT, fill=stk.Y)
    text = stk.Text(frm, wrap=stk.WORD, yscrollcommand=scroll_bar.set)
    text.pack(pady=(10, 5))
    scroll_bar.config(command=text.yview)
    text.insert(stk.END, str(questions[str(question_id)]["quest"]))
    
    var = stk.IntVar()
    for i in range(1, 6):
        temp = questions[str(question_id)][str(i)]
        ttk.Radiobutton(frm, text=temp, variable=var, value=i).pack()
        
    next_button = ttk.Button(frm, text="Далее", command=check_answer)
    next_button.pack(pady=(10, 0))  

def check_answer():
	global var, question_id, frm, root, questions
	clear_screen()
	if str(var.get())==questions[str(question_id)]["answer"]:
		question_id += 1
		if question_id == 6:
			sys.exit(0)
		render_question()
	else: bad_answer(questions[str(question_id)]["fail"])
		
def bad_answer(fail):
	global root, frm
	clear_screen()
	scroll_bar = ttk.Scrollbar(frm)
	scroll_bar.pack(side=stk.RIGHT, fill=stk.Y)
	text = stk.Text(frm, wrap=stk.WORD, yscrollcommand=scroll_bar.set)
	text.pack(pady=(10, 5))
	scroll_bar.config(command=text.yview)
	text.insert(stk.END, str(fail))
	ttk.Button(frm, text="Вернутся", command=render_question).pack(anchor="center")
	
def checker():
	global questions, frm
	try:
		for idit in questions:
			i = questions[idit]
			if len(i["fail"])>5 and str(i["fail"])!="None":
				ttk.Label(frm, text="2").pack(side=TOP)
				for id in range(1, 6):
					if len(i[str(id)])>0 and i[str(id)]!="None":
						print("check true!")
						return True
	except Exception:
		print("check false!")
		return False
	print("check false!")
	return False
	
	
	
	

render_first()
root.mainloop()
