from django.contrib import admin
from django.http import HttpResponse,FileResponse


from .models import Order, Item, Transcation, OffCode, RefrallRequest
from pathlib import Path

import os
import csv
import openpyxl

def extract_exel(model_admin, request, queryset):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "orders"
    columns = ["شماره سفارش", "قیمت", "شماره خریدار", "تاریخ"]
    ws.append(columns)

    for order in queryset:
        order.date_created.replace(tzinfo=None)
        column = [order.pk, order.get_total_price(), order.buyer.phone,"1404" ]
        ws.append(column)
    respone =  HttpResponse( content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    respone["Content-Disposition"] = f"attachment; filename=output.xlsx"
    wb.save(respone)
    return respone
extract_exel.short_description = "خروجی گیری به صورت اکسل"

def extractCSV(model_admin , request, queryset):
    response = HttpResponse()
    writer = csv.writer(response)
    row = ["خریدار", "قیمت کل" , "تاریخ"]
    writer.writerow(row)
    for order in queryset:
        row = [order.buyer.phone, order.total_price, order.date_created.strftime("%Y/%m/%d")]
        writer.writerow(row)
    response["Content-Type"] ='text/csv'
    response["Content-Disposition"] = "attachment; filename=output.csv"
    return response

    


class ItemInLine(admin.TabularInline):
    model = Item
    fields = ["product", "price", "weight", "quantity", "color"]
    readonly_fields = ["color"]
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    model = Order
    actions = [extract_exel, extractCSV]
    raw_id_fields = ["buyer", "seller"]
    list_display = ["id", "buyer", "fname", "total_price", "post_type", "lname", "seller", "phone",
                    "date_created", "date_updated",  "is_rejected"]
    search_fields = ["seller__phone", "buyer__phone",
                     "phone", "fname", "lname", "phone"]
    list_editable = ["is_rejected"]
    list_filter = ["date_created", "date_updated", "buyer", "seller", ]
    inlines = [ItemInLine]
    exclude = ["color"]
    

class TranscationAdmin(admin.ModelAdmin):
    model = Transcation
    list_display = ["reciever", "sender", "date_teked_place", "price"]
    search_fields = ["reciever__phone", "sender__phone"]


class OffCodeAdmin(admin.ModelAdmin):
    model = OffCode
    readonly_fields = ["orders"]
    filter_horizontal = ["users",]

class RefrallReqeustsAdmin(admin.ModelAdmin):
    model = RefrallRequest
    raw_id_fields = ["user", "item"]
    search_fields =["user__phone", "item__name"]
    list_filter = ["is_accepted", "date_created"]
    list_display = ["user", "item", "is_accepted", "date_created"]
    list_editable = ["is_accepted"]    



admin.site.register(RefrallRequest, RefrallReqeustsAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Transcation, TranscationAdmin)
admin.site.register(OffCode, OffCodeAdmin)
