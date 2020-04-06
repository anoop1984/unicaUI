from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . models import healthCheck
from . models import Logfile_Testlab1
from . models import Logfile_Testlab2
from . forms import LogfileForm_Testlab1
from . forms import LogfileForm_Testlab2
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
import re
import json

# Create your views here.
@login_required
def index(reqeust):
    date_list = healthCheck.objects.values("date").distinct().order_by('-date')
    return render(reqeust, 'pages/index.html',{'dates':date_list})

@login_required
def about(request):
    return render(request, 'pages/about.html')

@login_required
def index2(request):
    """
    index page of testlab-1
    """
    date_list = healthCheck.objects.filter(site__contains="test-lab1").values("date").distinct().order_by('-date')
    return render(request, 'pages/testlab-1.html',{'dates':date_list})

@login_required
def testlab2(request):
    """index page of testlab-2"""
    date_list = healthCheck.objects.filter(site__contains="test-lab2").values("date").distinct().order_by('-date')
    return render(request, 'pages/testlab-2.html',{'dates':date_list})

@login_required
def index3(request):
    return render(request, 'pages/index3.html')

@login_required
def healtcheck(request):
    return render(request, 'admin/healthcheck.html')


@csrf_exempt
def loadjsonindb(request):
    if request.method == "POST":
       test_json = json.loads(request.body)
       #datet = datetime.date(2020, 3, 9)
       #datet = datetime.date.today() #it will add todays dates.
       datet =  datetime.date(*map(int,test_json['Date'].split('-')))
       try:
        for item in test_json['Test-Cases']:
          ip = item['IPAddress'].strip()
          healthCheck.objects.create(desc=item['Test Description'], severity=item['Severity'], ipaddr=ip, hostname=item['Hostname'], command=item['Command-Executed'], verdict=item['Verdict'], remarks=item['Remarks'],test_id=item['Test ID'],date=datet, site=test_json['Site'])
          
       #print(test_json) 
       #return HttpResponse(test_json[0]['Test_Description'])
        return HttpResponse("<em>DATA Stored</em>",status=201)
       except Exception as e:
          print("Exception Occurred while storing json: ",str(e))
          return HttpResponse("<em>DATA not Stored</em>", status=500)

    if request.method == "GET":
      date_list = healthCheck.objects.values("date").distinct()
      print(date_list)
      return HttpResponse(date_list)
          
    return render(request, 'upload.html')



@login_required
def dbtable(request):
    data = healthCheck.objects.all()
    data_dict = {'monitor_records': data }
    return render(request,'dbtable.html', context=data_dict)

@login_required
def dbtable_latest(request):
    site = request.GET['site']
    date_lst = healthCheck.objects.all().values('date').distinct().order_by('-date')
    if date_lst:
       data = healthCheck.objects.filter(date=date_lst[0]['date'],site__contains=site) 
       data_dict = {'monitor_records': data , 'date': date_lst[0]['date'], 'site': site.upper()}
    else:
       data_dict = {}
    return render(request,'dbtable_latest.html', context=data_dict)


def ajax1(request):
   test1 = "ajax-testing-successful"
   test2 = "wow"
   response = {}
   response['1']=test1
   response['2']=test2
   return JsonResponse(response)


def convert_date(date):
   if date:
    date_lt = date.split(',')  
    print(date_lt)
    yy = date_lt[1].strip()
    print(yy)
    if '.' in date_lt[0]:
      mm_dd = date_lt[0].split('.')
    else:
      mm_dd = date_lt[0].split(' ')
    print(mm_dd)
    dd = mm_dd[1].strip()
    print(dd)
    mm = mm_dd[0]
    mm = mm.lower()
    print(mm)
    if "jan" in mm: return yy+"-1-"+dd
    if "feb" in mm: return yy+"-2-"+dd
    if "mar" in mm: return yy+"-3-"+dd
    if "apr" in mm: return yy+"-4-"+dd
    if "may" in mm: return yy+"-5-"+dd
    if "jun" in mm: return yy+"-6-"+dd
    if "jul" in mm: return yy+"-7-"+dd
    if "aug" in mm: return yy+"-8-"+dd
    if "sep" in mm: return yy+"-9-"+dd
    if "oct" in mm: return yy+"-10-"+dd
    if "nov" in mm: return yy+"-11-"+dd
    if "dec" in mm: return yy+"-12-"+dd
   
    
    
