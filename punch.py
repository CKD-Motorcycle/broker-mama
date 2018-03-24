#                                         This is mah lyf...

from tkinter import *
from PIL import ImageTk,Image
import sqlite3
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as pyplot

#prerequisites--------------------
def _quit():
    main.quit()
    main.destroy()

dark='#2b2927'
sec_accent="#66757f"
accent="#55acee"
table="apple"
sqldb="stocks.sqlite"
newsdb="news.sqlite"
#main window----------------------------
main=Tk()
main.lift()
main.geometry("1200x600")
main.title('stock market helper')
main.configure(bg=dark)
main.protocol('WM_DELETE_WINDOW', _quit)

#title frame------------------------------
tit=Frame(main)
tit.configure(bg=dark)
tit.grid(row=0,column=0,sticky=W+N+E+S)
Grid.rowconfigure(main,0,weight=0)

title=Label(tit,text="Broker Mama",font="Times 20 bold italic",bg=accent,fg="white").pack(fill=BOTH,expand=1)

settings=Button(tit,text="settings",bitmap="info",bg=dark,fg=sec_accent).pack(side=RIGHT)

#content frame---------------------------
content=Frame(main,bg=dark)
content.grid(row=1,sticky=N+W+E+S,padx=20,pady=20,ipadx=10,ipady=10)
Grid.rowconfigure(main,1,weight=0)

Grid.rowconfigure(content,0,weight=1)

#matplot  column
mplot=Frame(content,bg="black")
mplot.grid(row=0,column=1,sticky=N+E+W+S,padx=5,pady=5)
Grid.columnconfigure(content,1,weight=15)
plottitle=Label(mplot,text='Sony',bg=dark,fg=sec_accent)
plottitle.pack(side=TOP,fill=X,expand=1)
pic=Image.open('grph.png')
photo=ImageTk.PhotoImage(pic)
plt=Label(mplot,background=dark,image=photo)
plt.image=photo
plt.pack(fill=BOTH,expand=1)
def plot(table):
    global plt
    conn=sqlite3.connect(sqldb)
    cursor=conn.cursor()
    f,ax=pyplot.subplots(2,2)
    f.tight_layout()
    f.patch.set_facecolor(accent)
    for i,v in enumerate(['open', 'high','low','close']):
        cursor.execute("select "+ v + " from " + table )
        ax[i//2,i%2].set_title(v.title())
        ax[i//2,i%2].set_facecolor(dark)
        ax[i//2,i%2].yaxis.label.set_color(sec_accent)
        ax[i//2,i%2].xaxis.set_visible(False)
        y=cursor.fetchall()
        ax[i//2,i%2].plot(range(len(y)),y[::-1])
    pyplot.savefig(table+'.png',dpi=75,bbox_inches='tight',transparent=False)
    photo=ImageTk.PhotoImage(Image.open(table+'.png'))
    plt.configure(image=photo)
    plt.image=photo
    plottitle.configure(text=table.title())
    main.update()
#company list column
comp=Frame(content,bg=dark)
comp.grid(row=0,column=0,sticky=N+E+W+S,padx=5,pady=5,ipadx=5,ipady=5)
Grid.columnconfigure(content,0,weight=5)

comp_list=['apple','google','amazon','microsoft','sony']

for ind,c in enumerate(comp_list):
    Button(comp,text=c.title(),font="Times 13",fg=accent,bd=0,highlightbackground=dark,bg=sec_accent,command=lambda i=c: plot(i),padx=0,pady=0).pack(fill=BOTH,expand=1)

#trends column
trend=Frame(content,bg=sec_accent)
trend.grid(row=0,column=2,sticky=N+E+W+S,padx=5,pady=5)

Grid.columnconfigure(content,2,weight=2)

Grid.columnconfigure(main,0,weight=1)


#news frame----------------------------
news=Frame(main,bg=dark,bd=1)
newstitle=Label(news,bg=dark,fg=sec_accent,text='News').pack(side=TOP,fill=X,expand=1)
news.grid(row=2,sticky=N+W+E+S,ipadx=10,ipady=10)
story=Text(news,bg=dark,fg=accent)
conn=sqlite3.connect(newsdb)
story.pack(side=TOP,fill=BOTH,expand=1)
cursor=conn.cursor()
cursor.execute('select * from news;')
data=cursor.fetchall()
data=[j for i in data for j in i]
story.insert(END,'\n\n'.join(data))
story.configure(state=DISABLED)

Grid.rowconfigure(main,2,weight=1)

main.mainloop()
