"""-----------------------------------------------------------------------------------
--------------------------------------Modules importation-----------------------------
-----------------------------------------------------------------------------------"""
from tkinter import *
import tkinter.messagebox as tk_box
import tkinter.font as tk_font
import time, random, webbrowser, datetime, pickle


"""-----------------------------------------------------------------------------------
------------------------------------------Fonctions-----------------------------------
-----------------------------------------------------------------------------------"""

def end_game_screen(nb_help,nb_click,chrono_value,bomb_counter,lvl_difficulty,victory=True):
    global language, fini
    fini = True
    end_game_window = Toplevel(window)
    end_game_window.geometry("400x300")
    #frame
    frame_title = Frame(end_game_window)
    frame_ligne_1 = Frame(end_game_window,height = 110,width=400,pady=10)
    frame_ligne_2 = Frame(end_game_window)
    frame_buttons = Frame(end_game_window)
    frame_title.pack()
    frame_ligne_1.pack()
    frame_ligne_2.pack()
    frame_buttons.pack()
    #under frame
    frame_time = Frame(frame_ligne_1)
    frame_difficulty = Frame(frame_ligne_1)
    frame_click = Frame(frame_ligne_2)
    frame_help = Frame(frame_ligne_2)
    frame_time.pack(side=LEFT)
    frame_difficulty.pack(side=RIGHT)
    frame_click.pack(side=LEFT)
    frame_help.pack(side=RIGHT)
    
    #image configuration

    #language setting         
    if language == "français":
        message_list = ["Résumé de la partie","Victoire","Défaite","Quitter","Voulez-vous vraiment quitter ?","Rejouer","Difficulté: ","facile","intermédiaire","difficile","Temps: ","Nombre d'aide(s): ","Nombre d'action(s): "]
    else:
        message_list = ["Recap of the game","Victory","Defeat","Quit","Do you really want to quit ?","Play again","Difficulty: ","easy","medium","hard","Time: ","Number of help(s): ","Number of action(s): "]
    end_game_window.title(message_list[0])

    #wdiget setting
    if victory:
        victory_text = message_list[1]
    else:
        victory_text = message_list[2]
        
    #title content
    victory_label = Label(frame_title, text=victory_text, font="Helvetica 35 bold")
    victory_label.pack(pady=(10,40))

    #time content
    time_txt = message_list[10] + str(chrono_value) + "s"
    time_label = Label(frame_time, text=time_txt)
    time_label.pack(padx=(0,100))

    #difficulty content
    difficulty_txt = message_list[6] + message_list[6 + int(lvl_difficulty)]
    difficulty_label = Label(frame_difficulty, text=difficulty_txt)
    difficulty_label.pack()

    #click content
    click_txt = message_list[12] + str(nb_click)
    computer_click_label = Label(frame_click,text=click_txt)
    computer_click_label.pack(padx=(0,100))

    #help content
    help_txt = message_list[11] + str(nb_help)
    help_label = Label(frame_help, text=help_txt)
    help_label.pack()

    #bottom buttons
    leave_button = Button(end_game_window, text=message_list[3], command=lambda: leave_game(message_list[4]))
    leave_button.pack(side=BOTTOM,fill="x")
    new_game_button = Button(end_game_window, text=message_list[5], command=new_game)
    new_game_button.pack(side=BOTTOM,fill="x")



def open_web(url):
    """Function that opens a web page from an url in argument. Does not return anything"""
    webbrowser.open(url)



