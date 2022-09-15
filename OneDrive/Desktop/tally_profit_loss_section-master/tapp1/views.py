from functools import total_ordering
from pickle import FALSE
from django.shortcuts import render,redirect
from .models import CreateStockGrp,group_summary,payhead_crt,create_payhead,Ledger,ledger_tax,Ledger_Banking_Details,Ledger_Mailing_Address,Ledger_Rounding,Ledger_Satutory,Ledger_sundry,Ledger_Tax_Register,add_voucher,add_voucher2

# Create your views here.


def index(request):
    return render(request,'base.html')

def grp_month(request,pk):
    std=Ledger.objects.get(id=pk)
    vouch2=add_voucher2.objects.all()
    total_debit=0
    total_credit=0
    for i in vouch2:
        total_debit+=int(i.debit)
        total_credit+=int(i.credit)
        
    opening_balance=total_debit-int(std.ledger_opening_bal)+total_credit
    if opening_balance>0 :
        std.ledger_type=opening_balance
        std.save()
        
    else :
        std.provide_banking_details=opening_balance*-1
        std.save()
            
    return render(request,'group_month.html',{'std':std,'vouch2':vouch2,'total_debit':total_debit,'total_credit':total_credit,'opening_balance':opening_balance})

def sales_month(request,pk):
    std=Ledger.objects.get(id=pk)
    
    vouch2=add_voucher2.objects.all()
    total_debit=0
    total_credit=0
    for i in vouch2:
        total_debit+=int(i.debit)
        total_credit+=int(i.credit)
        
    opening_balance=total_debit-int(std.ledger_opening_bal)+total_credit
    
    # std.ledger_type=opening_balance
    # std.save()
    
    return render(request,'sales_month.html',{'std':std,'total_debit':total_debit,'total_credit':total_credit,'opening_balance':opening_balance})


def payhead_month(request,pk):
    std=create_payhead.objects.get(id=pk)
    vouch2=add_voucher2.objects.all()
    total_debit=0
    total_credit=0
    for i in vouch2:
        total_debit+=int(i.debit)
        total_credit+=int(i.credit)
        
    opening_balance=total_debit-int(std.opening_balance)+total_credit
    return render(request,'month_payhead.html',{'std':std,'total_debit':total_debit,'total_credit':total_credit,'opening_balance':opening_balance})

def pay_voucher(request,pk):
    std=create_payhead.objects.get(id=pk)
    vouch2=add_voucher2.objects.all()
    total_debit=0
    total_credit=0
    
    for i in vouch2 :
        total_debit+=int(i.debit)
        total_credit+=int(i.credit)
        
    opening_balance=total_debit-int(std.opening_balance)+total_credit
    
    if opening_balance>0 :
        std.leave_withpay=opening_balance
        std.save()
        
    else :
        std.leave_with_out_pay=opening_balance*-1
        std.save()
    
    return render(request,'payhead_voucher.html',{'std':std,'vouch2':vouch2,'total_debit':total_debit,'total_credit':total_credit,'opening_balance':opening_balance})

def stock_voucher(request,pk):
    std=group_summary.objects.get(id=pk)
    vouch=add_voucher.objects.all()
    total_value=0
    total_qunity=0
    total_val=int(std.value)
    total_qun=int(std.quantity)
    for i in vouch:
        if (i.voucher_type=='sales'):
            total_value +=int(i.value)
            total_qunity+=int(i.quntity)
        elif (i.voucher_type=='purchase'):
            total_val+=int(i.value) 
            total_qun+=int(i.quntity)
    closing_qun=total_qun-total_qunity  
    closing_val=total_val-total_value      
    context={
        'std':std,
        'vouch':vouch,
        'total_sales_value':total_value,
        'total_sales_quntity':total_qunity, 
        'total_purchase_value':total_val,
        'total_purchase_quntity':total_qun,
        'closing_qun':closing_qun,
        'closing_val':closing_val,
        }        
    return render(request,'stock_voucher.html',context)