def date_wise_start(date,date_str,site):
    stat_qs = healthCheck.objects.filter(date=date, site__contains=site)
    report_prv = {} 
    if date:
      date_previous_qs = healthCheck.objects.filter(date__lt=date, site__contains=site).values('date').distinct().order_by('-date')
      if date_previous_qs:
        date_previous = date_previous_qs[0]['date']
        print("Previous Date:", date_previous)
        report_prv = date_wise_start_prv(date_previous,site)
      else:
        print("No Previous Date found to selection Date:",date_str)
    report={}
    # date
    report['date'] = date_str
    #total test cases
    report['total_TC'] = stat_qs.count()
    #total passed testcases
    report['passed_TC'] = stat_qs.filter(verdict__contains="Passed").count()

    #total failed testcases
    report['failed_TC'] = stat_qs.filter(verdict__contains="Failed").count()

    #total failed major testcases
    report['failed_major_TC'] = stat_qs.filter(severity__contains="Major",verdict__contains="Failed").count()

    #total minor testcases
    report['failed_minor_TC'] = stat_qs.filter(severity__contains="Minor",verdict__contains="Failed").count()

    #total warning testcases#changed to all warning Test-cases
    report['failed_war_TC'] = stat_qs.filter(severity__contains="Warning").count()

    #total catestrophic testcases
    report['failed_cat_TC'] = stat_qs.filter(severity__contains="Catestrophic",verdict__contains="Failed").count()

    #SDN passed test-cases
    report['sdn_passed_TC'] = stat_qs.filter(verdict__contains="Passed", test_id__icontains="SDNC").count()
    #SDN Failed test-cases
    report['sdn_failed_TC'] = stat_qs.filter(verdict__contains="Failed", test_id__icontains="SDNC").count()

    #FUEL Passed test-cases
    report['fuel_passed_TC'] = stat_qs.filter(verdict__contains="Passed", test_id__icontains="FUEL").count()
    #FUEL Failed test-cases
    report['fuel_failed_TC'] = stat_qs.filter(verdict__contains="Failed", test_id__icontains="FUEL").count()

    #CEE passed test-cases
    report['cee_passed_TC'] = stat_qs.filter(verdict__contains="Passed", test_id__icontains="CEE").count()
    #CEE failed test-cases
    report['cee_failed_TC'] = stat_qs.filter(verdict__contains="Failed", test_id__icontains="CEE").count()

    #All-node passed test-cases
    report['allnode_passed_TC'] = stat_qs.filter(verdict__contains="Passed", test_id__icontains="ALL-NODE").count()    
    #ALL-node failed test-cases
    report['allnode_failed_TC'] = stat_qs.filter(verdict__contains="Failed", test_id__icontains="ALL-NODE").count()
     
    #report['failed_list'] = list(stat_qs.filter(verdict__contains="Failed").values())
  
     # Openstack data
    report['os_nova_list'] = stat_qs.filter(test_id__icontains="CEE-001", verdict__contains="Failed").count()
    report['os_nova_hypv'] = stat_qs.filter(test_id__icontains="CEE-002", verdict__contains="Failed").count()
    report['os_cinder_srv'] = stat_qs.filter(test_id__icontains="CEE-003", verdict__contains="Failed").count()
    report['os_neutron_agent'] = stat_qs.filter(test_id__icontains="CEE-004", verdict__contains="Failed").count()
    report['os_nova_srv'] = stat_qs.filter(test_id__icontains="CEE-005", verdict__contains="Failed").count()
    report['os_glance_image'] = stat_qs.filter(test_id__icontains="CEE-006", verdict__contains="Failed").count()
    report['os_ceilometer_meter'] = stat_qs.filter(test_id__icontains="CEE-007", verdict__contains="Failed").count()
    report['os_project_list'] = stat_qs.filter(test_id__icontains="CEE-008", verdict__contains="Failed").count()
    report['os_srv_list'] = stat_qs.filter(test_id__icontains="CEE-009", verdict__contains="Failed").count()
    report['os_neutron_net'] = stat_qs.filter(test_id__icontains="CEE-010", verdict__contains="Failed").count()


    #service data
    report['srv_watchmen'] = stat_qs.filter(test_id__icontains="CEE-011", verdict__contains="Failed").count()
    report['srv_rabbitmq_cls'] = stat_qs.filter(test_id__icontains="CEE-013", verdict__contains="Failed").count()
    report['srv_rabbitmq_lst'] = stat_qs.filter(test_id__icontains="CEE-014", verdict__contains="Failed").count()
    report['srv_galera_mysql'] = stat_qs.filter(test_id__icontains="CEE-015", verdict__contains="Failed").count()
    report['srv_mongodb'] = stat_qs.filter(test_id__icontains="CEE-016", verdict__contains="Failed").count()
    report['srv_mongodb_rep'] = stat_qs.filter(test_id__icontains="CEE-017", verdict__contains="Failed").count()
    report['srv_rabbitmg_file'] = stat_qs.filter(test_id__icontains="CEE-018", verdict__contains="Failed").count()
    report['srv_rest_srv'] = stat_qs.filter(test_id__icontains="SDNC-012", verdict__contains="Failed").count()
    report['srv_openflow'] = stat_qs.filter(test_id__icontains="SDNC-013", verdict__contains="Failed").count()
    report['srv_ovsdb'] = stat_qs.filter(test_id__icontains="SDNC-014", verdict__contains="Failed").count()
    report['srv_odlbgp'] = stat_qs.filter(test_id__icontains="SDNC-015", verdict__contains="Failed").count()
    


    #sdnc
    report['sdn_dpns'] = stat_qs.filter(test_id__icontains="SDNC-001", verdict__contains="Failed").count()
    report['sdn_tep'] = stat_qs.filter(test_id__icontains="SDNC-002", verdict__contains="Failed").count()
    report['sdn_tunnel'] = stat_qs.filter(test_id__icontains="SDNC-003", verdict__contains="Failed").count()

    report['sdn_tunnel_st'] = stat_qs.filter(test_id__icontains="SDNC-004", verdict__contains="Failed").count()

    temp = list(stat_qs.filter(test_id__icontains="SDNC-004").distinct().values('remarks'))
    if temp:
      val = re.search("[0-9]+$",temp[0]['remarks'].strip())
      if val:
          report['sdn_tunnel_st_count'] = val.group() 
      else:
          report['sdn_tunnel_st_count'] = '-' 

    else:
      report['sdn_tunnel_st_count'] = '-' 

    report['sdn_app_status'] = stat_qs.filter(test_id__icontains="SDNC-005", verdict__contains="Failed").count()

    temp = list(stat_qs.filter(test_id__icontains="SDNC-005").distinct().values('remarks'))
    if temp:
       val = re.search(r"((?<==)|(?<==)\s+)[0-9]+",temp[0]['remarks'])
       if val:
         report['sdn_app_count'] = val.group().strip() 
       else:
         report['sdn_app_count'] = '-' 
    else:
       report['sdn_app_count'] = '-' 


    report['sdn_shard_inv_status'] = stat_qs.filter(test_id__icontains="SDNC-006", verdict__contains="Failed").count()
    temp = list(stat_qs.filter(test_id__icontains="SDNC-006").values('remarks'))
    if temp:
      val = re.search('cic-[0-9]+',temp[0]['remarks'].strip())
      if val:
         report['sdn_shard_inv_data'] = val.group()
      else:
        report['sdn_shard_inv_data'] = '-' 
    else:
       report['sdn_shard_inv_data'] = '-'

    report['sdn_shard_def_status'] = stat_qs.filter(test_id__icontains="SDNC-007", verdict__contains="Failed").count()
    temp = list(stat_qs.filter(test_id__icontains="SDNC-007").values('remarks'))
    if temp:
      val = re.search('cic-[0-9]+',temp[0]['remarks'].strip())
      if val:
        report['sdn_shard_def_data'] = val.group()
      else:
       report['sdn_shard_def_data'] = '-' 
    else: 
      report['sdn_shard_def_data'] = '-'

    report['sdn_shard_top_status'] = stat_qs.filter(test_id__icontains="SDNC-008", verdict__contains="Failed").count()
    temp = list(stat_qs.filter(test_id__icontains="SDNC-008").values('remarks'))
    if temp:
      val = re.search('cic-[0-9]+',temp[0]['remarks'].strip())
      if val:
        report['sdn_shard_top_data'] = val.group()
      else:
        report['sdn_shard_top_data'] = '-'
    else:
      report['sdn_shard_top_data'] = '-'

    report['sdn_shard_invo_status'] = stat_qs.filter(test_id__icontains="SDNC-009", verdict__contains="Failed").count()

    temp = list(stat_qs.filter(test_id__icontains="SDNC-009").values('remarks'))
    if temp:
       val = re.search('cic-[0-9]+',temp[0]['remarks'].strip())
       if val:
         report['sdn_shard_invo_data'] = val.group() 
       else:
        report['sdn_shard_invo_data'] = '-'
    else:
        report['sdn_shard_invo_data'] = '-'


    report['sdn_shard_defo_status'] = stat_qs.filter(test_id__icontains="SDNC-010", verdict__contains="Failed").count()
    temp = list(stat_qs.filter(test_id__icontains="SDNC-010").values('remarks'))
    if temp:
       val = re.search('cic-[0-9]+',temp[0]['remarks'].strip())
       if val:
          report['sdn_shard_defo_data'] = val.group()
       else:
         report['sdn_shard_defo_data'] = '-'
    else:
         report['sdn_shard_defo_data'] = '-'


    report['sdn_shard_topo_status'] = stat_qs.filter(test_id__icontains="SDNC-011", verdict__contains="Failed").count()
    temp = list(stat_qs.filter(test_id__icontains="SDNC-011").values('remarks'))
    if temp:
       val = re.search('cic-[0-9]+',temp[0]['remarks'].strip())
       if val:
          report['sdn_shard_topo_data'] = val.group() 
       else:
          report['sdn_shard_topo_data'] = '-'
    else:
      report['sdn_shard_topo_data'] = '-'

    report['sdn_dpn_status']= stat_qs.filter(test_id__icontains="SDNC-016",verdict__contains="Failed").count()

    temp = list(stat_qs.filter(test_id__icontains="SDNC-016").values('remarks'))
    val2 = []
    for item in temp:
       val = re.search(r'^(\S+).*\b(\w).*?$',item['remarks'].strip())
       if val:
         val1 = val.groups()[0] +": " + val.groups()[1]
         val2.append(val1)

    val2.sort()
    print("val2",val2)
    count=0
    for m in range(len(val2)):
      count += int(val2[m].split(':')[1])
    report['sdn_dpn_data']= str(count) + '[ ' + ' ,'.join(val2) + ' ]' 
   
    

    report['sdn_tunnel_st_count_diff'] = 0
    report['sdn_app_count_diff'] = 0
    report['sdn_shard_inv_data_diff'] = 0
    report['sdn_shard_def_data_diff'] = 0
    report['sdn_shard_top_data_diff'] = 0
    report['sdn_shard_invo_data_diff'] = 0
    report['sdn_shard_defo_data_diff'] = 0
    report['sdn_shard_topo_data_diff'] = 0
    report['sdn_dpn_data_diff'] = 0     
    if  report_prv:
        if report_prv['sdn_tunnel_st_count'] != report['sdn_tunnel_st_count']:
            report['sdn_tunnel_st_count_diff'] = 1
        if report_prv['sdn_app_count'] != report['sdn_app_count']:
            report['sdn_app_count_diff'] = 1
        if report_prv['sdn_shard_inv_data'] != report['sdn_shard_inv_data']:
            report['sdn_shard_inv_data_diff'] = 1
        if report_prv['sdn_shard_def_data'] != report['sdn_shard_def_data']:
            report['sdn_shard_def_data_diff'] = 1
        if report_prv['sdn_shard_top_data'] != report['sdn_shard_top_data']:
            report['sdn_shard_top_data_diff'] = 1
        if report_prv['sdn_shard_invo_data'] != report['sdn_shard_invo_data']:
            report['sdn_shard_invo_data_diff'] = 1
        if report_prv['sdn_shard_defo_data'] != report['sdn_shard_defo_data']:
            report['sdn_shard_defo_data_diff'] = 1
        if report_prv['sdn_shard_topo_data'] != report['sdn_shard_topo_data']:
            report['sdn_shard_topo_data_diff'] = 1
        if report_prv['sdn_dpn_data'] != report['sdn_dpn_data']:
            report['sdn_dpn_data_diff'] = 1

    return report



