from pickle import FALSE
from django.shortcuts import render,redirect
from .models import CreateStockGrp,group_summary,payhead_crt,create_payhead

# Create your views here.


def index(request):
    return render(request,'base.html')

def profit(request):
    return render(request,'profit.html') 


def stockgroup(request):
    std=CreateStockGrp.objects.all()
    return render(request,'stockgroup.html',{'std':std})

def item_list(request,pk):
    std=group_summary.objects.filter(CreateStockGrp_id=pk)
    return render(request,'items.html',{'std':std})  

def  payhead_list(request):
    std=create_payhead.objects.filter(under='Direct Incomes')
    return render(request,'payhead_items.html',{'std':std}) 


def stock_groups(request):
    und=CreateStockGrp.objects.all()
    if request.method=='POST':
        name=request.POST['name']
        alias=request.POST['alias']
        under_name=request.POST['under_name']
        quantities=request.POST['quantities']
        stockgrp=CreateStockGrp(name=name,alias=alias,under_name=under_name,quantities=quantities)
        stockgrp.save()
        return redirect('stock_items')
    return render(request,'group_stock.html',{'und':und})    



def stock_items(request):
    grp=CreateStockGrp.objects.all()
    if request.method=='POST':
        name=request.POST['name']
        alias=request.POST['alias']
        under=request.POST['under']
        grp1=CreateStockGrp.objects.get(id=under)
        # category=request.POST['category',FALSE]
        units=request.POST['units']
        batches=request.POST['batches']
        manufacturing_date=request.POST['manufacturing_date']
        expiry_dates=request.POST['expiry_dates']
        rate_of_duty=request.POST['rate_of_duty']
        quantity=request.POST['quantity']
        rate=request.POST['rate']
        per=request.POST['per']
        value=request.POST['value']
        additional=request.POST['additional']
        crt=group_summary(name=name,alias=alias,under=under,units=units,batches=batches,
                           manufacturing_date=manufacturing_date,expiry_dates=expiry_dates,
                           rate_of_duty=rate_of_duty,quantity=quantity,rate=rate,per=per,value=value,additional=additional,CreateStockGrp=grp1)
        crt.save()
        return redirect('stock_items')
    return render(request,'stockitem.html',{'grp':grp})


def payhead(request):
    # att=attendance_crt.objects.all()
    pay=payhead_crt.objects.all()
    if request.method=='POST':
        name=request.POST['name']
        alias=request.POST['alias']
        pay_head_type=request.POST['payhead']
        income_type=request.POST['income']
        under=request.POST['under']
        affect_net_salary=request.POST['netsalary']
        payslip=request.POST['payslip']
        calculation_of_gratuity=request.POST['caltype']
        calculation_period=request.POST['ctype']
        calculation_type=request.POST['caltype']
        attendence_leave_withpay=request.POST['attendence with pay']
        attendence_leave_with_outpay=request.POST['Attendance with out pay']
        production_type=request.POST['ptype']
        opening_balance=request.POST['balance']

        #compute information
        compute=request.POST['compute']
        effective_from=request.POST['effective_from']
        # amount_greaterthan=request.POST['', False]
        amount_upto=request.POST['amount_upto']
        slabtype=request.POST['slab_type']
        value=request.POST['value']

        #Rounding
        round_method=request.POST['roundmethod']
        limit=request.POST['limit']

        #Gratuity
        days_of_months=request.POST['days_of_months']
        from_date=request.POST['from']
        to=request.POST['to']
        calculation_per_year=request.POST['eligiibility']

        std=create_payhead(name=name,
                           alias=alias,
                           pay_type=pay_head_type,
                           income_type=income_type,
                           under=under,
                           affect_net=affect_net_salary,
                           payslip=payslip,
                           calculation_of_gratuity=calculation_of_gratuity,
                           cal_type=calculation_type,
                           calculation_period=calculation_period,
                           leave_withpay=attendence_leave_withpay,
                           leave_with_out_pay=attendence_leave_with_outpay,
                           production_type=production_type,
                           opening_balance=opening_balance,
                           compute=compute,
                           effective_from=effective_from,
                           #  amount_greater=amount_greaterthan,
                           amount_upto=amount_upto,
                           slab_type=slabtype,
                           value=value,
                           Rounding_Method=round_method,
                           Round_limit=limit,
                           days_of_months=days_of_months,
                           number_of_months_from=from_date,
                           to=to,
                           calculation_per_year=calculation_per_year,
                           
        )
        std.save()
        return redirect('payhead')
    return render(request,'payhead.html')   

        # std2=compute_information(Pay_head_id=idd,
        #                          compute=compute,
        #                          effective_from=effective_from,
        #                         #  amount_greater=amount_greaterthan,
        #                          amount_upto=amount_upto,
        #                          slab_type=slabtype,
        #                          value=value,
        # )
        # std2.save()

        # std3=Rounding(pay_head_id=idd,
        #              Rounding_Method=round_method,
        #              Round_limit=limit,
        # )
        # std3.save()

        # std4=gratuity(pay_head_id=idd,
        #              days_of_months=days_of_months,
        #              number_of_months_from=from_date,
        #              to=to,
        #              calculation_per_year=calculation_per_year,
        # )
        # std4.save()
        # messages.success(request,'successfully Added !!!')
         

def ledger(request):
    return render(request,'ledger.html')