def profit(request):
    balance=Ledger.objects.all()
    balance_py=create_payhead.objects.all()
    balance_le=Ledger.objects.all()
    balance_group=group_summary.objects.all()
    total_grp=0
    total_direct=0
    total=0
    total_income=0
    total_purch=0
    total_direct_exp=0
    total_indirect=0
    #sales account total
    for i in balance:
        if(i.group_under=='Sales_Account'):
            total+=int(i.ledger_type)
            total+=int(i.provide_banking_details)
            
    #indirect income total        
    for i in balance_py:
        if(i.under=='Income(Indirect)'):
            total_income+=int(i.leave_withpay)
            total_income+=int(i.leave_with_out_pay)
    for p in balance_le:
         if(p.group_under=='income_Indirect'):
             total_income+=int(p.ledger_type) 
             total_income+=int(p.provide_banking_details)
             
    #direct income total
             
    for i in balance_py:
        if(i.under=='Direct Incomes'):
            total_direct+=int(i.leave_withpay) 
            total_direct+=int(i.leave_with_out_pay) 
    
    for p in balance_le:
        if(p.group_under=='Direct Incomes'):
            total_direct+=int(p.ledger_type) 
            total_direct+=int(p.provide_banking_details)
            
    #closing stock
    for k in  balance_group:
        total_grp+=int(k.value)
        
    #purchase account total 
    
    for i in balance:
        if(i.group_under=='Purchase_Account'):
            total_purch+=int(i.ledger_type)
            total_purch+=int(i.provide_banking_details)
    
    #direct expenses total
           
    for i in balance_py:
        if(i.under=='Direct Expenses'):
            total_direct_exp+=int(i.leave_withpay) 
            total_direct_exp+=int(i.leave_with_out_pay)     
    
    for p in balance_le:
        if(p.group_under=='Direct Expenses'):
            total_direct_exp+=int(p.ledger_type) 
            total_direct_exp+=int(p.provide_banking_details) 
            
    #indirect expenses total   
    
    for i in balance_py:
        if(i.under=='Indirect Expenses'):
            total_indirect+=int(i.leave_withpay)
            total_indirect+=int(i.leave_with_out_pay)
    for p in balance_le:
         if(p.group_under=='Expences_Indirect'):
            total_indirect+=int(p.ledger_type) 
            total_indirect+=int(p.provide_banking_details)    
            
    #closing stock
    std=group_summary.objects.all()
    vouch=add_voucher.objects.all()
    total_val=0
    total_qun=0
    total_value=0
    total_qunity=0
    
    for i in vouch:
        if (i.voucher_type=='sales'):
            total_value+=int(i.value)
            total_qunity+=int(i.quntity)
        elif (i.voucher_type=='purchase'):
            total_val+=int(i.value) 
            total_qun+=int(i.quntity)
       
    for p in std:
        total_val+=int(p.value)
        total_qun+=int(p.quantity)
                
    closing_value=total_val
    closing_quntity=total_qun-total_qunity        
            
                   
    return render(request,'profit.html',{'total':total,'total_income':total_income,'total_direct':total_direct,'total_grp':total_grp,'total_purch':total_purch,'total_direct_exp':total_direct_exp,'total_indirect':total_indirect,'closing_value':closing_value,'closing_quntity':closing_quntity,}) 





def  payhead_list(request):
    std=create_payhead.objects.filter(under='Direct Incomes')
    stm=Ledger.objects.filter(group_under='Direct Incomes')
    balance=create_payhead.objects.all()
    balance_le=Ledger.objects.all()
    total=0
    total_d=0
    for i in balance:
        if(i.under=='Direct Incomes'):
            total+=int(i.leave_withpay)
            total_d+=int(i.leave_with_out_pay)
    for p in balance_le:
         if(p.group_under=='Direct Incomes') :
             total+=int(p.ledger_type) 
             total_d+=int(p.provide_banking_details)
         
    
    
    return render(request,'payhead_items.html',{'std':std,'stm':stm,'total':total,'total_d':total_d}) 