from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def ajax(request):
    date = request.POST['date']
    site = request.POST['site']
    #convert date string into YYYY-MM-DD formate
    try: 
     date1=convert_date(date)  
    except Exception as e:
       return HttpResponse('Server-Error', status=503)

    print("<<get request>> date = ",date1)
    
    print("<<get request>> site = ",site)
    
    response = date_wise_start(date1,date,site)
    #print(response)
  
    #print("hahaha: ",type(date1))
    #testcount = healthCheck.objects.filter(date=date1).count()
    #testcount = healthCheck.objects.filter(date=date1).count()
    #print("selected-date:", date)

    #response={'date':date, 'test-count': testcount} 
    return JsonResponse(response)



def strip_spaces(list_of_dict):
    final=[]
    for m in list_of_dict:
        temp = {}
        for k,v in m.items():
            if k == 'Test Description':
              temp['Test_Description']=str(v).strip()
            elif k == 'Test ID':
              temp['Test_ID'] = str(v).strip()
            elif k == 'Command-Executed':
              temp['Command_Executed'] = str(v).strip()
            else: 
              temp[k]=str(v).strip()
        final.append(temp)
    return final


#@login_required
def refine_result(list_of_dict):
  final_dict = {}
  for item in list_of_dict:
    for k,v in item.items():
       if k in final_dict:
          final_dict[k].append(v)
       else:
          final_dict[k] = [v]	

  return final_dict