def leave_game(msg):
    """Fonction that asks the user for a confirmation. Quit the game if the player confirms.
Writes in a txt file the options modified by the player. Does not return anything."""
    choice = tk_box.askokcancel("Confirmation",msg)
    if choice == 1:
        time_before_stop = stop_stopwatch()
        global file, fini, dictionary_box, nb_click, nb_help, nb_bombs, image_box_list
        if fini == False:
            with open("save_previous_game.txt","wb") as file_txt:
                pickle_save = pickle.Pickler(file_txt)
                pickle_save.dump(dictionary_box)
                pickle_save.dump(nb_click)
                pickle_save.dump(nb_help)
                pickle_save.dump(nb_bombs)
                pickle_save.dump(time_before_stop)
        language = file[0]
        maker = "\n"
        file = maker.join(file)
        with open("Minesweeper_data.txt","w",encoding="UTF-8") as f:
            f.write(file)
        try:
            end_game_window.destroy()
            window.destroy()
        except:
            window.destroy()
        

def change_in_file(number,change):
    global file
    if int(number) != 1:
        file[number] = str(change)
        maker = "\n"
        change_file = maker.join(file)
        with open("Minesweeper_data.txt","w",encoding="UTF-8") as f:
            f.write(change_file)
    else:
        if change == "1":
            file[1] = str(change)
            file[2] = str(10) 
            maker = "\n"
            change_file = maker.join(file)
        elif change == "2":
            file[1] = str(change)
            file[2] = str(18) 
            maker = "\n"
            change_file = maker.join(file)
        else:
            file[1] = str(change)
            file[2] = str(25) 
            maker = "\n"
            change_file = maker.join(file)
        with open("Minesweeper_data.txt","w",encoding="UTF-8") as f:
            f.write(change_file)
    if file[0] == "français":
        tk_box.showinfo("Information","Le changement s'effectuera au prochain lancement du jeu")
    else:
        tk_box.showinfo("Information","The change will take place at the next launch of the game")





    
def first_click_game_configuration(click_box_number):
    """Function that changes the number of bombs according to the difficulty of the game."""
    global dictionary_box, fini
    fini = False
    liste_shuffle_bomb = mixed_bomb_list(click_box_number)
    for element in liste_shuffle_bomb:
        dictionary_in = {}
        dictionary_in["visible"] = False
        dictionary_in["value"] = element
        dictionary_in["flag"] = False
        dictionary_box.append(dictionary_in)
        



def click_box(click_box_number):
    #Function that is called when a box is pressed. It takes as argument the index of the box and does the actions accordingly.
    global nb_click, game_on, dictionary_box
    if nb_click == 0:
        first_click_game_configuration(click_box_number)
    if dictionary_box[click_box_number]["visible"]:
        pass
    elif dictionary_box[click_box_number]["flag"]:
        pass
    else:
        if not active:
            begin_stopwatch()
        nb_click +=1
        dictionary_box[click_box_number]["visible"] = True
        if dictionary_box[click_box_number]["value"] == "b":
            reveal_all_bombs(click_box_number)
        else:
            list_update = []
            update_box_number(click_box_number,dictionary_box,list_update)
            for indice in list_update:
                dictionary_box[indice]["visible"] = True
            update_box_screen(list_update)
            global nb_bombs
            if nb_bombs == 0:
                check_if_win()            
            #finish-----------------------------------



def check_if_win():
    global dictionary_box
    a = 0
    for element in dictionary_box:
        if (element["value"] != "b") and (element["flag"] == True):
            a = 1
        elif (element["visible"] == False) and (element["flag"] == False):
            a = 1
    if a==0:
        game_on = False
        stop_stopwatch()
        global time_counter_display
        chrono = round(float(time_counter_display.get()))
        global nb_help, nb_cick, bomb_counter, lvl_difficulty
        end_game_screen(nb_help,nb_click,chrono,0,lvl_difficulty,victory=True)
    

def update_box_number(number,dictionary_box,list_update):
    if number not in list_update:
        list_update.append(number)
        list_neighbour = box_neighbour(number)
        for neighbour in list_neighbour:
            if (dictionary_box[number]["value"] == 0):
                update_box_number(neighbour,dictionary_box,list_update)
    #finish---------




