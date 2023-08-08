# Copyright (c) 2023, techfinite and contributors
# For license information, please see license.txt
from frappe.model.document import Document
from datetime import date
import frappe

class TripBillingJob(Document):
    def init(self):
        self.today = date.today() 
        self.cumulative_toll_charges = 0
        self.items = []
        self.items.clear()
        self.billing_vehicle = None
        self.cumulative_km = 0
        self.trip_count  = 0
        self.item_price = None
        
        
    def validate(self):
        # ToDo add validations
        self.init()
        self.bill()

    def bill(self):
        
        vehicles = self.get_vehicles()
        if vehicles == None:
            frappe.throw("Vehicle Details Not Found")
        for vehicle in vehicles:
            if vehicle.truck_no == None:
                frappe.throw("Truck No not found on Tripsheet"+" "+vehicle.ref_no)
            self.cumulative_toll_charges = 0
            self.halting_charges = 0
            self.halt_days = 0
            self.cumulative_loading_unloading_charges = 0
            self.cumulative_toll_charges = self.get_toll_charges(vehicle)
            self.bill_vehicle(vehicle)
        # print(self.items)
        sales_order = self.new_sales_order(self.items)
        if sales_order:
            sales_order.insert()
        else:
            frappe.throw("Sales Order is Empty")

    def get_price(self):
        item_code = "TRANSPORT CHARGES - MONTHLY"
        item_price_list =[]
        
        item_prices = frappe.db.get_list("Item Price",
                    filters={
                    "customer": self.customer,
                    "price_list" : "Standard Selling",
                    "item_code" : item_code ,
                    "valid_from" : ["<=", self.bill_from_date]
                    #"valid_upto" : [">=", self.bill_to_date]
                    },
                    fields=['packing_unit', 'price_list_rate','valid_upto', 'excess_billing_type',"km_limit"])
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
        vehicles_with_date=[]
        vehicles = frappe.db.get_list('Tripsheets',
            filters={
                'customer': ['=', self.customer],
                'price_list':["=", "Standard Selling"], 
                #'location' : ['=', self.item_name],
                # 'load_date': ['>=', self.bill_from_date],
                # 'load_date': ['<=', self.bill_to_date]
                # 'truck_no':  ['=', self.truck_no]
            },
            fields=['distinct truck_no as truck_no',"original_truck_no","ref_no", "load_date",],
            group_by='truck_no')
        # for every_vehicle in vehicles:
        #     if str(every_vehicle.load_date) <= self.bill_to_date:
        #         vehicles_with_date.append(every_vehicle)
        if vehicles:
            return vehicles
        else:
            return None
    
    
    def bill_vehicle(self, vehicle):
        excess_trips, cumulative_km, self.halting_charges, halt_days = self.get_assorted_trips(vehicle)
        print("Vehicle_Truck_no", vehicle.truck_no)
        print("Cumulative_Km", cumulative_km)
        print("Cumulatice_Toll_Charges", self.cumulative_toll_charges)
        print("Cumulative_Loading_Unloading_Charges", self.cumulative_loading_unloading_charges)
        cost_center = (f'{vehicle.truck_no} - DL ')


        if excess_trips:
            excess_routes = list(map(lambda t:t.location, excess_trips))
            for excess_route in set(excess_routes):
                print("Route", excess_route)
                print("QTY", excess_routes.count(excess_route))
                item = "TRANSPORT CHARGES - TRIPS"
                # print(excess_route)
                self.add_item_auto_price(excess_route, item, vehicle.truck_no, excess_routes.count(excess_route),cost_center)
        if self.cumulative_toll_charges > 0:
            self.add_item("TOLL_CHARGES", "TOLL_CHARGES", vehicle.truck_no, 1, self.cumulative_toll_charges,cost_center)
        if self.halting_charges > 0 :
            self.add_item("HALTING_CHARGE", "HALTING_CHARGE", vehicle.truck_no,halt_days, self.halting_charges, cost_center )
        # if self.customer == "UNITECH PLASTO COMPONANTS PVT LTD":
        #     self.add_item_auto_price("MONTHLY_FOOD_CHARGES", "MONTHLY_FOOD_CHARGES", "Monthly Food Charges"+" "+vehicle.truck_no ,len(self.original_truck_no))
        if self.cumulative_loading_unloading_charges > 0:
            self.add_item_auto_price("LOADING/UNLOADING_CHARGES","LOADING/UNLOADING_CHARGES", "loading and unloading charge for the vehicle", 1 ,cost_center)
        
        print("***************************************************Next vehicle********************************************")
    
    def get_assorted_trips(self, vehicle): 
        trips_with_date = self.get_trips(vehicle)
        
        cumulative_km = 0
        excess_trips = []
        excess_trips.clear()

        for trip in trips_with_date:
            if trip == None:
                frappe.throw("Trips Not Found")
            self.trip_count += 1
            # print(self.trip_count)
            self.cumulative_loading_unloading_charges = self.get_loading_charges(trip)
            cumulative_km += trip.running_km
            # print("+", trip.truck_no, trip.load_date, trip.location, trip.running_km, cumulative_km)
            excess_trips.append(trip)
            if trip.halt_days > 0:
                self.halting_charges = int(trip.halting_charges)
                self.halt_days += trip.halt_days
        return excess_trips, cumulative_km, self.halting_charges, self.halt_days
    
    def get_total_kms(self, cumulative_km, trip):
        trip_km =  int(trip.closing_km) - int(trip.starting_km)
        self.cumulative_km += trip_km
        # print("cumulative_km: ", self.cumulative_km)
        return self.cumulative_km , self.cumulative_toll_charges
    
    def get_toll_charges(self, vehicle):
        toll_charges_with_date =[]
        if vehicle.original_truck_no == None:
            vehicle.original_truck_no = vehicle.truck_no
        tollcharges = frappe.db.get_list("Toll Charge", filters={
            "truck_no": vehicle.original_truck_no,
            "customer" : self.customer
        },fields=["amount","transaction_date_time"])
        if tollcharges:
            for every_toll_charge in tollcharges:
                test = str(every_toll_charge.transaction_date_time).split(" ")[0]
                if str(every_toll_charge.transaction_date_time).split(" ")[0] >= self.bill_from_date and str(every_toll_charge.transaction_date_time).split(" ")[0] <= self.bill_to_date :
                    toll_charges_with_date.append(every_toll_charge.amount)
        if toll_charges_with_date:
            for every_toll_charges_with_date in toll_charges_with_date:
                self.cumulative_toll_charges += int(every_toll_charges_with_date)
            return self.cumulative_toll_charges
        else:
            self.cumulative_toll_charges = 0
            return self.cumulative_toll_charges
    
    def get_loading_charges(self, trip):
        if (trip.loading_charges == None):
            trip.loading_charges = 0
        self.cumulative_loading_unloading_charges += trip.loading_charges
        return self.cumulative_loading_unloading_charges

    def get_trips(self, vehicle):
        trips_with_date =[]
        trips = frappe.db.get_list('Tripsheets',
            filters={
                'customer': ['=', self.customer],
                'price_list': ['=', "Standard Selling"],
                # 'route_name' : ['=', self.item_name],
                'truck_no' : ['=', vehicle.truck_no],
                'load_date': ['>=', self.bill_from_date]
            },
            fields=['price_list', 'load_date', 'truck_no', 'location', 'starting_km', 'closing_km', 'running_km', 'bill_type', 'lr_no', 'halt_days', 'pod_rec_date', 'driver',"halting_charges", "ref_no" ],
            order_by ='ref_no asc')
        # print("trips_value", trips)
        for every_trip in trips:
            if str(every_trip.load_date) <= self.bill_to_date:
                trips_with_date.append(every_trip)
       
        if trips_with_date: 
            return trips_with_date
    
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
    def add_item(self, code, name, description, qty, rate, cost_center):
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
            "doc_type": "Sales Order Item",
            "cost_center": cost_center
        })    
    def add_item_auto_price(self, code, name, description, qty, cost_center):
        # description_of_vehicle = description
        self.items.append({
            "item_code": code,
            "item_name": name,
            "delivery_date": "2023-07-15",
            "description": description,
            "qty": qty,
            "doc_type": "Sales Order Item",
            "cost_center": cost_center
        })            


