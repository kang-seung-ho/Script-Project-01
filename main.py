from customtkinter import *
from customtkinter import CTk as Tk
from customtkinter import CTkLabel as Label
from customtkinter import CTkButton as Button
from customtkinter import CTkRadioButton as Radiobutton
import tkinter.messagebox as messagebox
import shutil
from PIL import Image
import datetime
import zipfile

window = Tk()
window.title('File Assistant')
window.geometry("640x280+600+200")
window.resizable(False, False)

#선택된 폴더 위치
selectedFolerpath=''


def getPhotoDate(filepath):
    try:
        image = Image.open(filepath)
        if hasattr(image, '_getexif'):
            exifdata = image._getexif()
            if exifdata:
                for tag, value in exifdata.items():
                    if tag == 36867: # 날짜태그
                        return datetime.datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
    except Exception as errorN:
        messagebox.showerror('에러', '날짜를 불러오지 못한 사진이 있습니다.')
    return None


def sortPictures():
    global selectedFolerpath
    #폴더가 지정되지 않았을때를 대비해 예외처리 추가
    if selectedFolerpath == '':
        messagebox.showerror('에러', '폴더를 먼저 지정하십시오')
        return
    #사진이 있는 날에 대해서만 연, 월 폴더 추가
    for filename in os.listdir(selectedFolerpath):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            filepath = os.path.join(selectedFolerpath, filename)
            date_taken = getPhotoDate(filepath)
            if date_taken:
                year_folder = os.path.join(selectedFolerpath, str(date_taken.year) + "년")
                if not os.path.exists(year_folder):
                    os.makedirs(year_folder)
                month_folder = os.path.join(year_folder, str(date_taken.month) + "월")
                if not os.path.exists(month_folder):
                    os.makedirs(month_folder)
                shutil.move(filepath, month_folder)

    #완료되었다는 팝업창 띄우기
    messagebox.showinfo('완료 안내', '사진 정리가 끝났습니다.')
    selectedFolerpath = ''




sortPicButton = Button(window, text='사진분류하기', width=25, command=sortPictures)
sortPicButton.place(x=70, y=20)



#선택한 폴더 경로 출력

pathlabel=Label(window, text='폴더 경로: '+ selectedFolerpath)
pathlabel.place(x=0, y=50)


def selectFolder():
    global selectedFolerpath
    global pathlabel
    selectedFolerpath = filedialog.askdirectory(title="폴더 선택")
    pathlabel.configure(text='폴더 경로: ' + selectedFolerpath)  # 경로 출력을 위해 label 업데이트


selectFolButton = Button(window, text='폴더 선택', width=15,command=selectFolder)
selectFolButton.place(x=0, y=20)


import chardet

def fileReadTypes(filename):
    ext = ['.txt', '.py', '.c', '.cpp', '.java', '.js', '.go', '.rb', '.rs', '.php']
    return any(filename.endswith(ext) for ext in ext) #filename이 ext안에 해당하는 파일이면 true리턴


def getKeywordFiles(keyword):
    global selectedFolerpath
    if selectedFolerpath == '':
        messagebox.showerror('에러', '폴더를 먼저 지정하십시오')
        return
    sorted_keyword_path = selectedFolerpath + '/' + keyword
    if not os.path.exists(sorted_keyword_path):
        os.makedirs(sorted_keyword_path)

    for root, dirs, files in os.walk(selectedFolerpath):
        for file in files:
            if fileReadTypes(file):
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    binary_contents = f.read()
                detected = chardet.detect(binary_contents)
                encoding = detected['encoding']
                contents = binary_contents.decode(encoding)

                if keyword in contents:
                    dest_dir = sorted_keyword_path
                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)
                    dest_path = os.path.join(dest_dir, file)

                    # 원본 파일과 대상 파일이 동일한지 확인하고 같으면 건너뜀
                    if os.path.abspath(file_path) == os.path.abspath(dest_path):
                        continue
                    shutil.copy(file_path, dest_path)
    messagebox.showinfo('성공', '입력한 키워드가 포함된 파일을 모아왔습니다.')
    selectedFolerpath = ''
    global pathlabel
    pathlabel.configure(text='폴더 경로: ' + selectedFolerpath)  # 경로 출력을 위해 label 업데이트


def getKEYWORD():
    input_text = inputbox.get()
    getKeywordFiles(input_text)