def update_box_screen(list_update):
    global dictionary_box, minesweeper_dimension, image_box_list
    for number in list_update:
        column = number // minesweeper_dimension
        row = number % minesweeper_dimension
        if (dictionary_box[number]["flag"]) and (dictionary_box[number]["value"] != "ff"):
            if image_box_list[number] == 0:
                image_box_list[number] = PhotoImage(file="flag.gif")
                canvas_click.create_image(row*20+1,column*20+1,image=image_box_list[number],anchor=NW)
        elif dictionary_box[number]["value"] == "ff":
            image_box_list[number] = PhotoImage(file="black_bomb_crossed.gif")
            canvas_click.create_image(row*20+1,column*20+1,image=image_box_list[number],anchor=NW)
        elif dictionary_box[number]["value"] == "ab":
            image_box_list[number] = PhotoImage(file="black_bomb.gif")
            canvas_click.create_image(row*20+1,column*20+1,image=image_box_list[number],anchor=NW)
        elif dictionary_box[number]["value"] == "rb":
            image_box_list[number] = PhotoImage(file="red_bomb.gif")
            canvas_click.create_image(row*20+1,column*20+1,image=image_box_list[number],anchor=NW)
        elif dictionary_box[number]["value"] == "b":
            image_box_list[number] = PhotoImage(file="black_bomb.gif")
            canvas_click.create_image(row*20+1,column*20+1,image=image_box_list[number],anchor=NW)
        elif dictionary_box[number]["value"] >= 1 :
            canvas_click.create_text(row*20+10, column*20+10, text=str(dictionary_box[number]["value"]))
        else:
            canvas = canvas_click.create_rectangle(row*20,column*20,row*20+20,column*20+20, fill="#444444")


    
def reveal_all_bombs(number):
    #Function that reveals all the bombs and returns to the endgame screen.
    #arrêt de chronomètre
    global dictionary_box,nb_help,nb_click,game_on
    game_on = False
    stop_stopwatch()
    global time_counter_display
    chrono = round(float(time_counter_display.get()))
    bomb_counter = 0
    list_update= []
    for i in range(len(dictionary_box)):
        if number == i:
            dictionary_box[i]["value"] = "rb"
            list_update.append(i)
        elif (dictionary_box[i]["value"] == "b") and (dictionary_box[i]["flag"] == True):
            list_update.append(i)
            pass
        elif (dictionary_box[i]["value"] != "b") and (dictionary_box[i]["flag"] == True):
            list_update.append(i)
            dictionary_box[i]["value"] = "ff"
        elif (dictionary_box[i]["value"] == "b") and (dictionary_box[i]["flag"] == False):
            list_update.append(i)
            dictionary_box[i]["value"] = "ab"
    update_box_screen(list_update)
    end_game_screen(nb_help,nb_click,chrono,bomb_counter,lvl_difficulty,victory=False)



def grid_creation(minesweeper_dimension):
    canvas_click.delete("all") 
    for row in range(minesweeper_dimension):
        for column in range(minesweeper_dimension):
            canvas_click.create_rectangle(row*20,column*20,row*20+20,column*20+20,fill="grey")
    #finish=======================



def reveal_a_bomb():
    #Function that checks if the player is allowed to reveal a bomb. Reveals it if he can.
    global dictionary_box,nb_click,language,nb_help
    if nb_click == 0:
        if language == "français":
            tk_box.showerror("Erreur", "Aucune bombe ne peut être révélée tant que la partie n'a pas commencé")
        else:
            tk_box.showerror("Error", "No bombs can be revealed until the game has begun.")
    elif nb_help >=3:
        if language == "français":
            tk_box.showerror("Erreur", "Vous ne pouvez pas révéler plus de 3 fois une bombe")
        else:
            tk_box.showerror("Error", "You can't reveal a bomb more than three times")
    else:
        global nb_bombs
        if nb_bombs <=3:
            if language == "français":
                tk_box.showerror("Erreur", "Vous ne pouvez pas révéler de bombes lorsqu'il en reste 3 ou moins")
            else:
                tk_box.showerror("Error", "You can't reveal bombs when there are three or less left")
        else:
            nb_help +=1
            bomb_counter = []
            i=0
            for dictionary in dictionary_box:
                if (dictionary["value"] == "b") and (dictionary["flag"] == False) and (dictionary["visible"] == False):
                    bomb_counter.append(i)
                i += 1
            bomb_reveal = random.choice(bomb_counter)
            global image_box_list
            image_box_list[bomb_reveal] == 0
            dictionary_box[bomb_reveal]["flag"] = True
            update_box_screen([bomb_reveal])
            global nb_bombs_display
            nb_bombs -= 1
            nb_bombs_display.set('{}'.format(nb_bombs))
            #finish =================

