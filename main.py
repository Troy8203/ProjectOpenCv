from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2


class Interfaz:
    def __init__(self, root):
        self.root = root
        self.botones()
        self.labels()
        self.textb()

    def botones(self):
        bnt1 = self.crear_boton(valor='...', funcion='open')
        bnt1.grid(row=2, column=2, padx=10)
        bnt1 = self.crear_boton(valor='CONTAR', funcion='contar')
        bnt1.grid(row=3, column=1, padx=10)
        bnt1 = self.crear_boton(valor='SALIR', funcion='cancelar')
        bnt1.grid(row=3, column=2, padx=10)

    def labels(self):
        lb1 = Label(self.root, text='CONTADOR DE OBJETOS', bg='#070A0E', fg='#09A094', font=('', 12, 'bold'), pady=10,
                    padx=5)
        lb1.grid(row=0, column=0, columnspan=4, sticky='nsew')
        lb1 = self.crear_label(valor='UBICACION IMAGEN :')
        lb1.grid(row=1, column=1, columnspan=2, sticky='nsew', pady=2)
        lb2 = self.crear_label(valor='#Nro OBJETOS :')
        lb2.grid(row=4, column=1, sticky='nsew', pady=2)

    def textb(self):
        txtb1 = self.crear_textbox('disable', ruta)
        txtb1.grid(row=2, column=1)
        txtb1 = self.crear_textbox('disable', cont)
        txtb1.grid(row=4, column=2)

    @staticmethod
    def funcion_boton(cad):
        if cad == 'cancelar':
            root.destroy()
        elif cad == 'contar':
            ImageCV.contador_obj(ruta.get())
            Interfaz.load_image(ruta.get()[:len(ruta.get()) - 4] + '(bordes).jpg')
        elif cad == 'open':
            Interfaz.open_file()

    @staticmethod
    def load_image(path_img):
        img2 = ImageTk.PhotoImage(file=path_img)
        panel.config(image=img2)
        panel.image = img2
        ruta.set(path_img)

    @staticmethod
    def open_file():
        file_img = filedialog.askopenfile()
        Interfaz.load_image(file_img.name)

    def crear_boton(self, valor, funcion):
        return Button(self.root, bd=0, text=valor, bg='#070A0E', fg='#09A094', font=('', 10, 'bold'), relief='flat'
                      , cursor='hand2', activebackground='#09A094', activeforeground='#070A0E',
                      command=lambda: self.funcion_boton(funcion)
                      , width=10)

    def crear_textbox(self, estado, var):
        return Entry(self.root, relief='solid', state=estado, textvariable=var, width=15)

    def crear_label(self, valor):
        return Label(self.root, text=valor, bg='#15202B', fg='#09A094', font=('', 10, 'bold'), pady=0, padx=5)


class ImageCV:

    @staticmethod
    def read_image(path_img):
        if isinstance(path_img, str):
            img_ = cv2.imread(path_img)
            return img_
        else:
            print("formato no valido")

    @staticmethod
    def change_color_gray(path_img):
        return cv2.cvtColor(cv2.imread(path_img), cv2.COLOR_BGR2GRAY)

    @staticmethod
    def save_image(name_img, image):
        cv2.imwrite(name_img + '.jpg', image)

    @staticmethod
    def contador_obj(path_img):
        img_cv = cv2.imread(path_img)
        img_cv_gris = ImageCV.change_color_gray(path_img)
        borde = cv2.Canny(img_cv_gris, 200, 250)
        contador, _ = cv2.findContours(borde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img_cv, contador, -1, (0, 0, 255), 2)
        ImageCV.save_image(path_img[:len(path_img) - 4] + '(bordes)', img_cv)
        cont.set(str(len(contador)) + ' Objetos')


root = Tk()
#variables
ruta = StringVar()
ruta.set('imagenes\\img0.jpg')
cont = StringVar()
cont.set('0 Objetos')

imagencv = ImageCV.read_image(ruta.get())

#Configuracion para ventana
root.config(bg='#15202B')
root.geometry('595x290')
root.resizable(FALSE,FALSE)
ventana = Interfaz(root)
img = ImageTk.PhotoImage(Image.open(ruta.get()))
root.overrideredirect(1)

#Cetreado de ventana
width = 595
height = 290
root.withdraw()
root.withdraw()
ejex=root.winfo_screenwidth()/2
ejey=root.winfo_screenheight()/2
root.geometry('%dx%d+%d+%d' % (width,height,ejex-(width/2),ejey-(height/2)))
root.wm_deiconify()

#Ventana para Imagenes
panel = Label(root, image=img, width=348, height=220)
panel.grid(row=1, column=0, pady=10, padx=10, rowspan=8)

root.mainloop()