def dbtable_info(request):
    """Method to get date wise info"""

    date  = request.GET['date']
    date2 = date
    rq_type = request.GET['type']
    site = request.GET['site']
    print("<<More-Info >>date = ",date)
    print("<<More-Info >>Request_type = ",rq_type)
    print("<<More-Info >>site = ",site)
    try:
      date = convert_date(date)
    except Exception as e:
       print("Exception Occurred: ", str(e))
       return HttpResponse('Server-Error', status=503) 

    print("<<More-Info >>Date = ",date)
    if site == 'test-lab1':
       log = Logfile_Testlab1.objects.filter(uploaded_at=date).values()
       if log:
          logfile = log[0]['logfile']
       else:
          logfile = '#'
    if site == 'test-lab2':
       log = Logfile_Testlab2.objects.filter(uploaded_at=date).values()
       if log:
          logfile = log[0]['logfile']
       else:
          logfile = '#'
    print("<<More-Info>> Logfile = ", logfile)

    if  rq_type == "1" : data = healthCheck.objects.filter(date=date,site__contains=site); info="All Testcases"
    if  rq_type == "2" : data = healthCheck.objects.filter(date=date, verdict__contains = "Passed",site__contains=site);  info="All Passed"
    if  rq_type == "3" : data = healthCheck.objects.filter(date=date, verdict__contains = "Failed",site__contains=site); info="All Failed"
    #if  rq_type == "4" : data = healthCheck.objects.filter(date=date, verdict__contains = "Failed", severity__contains="Major",site__contains=site); info="All Failed Major"
    if  rq_type == "4" : data = healthCheck.objects.filter(date=date, severity__contains="Warning",site__contains=site); info="All Failed Major"

    data_dict = {'monitor_records': data , 'date': date2, 'info': info,'site_info':site.upper(),'logfile':logfile}
    return render(request,'dbtable_bydate.html', context=data_dict)



@csrf_exempt
def testlab1_logfile(request):
    if request.method == 'POST':
       form = LogfileForm_Testlab1(request.POST, request.FILES)
       if 'uploaded_at' in request.POST:
          date = request.POST['uploaded_at']
       else:
            return HttpResponse("Failed, Uploaded_at parameter missing in request", status=500)
  
       print("uploaded_at =", date)
       date_record = Logfile_Testlab1.objects.filter(uploaded_at=date)
       if date_record:
          print("Logfile already present in Testlab1....Deleted")
          date_record.delete()
       #form.uploaded_at = datetime.date.today()
       #extension = u_file.split(".")[1].lower()
       if form.is_valid():
            #return HttpResponse("Log File Uploaded!!!!!! ===")
            form.save()
            return HttpResponse("Log File Uploaded...Successfully!!!", status=201)
       else:
            print(form.errors)
            #return HttpResponse("Log File Uploaded....Failed", status=500)
            return HttpResponse(form.errors.as_json(), status=500)
     
    else:
      output = Logfile_Testlab1.objects.values()
      return HttpResponse(output) 