def direct_exprenses(request):
    std=create_payhead.objects.filter(under='Direct Expenses')
    stm=Ledger.objects.filter(group_under='Direct Expenses')
    total=0
    total_d=0
    for i in std:
        total+=int(i.leave_withpay)
        total_d+=int(i.leave_with_out_pay)
    for p in stm:
        total+=int(p.ledger_type) 
        total_d+=int(p.provide_banking_details)
    return render(request,'direct_expenses.html',{'std':std,'stm':stm,'total':total,'total_d':total_d}) 

def sales(request):
    std=Ledger.objects.filter(group_under='Sales_Account')
    balance=Ledger.objects.all()
    total=0
    total_d=0
    for i in balance:
        if (i.group_under=='Sales_Account') :
            total+=int(i.ledger_type)
            total_d+=int(i.provide_banking_details)
        
                 
    return render(request,'sales_accounts.html',{'std':std,'total':total,'total_d':total_d})

def purchase(request):
    std=Ledger.objects.filter(group_under='Purchase_Account')
    
    total=0
    total_d=0
    for i in std:
        total+=int(i.ledger_type)
        total_d+=int(i.provide_banking_details)
    return render(request,'purchase_list.html',{'std':std,'total':total,'total_d':total_d})




def stock_month(request,pk):
    std=group_summary.objects.get(id=pk)
    
    vouch=add_voucher.objects.all()
    total_value=0
    total_qunity=0
    total_val=int(std.value)
    total_qun=int(std.quantity)
    for i in vouch:
        if (i.voucher_type=='sales'):
            total_value +=int(i.value)
            total_qunity+=int(i.quntity)
        elif (i.voucher_type=='purchase'):
            total_val+=int(i.value) 
            total_qun+=int(i.quntity)
    closing_qun=total_qun-total_qunity  
    closing_val=total_val-total_value      
    context={
        'std':std,
        'vouch':vouch,
        'total_sales_value':total_value,
        'total_sales_quntity':total_qunity, 
        'total_purchase_value':total_val,
        'total_purchase_quntity':total_qun,
        'closing_qun':closing_qun,
        'closing_val':closing_val,
        }        
    
    return render(request,'stock_month.html',context)

def item_list(request,pk):
    std=group_summary.objects.filter(CreateStockGrp_id=pk)
    vouch=add_voucher.objects.all()
    total=0
    total_qty=0
    total_value=0
    total_qunity=0
    
    for p in std:
        total_qun=int(p.quantity)
        total_val=int(p.value)
    # calculation of voucher
    for i in vouch:
        if (i.voucher_type=='sales'):
            total_value +=int(i.value)
            total_qunity+=int(i.quntity)
        elif (i.voucher_type=='purchase'):
            total_val+=int(i.value) 
            total_qun+=int(i.quntity)
            closing_qun=total_qun-total_qunity  
    closing_val=total_val-total_value 
   
    
    for i in std:
        total+=int(i.value)
        total_qty+=int(i.quantity)
        
    return render(request,'items.html',{'std':std,'total':total,'total_qty':total_qty,'closing_val':closing_val,'closing_qun':closing_qun,}) 
 
def items_2(request,pk):
    ptm=group_summary.objects.filter(CreateStockGrp_id=pk)
    
    vouch=add_voucher.objects.all()
    total=0
    total_qty=0
    total_value=0
    total_qunity=0
    
    for p in ptm:
        total_qun=int(p.quantity)
        total_val=int(p.value)
    # calculation of voucher
    for i in vouch:
        if (i.voucher_type=='sales'):
            total_value +=int(i.value)
            total_qunity+=int(i.quntity)
        elif (i.voucher_type=='purchase'):
            total_val+=int(i.value) 
            total_qun+=int(i.quntity)
            closing_qun=total_qun-total_qunity  
    closing_val=total_val-total_value 
   
    
    for i in ptm:
        total+=int(i.value)
        total_qty+=int(i.quantity)
        
    return render(request,'item_2.html',{'ptm':ptm,'closing_val':closing_val,'closing_qun':closing_qun,'total':total})
    
