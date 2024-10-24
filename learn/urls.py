from django.urls import path
import learn.views

urlpatterns=[
     path('', learn.views.home,name='home'),
     path('home', learn.views.home,name='home'),
     path('news', learn.views.News, name='news'),
     path('login', learn.views.login, name='login'),
     path('student', learn.views.register_st, name='student'),
     path('teacher', learn.views.register_tr, name='teacher'),
     path('adminn', learn.views.admin_rg, name='adminn'),
     path('student_home', learn.views.Student_home, name='student_home'),
     path('teacher_home', learn.views.Teacher_home, name='teacher_home'),
     path('admin_home', learn.views.Admin_home, name='admin_home'),
     path('cat_admin', learn.views.cat_admin, name='cat_admin'),
     path('add_cat_admin', learn.views.add_cat_admin, name='add_cat_admin'),
     path('edit_cat_admin/<id>', learn.views.edit_cat_admin, name='edit_cat_admin'),
     path('delete_cat_admin/<id>', learn.views.delete_cat_admin, name='delete_cat_admin'),
     path('Course_tr', learn.views.course_tr, name='Course_tr'),
     path('edit_course_tr/<id>', learn.views.edit_course_tr, name='edit_course_tr'),
     path('delete_course_tr/<id>', learn.views.delete_course_tr, name='delete_course_tr'),
     path('chapter_tr/<id>', learn.views.chapter_tr, name='chapter_tr'),
     path('add_course_tr', learn.views.add_course_tr, name='add_course_tr'),
     path('edit_chapter_tr/<id>', learn.views.edit_chapter_tr, name='edit_chapter_tr'),
     path('delete_chapter/<id>', learn.views.delete_chapter, name='delete_chapter'),
     path('ch_co_tr/<id>', learn.views.ch_co_tr, name='ch_co_tr'),
     path('edit_content/<id>', learn.views.edit_content, name='edit_content'),
     path('delete_content/<id>', learn.views.delete_content, name='delete_content'),
     path('add_ch_con', learn.views.add_ch_con, name='add_ch_con'),
     path('add_chapter', learn.views.add_chapter, name='add_chapter'),
     path('stu_sub_selnew', learn.views.stu_sub_selnew, name='stu_sub_selnew'),
     path('stu_sub_selnew1', learn.views.stu_sub_selnew1, name='stu_sub_selnew1'),
     path('stu_buk_teacher/<id>', learn.views.stu_buk_teacher, name='stu_buk_teacher'),
     path('logout', learn.views.logout, name='logout'),
     path('stu_buk_acc', learn.views.stu_buk_acc, name='stu_buk_acc'),
     path('stu_accept/<id>', learn.views.stu_accept, name='stu_accept'),
     path('stu_reject/<id>', learn.views.stu_reject, name='stu_reject'),
     path('stu_delete/<id>', learn.views.stu_delete, name='stu_delete'),
     path('pay_student', learn.views.pay_student, name='pay_student'),
     path('stu_buk_teacherr/<id>', learn.views.stu_buk_teacherr, name='stu_buk_teacherr'),
     path('pay_stud_cours/<id>', learn.views.payment, name='pay_stud_cours'),
     path('payment-success/', learn.views.payment_success, name='payment_success'),
     path('st_book_courses', learn.views.st_book_courses, name='st_book_courses'),
     path('acc_chapter/<id>', learn.views.acc_chapter, name='acc_chapter'),
     path('acc_chapter1', learn.views.acc_chapter1, name='acc_chapter1'),
     path('compp', learn.views.compp, name='compp'),
     path('st_pr', learn.views.st_pr, name='st_pr'),
     path('QA', learn.views.QA, name='QA'),
     path('test', learn.views.test, name='test'),
     path('send_email', learn.views.email, name='send_email'),
     path('exam_notification', learn.views.exam_notification, name='exam_notification'),
     path('scheduled_students', learn.views.scheduled_students, name='scheduled_students'),
     path('student_exam_start/<int:id>/', learn.views.student_exam_start, name='student_exam_start'),
     path('students_exam_result', learn.views.students_exam_result, name='students_exam_result'),
     path('search', learn.views.search, name='search')












]