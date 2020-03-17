from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . models import healthCheck
from . models import Logfile 
from . forms import LogfileForm
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
    date_list = healthCheck.objects.filter(site__contains="test-lab1").values("date").distinct().order_by('-date')
    return render(request, 'pages/testlab-1.html',{'dates':date_list})

@login_required
def testlab2(request):
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
       for item in test_json['Test-Cases']:
          ip = item['IPAddress'].strip()
          healthCheck.objects.create(desc=item['Test Description'], severity=item['Severity'], ipaddr=ip, hostname=item['Hostname'], command=item['Command-Executed'], verdict=item['Verdict'], remarks=item['Remarks'],test_id=item['Test ID'],date=datet, site=test_json['Site'])
          
       #print(test_json) 
       #return HttpResponse(test_json[0]['Test_Description'])
       return HttpResponse("<em>DATA Stored</em>")
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
    data = healthCheck.objects.filter(date=date_lst[0]['date'],site__contains=site) 
    data_dict = {'monitor_records': data , 'date': date_lst[0]['date'], 'site': site}
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

    #total warning testcases
    report['failed_war_TC'] = stat_qs.filter(severity__contains="Warning",verdict__contains="Failed").count()

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

    print("val2",val2)
    report['sdn_dpn_data']= val2
   
    
    return report



from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def ajax(request):
    date = request.POST['date']
    site = request.POST['site']
    #convert date string into YYYY-MM-DD formate
    
    date1=convert_date(date)  
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



















 
    
    

def dbdata(request):
    data = healthCheck.objects.all().values()
    data1 = healthCheck.objects.filter(verdict__contains="Passed").values('remarks')
    severity_failed_major = healthCheck.objects.filter(severity__contains="Major",verdict__contains="Failed")
    severity_failed_minor = healthCheck.objects.filter(severity__contains="Minor",verdict__contains="Failed")
    severity_failed_catestrophic = healthCheck.objects.filter(severity__contains="Catestrophic",verdict__contains="Failed")
    severity_failed_warning = healthCheck.objects.filter(severity__contains="Warning",verdict__contains="Failed")

    #print(list(data))
    count_passed = len(data1)
    print("Passed Test Case",count_passed)
    fail = healthCheck.objects.filter(verdict__contains="Failed")
    print("Failed Test Case",len(fail))
    print("Total Test Case",len(data))
    date =(data[0])['date'].strftime('%m %B,%Y')
    result={}

    result['passed']=count_passed
    result['failed']=len(fail)
    result['total']=len(data)
    result['date']=date
    result['severity_failed_major']=len(severity_failed_major)
    result['severity_failed_minor']=len(severity_failed_minor)
    result['severity_failed_catestrophic']=len(severity_failed_catestrophic)
    result['severity_failed_warning']=len(severity_failed_warning)
   
    

    return JsonResponse(result)

    #data_dict = {'monitor_records': list(data) }
    #return JsonResponse(data_dict)


def strip_spaces(list_of_dict):
    final=[]
    for m in list_of_dict:
        temp = {}
        for k,v in m.items():
            temp[k]=str(v).strip()
        final.append(temp)
    return final


@login_required
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
    date  = request.GET['date']
    date2 = date
    rq_type = request.GET['type']
    site = request.GET['site']
    print("<<More-Info >>date = ",date)
    print("<<More-Info >>Request_type = ",rq_type)
    print("<<More-Info >>site = ",site)
    date = convert_date(date)
    print("<<More-Info >>Date = ",date)
    logfile = 'unica-healthchk-log-test-lab1-'+date+'.txt'
    print("<<More-Info>> Logfile = ", logfile)

    if  rq_type == "1" : data = healthCheck.objects.filter(date=date,site__contains=site); info="All Testcases"
    if  rq_type == "2" : data = healthCheck.objects.filter(date=date, verdict__contains = "Passed",site__contains=site);  info="All Passed"
    if  rq_type == "3" : data = healthCheck.objects.filter(date=date, verdict__contains = "Failed",site__contains=site); info="All Failed"
    if  rq_type == "4" : data = healthCheck.objects.filter(date=date, verdict__contains = "Failed", severity__contains="Major",site__contains=site); info="All Failed Major"

    data_dict = {'monitor_records': data , 'date': date2, 'info': info,'site':site,'logfile':logfile}
    return render(request,'dbtable_bydate.html', context=data_dict)


def dbdata1(request):
    
    return JsonResponse(result)


@csrf_exempt
def logfile(request):
    if request.method == 'POST':
       form = LogfileForm(request.POST, request.FILES)
       #u_file = request.FILES['file']
       print(form)
       form.uploaded_at = datetime.date.today()
       #extension = u_file.split(".")[1].lower()
       if form.is_valid():
            #return HttpResponse("Log File Uploaded!!!!!! ===")
            form.save()
            return HttpResponse("Log File Uploaded...Yes")
       else:
            print(form.errors)
            return HttpResponse("Log File Uploaded....NONONO")
     
    else:
      return render(request,'test.html')