def stockgroup(request):
    ptm=CreateStockGrp.objects.all()
    std=group_summary.objects.all()
    vouch=add_voucher.objects.all()
    total_val=0
    total_qun=0
    total_value=0
    total_qunity=0
    
    for i in vouch:
        if (i.voucher_type=='sales'):
            total_value+=int(i.value)
            total_qunity+=int(i.quntity)
        elif (i.voucher_type=='purchase'):
            total_val+=int(i.value) 
            total_qun+=int(i.quntity)
       
    for p in std:
        total_val+=int(p.value)
        total_qun+=int(p.quantity)
                
    closing_value=total_val-total_value
    closing_quntity=total_qun-total_qunity
    return render(request,'stockgroup.html',{'std':std,'closing_value':closing_value,'closing_quntity':closing_quntity,'ptm':ptm})

def stock_group2(request):
    ptm=CreateStockGrp.objects.all()
    std=group_summary.objects.all()
    total_val=0
    total_qun=0
    for p in std:
        total_val+=int(p.value)
        total_qun+=int(p.quantity)
        
    return render(request,'stockgroup_2.html',{'std':std,'opening_value':total_val,'opening_quntity':total_qun,'ptm':ptm})
    

def indirect(request):
    std=create_payhead.objects.filter(under='Income(Indirect)')
    stm=Ledger.objects.filter(group_under='income_Indirect')
    
    total=0
    total_d=0
    for i in std:
        total+=int(i.leave_withpay)
        total_d+=int(i.leave_with_out_pay)
    for p in stm:
        total+=int(p.ledger_type) 
        total_d+=int(p.provide_banking_details)
    
    
    return render(request,'indirect_income.html',{'std':std,'stm':stm,'total':total,'total_d':total_d})



def indirect_expenses(request):
    std=create_payhead.objects.filter(under='Indirect Expenses')
    stm=Ledger.objects.filter(group_under='Expences_Indirect')
    
    total=0
    total_d=0
    for i in std:
        total+=int(i.leave_withpay)
        total_d+=int(i.leave_with_out_pay)
    for p in stm:
        total+=int(p.ledger_type) 
        total_d+=int(p.provide_banking_details)
    
    
    return render(request,'indirect_expences.html',{'std':std,'stm':stm,'total':total,'total_d':total_d})



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