def new_game():
    a=stop_stopwatch()
    initialize_stopwatch()
    global nb_click, nb_help, dictionary_box, image_box_list, nb_bombs, nb_bombs_display, file, end_game_window,game_on, minesweeper_dimension
    nb_click = 0
    nb_help = 0
    dictionary_box = []
    time_before_stop = 0
    canvas_click.delete('all')
    image_box_list = [0]*minesweeper_dimension*minesweeper_dimension
    if int(file[1]) == 1:
        nb_bombs = 10
    elif int(file[1]) == 2:
        nb_bombs = 40
    else:
        nb_bombs = 99
    nb_bombs_display.set('{}'.format(nb_bombs))
    #destroy end_game_window
    grid_creation(minesweeper_dimension)
    game_on = True



    

def mixed_bomb_list(click_box_number):
    #Shuffles the list containing the bombs so that the square the player clicks on has a 0 value. Set the value of each box.
    global minesweeper_dimension, nb_bombs
    list_grid = [0]*(minesweeper_dimension * minesweeper_dimension - nb_bombs)
    for _ in range(nb_bombs):
        list_grid.append("b")
    while True:
        test = 0
        random.shuffle(list_grid)
        list_neighbour = box_neighbour(click_box_number)
        list_neighbour.append(click_box_number)
        for i in list_neighbour:
            if list_grid[i] == "b":
                test = 1
        if test == 0:
            break
    for i in range(len(list_grid)):
        if list_grid[i] == "b":
            continue
        neighbour_of_i = box_neighbour(i)
        bomb_counter = 0
        for value in neighbour_of_i:
            if list_grid[value] == 'b':
                bomb_counter+=1
        list_grid[i] = bomb_counter
    return list_grid
    #finish ===============



def box_neighbour(box):
    #Function that takes as argument the clicked box and returns a list with the adjacent boxes.
    global minesweeper_dimension
    list_neighbour_box_tempory = [1]*8
    if (box % minesweeper_dimension) == 0:
        list_neighbour_box_tempory[0] = 0
        list_neighbour_box_tempory[6] = 0
        list_neighbour_box_tempory[7] = 0
    if (((box+1) % (minesweeper_dimension)) == 0) and (box != 0):
        list_neighbour_box_tempory[2] = 0
        list_neighbour_box_tempory[3] = 0
        list_neighbour_box_tempory[4] = 0
    if (box < minesweeper_dimension):
        list_neighbour_box_tempory[0] = 0
        list_neighbour_box_tempory[1] = 0
        list_neighbour_box_tempory[2] = 0
    if (box >= ((minesweeper_dimension*minesweeper_dimension)-minesweeper_dimension)):
        list_neighbour_box_tempory[4] = 0
        list_neighbour_box_tempory[5] = 0
        list_neighbour_box_tempory[6] = 0
    list_neighbour_box = []
    list_tempory = [box-minesweeper_dimension-1 , box-minesweeper_dimension , box-minesweeper_dimension+1 , box+1 , box+minesweeper_dimension+1 , box+minesweeper_dimension,box+minesweeper_dimension-1,box-1]
    x = 0
    for i in list_neighbour_box_tempory:
        if i ==1:
            list_neighbour_box.append(list_tempory[x])
        x+=1
    return list_neighbour_box
    #finish============