getKeyword = Button(window, text='입력한 키워드 포함된파일 모으기', width=30, command=getKEYWORD)
getKeyword.place(x=280, y=100)




copied_ext = list()
def copy_files_EXT(ext):

    global selectedFolerpath
    extflag=False
    if selectedFolerpath == '':
        messagebox.showerror('에러', '폴더를 먼저 지정하십시오')
        return
    sorted_files_folder = os.path.join(selectedFolerpath, '분류된 파일')
    if not os.path.exists(sorted_files_folder):
        os.makedirs(sorted_files_folder)

    ext_folder = os.path.join(sorted_files_folder, ext)


    for root, dirs, files in os.walk(selectedFolerpath):
        for file in files:
            if file.endswith(ext):
                if not os.path.exists(ext_folder):
                    os.makedirs(ext_folder)
                    copied_ext.append(ext)
                    extflag=True
                if ext in copied_ext:
                    extflag=True
                abspath = os.path.join(root, file)
                movedpath = os.path.join(ext_folder, file)
                if abspath != movedpath:
                    shutil.copy(abspath, movedpath)
    if extflag==True:
        messagebox.showinfo('성공', f'{ext} 파일끼리 분류가 완료되었습니다.')
    else:
        messagebox.showerror('실패', f'{ext} 파일이 없거나 분류에 실패했습니다.')




#확장자 입력받기
def gettext():
    input_text = inputbox.get()
    copy_files_EXT(input_text)

inputbox = CTkEntry(window, width=100)
inputbox.place(x=0, y=100)

getEXT = Button(window, text='입력한 확장자 모으기', width=30, command=gettext)
getEXT.place(x=130, y=100)



#정보 및 도움말 팝업
def showInfo():
    messagebox.showinfo('도움말', '폴더 선택 후 사진 분류버튼을 누르세요.\n선택된 폴더 내의 사진들을 연월별로 분류합니다.\nTOPDF: 워드, PPT 파일을 PDF로 변환할 수 있습니다.\n오래된 파일 정리: 폴더 선택 후 오래된 기준을 선택하면\nOLD.zip 파일로 모으는 정리가 시작됩니다.\n입력한 확장자 모으기: 폴더 선택 후 박스에 원하는 확장자를\n입력하면 입력한 확장자 이름의 폴더로 해당 확장자 파일들을 복사합니다. \n\n만든이: 2019182001 게임공학과 강승호')


InfoButton = Button(window, text='도움말', width=15, command=showInfo)
InfoButton.place(x=530, y=20)





selectedFilePath = ''

import os
import comtypes.client


def select_File():
    selectedFilePaths = filedialog.askopenfilenames()  # 여러 파일을 선택할 수 있게 변경
    for selectedFilePath in selectedFilePaths:
        selectedFilePath = os.path.abspath(selectedFilePath)  # 파일 경로를 절대 경로로 변환
        selectedFilePath = os.path.normpath(selectedFilePath)  # 파일 경로 정규화
        file_name = os.path.splitext(os.path.basename(selectedFilePath))[0]
        output_dir = os.path.dirname(selectedFilePath)
        output_file = os.path.join(output_dir, file_name + '.pdf')
        convert2PDF(selectedFilePath, output_file)


def convert2PDF(input_file, output_file):
    # MS Office 어플리케이션 생성
    powerpoint = comtypes.client.CreateObject('Powerpoint.Application')
    word = comtypes.client.CreateObject('Word.Application')

    input_file = os.fsdecode(input_file)  # 파일 경로에 있는 유니코드문자처리
    output_file = os.fsdecode(output_file)  # 파일 경로에 있는 유니코드문자처리

    try:
        # PPT -> PDF
        if input_file.endswith('.ppt') or input_file.endswith('.pptx'):
            presentation = powerpoint.Presentations.Open(input_file)
            presentation.SaveAs(output_file, FileFormat=32)  # 파워포인트를 pdf로 저장하는 상수값 32
            presentation.Close()

        # Word -> PDF
        elif input_file.endswith('.doc') or input_file.endswith('.docx'):
            document = word.Documents.Open(input_file)
            document.SaveAs(output_file, FileFormat=17)  # 워드를 pdf로 저장하는 상수값 17
            document.Close()

        # 지원하지 않는 파일 형식인 경우
        else:
            messagebox.showerror('에러', '지원하지 않는 파일입니다.\n워드,PPT 형식만 지원합니다.')
            return False

    except Exception as e:
        messagebox.showerror('에러', e)
        return False


    # MS Office 어플리케이션 종료
    powerpoint.Quit()
    word.Quit()
    messagebox.showinfo('변환성공', '선택한 파일을 성공적으로 PDF로 변환하였습니다.')



