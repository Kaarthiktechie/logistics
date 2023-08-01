# Copyright (c) 2023, techfinite and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date

class BillingJob(Document):
    def init(self):
        self.today = date.today()
        self.diesel_rate = 90 
        self.cumulative_toll_charges = 0
        self.items = []
        self.items.clear()
        self.billing_vehicle = None
        self.cumulative_km = 0
        self.item_price = None
        self.cumulative_loading_unloading_charges = 0
        # # Todo Remove these lines after updating the field names in doctype
        # self.customer_id = None
        # self.route_name = None
        # self.price_list_name = None
        # self.bill_from_date = None
        # self.bill_to_date = None
        # self.price_list = None

    def validate(self):
        # ToDo add validations
        self.init()
        self.bill()

    def bill(self):
        self.item_price = self.get_price()
        if self.item_price == None:
            frappe.throw("Pricing Details Not Found")
        print("* Item Price : ", self.item_price.packing_unit, self.item_price.price_list_rate, self.item_price.excess_billing_type)
        vehicles = self.get_vehicles()
        for vehicle in vehicles:
            self.cumulative_toll_charges = 0
            self.cumulative_loading_unloading_charges = 0
            self.bill_vehicle(vehicle)
        print(self.items)
        sales_order = self.new_sales_order(self.items)
        sales_order.insert()

    def get_price(self):
        item_code = "TRANSPORT CHARGES - MONTHLY"
        item_prices = frappe.db.get_list("Item Price",
                    filters={
                    "customer": self.customer,
                    "price_list" : self.price_list,
                    "item_code" : item_code #,
                    #"valid_from" : ["<=", self.bill_from_date],
                    #"valid_upto" : [">=", self.bill_to_date]
                    },
                    fields=['packing_unit', 'price_list_rate', 'excess_billing_type',"km_limit"])
        if item_prices :
            return item_prices[0]
        return None

    def get_vehicles(self):
        vehicles = frappe.db.get_list('Tripsheets',
            filters={
                'customer': ['=', self.customer],
                'price_list':["=", self.price_list], 
                #'location' : ['=', self.item_name],
                'load_date': ['>=', self.bill_from_date],
                'load_date': ['<=', self.bill_to_date]
                # 'truck_no':  ['=', self.truck_no]
            },
            fields=['distinct truck_no as truck_no'],
            group_by='truck_no')
        return vehicles
    
    # def mileage(self, truck_size):
    #     r = frappe.db.get_value("Mileage", filters = { 
    #         "truck_size": truck_size # have to check weather the truck no is matched withth the truck to bring the mileage amount
    #     },fields=["mileage"])
    #     # print("Tehfuhsdkhfbjsdkfh", vehicle_details.mileage)
    #     return r.mileage
    
    # def rd_brown(self):
    #     diesel_rate = 50
    #     vehicles = self.get_vehicles(self.route)
    #     for vehicle in vehicles():
    #         mileage = self.mileage(trip.truck_no) #if said the value will be billingtruck no then have to change the value
    #         trips = self.get_trips(self.route, vehicle)
    #         for trip in trips():
    #             cumulative_km, cumulative_toll_charges = self.get_total_kms(self, trip)
    #             self.add_item(2, "TRANSPORT CHARGES - KM", vehicle.truck_no, cumulative_km, diesel_rate)
    #         if cumulative_toll_charges > 0:
    #             self.add_item(4, "Toll_charges", "Total toll_charges", 1, cumulative_toll_charges)   

    def bill_vehicle(self, vehicle):
        on_contract_trips, excess_trips, crossover_excess_km = self.get_assorted_trips(vehicle)

        if on_contract_trips:
            item = "TRANSPORT CHARGES - MONTHLY"
            self.add_item(item, item, vehicle.truck_no, 1,self.item_price.price_list_rate)
            # print (item)
            #print("vehicle.truck_no : ",  vehicle.truck_no)
        if crossover_excess_km > 0:
            item = "TRANSPORT CHARGES - KM"
            self.add_item_auto_price(item, item, vehicle.truck_no, crossover_excess_km)
            # print("crossover_excess_km : ", crossover_excess_km)
        if excess_trips:
            excess_km = 0
            if(self.item_price.excess_billing_type == "Per-Km"):
                for excess_trip in excess_trips:
                    excess_km += excess_trip.running_km
                item = "TRANSPORT CHARGES - KM"
                self.add_item_auto_price(item, item, vehicle.truck_no, excess_km)
            else:
                excess_routes = list(map(lambda t:t.location, excess_trips))
                for excess_route in set(excess_routes):
                    item = "TRANSPORT CHARGES - TRIPS"
                    print(excess_route)
                    self.add_item_auto_price(excess_route, item, vehicle.truck_no, excess_routes.count(excess_route))
        
        if self.cumulative_toll_charges > 0:
           self.add_item(4, "TOLL_CHARGES", "Total toll_charges", 1, self.cumulative_toll_charges)
        if self.customer == "UNITECH PLASTO COMPONANTS PVT LTD":
            self.add_item_auto_price("MONTHLY_FOOD_CHARGES", "MONTHLY_FOOD_CHARGES", "Monthly Food Charges For the Customer",1)
        if self.cumulative_loading_unloading_charges > 0:
            self.add_item_auto_price("LOADING/UNLOADING_CHARGES","LOADING/UNLOADING_CHARGES", "loading and unloading charge for the vehicle", 1 )
            # print("test _cumulative_toll_charges lhsdgig", cumulative_toll_charges)
    # def get_price(route_name, self, route):  # for the customer
        #return Prici_nameng("HITRO CH-HITRO-LOCAL", 27, 0, 108000, 2500)
        # return Price_list("HITRO CH-HITRO-LOCAL", 27, 1200, 140000, 4500)
    
    def get_assorted_trips(self, vehicle): #
        trips = self.get_trips(vehicle)  # date missing #data
        limit = self.item_price.km_limit
        cumulative_km = 0
        crossover_excess_km = 0
        on_contract_trips = []
        excess_trips = []

        for trip in trips:
            self.cumulative_toll_charges = self.get_toll_charges(trip)
            self.cumulative_loading_unloading_charges = self.get_loading_charges(trip)
            crossover_trip = None
            cumulative_km += trip.running_km
            print("+", trip.truck_no, trip.load_date, trip.location, trip.running_km, cumulative_km)

            if cumulative_km >= int(limit) and crossover_excess_km == 0:
                crossover_excess_km = cumulative_km - int(limit)
                crossover_trip = "Yes"
                print("crossover_excess_km : " , crossover_excess_km)

            if crossover_excess_km > 0 and crossover_trip == None:
                excess_trips.append(trip)
                continue
            else:
                on_contract_trips.append(trip)

        return on_contract_trips, excess_trips, crossover_excess_km
    
    def get_toll_charges(self, trip):
        # cumulative_km = 0
        if (trip.toll_charges == None):
            trip.toll_charges = 0
            # print(trip.closing_km)
            # print(trip.starting_km)
        # trip_km =  int(trip.closing_km) - int(trip.starting_km)
            # print(trip_km)
        # self.cumulative_km += trip_km
        self.cumulative_toll_charges += trip.toll_charges
            # print("-", trip.truck_no, trip.load_date, trip.location, cumulative_km)
        return self.cumulative_toll_charges
    
    def get_loading_charges(self, trip):
        if (trip.loading_charges == None):
            trip.loading_charges = 0
        self.cumulative_loading_unloading_charges += trip.loading_charges
        return self.cumulative_loading_unloading_charges

    def get_trips(self, vehicle):
        trips = frappe.db.get_list('Tripsheets',
            filters={
                'customer': ['=', self.customer],
                'price_list': ['=', self.price_list],
                # 'route_name' : ['=', self.item_name],
                'truck_no' : ['=', vehicle.truck_no],
                'load_date': ['>=', self.bill_from_date],
                'load_date': ['<=', self.bill_to_date]
            },
            fields=['price_list', 'load_date', 'truck_no', 'location', 'starting_km', 'closing_km', 'running_km', 'bill_type', 'lr_no', 'halt_days', 'pod_rec_date', 'driver', ],
            order_by = 'ref_no asc')
        # print("trips_value", trips)
       
        return trips
    
    #def get_vehicles(self, route): # get vehicles assigned for that route
    # vehicles = ["TN99BH0001"]
    # vehicles = ["TN25BC3954","TN28BE3920","TN28BE3935","TN28BE3954","TN28BH1032","TN28BH3373","TN28BH3540","TN28BH4531","TN28BH4702","TN28BJ0016","TN28BJ0180","TN28BJ5061"]
    # vehicles = ["TN28BE3920", "TN28BE3954", "TN28BH3540", "TN28BJ0016", "TN28BJ0167", "TN28J0180"]
    # return vehicles
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