def right_click(event):
    global game_on, minesweeper_dimension, active
    if active == False:
        begin_stopwatch()
    if game_on:
        x_position_click = event.x
        y_position_click = event.y
        x_calcul = x_position_click // 20
        y_calcul = y_position_click // 20
        number = x_calcul + ( y_calcul * minesweeper_dimension)
        click_box_flag(number)
        global nb_bombs
        if nb_bombs == 0:
            check_if_win()



def left_click(event):
    global game_on, minesweeper_dimension, active
    if active == False:
        begin_stopwatch()
    if game_on:
        x_position_click = event.x
        y_position_click = event.y
        x_calcul = x_position_click // 20
        y_calcul = y_position_click // 20
        number = x_calcul + ( y_calcul * minesweeper_dimension)
        click_box(number)



def click_box_flag(number):
    global dictionary_box, nb_bombs, image_box_list, nb_bombs_display
    if dictionary_box[number]["visible"]:
        pass
    else:
        if dictionary_box[number]["flag"]:
            dictionary_box[number]["flag"] = False
            image_box_list[number] = 0
            nb_bombs += 1
        else:
            dictionary_box[number]["flag"] = True
            nb_bombs -= 1
            update_box_screen([number])
        nb_bombs_display.set('{}'.format(nb_bombs))



def pause_game():
    global time_before_stop
    time_before_stop = float(stop_stopwatch())
      


def bye():
    time_before_stop = stop_stopwatch()
    global file, fini, dictionary_box, nb_click, nb_help, nb_bombs, image_box_list
    if fini == False:
        with open("save_previous_game.txt","wb") as file_txt:
            pickle_save = pickle.Pickler(file_txt)
            pickle_save.dump(dictionary_box)
            pickle_save.dump(nb_click)
            pickle_save.dump(nb_help)
            pickle_save.dump(nb_bombs)
            pickle_save.dump(time_before_stop)
            language = file[0]
        maker = "\n"
        file = maker.join(file)
        with open("Minesweeper_data.txt","w",encoding="UTF-8") as f:
            f.write(file)




