from django.shortcuts import render,redirect
from . import models
import os
import uuid

def login(request):
    if request.session.get('is_login',None):
        return redirect('/bsl/index/')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username.strip() and password:
            try:
                user = models.User.objects.get(name=username)
            except:
                print(1)
                return render(request, 'login.html')
            if user.password == password:
                request.session['is_login'] = True
                request.session['user_name'] = user.name
                return redirect('/bsl/index/')
    return render(request, 'login.html')

def index(request):
    if not request.session.get('is_login', None):
        return redirect("/bsl/login/")
    pass
    return render(request, 'index.html')

def history_list(request):
    if not request.session.get('is_login', None):
        return redirect("/bsl/login/")
    history_lists = models.job_history.objects.all()
    return render(request, 'history_list.html', context={"history_lists": history_lists})

def delete_host(request):
    if not request.session.get('is_login', None):
        return redirect("/bsl/login/")
    id = request.GET.get('id', '')
    host_id = models.add_host.objects.get(id=id)
    if request.method == 'POST':
        os.remove('pemkey/' + host_id.keyname)
        host_id.delete()
        return redirect('/bsl/host_list/')

    with open('pemkey/' + host_id.keyname, 'r') as hf:
        pem = hf.read()
        hf.close()
    return render(request, 'delete_host.html',
                  {'hostname': host_id.hostname, 'username': host_id.username, 'ip': host_id.IP,
                   'port': host_id.port, 'infro': host_id.infro, 'pem': pem})

def edit_host(request):
    if not request.session.get('is_login', None):
        return redirect("/bsl/login/")
    id = request.GET.get('id', '')
    host_id = models.add_host.objects.get(id=id)
    keyname_old = host_id.keyname
    with open('pemkey/' + host_id.keyname, 'r') as hf:
        pem = hf.read()
        hf.close()
    if request.method == 'POST':
        hostname = request.POST.get('hostname')
        ip = request.POST.get('ip')
        port = request.POST.get('port')
        infro = request.POST.get('infro')
        keyname = "%s.pem" % hostname
        pem = request.POST.get('pem')
        up_host = models.add_host.objects.get(id=id)
        up_host.hostname = hostname
        up_host.IP = ip
        up_host.port = port
        up_host.infro = infro
        up_host.keyname = keyname
        up_host.save()
        keyname_tmp = keyname + '_tmp'
        with open('pemkey/' + keyname_tmp, 'w') as tp:
            tp.write(pem)
            tp.close()
        os.remove('pemkey/' + keyname_old)
        os.rename('pemkey/' + keyname_tmp, 'pemkey/' + up_host.keyname)
        return redirect('/bsl/host_list/')
    return render(request, 'edit_host.html',{'hostname':host_id.hostname,'username':host_id.username,'ip':host_id.IP,
                                             'port':host_id.port,'infro':host_id.infro,'pem':pem})

def host_list(request):
    if not request.session.get('is_login', None):
        return redirect("/bsl/login/")
    host_lists = models.add_host.objects.all()
    return render(request, 'host_list.html', context={"host_lists": host_lists})

def edit_job(request):
    if not request.session.get('is_login', None):
        return redirect("/bsl/login/")
    id = request.GET.get('id', '')
    mid = models.job_list.objects.get(id=id)
    if request.method == 'POST':
        script = request.POST.get('script')
        new_jname = request.POST.get('jname')
        up_jname = models.job_list.objects.get(jname=mid.jname)
        up_jname.jname = new_jname
        up_jname.save()
        tmp_jid = "%s.tmp" % mid.jid
        with open('job/' + tmp_jid,'w+') as f1:
            f1.write(script)
            f1.close()
        os.remove('job/' + mid.jid)
        os.rename('job/' + tmp_jid, 'job/' + mid.jid)
        checkshell('job/' + mid.jid)
        return redirect('/bsl/job_list/')
    with open('job/' + mid.jid, 'r', encoding='utf-8') as tf:
        show_job = tf.read()
        tf.close()
    return render(request, 'edit_job.html',
                  {"job_name": mid.jname, "show_job": show_job})


def delete_job(request):
    if not request.session.get('is_login', None):
        return redirect("/bsl/login/")
    id = request.GET.get('id', '')
    mid = models.job_list.objects.get(id=id)
    if request.method == 'POST':
        jid_tmp = mid.jid
        mid.delete()
        os.remove('job/' + jid_tmp)
        return redirect('/bsl/job_list/')

    with open('job/' + mid.jid, 'r') as tf:
        sjob = tf.read()
        tf.close()
    return render(request, 'delete_job.html',
                  {"job_name": mid.jname, "show_job": sjob})

