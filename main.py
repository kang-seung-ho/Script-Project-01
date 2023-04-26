from customtkinter import *
from customtkinter import CTk as Tk
from customtkinter import CTkLabel as Label
from customtkinter import CTkFrame as Frame
from customtkinter import CTkButton as Button
from customtkinter import CTkEntry as Entry
from customtkinter import CTkTextbox as ScrolledText
from customtkinter import CTkCheckBox as Checkbutton
from customtkinter import CTkRadioButton as Radiobutton
import tkinter.messagebox as messagebox
import shutil
from PIL import Image
import datetime
import zipfile
# from fpdf import FPDF

window = Tk()
window.title('File Assistant')
window.geometry("640x280+600+200")
window.resizable(False, False)

#선택된 폴더 위치
selectedFolerpath=''

# #보이지 않는 액자
# first_line_frame=Frame(window)
# first_line_frame.pack()

def getPhotoDate(filepath):
    try:
        image = Image.open(filepath)
        if hasattr(image, '_getexif'):
            exifdata = image._getexif()
            if exifdata:
                for tag, value in exifdata.items():
                    if tag == 36867: # DateTimeOriginal tag
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

    # create folders for each year and month
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
                # 현재 처리중인 파일 진행상황 출력
                # nowpathlabel = Label(window, text='처리중 경로: ' + filepath)
                # nowpathlabel.place(x=0, y=80)

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


#python을 이용해 키워드 입력시  텍스트나 소스파일에 있는 그 내용에서 입력한 키워드가 포함된 파일을 따로 모아준다.
def get_KEYWORD_Files():
    # 1. 키워드 입력 받기
    keyword = input("Enter a keyword: ")

    # 2. 모든 파일을 탐색하여 키워드가 포함된 파일의 경로를 찾기
    found_files = []
    for root, dirs, files in os.walk("."):
        for filename in files:
            filepath = os.path.join(root, filename)
            with open(filepath, "r") as f:
                file_content = f.read()
                if keyword in file_content:
                    found_files.append(filename)

    # 3. 찾은 파일 이름을 리스트에 저장하기
    # 4. 저장된 파일 이름 출력하기
    if found_files:
        print("Found files:")
        for filename in found_files:
            print(filename)
    else:
        print("No files found.")


#특정 폴더 내에서 오늘 날짜를 기준으로 30일, 60일, 90일, 6개월 이상 사용하지 않은(액세스 하지 않은) 폴더 및 파일들에 대해서 따로 OLD 폴더로 옮겨주는 함수
def move_old_files(folder_path):
    # 1. 오늘 날짜 가져오기
    today = datetime.datetime.today()

    # 2. OLD 폴더 생성
    old_folder = os.path.join(folder_path, "OLD")
    if not os.path.exists(old_folder):
        os.mkdir(old_folder)

    # 3. 폴더 및 파일 탐색
    moved_files = []
    for root, dirs, files in os.walk(folder_path):
        for d in dirs:
            dir_path = os.path.join(root, d)
            try:
                accessed_time = os.path.getatime(dir_path)
            except:
                continue
            accessed_date = datetime.datetime.fromtimestamp(accessed_time)
            elapsed_days = (today - accessed_date).days
            if elapsed_days >= 30 and elapsed_days < 60:
                print(f"Moving {dir_path} to {old_folder}")
                shutil.move(dir_path, old_folder)
                moved_files.append(dir_path)
            elif elapsed_days >= 60 and elapsed_days < 90:
                print(f"Moving {dir_path} to {old_folder}")
                shutil.move(dir_path, old_folder)
                moved_files.append(dir_path)
            elif elapsed_days >= 90 and elapsed_days < 180:
                print(f"Moving {dir_path} to {old_folder}")
                shutil.move(dir_path, old_folder)
                moved_files.append(dir_path)
            elif elapsed_days >= 180:
                print(f"Moving {dir_path} to {old_folder}")
                shutil.move(dir_path, old_folder)
                moved_files.append(dir_path)

        for f in files:
            file_path = os.path.join(root, f)
            try:
                accessed_time = os.path.getatime(file_path)
            except:
                continue
            accessed_date = datetime.datetime.fromtimestamp(accessed_time)
            elapsed_days = (today - accessed_date).days
            if elapsed_days >= 30 and elapsed_days < 60:
                print(f"Moving {file_path} to {old_folder}")
                shutil.move(file_path, old_folder)
                moved_files.append(file_path)
            elif elapsed_days >= 60 and elapsed_days < 90:
                print(f"Moving {file_path} to {old_folder}")
                shutil.move(file_path, old_folder)
                moved_files.append(file_path)
            elif elapsed_days >= 90 and elapsed_days < 180:
                print(f"Moving {file_path} to {old_folder}")
                shutil.move(file_path, old_folder)
                moved_files.append(file_path)
            elif elapsed_days >= 180:
                print(f"Moving {file_path} to {old_folder}")
                shutil.move(file_path, old_folder)
                moved_files.append(file_path)

    # 4. OLD 폴더로 이동한 파일 리스트를 이메일로 보내기
    # send_email(moved_files)