def save_ledger(request):
    if request.method == 'POST':
        # Ledger Basic
        Lname = request.POST.get('ledger_name', False)
        Lalias = request.POST.get('ledger_alias', False)
        Lunder = request.POST.get('group_under', False)
        Lopening_bal = request.POST.get('ledger_opening_bal', False)
        cd_db=request.POST.get('cd_db',False)
        typ_of_ledg = request.POST.get('ledger_type', False)
        provide_banking = request.POST.get('provide_banking_details', False)

        # Banking_details
        B_od_limit = request.POST.get('od_limit', False)
        B_ac_holder_name =request.POST.get('holder_name', False)
        B_ac_no = request.POST.get('ac_number', False)
        B_ifsc = request.POST.get('ifsc', False)
        B_swift_code =request.POST.get('swift_code', False)
        B_name = request.POST.get('bank_name', False)
        B_branch = request.POST.get('branch_name', False)
        B_alter_chq_bks =request.POST.get('alter_chk_bks', False)
        B_name_enbl_chq_prtg = request.POST.get('enbl_chk_printing', False) 
        B_chqconfg= request.POST.get('chqconfg', False) 
        # Mailing_details
        Mname = request.POST.get('name', False)
        Maddress = request.POST.get('address', False)
        Mstate =request.POST.get('state', False)
        Mcountry = request.POST.get('country', False)
        Mpincode = request.POST.get('pincode', False)

        # Tax_Registration_Details
        Tgst_uin = request.POST.get('gst_uin', False)
        Treg_typ = request.POST.get('register_type', False)
        Tpan_no = request.POST.get('pan_no', False)
        T_alter_gst =request.POST.get('alter_gst_details', False)

        # Satutory Details
        assessable_calculationn = request.POST.get('assessable_calculation', False)
        Appropriate_too =request.POST.get('Appropriate_to', False)
        gst_applicablee = request.POST.get('is_gst_applicable',False)
        Set_alter_GSTT=request.POST.get('Set_alter_GST', False)
        type_of_supplyy = request.POST.get('type_of_supply',False)
        Method_of_calcc=request.POST.get('Method_of_calc', False)

        #leadger Rounding
        ledger_idd=request.POST.get('useadvc', False)
        Rounding_Methodd=request.POST.get('Rounding_Method', False)
        Round_limitt =request.POST.get('Round_limit', False)

        #ledger_tax 
        type_of_duty_or_taxx=request.POST.get('type_of_duty_or_tax', False)
        type_of_taxx=request.POST.get('type_of_tax', False)
        valuation_typee=request.POST.get('valuation_type', False)
        rate_per_unitt=request.POST.get('rate_per_unit', False)
        Persentage_of_calculationn=request.POST.get('Persentage_of_calculation', False)

        #sundry
        maintain_balance_bill_by_billl=request.POST.get('maintain_balance_bill_by_bill', False)
        Default_credit_periodd=request.POST.get('Default_credit_period', False)
        Check_for_credit_dayss=request.POST.get('Check_for_credit_days', False)

        if Ledger.objects.filter(ledger_name = Lname ).exists():
                messages.info(request,'This Name is already taken...!')
                return redirect('load_create_ledger.html')

        Lmdl = Ledger(
            ledger_name=Lname,
            ledger_alias=Lalias,
            group_under=Lunder,
            ledger_cr_db=cd_db,
            ledger_opening_bal=Lopening_bal,
            ledger_type=typ_of_ledg,
            provide_banking_details=provide_banking,
        )
        Lmdl.save()
        idd = Lmdl
        Bmdl = Ledger_Banking_Details(
        
            ledger_id=idd,
            od_limit=B_od_limit,
            holder_name=B_ac_holder_name,
            ac_number=B_ac_no,
            ifsc=B_ifsc,
            swift_code=B_swift_code,
            bank_name=B_name,
            branch_name=B_branch,
            alter_chk_bks=B_alter_chq_bks,
            enbl_chk_printing=B_name_enbl_chq_prtg,

        )
        Bmdl.save()
        M_mdl = Ledger_Mailing_Address(

            name=Mname,
            address=Maddress,
            state=Mstate,
            country=Mcountry,
            pincode=Mpincode,
        )
        M_mdl.save()
        T_mdl = Ledger_Tax_Register(
           
          
            gst_uin=Tgst_uin,
            register_type=Treg_typ,
            pan_no=Tpan_no,
            alter_gst_details=T_alter_gst,

        )
        T_mdl.save()
        LS_mdl = Ledger_Satutory(

            ledger_id=idd,
            assessable_calculation=assessable_calculationn,
            Appropriate_to =Appropriate_too ,
            gst_applicable=gst_applicablee,
            Set_alter_GST = Set_alter_GSTT,
            type_of_supply=type_of_supplyy,
            Method_of_calc = Method_of_calcc,


        )
        LS_mdl.save()

        rnd_mdl = Ledger_Rounding(
            ledger_id=idd,
            Rounding_Method=Rounding_Methodd,
            Round_limit =Round_limitt,

        )
        rnd_mdl.save()

        tax_mdl = ledger_tax(
            ledger_id=idd,
            type_of_duty_or_tax=type_of_duty_or_taxx,
            type_of_tax =type_of_taxx,
            valuation_type=valuation_typee,
            rate_per_unit=rate_per_unitt,
            Persentage_of_calculation=Persentage_of_calculationn,
        )
        tax_mdl.save()

        sndry_mdl = Ledger_sundry(
            ledger_id=idd,
            maintain_balance_bill_by_bill=maintain_balance_bill_by_billl,
            Default_credit_period=Default_credit_periodd,
            Check_for_credit_days =Check_for_credit_dayss,
        )
        sndry_mdl.save()
        # messages.info(request,'LEDGER CREATED SUCCESSFULLY')
        return redirect('ledger')