PDFBUTTON = Button(window, text='TO PDF 파일 선택', width=20, command=select_File)
PDFBUTTON.place(x=0, y=150)


days = IntVar()
days.set(0)



def zip_and_remove_OLD():
    global selectedFolerpath
    old_folder = os.path.join(selectedFolerpath, 'OLD')
    zip_file = os.path.join(selectedFolerpath, 'OLD.zip')

    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(old_folder):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, old_folder))

    shutil.rmtree(old_folder)
    selectedFolerpath = ''
    messagebox.showinfo('완료', '정리가 완료되었습니다')
    global pathlabel
    pathlabel.configure(text='폴더 경로: ' + selectedFolerpath)  # 경로 출력을 위해 label 업데이트
    return


def move_old_files(days_threshold):
    now = datetime.datetime.now()
    old_folder = os.path.join(selectedFolerpath, 'OLD')

    if not os.path.exists(old_folder):
        os.makedirs(old_folder)

    for file in os.listdir(selectedFolerpath):
        file_path = os.path.join(selectedFolerpath, file)
        if os.path.isfile(file_path):
            file_age = now - datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_age.days > days_threshold.get():  # get() 메서드를 사용하여 IntVar 값으로 가져옴 (int랑 intVar이랑 비교가 안되기 때문에 수정함)
                shutil.move(file_path, os.path.join(old_folder, file))

    zip_and_remove_OLD()


def select_gijun_Date_popup():
    if selectedFolerpath == '':
        messagebox.showerror('에러', '폴더를 먼저 지정하십시오')
        return

    global days
    popup = CTkToplevel(window)
    popup.title('기준 기간 선택창')
    popup.geometry('300x240+700+400')
    popup.transient(window)

    option1_radiobutton = Radiobutton(popup, text="7 days", variable=days, value=7)
    option2_radiobutton = Radiobutton(popup, text="14 days", variable=days, value=14)
    option3_radiobutton = Radiobutton(popup, text="30 days", variable=days, value=30)
    option4_radiobutton = Radiobutton(popup, text="90 days", variable=days, value=90)
    option5_radiobutton = Radiobutton(popup, text="180 days", variable=days, value=180)
    option1_radiobutton.pack()
    option2_radiobutton.pack()
    option3_radiobutton.pack()
    option4_radiobutton.pack()
    option5_radiobutton.pack()

    def date_confirm():
        if days.get() == 7:
            messagebox.showinfo('확인', '7일을 선택하셨습니다.\n열어본지 7일 이상된 파일들을 정리합니다.')
            move_old_files(days)
        elif days.get() == 14:
            messagebox.showinfo('확인', '14일을 선택하셨습니다.\n열어본지 14일 이상된 파일들을 정리합니다.')
            move_old_files(days)
        elif days.get() == 30:
            messagebox.showinfo('확인', '30일을 선택하셨습니다.\n열어본지 30일 이상된 파일들을 정리합니다.')
            move_old_files(days)
        elif days.get() == 4:
            messagebox.showinfo('확인', '90일을 선택하셨습니다.\n열어본지 90일 이상된 파일들을 정리합니다.')
            move_old_files(days)
        elif days.get() == 5:
            messagebox.showinfo('확인', '180일을 선택하셨습니다.\n열어본지 180일 이상된 파일들을 정리합니다.')
            move_old_files(days)
        else:
            messagebox.showinfo('선택하세요', '옵션을 선택해주세요.')
        popup.destroy()

    confirm_button = Button(popup, text='기간 선택', command=date_confirm)
    confirm_button.pack(side=BOTTOM)

select_gijun_Date_Button = Button(window, text='오래된 파일 모으기: 기간 선택하기', command=select_gijun_Date_popup)
select_gijun_Date_Button.place(x=170, y=20)

def stop(event=None):
    window.quit()

window.bind('<Escape>', stop)
window.mainloop()