@csrf_exempt
def testlab2_logfile(request):
    if request.method == 'POST':
       form = LogfileForm_Testlab2(request.POST, request.FILES)
       if 'uploaded_at' in request.POST:
          date = request.POST['uploaded_at']
       else:
            return HttpResponse("Failed, Uploaded_at parameter missing in request", status=500)

       print("uploaded_at =", date)
       date_record = Logfile_Testlab2.objects.filter(uploaded_at=date)
       if date_record:
          print("Logfile already present in Testlab2....Deleted")
          date_record.delete()

       if form.is_valid():
            #return HttpResponse("Log File Uploaded!!!!!! ===")
            form.save()
            return HttpResponse("Log File Uploaded...Successfully!!!", status=201)
       else:
            print(form.errors)
            return HttpResponse(form.errors.as_json(), status=500)

    else:
      output = Logfile_Testlab2.objects.values()
      return HttpResponse(output)


def sample_report(request):
  return render(request,'sample_report.html')
  
#def sample_report(request):
  #if request.method == 'POST':
  #    myfile = request.FILES['myfile']
def sample_report1():
  myfile = open('test.json','r')
  if myfile:
      myfile = json.load(myfile)
      myfile = strip_spaces(myfile)
      myfile1 = myfile
      myfile = refine_result(myfile)
      import time
      time.sleep(6)
      output={}
      total_tc = len(myfile['Verdict'])
      output['total_tc'] = total_tc
      pass_tc = myfile['Verdict'].count('Passed')
      output['pass_tc'] = pass_tc
      fail_tc = myfile['Verdict'].count('Failed')
      output['fail_tc'] = fail_tc
      warning_tc = myfile['Severity'].count('Warning')  
      output['warning_tc'] = warning_tc
      fail_mj_tc = 0
      fail_mi_tc = 0
      fail_cat_tc = 0
      sdn_pass = 0 
      sdn_fail = 0
      cee_pass = 0
      cee_fail = 0
      allnode_pass = 0
      allnode_fail = 0 
      fuel_pass = 0
      fuel_fail = 0
      for i in range(len(myfile['Verdict'])):
         if myfile['Verdict'][i] == 'Failed':
            if myfile['Severity'][i] == 'Major':
               fail_mj_tc = fail_mj_tc + 1
            if myfile['Severity'][i] == 'Minor':
               fail_mi_tc = fail_mi_tc + 1
            if myfile['Severity'][i] == 'Catestrophic':
               fail_cat_tc = fail_cat_tc + 1
            if 'CEE' in myfile['Test_ID'][i]:
               cee_fail = cee_fail + 1
            if 'SDN' in myfile['Test_ID'][i]:
               sdn_fail = sdn_fail + 1
            if 'FUEL' in myfile['Test_ID'][i]:
               fuel_fail = fuel_fail + 1
            if 'ALL-NODE' in myfile['Test_ID'][i]:
               allnode_fail = allnode_fail + 1
         if myfile['Verdict'][i] == 'Passed':
            if 'CEE' in myfile['Test_ID'][i]:
               cee_pass = cee_pass + 1
            if 'SDN' in myfile['Test_ID'][i]:
               sdn_pass = sdn_pass + 1
            if 'FUEL' in myfile['Test_ID'][i]:
               fuel_pass = fuel_pass + 1
            if 'ALL-NODE' in myfile['Test_ID'][i]:
               allnode_pass = allnode_pass + 1
       
      fuel_tc = fuel_pass + fuel_fail
      output['fuel_tc']=fuel_tc
      cee_tc = cee_pass + cee_fail
      output['cee_tc'] = cee_tc
      sdn_tc = sdn_pass + sdn_fail
      output['sdn_tc'] = sdn_tc
      allnode_tc =allnode_pass + allnode_fail
      output['allnode_tc'] = allnode_tc
      fuel_per = str(int(fuel_pass/fuel_tc * 100)) + '%'
      cee_per = str(int(cee_pass/cee_tc * 100)) + '%'
      print(cee_per)
      sdn_per = str(int(sdn_pass/sdn_tc * 100)) + '%'
      allnode_per =str(int(allnode_pass/allnode_tc * 100)) + '%'

      output['fail_mj_tc'] = fail_mj_tc
      output['fail_mi_tc'] = fail_mi_tc
      output['fail_cat_tc'] = fail_cat_tc
      output['cee_fail'] = cee_fail
      output['sdn_fail'] = sdn_fail
      output['fuel_fail'] = fuel_fail
      output['allnode_fail'] = allnode_fail
      output['cee_pass'] = cee_pass
      output['sdn_pass'] = sdn_pass
      output['fuel_pass'] = fuel_pass
      output['allnode_pass'] = allnode_pass
      output['fuel_per'] = fuel_per
      output['cee_per'] = cee_per
      output['sdn_per'] = sdn_per
      output['allnode_per'] = allnode_per


      ##CEE Commands ##OS
      os_nova_list = 0
      os_nova_hypv = 0
      os_cinder_srv = 0
      os_neutron_agent = 0
      os_nova_srv = 0
      os_glance_image = 0
      os_ceilometer_meter = 0
      os_project_list = 0
      os_srv_list = 0
      os_neutron_net = 0
      srv_watchmen =0; srv_rabbitmq_cls=0; srv_rabbitmq_lst=0; srv_galera_mysql=0; srv_mongodb=0; srv_mongodb_rep=0; srv_rabbitmg_file=0
      srv_rest_srv=0; srv_openflow=0; srv_ovsdb=0; srv_odlbgp=0
      sdn_dpns = 0;sdn_tep = 0;sdn_tunnel = 0;sdn_tunnel_st =0
      sdn_tunnel_st_count ='-'; sdn_app_status=0; sdn_app_count='-'; sdn_shard_inv_status=0; sdn_shard_inv_data='-'
      sdn_shard_def_status=0; sdn_shard_def_data='-'; sdn_shard_top_status=0; sdn_shard_top_data='-'; sdn_shard_invo_status=0; sdn_shard_invo_data='-'
      sdn_shard_defo_status=0; sdn_shard_defo_data='-';sdn_shard_topo_status=0; sdn_shard_topo_data='-'; sdn_dpn_status=0; sdn_dpn_data=[]
      
 
      for i in range(len(myfile['Test_ID'])):
          if 'CEE-001' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              os_nova_list = os_nova_list + 1
          if 'CEE-002' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              os_nova_hypv = os_nova_hypv + 1
          if 'CEE-003' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              os_cinder_srv = os_cinder_srv + 1
          if 'CEE-004' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              os_neutron_agent += 1
          if 'CEE-005' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              os_nova_srv += 1
          if 'CEE-006' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              os_glance_image += 1
          if 'CEE-007' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              os_ceilometer_meter += 1
          if 'CEE-008' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              os_project_list += 1
          if 'CEE-009' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              os_srv_list += 1
          if 'CEE-010' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              os_neutron_net += 1

