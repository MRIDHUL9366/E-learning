from django.shortcuts import render, redirect
from datetime import datetime
import datetime
from . models import *
from django.utils import timezone
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, auth
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse



def home(request):
    total = Registration.objects.all()
    cat_tot = Category.objects.all()
    tea = 0
    stu = 0
    cat = 0
    for c in cat_tot:
        cat += 1
    for i in total:
        if i.User_role == 'teacher':
            tea += 1
        elif i.User_role == 'student':
            stu += 1
    context = {
        'tea': tea,
        'stu': stu,
        'cat': cat,
        'cat_tot': cat_tot
        }
    return render(request,'tem/index.html', context)


def News(request):
    page = requests.get('https://www.indiatoday.in/education-today')
    soup = BeautifulSoup(page.content,'html.parser')
    week = soup.find(class_ = 'story__grid')
    #wm = week.find(class_ = 'itg-listing')
    w = week.find_all('h2')
    ww = []
    lnk = []
    for x in w:
        k = x.a
        lnk.append(k['href'])
        ww.append(x.get_text())
    jhj = zip(ww,lnk)
    x = datetime.datetime.now()
    return render(request,'news.html',{'mrd': jhj, 'x': x})



def register_tr(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        qual = request.POST.get('qual')
        intro = request.POST.get('intro')
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        reg1 = Registration.objects.all()
        for i in reg1:
            if i.user.email == email:
                messages.success(request, 'User already exists')
                return redirect('teacher')

        user_name = request.POST.get('user_name')
        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return redirect('teacher')

        user = User.objects.create_user(username=user_name, email=email, password=psw, first_name=first_name,
                                        last_name=last_name)
        user.save()

        t = Registration()
        t.Password = psw
        t.Qualification = qual
        t.Introduction_brief = intro
        t.Image = photo
        t.Registration_fee = '100'
        t.User_role = 'teacher'
        t.user = user
        t.save()
        messages.success(request, 'You have successfully registered as teacher')
        return redirect('home')

    else:
         return render(request, 'register_teacher.html')




def login(request):
    if request.method == 'POST':
        username = request.POST.get("user_name")
        password = request.POST.get("pword")
        user = auth.authenticate(username = username, password = password)
        if user is None:
            messages.success(request, 'Invalid credentials')
            return render(request, 'loginnew.html')
        auth.login(request, user)
        if Registration.objects.filter(user = user, Password = password).exists():
            logs = Registration.objects.filter(user = user, Password = password)
            for value in logs:
                user_id = value.id
                usertype  = value.User_role
                teacher_email = value.user.email
                if usertype == 'admin':
                    request.session['logg'] = user_id
                    return redirect('admin_home')

                elif usertype == 'teacher':
                    request.session['logg'] = user_id
                    request.session['teacher'] = teacher_email
                    cm = Registration.objects.get(id = request.session['logg'])
                    g = Enrollment.objects.filter(enrol_tea = cm)
                    count = 0
                    for i in g:
                        count += 1
                    cm.Num_of_enrolled_students = count
                    mb = Feedback.objects.filter(Feed_tea_reg = cm)
                    cnn = 0
                    avs = []
                    for t in mb:
                        cnn += 1
                        avs.append(t.Rating_score)
                    aa = avs.count(5)
                    bb = avs.count(4)
                    cc = avs.count(3)
                    dd = avs.count(2)
                    ee = avs.count(1)
                    ff = [aa,bb,cc,dd,ee]
                    gg = max(ff)
                    if int(gg) == int(aa):
                        cm.Average_review_rating = 5
                    if int(gg) == int(bb):
                        cm.Average_review_rating = 4
                    if int(gg) == int(cc):
                        cm.Average_review_rating = 3
                    if int(gg) == int(dd):
                        cm.Average_review_rating = 2
                    if int(gg) == int(ee):
                        cm.Average_review_rating = 1
                    cm.Num_of_reviews = cnn
                    cm.save()
                    for i in g:
                        delta = datetime.datetime.now().date() - i.Enrollment_date
                        d = int(delta.days)
                        nwn = int(i.enrol_tea.id)
                        mkn = Registration.objects.get(id = nwn)
                        df = Course.objects.filter(cou_reg = mkn)
                        for u in df:
                            st = int(u.Course_duration)
                            st1 = st - d
                            i.Pending_days = st1
                            i.save()
                            break
                    return redirect('teacher_home')

                elif usertype == 'student':
                    request.session['logg'] = user_id
                    g = Enrollment.objects.all()
                    mhp = Registration.objects.get(id = request.session['logg'])
                    dt = Enrollment.objects.filter(enrol_reg = mhp)

                    ggpp = []
                    for t in dt:
                        ksk = int(t.enrol_cou.id)
                        ggpp.append(ksk)

                    dgf = Course.objects.filter(id__in = ggpp)
                    cou_cmpltd = 0
                    for e in dgf:
                        mbt = 0
                        pas = 0
                        pas1 = 4
                        hdc = Chapter.objects.filter(cha_cou = e)
                        for t in hdc:
                            hdc1 = Content.objects.filter(cont_cha = t)
                            for c in hdc1:
                                if Learning_progress.objects.filter(Learn_p_reg = mhp, Learn_p_cnt = c, Status = 'C').exists():
                                    pas += 1
                            pas1 = Content.objects.filter(cont_cha = t).count()
                            if pas == pas1:
                                mbt += 1

                        ch_cnts = Chapter.objects.filter(cha_cou = e).count()

                        if ch_cnts == mbt:
                            cou_cmpltd += 1


                    mhp.Num_of_courses_completed = cou_cmpltd

                    pas = Learning_progress.objects.filter(Learn_p_reg = mhp, Status = 'P')
                    ggpp = []
                    for t in pas:
                        ksk = int(t.Learn_p_cnt.cont_cha.cha_cou.id)
                        ggpp.append(ksk)
                    dgf = Course.objects.filter(id__in=ggpp).count()

                    mhp.Num_of_courses_enrolled = dgf
                    mhp.save()
                    for i in g:
                        delta = datetime.datetime.now().date() - i.Enrollment_date
                        d = int(delta.days)
                        nwn = int(i.enrol_tea.id)
                        mkn = Registration.objects.get(id=nwn)
                        df = Course.objects.filter(cou_reg = mkn)
                        for u in df:
                            st = int(u.Course_duration)
                            st1 = st - d
                            i.Pending_days = st1
                            i.save()
                            break
                    return redirect('student_home')
                else:
                    messages.success(request, 'Your access to the website is blocked. Please contact admin')
                    return redirect('login')
        else:
            messages.success(request, 'Username or password entered is incorrect')
            return redirect('login')
    else:
        return render(request, 'loginnew.html')




def register_st(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mgn = Registration.objects.all()
        for w in mgn:
            if w.user.email == email and w.User_role == 'student':
                messages.success(request, 'You have already registered. Please login')
                return redirect('student')
        psw = request.POST.get('psw')
        user_name = request.POST.get('user_name')
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)

        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return redirect('student')

        user = User.objects.create_user(username=user_name, email=email, password=psw, first_name=first_name,last_name=last_name)
        user.save()

        reg = Registration()
        reg.Password = psw
        reg.Image = photo
        reg.User_role = 'student'
        reg.user = user
        reg.save()
        messages.success(request, 'You have successfully registered as student')
        return redirect('home')
    else:
        return render(request, 'register_student.html')

        username = request.POST.get("user_name")




def admin_rg(request):
    if request.method == 'POST':
        lk = Registration.objects.all()
        for t in lk:
            if t.User_role == 'admin':
                messages.success(request, 'You are not allowed to be registered as admin')
                return redirect('adminn')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fs.save(photo.name, photo)
        reg1 = Registration.objects.all()
        for i in reg1:
            if i.user.email == email:
                messages.success(request, 'User already exists')
                return redirect('adminn')

        user_name = request.POST.get('user_name')
        for t in User.objects.all():
            if t.username == user_name:
                messages.success(request, 'Username taken. Please try another')
                return redirect('adminn')

        user = User.objects.create_user(username = user_name, email = email, password = psw, first_name = first_name, last_name = last_name)
        user.save()

        t = Registration()
        t.Password = psw
        t.Image = photo
        t.User_role = 'admin'
        t.user = user
        t.save()
        messages.success(request, 'You have successfully registered as admin')
        return redirect('adminn')
    else:
        return render(request, 'register_admin.html')




def Student_home(request):
    nam = Registration.objects.filter(id=request.session['logg'])
    return render(request,'student_home.html',{'nam': nam})




def Teacher_home(request):
    nam = Registration.objects.filter(id=request.session['logg'])
    return render(request,'teacher_home.html', {'nam': nam})




def Admin_home(request):
    nam = Registration.objects.filter(id = request.session['logg'])
    return render(request,'admin_home.html', {'nam': nam})


def cat_admin(request):
    mkk = Category.objects.all()
    return render(request,'cat_admin.html',{'mkk':mkk})


def add_cat_admin(request):
    if request.method == 'POST':
        cat = request.POST.get('cat')
        imgg = request.FILES['imgg']
        brf = request.POST.get('brief')
        tim = request.POST.get('duration')
        fee = request.POST.get('fee')
        fs = FileSystemStorage()
        fs.save(imgg.name, imgg)
        gh = Category()
        gh.Category_title = cat
        gh.Image = imgg
        gh.brief = brf
        gh.Cat_time = tim
        gh.cat_fee = fee
        gh.save()
        messages.success(request, 'Course category added successfully')
        return redirect('cat_admin')
    return render(request,'add_cat_admin.html')





def edit_cat_admin(request, id):
    gh = Category.objects.get(id = id)
    if request.method == 'POST':
        try:
            imgg = request.FILES['imgg']
            fs = FileSystemStorage()
            fs.save(imgg.name,imgg)
            cat = request.POST.get('cat')
            ed_brf = request.POST.get('ed_brief')
            ed_dur = request.POST.get('ed_cat_time')
            ed_fee = request.POST.get('ed_cat_fee')
            gh.Category_title = cat
            gh.Image = imgg
            gh.brief = ed_brf
            gh.Cat_time = ed_dur
            gh.cat_fee = ed_fee
            gh.save()
        except:
            imgg1 = request.POST.get('imgg1')
            cat = request.POST.get('cat')
            ed_brf = request.POST.get('ed_brief')
            ed_dur = request.POST.get('ed_cat_time')
            ed_fee = request.POST.get('ed_cat_fee')
            gh.Category_title = cat
            gh.Image = imgg1
            gh.brief = ed_brf
            gh.Cat_time = ed_dur
            gh.cat_fee = ed_fee
            gh.save()
        messages.success(request, 'Course category edited successfully')
        return redirect('cat_admin')
    return render(request, 'edit_cat_admin.html', {'gh': gh})




def delete_cat_admin(request, id):
    Category.objects.get(id = id).delete()
    messages.success(request, 'Category deleted successfully')
    return redirect('cat_admin')



def course_tr(request):
    dd = Course.objects.filter(cou_reg = request.session['logg'])
    return render(request, 'course_tr.html',{'dd':dd})




def edit_course_tr(request, id):
    mkm = Category.objects.all()
    gh = Course.objects.get(id = id)
    if request.method == 'POST':
        cat = request.POST.get('cat')
        cat = int(cat)
        yky = Category.objects.get(id = cat)
        cou = request.POST.get('cou')
        c_b = request.POST.get('c_b')
        c_d = request.POST.get('c_d')
        c_f = request.POST.get('c_f')
        lan = request.POST.get('lan')
        gh.Course_title = cou
        gh.Course_brief = c_b
        gh.Course_duration = c_d
        gh.Course_fee  = c_f
        gh.Language  = lan
        gh.cou_cat = yky
        gh.save()
        messages.success(request, 'Course edited successfully')
        return redirect('Course_tr')
    return render(request,'edit_course_tr.html',{'gh':gh,'mkm':mkm})



def delete_course_tr(request, id):
    Course.objects.get(id = id).delete()
    messages.success(request, 'Course deleted successfully')
    return redirect('Course_tr')




def chapter_tr(request, id):
    id = int(id)
    request.session['teacher_course'] = id
    hh = Chapter.objects.filter(cha_cou = id)
    return render(request, 'chap_tr.html', {'hh': hh})



def add_course_tr(request):
    hrb = Registration.objects.get(id = request.session['logg'])
    mkm = Category.objects.all()
    if request.method == 'POST':
        cat = request.POST.get('cat')
        cat = int(cat)
        bbt = Category.objects.get(id = cat)
        cou_tit = request.POST.get('cou_tit')
        c_b1 = request.POST.get('c_b1')
        c_d1 = request.POST.get('c_d1')
        c_f1 = request.POST.get('c_f1')
        lang = request.POST.get('lang')

        if Course.objects.filter(cou_reg = hrb, Course_title = cou_tit).exists():
            messages.success(request, 'Course already exists')
            return redirect('Course_tr')

        cdt = Course()
        cdt.Course_title = cou_tit
        cdt.Course_brief = c_b1
        cdt.Course_duration = c_d1
        cdt.Course_fee = c_f1
        cdt.Language = lang
        cdt.cou_reg = hrb
        cdt.cou_cat = bbt
        cdt.save()

        cou_st_date = request.POST.get('cou_st_date')
        cou_end_date = request.POST.get('cou_end_date')

        cmk = Course_st_stop()
        cmk.start_date = cou_st_date
        cmk.end_date = cou_end_date
        cmk.cou_st_stop_cou = cdt
        cmk.save()

        messages.success(request, 'Course added successfully')
        return redirect('Course_tr')
    return render(request,'add_course_tr.html',{'mkm':mkm})



def edit_chapter_tr(request, id):
    kkp = Course.objects.get(id = request.session['teacher_course'])
    gh = Chapter.objects.get(id = id)
    if request.method == 'POST':
        c_tt = request.POST.get('c_tt')
        gh.Chapter_title = c_tt
        gh.save()
        messages.success(request, 'Chapter edited successfully')
        redd = '/chapter_tr/'+str(kkp.id)
        return redirect(redd)
    return render(request,'edit_chapter_tr.html',{'gh':gh,'kkp':kkp})





def delete_chapter(request, id):
    kkp = Course.objects.get(id = request.session['teacher_course'])
    Chapter.objects.get(id = id).delete()
    messages.success(request, 'Chapter deleted successfully')
    redd = '/chapter_tr/' + str(kkp.id)
    return redirect(redd)




def ch_co_tr(request, id):
    id = int(id)
    request.session['teacher_chapter'] = id
    idm = request.session['teacher_course']
    idm = int(idm)
    mm1 = Content.objects.filter(cont_cha = id)
    return render(request, 'cont_tr.html', {'mm1': mm1,'idm':idm})





def edit_content(request, id):
    tt_chapt = request.session['teacher_chapter']
    tt_chapt1 = int(tt_chapt)
    tt_chapt = Chapter.objects.get(id = tt_chapt1)
    gh = Content.objects.get(id = id)
    if request.method == 'POST':
        try:
            c_t = request.POST.get('c_t')
            up_cont = request.FILES['up_cont']
            upp = str(up_cont)
            imm = ['.jpeg','.jpg','.png']
            vid = ['.mov','.mp4','.wmv','.avi','.avchd','.flv','.f4v','.swf','.mkv','.webm','.mpeg4']
            nbg = 0

            for i in imm:
                if upp.endswith(i):
                    nbg += 1
                    gh.Chapter_Content_type = 'Image'

            for i in vid:
                if upp.endswith(i):
                    nbg += 1
                    gh.Chapter_Content_type = 'Video'

            if nbg == 0:
                gh.Chapter_Content_type = 'File'

            fs = FileSystemStorage()
            fs.save(up_cont.name, up_cont)

            gh.Chapter_Content = up_cont
            gh.Chapter_text_content = c_t
            gh.save()
            redd = '/ch_co_tr/'+str(tt_chapt1)
            messages.success(request, 'Chapter content edited successfully')
            return redirect(redd)

        except:
            c_t = request.POST.get('c_t')
            u_con = request.POST.get('u_con')
            u_con_typ = request.POST.get('u_con_typ')
            gh.Chapter_Content = u_con
            gh.Chapter_text_content = c_t
            gh.Chapter_Content_type = u_con_typ
            gh.save()
            redd = '/ch_co_tr/' + str(tt_chapt1)
            messages.success(request, 'Chapter content edited successfully')
            return redirect(redd)
    return render(request, 'edit_content.html', {'gh': gh,'tt_chapt':tt_chapt})



def delete_content(request, id):
    Content.objects.get(id = id).delete()
    tt_chapt = request.session['teacher_chapter']
    tt_chapt1 = int(tt_chapt)
    redd = '/ch_co_tr/' + str(tt_chapt1)
    messages.success(request, 'Chapter content deleted successfully')
    return redirect(redd)




def add_ch_con(request):
    tt_chapt = request.session['teacher_chapter']
    tt_chapt1 = int(tt_chapt)
    tt_chapt = Chapter.objects.get(id=tt_chapt1)
    if request.method == 'POST':
        c_t = request.POST.get('c_t')
        up_cont = request.FILES['up_cont']
        fs = FileSystemStorage()
        fs.save(up_cont.name, up_cont)

        upp = str(up_cont)
        imm = ['.jpeg', '.jpg', '.png']
        vid = ['.mov', '.mp4', '.wmv', '.avi', '.avchd', '.flv', '.f4v', '.swf', '.mkv', '.webm', '.mpeg4']

        cdt = Content()
        nbg = 0
        for i in imm:
            if upp.endswith(i):
                nbg += 1
                cdt.Chapter_Content_type = 'Image'

        for i in vid:
            if upp.endswith(i):
                nbg += 1
                cdt.Chapter_Content_type = 'Video'

        if nbg == 0:
            cdt.Chapter_Content_type = 'File'

        cdt.Chapter_Content = up_cont
        cdt.Chapter_text_content = c_t
        cdt.cont_cha = tt_chapt
        cdt.save()
        redd = '/ch_co_tr/' + str(tt_chapt1)
        messages.success(request, 'Chapter content added successfully')
        return redirect(redd)
    return render(request,'add_chapter_content.html',{'tt_chapt':tt_chapt})





def add_chapter(request):
    kkp = Course.objects.get(id = request.session['teacher_course'])
    if request.method == 'POST':
        c_tt = request.POST.get('c_tt')
        if Chapter.objects.filter(cha_cou = kkp, Chapter_title = c_tt).exists():
            messages.success(request, 'Chapter already exists')
            redd = '/chapter_tr/' + str(kkp.id)
            return redirect(redd)

        cdt = Chapter()
        cdt.Chapter_title = c_tt
        cdt.cha_cou = kkp
        cdt.save()

        messages.success(request, 'Chapter added successfully')
        redd = '/chapter_tr/' + str(kkp.id)
        return redirect(redd)
    return render(request,'add_chapter.html',{'kkp':kkp})




def stu_sub_selnew(request):
    sne = Category.objects.all()
    if request.method == 'POST':
        cat = request.POST.get('cat')
        cat1 = int(cat)
        request.session['st_bk_category'] = cat1
        cc = Course.objects.filter(cou_cat =cat1)
        return render(request, 'st_sub_new2.html', {'cc':cc})
    return render(request, 'st_sub_selnew1.html', {'snew':sne})



def stu_sub_selnew1(request):
    sne = Category.objects.get(id = request.session['st_bk_category'])
    cou = request.POST.get('cou')
    cou1 = int(cou)
    request.session['st_bk_course'] = cou1
    cse = Course.objects.get(id = cou1)
    c_tit = str(cse.Course_title)
    cse = Course.objects.filter(cou_cat = sne, Course_title = c_tit)
    return render(request, 'st_sub_selnew3.html', {'cse': cse})



def stu_buk_teacher(request, id):
    id = int(id)
    dh = Registration.objects.get(id = request.session['logg'])
    cou = Course.objects.get(id = id)
    id_tea = int(cou.cou_reg.id)
    nm = Registration.objects.get(id = id_tea)
    if Enrollment.objects.filter(enrol_reg = dh, enrol_tea = nm, enrol_cou = cou).exists():
        messages.success(request, 'You have already booked this course')
        return redirect('student_home')

    spp = Enrollment()
    spp.enrol_reg = dh
    spp.enrol_tea = nm
    spp.enrol_cou = cou
    spp.Teacher_response = 'To be expected'
    spp.notify = 'new'
    spp.save()

    messages.success(request, 'You have successfully booked a course')
    return redirect('student_home')


def logout(request):
    auth.logout(request)
    return redirect('home')


def stu_buk_acc(request):
    stzz = Enrollment.objects.filter(enrol_tea = request.session['logg'])
    return render(request,'stu_buk_acc.html',{'stzz':stzz})


def stu_accept(request, id):
    sas = Enrollment.objects.get(id = id)
    sas.Teacher_response = 'Accepted'
    sas.save()
    return redirect('stu_buk_acc')



def stu_reject(request, id):
    sas = Enrollment.objects.get(id=id)
    sas.Teacher_response = 'Rejected'
    sas.save()
    return redirect('stu_buk_acc')




def stu_delete(request, id):
    Enrollment.objects.get(id = id).delete()
    messages.success(request, 'Enrolled student deleted successfully')
    return redirect('stu_buk_acc')



def pay_student(request):
    ds = Enrollment.objects.filter(enrol_reg = request.session['logg'], Teacher_response = 'Accepted')
    msk = []
    for t in ds:
        c_f = float(t.enrol_cou.Course_fee)
        if c_f > 0:
            hh = int(t.id)
            msk.append(hh)
    ds = Enrollment.objects.filter(id__in = msk)
    return render(request, 'pay_student.html', {'ds': ds})




def stu_buk_teacherr(request, id):
    id = int(id)
    tgt = Enrollment.objects.get(id = id)
    if tgt.Payment_status == 'paid':
        messages.success(request, 'You have already paid')
        return redirect('pay_student')
    if request.method == 'POST':
        paid = request.POST.get('paid')
        paid = float(paid)
        if float(tgt.enrol_cou.Course_fee) > paid:
            messages.success(request, 'Please pay full amount')
            return render(request,'paid.html',{'tgt':tgt})
        tgt.Payment_status = 'paid'
        tgt.save()

        kmwe = 'You have paid for the course '+tgt.enrol_cou.cou_cat.Category_title+'('+tgt.enrol_cou.Course_title+')'
        messages.success(request, kmwe)
        return redirect('student_home')
    return render(request,'paid.html',{'tgt':tgt})





def payment(request, id):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


    payment_amount = 50000
    payment_currency = 'INR'
    payment_receipt = 'order_rcptid_11'
    payment_notes = {'Shipping address': 'Mumbai, India'}

    order = client.order.create({
        'amount': payment_amount,
        'currency': payment_currency,
        'receipt': payment_receipt,
        'notes': payment_notes
    })

    context = {
        'order_id': order['id'],
        'amount': payment_amount,
        'currency': payment_currency,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID
    }
    return render(request, 'payment.html', context)


def payment_success(request):
    return render(request, "Payment Successful!")




def st_book_courses(request):
    st = Registration.objects.get(id = request.session['logg'])
    buk = Enrollment.objects.filter(enrol_reg = st)
    return render(request, 'st_book_courses.html',{'buk':buk,'st':st})



def acc_chapter(request, id):
    gh = Enrollment.objects.get(id = id)
    if gh.Teacher_response == 'To be expected' or gh.Teacher_response == 'Rejected' or gh.Payment_status != 'paid':
        messages.success(request, 'Your payment is pending or wait for teacher\'s approval')
        return redirect('student_home')
    request.session['acc_cha_teacher'] = t_id = int(gh.enrol_tea.id)
    nn = Registration.objects.get(id = t_id)
    request.session['tch_idd'] = nn.id
    cou_idd = int(gh.enrol_cou.id)
    thr = Course.objects.get(id = cou_idd)
    fd = Chapter.objects.filter(cha_cou = thr)
    return render(request, 'acc_chapter1.html', {'fd':fd})




def acc_chapter1(request):
    mnm = Registration.objects.get(id = request.session["logg"])
    sz1 = request.POST.get('cha')
    request.session['cou_ch_nme'] = chtw = int(sz1)
    sz = Chapter.objects.get(id = chtw)
    sz_cnt = Content.objects.filter(cont_cha = sz)
    mj = Learning_progress.objects.filter(Learn_p_reg = mnm)
    return render(request, 'acc_chapter2.html', {'sz_cnt': sz_cnt,'mj':mj})




def compp(request):
    cco = Registration.objects.get(id = request.session['acc_cha_teacher'])
    mnm = Registration.objects.get(id = request.session["logg"])
    idd = request.POST.getlist('id')
    comm = request.POST.getlist('comm')
    ggt = zip(idd,comm)
    for i,h in ggt:
        dvt = int(i)
        dvt1 = Content.objects.get(id=dvt)
        if Learning_progress.objects.filter(Learn_p_cnt = dvt1).exists():
            pk = Learning_progress.objects.filter(Learn_p_cnt = dvt1)
            for t in pk:
                t.Status = h
                t.save()
        else:
            pk = Learning_progress()
            pk.Status = h
            pk.Learn_p_reg = mnm
            pk.Learn_p_tea_reg = cco
            pk.Learn_p_cnt = dvt1
            pk.save()
    messages.success(request, 'Learning progress updated')
    return redirect('student_home')



def st_pr(request):
    vc = Registration.objects.get(id = request.session['logg'])
    dd = Learning_progress.objects.filter(Learn_p_tea_reg = vc)
    return render(request,'student_progress.html',{'dd':dd})




def QA(request):
    cho = Course.objects.filter(cou_reg = request.session['logg'] )
    if request.method == 'POST':
        question = request.POST.get('question')
        answer1 = request.POST.get('answer1')
        answer2 = request.POST.get('answer2')
        answer3 = request.POST.get('answer3')
        correct_answer = request.POST.get('correct-answer')
        course_id = request.POST.get('course')
        bc = Registration.objects.get(id = request.session['logg'])
        test = Exam()
        test.Question = question
        test.Option1 = answer1
        test.Option2 = answer2
        test.Option3 = answer3
        test.Correct_answer = correct_answer
        test.Exam_reg_tea = bc
        test.Exam_cou_id = course_id
        test.save()
        messages.success(request, 'Question Add successfully')
        return redirect('QA')
    else:
        return render(request, 'Question_Answer.html',{'cho': cho})




def test(request):
    mrd = Enrollment.objects.filter(enrol_tea=request.session['logg'])
    unique_mrd = {}
    for enr in mrd:
        student = enr.enrol_reg
        if student not in unique_mrd:
            unique_mrd[student] = []
        unique_mrd[student].append(enr.enrol_cou)
    context = {'mrd': unique_mrd, }
    return render(request, 'exam.html', context)




def email(request):
    student_ids = []
    course_ids = []
    for key, value in request.POST.items():
        if key.startswith('choose_') and value:
            student_id = key.split('_')[1]  # Extract student ID from the checkbox name

            # Get the corresponding course ID from the dropdown
            course_id = request.POST.get(f'cou_drop_{student_id}')

            if course_id:  # Only add if a course is selected
                student_ids.append(student_id)  # Store student ID
                course_ids.append(course_id)

    time_start = request.POST.getlist('start_time')
    time_st = [i for i in time_start if i != '']
    time_ending = request.POST.getlist('end_time')
    time_end = [i for i in time_ending if i != '']
    ex_date = request.POST.getlist('ex_date')
    ex_dt = [i for i in ex_date if i != '']
    e_list = []
    if len(time_st) == len(time_end) == len(student_ids) :
        for i, j, k, ex_d, c in zip(student_ids, time_st, time_end, ex_dt, course_ids):
            e_list = []
            a = int(i)
            cou = int(c)
            b = Registration.objects.get(id = a)
            xx = Exam_register.objects.filter(ex_reg_st = a, ex_reg_cou = cou, ex_reg_tea =request.session['logg'] )
            if xx:
                messages.success(request, 'Already exam Scheduled')
                return render(request, 'exam.html')
            else:
                enr = Enrollment.objects.filter(enrol_reg_id = a, enrol_cou_id = cou, enrol_tea_id= request.session['logg'] )
                for m in enr:
                    register = Exam_register()
                    register.Time_start = j
                    register.Time_stop = k
                    register.Ex_date = ex_d
                    register.ex_reg_st_id = m.enrol_reg.id
                    register.ex_reg_tea_id = m.enrol_tea.id
                    register.ex_reg_cou_id = m.enrol_cou.id
                    register.Lock = 'Schedule'
                    register.save()
                    # This line get the mail details
                    c = b.user.pk
                    d = User.objects.get(id=c)
                    e = str(d.email)
                    e_list.append(e)
                    name = str(d.first_name)
                    subject = 'Important: Upcoming Exam Notification'
                    message = f'Dear {name},I hope you re doing well.Your Exam  date:{ex_d} and Start time:{j} and End time:{k}. Good luck with your preparation, and I trust you will perform excellently!'
                    from_email = 'mridhulmaddy8943@gmail.com'
                    send_mail(subject, message, from_email, e_list)
                    messages.success(request, 'Email send successfully ')
                    return render(request, 'exam.html', )
    else:
        messages.success(request, 'One Option is missing')
        return render(request, 'exam.html')



def scheduled_students(request):
    try:
       sche = Exam_register.objects.filter(ex_reg_tea_id= request.session['logg'])
       return render(request,'scheduled_students.html', {'sche': sche})
    except Exam_register.DoesNotExist:
        pass
    return render(request, 'scheduled_students.html')




def exam_notification(request):
    try:
        ntn = Exam_register.objects.filter(ex_reg_st=request.session['logg'])
        current_time = datetime.datetime.now()
        for e in ntn:
            end_time = datetime.datetime.combine(e.Ex_date, e.Time_stop)
            if current_time > end_time:
                messages.success(request, f"Exam Time Expired of {e.ex_reg_cou.Course_title}.")
                e.delete()

        return render(request, 'exam_notification.html', {'ntn': ntn})

    except Exam_register.DoesNotExist:
        pass
    return render(request, 'exam_notification.html')





def student_exam_start(request, id):
    que = Exam.objects.filter(Exam_cou = id)
    tit = Exam_register.objects.filter(ex_reg_st = request.session['logg'], ex_reg_cou_id = id)
    if request.method == 'POST':
        Total_mark = 0
        Acquired_mark = 0
        for q in que:
            Reg_tea = q.Exam_reg_tea_id
            Reg_cou = q.Exam_cou_id
            Total_mark += 2
            ans = request.POST.get(f'question_{q.id}')
            if q.Correct_answer == ans :
                Acquired_mark += 2
        if Acquired_mark > 0:
            percentage = (Acquired_mark/Total_mark)*100
        else:
            percentage = 0

        if percentage >=90:
            grade = 'A'
        elif percentage >= 80:
            grade = 'B'
        elif percentage >= 70:
            grade = 'C'
        elif percentage >= 60:
            grade = 'D'
        else:
            grade = 'Fail'

        sub = Exam_results()
        sub.Total_marks = Total_mark
        sub.Acquired_marks = Acquired_mark
        sub.Grade = grade
        sub.Exam_res_reg_st_id = request.session['logg']
        sub.Exam_res_reg_tea_id = Reg_tea
        sub.Exam_res_cou_id = Reg_cou
        sub.save()
        dele = Exam_register.objects.filter(ex_reg_st_id = request.session['logg'], ex_reg_cou_id = id)
        dele.delete()
        messages.success(request, 'Exam Submitted Successfully')
        return render(request, 'student_home.html')

    else:
        return render(request, 'student_exam_start.html', {'que': que, 'tit': tit} )



def students_exam_result(request):
    hea = Registration.objects.filter(id = request.session['logg'])
    res = Exam_results.objects.filter(Exam_res_reg_st = request.session['logg'])
    return render(request, 'students_exam_result.html', {'hea': hea, 'res': res})




def search(request):
    ss = request.GET.get('sea')
    if ss:
        results = Category.objects.filter(Category_title__icontains = ss)
        return render(request, 'search.html', {'results': results})
    else:
        return render(request, 'search.html')