def job_list(request):
    if not request.session.get('is_login', None):
        return redirect("/bsl/login/")
    job_lists = models.job_list.objects.all()
    return render(request, 'job_list.html', context={"job_lists":job_lists})

def add_job(request):
    if not request.session.get('is_login', None):
        return redirect("/bsl/login/")
    if request.method == 'POST':
        script = request.POST.get('script')
        jname = request.POST.get('jname')
        j_id = "%s.sh" % uuid.uuid1()
        if str(jname) == "":
            return render(request, 'add_job.html')
        else:
            with open('job/' + j_id, 'w', encoding='utf-8') as tc:
                tc.write(script)
                tc.close()
            job_list = models.job_list()
            job_list.jname = jname
            job_list.jid = j_id
            job_list.save()
            checkshell('job/' + j_id)
            return redirect('/bsl/job_list/')
    return render(request, 'add_job.html')
def run_job(request):
    if not request.session.get('is_login', None):
        return redirect("/bsl/login/")
    id = request.GET.get('id', '')
    mid = models.job_list.objects.get(id=id)
    host_list = models.add_host.objects.all()
    with open('job/' + mid.jid,'r', encoding='utf-8') as tf:
        sjob = tf.read()
        tf.close()
    return render(request, 'run_job.html',{"job_name":mid.jname,"job_id":mid.jid,"show_job":sjob,"host_list":host_list})

def add_host(request):
    if not request.session.get('is_login', None):
        return redirect("/bsl/login/")
    if request.method == 'POST':
        hostname = request.POST.get('hostname')
        ip = request.POST.get('ip')
        port = request.POST.get('port')
        infro = request.POST.get('infro')
        keyname = "%s.pem" % hostname
        pem = request.POST.get('pem')
        add_host = models.add_host()
        add_host.hostname = hostname
        add_host.IP = ip
        add_host.port = port
        add_host.infro = infro
        add_host.keyname = keyname
        add_host.save()
        with open('pemkey/' + keyname, 'w') as tp:
            tp.write(pem)
            tp.close()
    return render(request, 'add_host.html')

def checkshell(name):
    fp = open(name,"rU")
    string = fp.read()
    fp.close()
    fp1 = open(name,"wb")
    fp1.seek(0)
    fp1.write(string.encode(encoding='utf-8'))
    fp1.flush()
    fp1.close()

def history_log(jid,hostname,exec_history):
    jid_tmp =models.job_list.objects.get(jid=jid)
    jname = jid_tmp.jname
    history_log = models.job_history()
    history_log.jname = jname
    history_log.jid = jid
    history_log.exec_host = hostname
    history_log.exec_history = exec_history
    history_log.save()

def logout(request):
    if not request.session.get('is_login',None):
        return redirect("/bsl/login/")
    request.session.flush()
    return redirect("/bsl/login/")

def update(request):
    pass
    return render(request, 'upversion/update.html')

def add_upversion(request):
    if not request.session.get('is_login', None):
        return redirect("/bsl/login/")
    if request.method == 'POST':
        up_name = request.POST.get('up_name')
        ser_name = request.POST.get('ser_name')
        ios_cname = request.POST.get('ios_cname')
        aos_cname = request.POST.get('aos_cname')
        env = request.POST.get('env')
        up_info = request.POST.get('up_info')
        if str(ser_name) == "" and str(ios_cname) == "" and str(aos_cname) == "":
            return render(request, 'add_job.html')
        else:
            up_version = models.update_version()
            up_version.up_name = up_name
            up_version.ser_name = ser_name
            up_version.ios_cname = ios_cname
            up_version.aos_cname = aos_cname
            up_version.env = env
            up_version.up_info = up_info
            up_version.save()
            return redirect('/bsl/update/')
    return render(request, 'upversion/add_upversion.html')

def upversion_list(request):
    if not request.session.get('is_login', None):
        return redirect("/bsl/login/")
    vlists = models.update_version.objects.all()
    return render(request, 'upversion/list.html', context={"vlists":vlists})

def ShowJob_update(request):
    pass
    messagelog = "juse a test!"
    return render(request,'upversion/update.html',{'messagelog':messagelog})