def active_stopwatch():
    current_time = datetime.datetime.now()
    difference = current_time - begin_time
    time_counter_display.set('%d.%02d' %(difference.seconds,difference.microseconds//10000))
    if active:
        window.after(20,active_stopwatch)
    #finish----------------------



def begin_stopwatch():
    global active, begin_time, time_before_stop
    if not active:
        active = True
        begin_time = datetime.datetime.now() - datetime.timedelta(seconds=float(time_before_stop))
        window.after(10,active_stopwatch)
        #finish------------------



def stop_stopwatch():
    global active, time_counter_display
    active = False
    return time_counter_display.get()
    #finish-------------



def initialize_stopwatch(previous_time=0):
    global begin_time
    begin_time = datetime.datetime.now()
    if not active:
        begin_time = datetime.datetime.now()
        time_counter_display.set('{}'.format(previous_time))
        #finish----------------
"""-----------------------------------------------------------------------------------
---------------------------------------Main programme---------------------------------
-----------------------------------------------------------------------------------"""

#Setting the language (we check the previous language selected)
try:
    with open("Minesweeper_data.txt","r",encoding="UTF-8") as f:
        file = f.read()
        file = file.split("\n")
        language = file[0]
except:
    language = "français"

if language == "français":
    msg = ["Choix","Une partie était en cours, voulez_vous la reprendre ?"]
else:
    msg = ["Choice","A game was in progress, would you like to take it back?"]




#settings of differents things depending on the choice of the user
window = Tk()
minesweeper_dimension = int(file[2])
try:
    with open("save_previous_game.txt","rb") as file_txt:
        depickle = pickle.Unpickler(file_txt)
        dictionary_box = depickle.load()
        nb_click = depickle.load()
        nb_click = 0
        nb_help = depickle.load()
        nb_bombs = depickle.load()
        time_before_stop = depickle.load()
    if not(tk_box.askyesno(title=msg[0], message=msg[1])):
        a += 1
    previous_list_update = []
    for i in range(len(dictionary_box)):
        if (dictionary_box[i]["visible"] == True) or (dictionary_box[i]["flag"] == True):
            previous_list_update.append(i)

            
except:
    previous_list_update = []
    dictionary_box = []
    nb_click = 0
    nb_help = 0
    if int(file[1]) == 1:
        nb_bombs = 10
    elif int(file[1]) == 2:
        nb_bombs = 40
    else:
        nb_bombs = 99
    time_before_stop = 0

image_box_list = [0]*minesweeper_dimension*minesweeper_dimension








a=[] 
#reset the previous game data
with open("save_previous_game.txt","wb") as file_txt:
    pickle_save = pickle.Pickler(file_txt)
    pickle_save.dump(a)



#Setting of differents things
game_on = True
fini = True
lvl_difficulty = file[1]






#Window creation
if language == "français":
    window.title("Démineur")
else:
    window.title("Minesweeper")
window.iconbitmap("black_bomb.ico")
width_window = int(80+ minesweeper_dimension*20)
height_window = int(180 + minesweeper_dimension*20)
window.geometry("{}x{}".format(width_window,height_window))
window.resizable(width=False,height=False)





#Creation of the window menu
main_menu = Menu(window)

play_menu = Menu(main_menu, tearoff=0)
if language == "français":
    play_menu.add_command(label="Nouvelle partie",command=new_game)
    play_menu.add_command(label="Montrer une bombe", command=lambda: reveal_a_bomb())
    play_menu.add_command(label="Pause",command=pause_game)
    play_menu.add_separator()
    play_menu.add_command(label="Quitter", command=lambda: leave_game("Do you really want to quit ?"))          
else:
    play_menu.add_command(label="New game",command=new_game)
    play_menu.add_command(label="Reveal a bomb", command=lambda: reveal_a_bomb())
    play_menu.add_command(label="Pause",command=pause_game)
    play_menu.add_separator()
    play_menu.add_command(label="Quit",command=lambda: leave_game("Voulez-vous vraiment quitter ?"))
    
setting_menu = Menu(main_menu, tearoff=0)
if language == "français":
    setting_menu.add_command(label="Facile",command=lambda: change_in_file(1,"1"))
    setting_menu.add_command(label="Intermidaire",command=lambda: change_in_file(1,"2"))
    setting_menu.add_command(label="Difficile",command=lambda: change_in_file(1,"3"))
else:
    setting_menu.add_command(label="Easy",command=lambda: change_in_file(1,"1"))
    setting_menu.add_command(label="Medium",command=lambda: change_in_file(1,"2"))
    setting_menu.add_command(label="Hard",command=lambda: change_in_file(1,"3"))

language_menu = Menu(main_menu, tearoff=0)
if language == "français":
    language_menu.add_command(label="français",command=lambda: change_in_file(0,"français"))
    language_menu.add_command(label="anglais",command=lambda: change_in_file(0,"english"))
else:
    language_menu.add_command(label="french",command=lambda: change_in_file(0,"français"))
    language_menu.add_command(label="english",command=lambda: change_in_file(0,"english"))


help_menu = Menu(main_menu, tearoff=0)
if language == "français":
    help_menu.add_command(label="Règles", command= lambda : open_web("https://www.demineur-ligne.com/help/instructions"))
    help_menu.add_command(label="S'améliorer", command= lambda : open_web("http://n8on.free.fr/hackzines/shmeitcorp/6/Flash%20Tut%20XI/demineur/alwayswinatdemineur.html"))
    help_menu.add_separator()
    help_menu.add_command(label="Créé par Julien Chemillier", command= lambda : open_web("mailto:chemillier.julien@gmail.com"))
else:
    help_menu.add_command(label="Rules", command= lambda : open_web("https://www.instructables.com/id/How-to-play-minesweeper"))
    help_menu.add_command(label="Improve yourself", command = lambda : open_web("https://www.pcworld.com/article/238724/how-to-play-minesweeper-like-a-pro.html"))
    help_menu.add_separator()
    help_menu.add_command(label="Made by Julien Chemillier", command= lambda : open_web("mailto:chemillier.julien@gmail.com"))


if language == "français":
    main_menu.add_cascade(label="Jeu", menu=play_menu)
    main_menu.add_cascade(label="Option", menu=setting_menu)
    main_menu.add_cascade(label="Langue", menu=language_menu)
    main_menu.add_cascade(label="Aide", menu=help_menu)
else:
    main_menu.add_cascade(label="Game", menu=play_menu)
    main_menu.add_cascade(label="Setting", menu=setting_menu)
    main_menu.add_cascade(label="Language", menu=language_menu)
    main_menu.add_cascade(label="Help", menu=help_menu)



#images setting
image_black_bomb_nb = PhotoImage(master=window, file="black_bomb_nb.gif")
image_black_bomb = PhotoImage(master=window, file="black_bomb.gif")
image_red_bomb = PhotoImage(master=window, file="red_bomb.gif")
image_flag = PhotoImage(master=window, file="flag.gif")
image_watch = PhotoImage(master=window, file="watch.gif")



#frame empty setting
frame_empty_1 = Frame(window,height=40,width=width_window)
frame_empty_1.pack()



#frame display counter
frame_counter = Frame(window, height=40,width=width_window)

    #frame bomb counter
frame_counter_bomb = Frame(frame_counter, height=40, width=80,highlightbackground="black",highlightthickness=1)
nb_bombs_image = Label(frame_counter_bomb,image=image_black_bomb_nb)
nb_bombs_image.pack(side=LEFT,padx=(0,10))
frame_counter_bomb.pack(side=LEFT,padx=40)

    #frame time counter
frame_counter_time = Frame(frame_counter, height=40, width=80,highlightbackground="black",highlightthickness=1)
watch = Label(frame_counter_time,image=image_watch)
watch.pack(side=LEFT)
        #stopwatch setting
begin_time = None
active = False
time_counter_display = StringVar()
time_counter_display.set('0.00')
fontstyle = tk_font.Font(size=20)
stopwatch_time_counter = Label(frame_counter_time,textvariable= time_counter_display, font=fontstyle)
stopwatch_time_counter.pack(side=RIGHT)
frame_counter_time.pack(side=RIGHT)

frame_counter.pack()



#frame_empty_2 setting
frame_empty_2 = Frame(window,height=40,width=width_window)
frame_empty_2.pack()



#frame_empty_5 setting
frame_empty_5 = Frame(window,height=40,width=width_window)
frame_empty_5.pack(side=BOTTOM)



#frame_empty_3 setting
frame_empty_3 = Frame(window,height=(minesweeper_dimension*20),width=40)
frame_empty_3.pack(side= LEFT)



#frame_empty_4 setting
frame_empty_4 = Frame(window,height=(minesweeper_dimension*20),width=40)
frame_empty_4.pack(side=RIGHT)



#canvas
canvas_click = Canvas(window, width=(minesweeper_dimension*20),height=(minesweeper_dimension*20+20),bg="red")
#setting the click event
canvas_click.bind("<Button-1>",left_click)
canvas_click.bind("<Button-3>",right_click)
canvas_click.pack()


#bomb display setting
nb_bombs_display = StringVar()
nb_bombs_display.set('{}'.format(nb_bombs))
font_style  = tk_font.Font(size=20)
Label(frame_counter_bomb, textvariable=nb_bombs_display, font=font_style).pack(side=RIGHT)


grid_creation(minesweeper_dimension)
if len(previous_list_update) > 0:
    update_box_screen(previous_list_update)
window.config(menu=main_menu)
window.mainloop()

#save when the page is destroy
bye()

