from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image

root = Tk()
root.title("Survival Transform")
content = ttk.Frame(root)
content.grid()


#Set global variables
samplinganswer = StringVar()
retainedanswer = StringVar()
inputanswer = StringVar()
outputanswer = StringVar()

#Define main function

def mainfunction():
    global samplinganswer, retainedanswer, inputanswer, outputanswer
    importfile = str(inputanswer.get()) + '.csv'
    outputfile = str(outputanswer.get()) + '.csv'

    import csv
    with open(importfile, 'r') as f:
        reader = csv.reader(f)
        xdata = list(reader)
    
    timeunit = "Day"
    days= int(samplinganswer.get())
    position = 1
    extra = int(retainedanswer.get())
    censor = len(xdata[0])

    extra = -1 * extra #We want to use those extra columns, and we can address them in lists by using minus (to go from the back)

    #Take all the labels (first row) and store in new dataframe. This will be the labels for the transformed file.
    ydata = [list(xdata[0])]

    #delete all the 'time points' from ydata, so only useful labels are left over. First the censor row is removed.
    #Then, all the timepoints except one (we need one column leftover)
    del ydata[0][censor-1]
    del ydata[0][position-1:position-2+days]

    #Name first column to the time-unit used during experiment (e.g. Day)
    ydata[0][0] = timeunit
    #Append row for censored data (0's and 1's).
    ydata[0].append("Censor")

    #Run the for loop over all the table except first row of labels
    limiti=1
    for i in xdata[1:]: #for each row in xdata except the first (which contains the labels)
        limitj = 0
        for j in i: #For each element of that row
            if j.isdigit() and xdata[0][limitj].isdigit(): #If that element is a number. The 'and' clause makes sure we are not looking at the 'censor' column, which also consists of digits. So to do that, we look at the column name, which are digits for time points.
                b = xdata[0][limitj] #save the label the column wherein this element is positioned (e.g. day 1).
                ydata.extend([b] + xdata[limiti][extra-1:-1] + [1]  for k in range(int(j))) #extend data file with day of death + treatments for each individual. Afterwards add a 1 for censoring (because it died).
                limitj += 1
        ydata.extend([4] + xdata[limiti][extra-1:-1] + [0] for k in range(int(xdata[limiti][censor-1]))) #Now find out how many individuals were alive at the end of the experiment per treatment, and extend list with that number of 0's.
        limiti+=1


    #Save everything into a new file called newfile.csv
    b = open(outputfile, 'w', newline='')
    a = csv.writer(b)
    a.writerows(ydata)
    b.close()

    #Show confirmation message
    messagebox.showinfo(message='Done! File saved as %s!' %outputfile)

#Create helpframe when help is pressed
def helpframe():
    roothelp = Tk()
    roothelp.title("Help")
    contenthelp = ttk.Frame(roothelp)
    contenthelp.grid()

    #Helpfile labels
    Helplabel = ttk.Label(contenthelp, text ="This software is for biologists who want to analyse their survival data in R, \
but don't want to type in 1000s of lines of data.\n\
The first columns have to contain your mortality data (Column 1 is first time of measurement, column 2 the 2nd, etc.).\n\
After that there can be columns with treatments and notes.\n\
Lastly, there should be a column with how many individuals were still alive at the end of the experiment (in order to censor data), this can be 0.\n\
Data has to be in .csv format")
    Helplabel.grid()
   
# Set inputs of all important variables, and show them in green

Samplinglabel = ttk.Label(content, text = 'How many timepoints did you sample?')
Samplingentry = ttk.Entry(content, width=8, textvariable = samplinganswer)
Samplinganswerlabel = ttk.Label(content, textvariable=samplinganswer, width = 10, foreground = "Green")

Retainedlabel = ttk.Label(content, text = 'How many columns (treatments, notes etc.) should be retained?')
Retainedentry = ttk.Entry(content, width=8, textvariable = retainedanswer)
Retainedanswerlabel = ttk.Label(content, textvariable = retainedanswer, width = 10, foreground = "Green")

Inputnamelabel = ttk.Label(content, text = 'What is the input file called?')
Inputnameentry = ttk.Entry(content, width=8, textvariable = inputanswer)
Inputanswerlabel = ttk.Label(content, textvariable = inputanswer, width = 10, foreground = "Green")

Outputnamelabel = ttk.Label(content, text = 'What do you want the output file to be called?')
Outputnameentry = ttk.Entry(content, width=8, textvariable = outputanswer)
Outputanswerlabel = ttk.Label(content, textvariable = outputanswer, width = 10, foreground = "Green")

Warninglabel = ttk.Label(content, foreground="Red", text = "Warning, the input should be a .csv file.")
Warninglabel2 = ttk.Label(content, foreground="Red", text = "Do not include .csv in your name. So type 'example.csv' as 'example'")                        

Gobutton = ttk.Button(text = "Tranform!", command = mainfunction)
Helpbutton = ttk.Button(text ="Help!", command = helpframe)



# Put all labels, entries and buttons on the frame

Samplinglabel.grid(column=1, row = 0, sticky = (W))
Samplingentry.grid(column=2, row=0, sticky=(W,E))
Samplinganswerlabel.grid(column=3, row=0)

Retainedlabel.grid(column=1, row= 1, sticky=(W))
Retainedentry.grid(column=2, row = 1, sticky =(W,E))
Retainedanswerlabel.grid(column=3, row=1)

Inputnamelabel.grid(column=1, row= 2, sticky=(W))
Inputnameentry.grid(column=2, row = 2, sticky =(W,E))
Inputanswerlabel.grid(column=3, row=2)

Outputnamelabel.grid(column=1, row= 3, sticky=(W))
Outputnameentry.grid(column=2, row = 3, sticky =(W,E))
Outputanswerlabel.grid(column=3, row=3)

Warninglabel.grid(column=1,  columnspan = 2,row =4, sticky =(W))
Warninglabel2.grid(column=1,  columnspan = 2,row =5, sticky =(W))

Gobutton.grid(column=4)
Helpbutton.grid(column=4)

root.mainloop()
