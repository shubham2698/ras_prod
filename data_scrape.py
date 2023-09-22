import fitz  # PyMuPDF library


try:
    pdf_document = fitz.open("APR23.pdf")
    extracted_text = ''
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        extracted_text += page.get_text()
except Exception as e:
    print("An error occurred:", str(e))


try:
    file = open(f"TEMP/APR23.csv", "w")
    column_name = "SEAT NO,PRN NO,SEX,MOTHER NAME,SEM,NAME OF STUDENT,SUBJECT CODE,INTERNAL,EXTERNAL,TOTAL,GRADE,GRADE POINT\n"
    file.write(column_name)
except Exception:
    print("Error : Creating file APR23.csv failed.")

extracted_text=extracted_text.split("\n")

for i in range(len(extracted_text)):
    each_line = extracted_text[i]
    word_list = [word for word in each_line.split(' ') if word]
    # print(len(each_line),each_line)
    # and each_line.lstrip().startswith("46", 1, 4)

    if len(each_line) == 133 :
        try:
            seat_no = int(each_line[1:6].strip())
            prn_no = int(each_line[82:96].strip())
            sex = each_line[80].strip()
            mother_name = each_line[52:70].strip()
            sem = int(each_line[96:99].strip())
            name = each_line[8:51].strip()
            print(seat_no, prn_no, sex, mother_name, sem, name)
        except ValueError:
            pass

    try:
        if len(word_list[0].strip()) == 3:
            # print(each_line[0:29])
            # {seat_no},{prn_no},{sex},{mother_name},{sem},{name},
            if f"{each_line[0:4].strip()},{each_line[7:11].strip()},{each_line[12:15].strip()},{each_line[17:20].strip()},{each_line[22:24].strip()},{each_line[25:29].strip()}" != ",,,,,":
                file.write(
                    f"{seat_no},{prn_no},{sex},{mother_name},{sem},{name},{each_line[0:4].strip()},{each_line[7:11].strip()},{each_line[12:15].strip()},{each_line[17:20].strip()},{each_line[22:24].strip()},{each_line[25:29].strip()}\n")
            # print(each_line[30:59])
            if f"{each_line[30:34].strip()},{each_line[37:41].strip()},{each_line[42:45].strip()},{each_line[47:50].strip()},{each_line[52:54].strip()},{each_line[55:59].strip()}" != ",,,,,":
                file.write(
                    f"{seat_no},{prn_no},{sex},{mother_name},{sem},{name},{each_line[30:34].strip()},{each_line[37:41].strip()},{each_line[42:45].strip()},{each_line[47:50].strip()},{each_line[52:54].strip()},{each_line[55:59].strip()}\n")
            # print(each_line[60:89])
            if f"{each_line[60:64].strip()},{each_line[67:71].strip()},{each_line[72:75].strip()},{each_line[77:80].strip()},{each_line[82:84].strip()},{each_line[85:89].strip()}" != ",,,,,":
                file.write(
                    f"{seat_no},{prn_no},{sex},{mother_name},{sem},{name},{each_line[60:64].strip()},{each_line[67:71].strip()},{each_line[72:75].strip()},{each_line[77:80].strip()},{each_line[82:84].strip()},{each_line[85:89].strip()}\n")
            # print(each_line[90:119])
            if f"{each_line[90:94].strip()},{each_line[97:101].strip()},{each_line[102:105].strip()},{each_line[107:110].strip()},{each_line[112:114].strip()},{each_line[115:119].strip()}" != ",,,,,":
                file.write(
                    f"{seat_no},{prn_no},{sex},{mother_name},{sem},{name},{each_line[90:94].strip()},{each_line[97:101].strip()},{each_line[102:105].strip()},{each_line[107:110].strip()},{each_line[112:114].strip()},{each_line[115:119].strip()}\n")

    except IndexError:
        pass