def send_email(moved_files):
    pass
    # # 1. 이메일 설정
    # smtp_server = "smtp.gmail.com"  # SMTP 서버 주소
    # smtp_port = 587  # SMTP 포트 번호
    # sender_email = "sender_email_address"  # 발신자 이메일 주소
    # sender_password = "sender_email_password"  # 발신자 이메일 비밀번호
    # recipient_email = "recipient_email_address"  # 수신자 이메일 주소
    #
    # # 2. 이메일 내용 생성
    # message = MIMEMultipart()
    # message["From"] = sender_email
    # message["To"] = recipient_email
    # message["Subject"] = "Moved Files List"
    # message.attach(MIMEText("\n".join(moved_files), "plain"))
    #
    # # 3. SMTP 서버에 로그인하여 이메일 보내기
    # with smtplib.SMTP(smtp_server, smtp_port) as server:
    #     server.starttls()
    #     server.login(sender_email, sender_password)
    #     server.sendmail(sender_email, recipient_email, message.as_string())




getEXT = Button(window, text='입력한 확장자 모으기', width=30 , command=None)
getEXT.place(x=0, y=100)


#정보 및 도움말 팝업
def showInfo():
    messagebox.showinfo('도움말', '폴더 선택 후 사진 분류버튼을 누르세요.\n선택된 폴더 내의 사진들을 연월별로 분류합니다.\nTOPDF: 워드, PPT 파일을 PDF로 변환할 수 있습니다.\n오래된 파일 정리: 폴더 선택 후 오래된 기준을 선택하면 정리가 시작됩니다. \n\n 만든이: 한국공학대학교 게임공학과 강승호')


InfoButton = Button(window, text='도움말', width=15, command=showInfo)
InfoButton.place(x=500, y=20)


def stop(event=None):
    window.quit()



# from tkinter import *
# menu = Menu()
# menu_quit = Menu(menu, tearoff=False)
# menu_quit.add_command(label="끝내기", accelerator='Ctrl+Q', command=stop)

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
        convert_to_pdf(selectedFilePath, output_file)


import comtypes.client

def convert_to_pdf(input_file, output_file):
    # MS Office 어플리케이션 생성
    powerpoint = comtypes.client.CreateObject('Powerpoint.Application')
    word = comtypes.client.CreateObject('Word.Application')

    input_file = os.fsdecode(input_file)  # 파일 경로에 있는 Unicode 문자를 처리합니다.
    output_file = os.fsdecode(output_file)  # 파일 경로에 있는 Unicode 문자를 처리합니다.

    try:
        # PPT 파일을 PDF로 변환
        if input_file.endswith('.ppt') or input_file.endswith('.pptx'):
            presentation = powerpoint.Presentations.Open(input_file)
            presentation.SaveAs(output_file, FileFormat=32)  # ppSaveAsPDF 상수 값 (32)를 직접 사용합니다.
            presentation.Close()

        # Word 파일을 PDF로 변환
        elif input_file.endswith('.doc') or input_file.endswith('.docx'):
            document = word.Documents.Open(input_file)
            document.SaveAs(output_file, FileFormat=17)  # wdFormatPDF 상수 값 (17)를 직접 사용합니다.
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



def zip_and_remove_old_folder():
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

    zip_and_remove_old_folder()


def select_gijun_Date_popup():
    if selectedFolerpath == '':
        messagebox.showerror('에러', '폴더를 먼저 지정하십시오')
        return

    global days
    popup = CTkToplevel(window)
    popup.title('기준 기간 선택창')
    popup.geometry('300x240+700+400')
    popup.transient(window)
    # option = IntVar(value=0)

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

    def on_confirm():
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

    confirm_button = Button(popup, text='기간 선택', command=on_confirm)
    confirm_button.pack(side=BOTTOM)

select_gijun_Date_Button = Button(window, text='오래된 파일 모으기: 기간 선택하기', command=select_gijun_Date_popup)
select_gijun_Date_Button.place(x=170, y=20)


# window.config(menu=menu)

window.bind('<Escape>', stop)
window.mainloop()