##Service 
          if 'CEE-011' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              os_nova_hypv += 1
          if 'CEE-013' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              srv_rabbitmq_cls += 1
          if 'CEE-014' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              srv_rabbitmq_lst += 1
          if 'CEE-015' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              srv_rabbitmq_lst += 1
          if 'CEE-016' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              srv_mongodb += 1
          if 'CEE-017' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              srv_mongodb += 1
          if 'CEE-018' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              srv_mongodb += 1


          if 'SDNC-012' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              srv_rest_srv += 1
          if 'SDNC-013' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              srv_openflow += 1
          if 'SDNC-014' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              srv_ovsdb += 1
          if 'SDNC-015' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              srv_odlbgp += 1

          if 'SDNC-001' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              sdn_dpns += 1
          if 'SDNC-002' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              sdn_tep += 1
          if 'SDNC-003' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              sdn_tunnel += 1
          if 'SDNC-004' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              sdn_tunnel_st += 1
          if 'SDNC-004' in myfile['Test_ID'][i].upper():
              temp = myfile['Remarks'][i]
              sdn_tunnel_st_count =  re.search("[0-9]+$",temp.strip()).group()
           
          if 'SDNC-005' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              sdn_app_status += 1
          if 'SDNC-005' in myfile['Test_ID'][i].upper():
              temp = myfile['Remarks'][i]
              sdn_app_count = re.search(r"((?<==)|(?<==)\s+)[0-9]+",temp).group().strip() 

          if 'SDNC-006' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              sdn_shard_inv_status = sdn_shard_inv_status + 1
          if 'SDNC-006' in myfile['Test_ID'][i].upper():
              temp = myfile['Remarks'][i]
              sdn_shard_inv_data = re.search('cic-[0-9]+',temp.strip()).group()

          if 'SDNC-007' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              sdn_shard_def_status += 1
          if 'SDNC-007' in myfile['Test_ID'][i].upper():
              temp = myfile['Remarks'][i]
              sdn_shard_def_data = re.search('cic-[0-9]+',temp.strip()).group()
              
          if 'SDNC-008' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              sdn_shard_top_status += 1
          if 'SDNC-008' in myfile['Test_ID'][i].upper():
              temp = myfile['Remarks'][i]
              sdn_shard_top_data = re.search('cic-[0-9]+',temp.strip()).group()
 
          if 'SDNC-009' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              sdn_shard_invo_status += 1
          if 'SDNC-009' in myfile['Test_ID'][i].upper():
              temp = myfile['Remarks'][i]
              sdn_shard_invo_data = re.search('cic-[0-9]+',temp.strip()).group()

          if 'SDNC-010' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              sdn_shard_defo_status += 1
          if 'SDNC-010' in myfile['Test_ID'][i].upper():
              temp = myfile['Remarks'][i]
              print("defo=", temp)
              sdn_shard_defo_data = re.search('cic-[0-9]+',temp.strip()).group()

          if 'SDNC-011' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              sdn_shard_topo_status += 1
          if 'SDNC-011' in myfile['Test_ID'][i].upper():
              temp = myfile['Remarks'][i]
              print("topo=", temp)
              sdn_shard_topo_data = re.search('cic-[0-9]+',temp.strip()).group()
       
          if 'SDNC-016' in myfile['Test_ID'][i].upper() and 'Failed' in myfile['Verdict'][i]:
              sdn_dpn_status += 1

          if 'SDNC-016' in myfile['Test_ID'][i].upper():
              temp = myfile['Remarks'][i]
              val = re.search(r'^(\S+).*\b(\w).*?$',temp.strip())
              if val:
                 val1 = val.groups()[0] +": " + val.groups()[1]
                 sdn_dpn_data.append(val1)
      
      output['sdn_dpn_data_sum']=0
      for i in sdn_dpn_data:
         val = i.split(':')[1]
         output['sdn_dpn_data_sum'] += int(val)
      strg=str(output['sdn_dpn_data_sum']) + '[ '
      for m in sdn_dpn_data:
        strg += m + '  '
      strg += ']'
      output['os_nova_list'] = os_nova_list
      output['os_nova_hypv'] = os_nova_hypv
      output['os_cinder_srv'] = os_cinder_srv
      output['os_neutron_agent'] = os_cinder_srv
      output['os_nova_srv'] = os_nova_srv
      output['os_glance_image'] = os_glance_image
      output['os_ceilometer_meter'] = os_ceilometer_meter
      output['os_project_list'] = os_project_list
      output['os_srv_list'] = os_srv_list
      output['os_neutron_net'] = os_neutron_net
      output['srv_watchmen'] = srv_watchmen
      output['srv_rabbitmq_cls'] = srv_rabbitmq_cls
      output['srv_rabbitmq_lst']=srv_rabbitmq_lst
      output['srv_galera_mysql']=srv_galera_mysql
      output['srv_mongodb']=srv_mongodb
      output['srv_mongodb_rep']=srv_mongodb_rep
      output['srv_rabbitmg_file']=srv_rabbitmg_file
      output['srv_rest_srv']=srv_rest_srv
      output['srv_openflow']=srv_openflow
      output['srv_ovsdb']=srv_ovsdb
      output['srv_odlbgp']=srv_odlbgp
      output['sdn_dpns'] = sdn_dpns
      output['sdn_tep'] = sdn_tep
      output['sdn_tunnel'] = sdn_tunnel
      output['sdn_tunnel_st'] =sdn_tunnel_st
      output['sdn_tunnel_st_count'] =sdn_tunnel_st_count
      output['sdn_app_status']=sdn_app_status
      output['sdn_app_count']=sdn_app_count
      output['sdn_shard_inv_status']=sdn_shard_inv_status
      output['sdn_shard_inv_data']=sdn_shard_inv_data
      output['sdn_shard_def_status']=sdn_shard_def_status
      output['sdn_shard_def_data']=sdn_shard_def_data
      output['sdn_shard_top_status']=sdn_shard_top_status
      output['sdn_shard_top_data']=sdn_shard_top_data
      output['sdn_shard_invo_status']=sdn_shard_invo_status
      output['sdn_shard_invo_data']= sdn_shard_invo_data
      output['sdn_shard_defo_status']=sdn_shard_defo_status
      output['sdn_shard_defo_data']=sdn_shard_defo_data
      output['sdn_shard_topo_status']=sdn_shard_topo_status
      output['sdn_shard_topo_data']=sdn_shard_topo_data
      output['sdn_dpn_status']=sdn_dpn_status
      output['sdn_dpn_data']= strg              

      #return HttpResponse(json.dumps(myfile))
      #return render(request,'pages/sample.html', {'monitor_records':myfile1, 'tc':total_tc})
      import pprint
      pprint.pprint(output)
      output['monitor_records'] = myfile1
      #return render(request,'pages/sample.html', output)
      return output

 # return render(request,'sample_report.html')


