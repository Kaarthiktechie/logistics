# Copyright (c) 2023, techfinite and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date

class RD_BrownBillingJob(Document):
    
    def init(self):
        self.today = date.today()
        self.diesel_rate = 90 
        self.cumulative_toll_charges = 0
        self.items = []
        self.items.clear()
        self.billing_vehicle = None
        self.cumulative_km = 0
        self.item_price = None
        self.rent_amount = 0
        self.cumulative_rent_amount = 0
        self.original_truck_no = []

    def validate(self):
        self.init()
        if self.customer:
            customer_list=[self.customer]
        else:
            customer_list = ["RD BROWN BOX PACKING PVT LTD-ORG",
                             "RD BROWN BOX PACKING PVT LTD-VYR",
                             "RD BROWN BOX PACKING PVT LTD-SPR"]
        for every_customer in customer_list:
            self.items.clear()
            self.customer = every_customer
            self.rd_brown()
    
    def get_price(self):
        item_code = "TRANSPORT CHARGES"
        item_price_list =[]
        item_prices = frappe.db.get_list("Item Price",
                    filters={
                    "customer": self.customer,
                    # "price_list" : self.price_list,
                    "item_code" : item_code ,
                    "valid_from" : ["<=", self.bill_from_date]
                    #"valid_upto" : [">=", self.bill_to_date]
                    },
                    fields=['packing_unit', 'price_list_rate'])
        for every_item_prices in item_prices:
            if every_item_prices.valid_upto == None:
                every_item_prices.valid_upto = 0
            if str(every_item_prices.valid_upto) >= self.bill_to_date or every_item_prices.valid_upto == 0:
                item_price_list.append(every_item_prices)
        if item_price_list:
            return item_price_list[0]
        else:
            return None

    def get_vehicles(self):
        vehicles = frappe.db.get_list('Tripsheets',
            filters={
                'customer': ['=', self.customer],
                # 'price_list':["=", self.price_list], 
                #'location' : ['=', self.item_name],
                'load_date': ['>=', self.bill_from_date],
                'load_date': ['<=', self.bill_to_date]
                # 'truck_no':  ['=', self.truck_no]
            },
            fields=['distinct truck_no as truck_no'],
            group_by='truck_no')
        return vehicles

    def vehicle_details(self, truck_size):
        mileage = frappe.db.get_list("Mileage", 
                                filters = { "truck_size": ['=', truck_size]},
                                fields=["mileage"])[0]
        # print("Tehfuhsdkhfbjsdkfh", vehicle_details.mileage)
        return mileage
    def vehicle_truck_size(self, truck_no):
        truck_size = None
        truck_size = frappe.db.get_list("Asset", 
                                        filters= {"asset_name": [ "=", truck_no]},
                                        fields = ["truck_size"])[0]
        return truck_size.truck_size

    def rd_brown(self):
        diesel_average_rate = self.get_diesel_average_rate()
        self.item_price = self.get_price()
        vehicles = self.get_vehicles()
        
        for vehicle in vehicles:
            self.original_truck_no.clear()
            cumulative_km = 0
            self.cumulative_rent_amount = 0
            print(vehicle.truck_no)
            truck_size = self.vehicle_truck_size(vehicle.truck_no)
            mileage = self.vehicle_details(truck_size)
            trips = self.get_trips(vehicle)
            
            for trip in trips:
                if trip.original_truck_no not in self.original_truck_no:
                    self.original_truck_no.append(trip.original_truck_no)
                cumulative_rent_amount = self.get_rent_amount(trip.total_freight)
                cumulative_km, cumulative_toll_charges = self.get_total_kms(cumulative_km, trip)
            total_amount_wihout_rental = ((cumulative_km/mileage.mileage)*diesel_average_rate)
            print(cumulative_rent_amount)
            total_amount_with_rental = total_amount_wihout_rental + cumulative_rent_amount
            original_truck_no_string = ""
            
            for every_truck_no in self.original_truck_no:
                if every_truck_no == self.original_truck_no[-1]:
                    original_truck_no_string += str(every_truck_no)
                else:
                    original_truck_no_string += str(every_truck_no)+","
            self.add_item("TRANSPORT CHARGES", "TRANSPORT CHARGES", vehicle.truck_no, 1,total_amount_with_rental)
            if cumulative_toll_charges > 0:
                self.add_item(4, "Toll_charges", "Total toll_charges", 1, cumulative_toll_charges)
        sales_order = self.new_sales_order(self.items)
        sales_order.insert()
    
    def get_rent_amount(self, rent_amount):
        self.cumulative_rent_amount += int(rent_amount)
        return self.cumulative_rent_amount

    def get_diesel_average_rate (self):
        i = 0
        cumulative_diesel_rate = 0
        total_diesel_rate = frappe.db.get_list(
            "Diesel Price", filters={
                'date': ['>=', self.bill_from_date],
                'date': ['<=', self.bill_to_date]
            }  , fields=["diesel_rate", "date"]                                 
        )
        
        for daily_diesel_rate in total_diesel_rate:
            cumulative_diesel_rate += daily_diesel_rate.diesel_rate
            i +=1
        diesel_average_rate = (cumulative_diesel_rate/i) 
        return diesel_average_rate
        

    def get_total_kms(self, cumulative_km, trip):
        trip_km =  int(trip.closing_km) - int(trip.starting_km)
        print(trip_km)
        cumulative_km += trip_km
        print("cumulative_km: ", cumulative_km)
        return cumulative_km , self.cumulative_toll_charges

    def get_trips(self, vehicle):
        trips = frappe.db.get_list('Tripsheets',
            filters={
                'customer': ['=', self.customer],
                # 'price_list': ['=', self.price_list],
                # 'route_name' : ['=', self.item_name],
                'truck_no' : ['=', vehicle.truck_no],
                'load_date': ['>=', self.bill_from_date],
                'load_date': ['<=', self.bill_to_date]
            },
            fields=['price_list', 'load_date','original_truck_no', 'truck_no',"total_freight",'total_freight', 'location', 'starting_km', 'closing_km', 'running_km', 'bill_type', 'lr_no', 'halt_days', 'pod_rec_date', 'driver', ],
            order_by ='ref_no asc')
        # print("trips_value", trips)

        return trips

    def new_sales_order(self, items):
        company = frappe.defaults.get_user_default("Company") # need to change
        sales_order = frappe.get_doc({
            "doctype": "Sales Order",
            "company": company,
            "customer": self.customer,
            "order_type": "Sales",
            "transaction_date": "2023-06-26",
            "due_date": "2023-07-26",
            "delivery_date": self.today,
            "status": "To Deliver and Bill",
            "naming_series": "SAL-ORD-.YYYY.-",
            "currency": "INR",
            "shipping_address": "No 4, Sengunthapuram",
            "billing_address": "No 4, Sengunthapuram",
            "items": items,
            "set_warehouse": "Stores - DL"
            # "selling_price_list": "Standard S"
        })
        return sales_order
    def add_item(self, code, name, description, qty, rate):
        # description_of_vehicle = description
        self.items.append({
            "item_code": code,
            "item_name": name,
            "delivery_date": "2023-07-15",
            "description": description,
            "uom": "Nos",
            "conversion_factor": "1",
            "qty": qty,
            "rate": rate,
            "doc_type": "Sales Order Item"
        })    
    def add_item_auto_price(self, code, name, description, qty):
        # description_of_vehicle = description
        self.items.append({
            "item_code": code,
            "item_name": name,
            "delivery_date": "2023-07-15",
            "description": description,
            "qty": qty,
            "doc_type": "Sales Order Item"
        })            