def date_wise_start_prv(date,site):
    report = {}
    print('prev date:' , date)
    stat_qs = healthCheck.objects.filter(date=date, site__contains=site)
    temp = list(stat_qs.filter(test_id__icontains="SDNC-004").distinct().values('remarks'))
    if temp:
      val = re.search("[0-9]+$",temp[0]['remarks'].strip())
      if val:
          report['sdn_tunnel_st_count'] = val.group() 
      else:
          report['sdn_tunnel_st_count'] = '-' 

    else:
      report['sdn_tunnel_st_count'] = '-' 

    report['sdn_app_status'] = stat_qs.filter(test_id__icontains="SDNC-005", verdict__contains="Failed").count()

    temp = list(stat_qs.filter(test_id__icontains="SDNC-005").distinct().values('remarks'))
    if temp:
       val = re.search(r"((?<==)|(?<==)\s+)[0-9]+",temp[0]['remarks'])
       if val:
         report['sdn_app_count'] = val.group().strip() 
       else:
         report['sdn_app_count'] = '-' 
    else:
       report['sdn_app_count'] = '-' 


    report['sdn_shard_inv_status'] = stat_qs.filter(test_id__icontains="SDNC-006", verdict__contains="Failed").count()
    temp = list(stat_qs.filter(test_id__icontains="SDNC-006").values('remarks'))
    if temp:
      val = re.search('cic-[0-9]+',temp[0]['remarks'].strip())
      if val:
         report['sdn_shard_inv_data'] = val.group()
      else:
        report['sdn_shard_inv_data'] = '-' 
    else:
       report['sdn_shard_inv_data'] = '-'

    report['sdn_shard_def_status'] = stat_qs.filter(test_id__icontains="SDNC-007", verdict__contains="Failed").count()
    temp = list(stat_qs.filter(test_id__icontains="SDNC-007").values('remarks'))
    if temp:
      val = re.search('cic-[0-9]+',temp[0]['remarks'].strip())
      if val:
        report['sdn_shard_def_data'] = val.group()
      else:
       report['sdn_shard_def_data'] = '-' 
    else: 
      report['sdn_shard_def_data'] = '-'

    report['sdn_shard_top_status'] = stat_qs.filter(test_id__icontains="SDNC-008", verdict__contains="Failed").count()
    temp = list(stat_qs.filter(test_id__icontains="SDNC-008").values('remarks'))
    if temp:
      val = re.search('cic-[0-9]+',temp[0]['remarks'].strip())
      if val:
        report['sdn_shard_top_data'] = val.group()
      else:
        report['sdn_shard_top_data'] = '-'
    else:
      report['sdn_shard_top_data'] = '-'

    report['sdn_shard_invo_status'] = stat_qs.filter(test_id__icontains="SDNC-009", verdict__contains="Failed").count()

    temp = list(stat_qs.filter(test_id__icontains="SDNC-009").values('remarks'))
    if temp:
       val = re.search('cic-[0-9]+',temp[0]['remarks'].strip())
       if val:
         report['sdn_shard_invo_data'] = val.group() 
       else:
        report['sdn_shard_invo_data'] = '-'
    else:
        report['sdn_shard_invo_data'] = '-'


    report['sdn_shard_defo_status'] = stat_qs.filter(test_id__icontains="SDNC-010", verdict__contains="Failed").count()
    temp = list(stat_qs.filter(test_id__icontains="SDNC-010").values('remarks'))
    if temp:
       val = re.search('cic-[0-9]+',temp[0]['remarks'].strip())
       if val:
          report['sdn_shard_defo_data'] = val.group()
       else:
         report['sdn_shard_defo_data'] = '-'
    else:
         report['sdn_shard_defo_data'] = '-'


    report['sdn_shard_topo_status'] = stat_qs.filter(test_id__icontains="SDNC-011", verdict__contains="Failed").count()
    temp = list(stat_qs.filter(test_id__icontains="SDNC-011").values('remarks'))
    if temp:
       val = re.search('cic-[0-9]+',temp[0]['remarks'].strip())
       if val:
          report['sdn_shard_topo_data'] = val.group() 
       else:
          report['sdn_shard_topo_data'] = '-'
    else:
      report['sdn_shard_topo_data'] = '-'

    report['sdn_dpn_status']= stat_qs.filter(test_id__icontains="SDNC-016",verdict__contains="Failed").count()

    temp = list(stat_qs.filter(test_id__icontains="SDNC-016").values('remarks'))
    val2 = []
    for item in temp:
       val = re.search(r'^(\S+).*\b(\w).*?$',item['remarks'].strip())
       if val:
         val1 = val.groups()[0] +": " + val.groups()[1]
         val2.append(val1)

    val2.sort()
    print("val2",val2)
    count=0
    for m in range(len(val2)):
      count += int(val2[m].split(':')[1])
    report['sdn_dpn_data']= str(count) + '[ ' + ' ,'.join(val2) + ' ]'


    return report

@csrf_exempt
def adhoc(request):
    import sys
    from subprocess import run,PIPE
    import time
    timestamp = request.POST['timestamp']
    print("timestamp=",timestamp)
    #time.sleep(600)
    out = run(['/bin/bash', '/tmp/test.sh'], stdout=PIPE)
    print(out)
    print(out.returncode)
    #return HttpResponse("Execution Done", out)
    m = sample_report1()
    return render(request,'pages/sample.html', m)


#####

@csrf_exempt
def execute1(request):
  from . models import Execute1
  if request.method == 'POST':
     timestamp = request.POST['timestamp']
     timestamp_str = request.POST['timestamp_str']
     Execute1.objects.create(timestamp=timestamp,timestamp_str=timestamp_str,status='started')
     import sys
     from subprocess import run,PIPE
     out = run(['/bin/bash', '/tmp/test.sh',timestamp], stdout=PIPE)
     print('timestamp_out=',out)
     print(out.returncode)
     if out.returncode == 0:
        print('timestamp success:',timestamp_str)
        Execute1.objects.filter(timestamp=timestamp).update(status='passed')
     else:
        print('timestamp failed:',timestamp_str)
        Execute1.objects.filter(timestamp=timestamp).update(status='failed')

     data = Execute1.objects.all().order_by('-timestamp')
     return render(request,'execute1.html', {'data': data})

  data = Execute1.objects.all().order_by('-timestamp')
  return render(request,'execute1.html', {'data': data})



def execute1_result(request):
  from . models import Execute1
  if request.method == 'GET':
     timestamp = request.GET['id']
     data = Execute1.objects.filter(timestamp=timestamp).values('status','timestamp_str')
     if data:
        timestamp_str=data[0]['timestamp_str']
        status = data[0]['status']
     return render(request,'execute1_result.html', {'timestamp':timestamp,'status':status,'timestamp_str':timestamp_str })


def logpoller(request):
    timestamp = request.GET['timestamp']
    line = request.GET['num']  
    import os.path
    status='-1'
    file_name='/tmp/'+str(timestamp)+'.log'
    output={}
    if os.path.isfile(file_name):
       file_str = open(file_name,'r')
       data = file_str.readlines()
       if int(line) != 0:
         l=int(line)
         data = data[l::]
       data_len = len(data)
       flag = 'open'
       print(data)
       if data and 'END' in data[-1]:
          flag = 'closed'
          print(data[-1])
          status = data[-1].split(':')[0]

       output['data']=data
       output['len']=data_len
       output['flag']=flag
       output['status']=status

    else:
       output['flag']='error'


    return JsonResponse(output)


          
