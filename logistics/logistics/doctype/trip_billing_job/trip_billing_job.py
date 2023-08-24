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
        self.uom = "Nos"
        
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
            self.halting_charges = 0
            self.cumulative_toll_charges = 0
            self.cumulative_loading_unloading_charges = 0
            self.cumulative_toll_charges = self.get_toll_charges(vehicle)
            self.bill_vehicle(vehicle)
        # print(self.items)
        sales_order = self.new_sales_order(self.items)
        if sales_order:
            sales_order.insert()
            sales_order_name = sales_order.name
            items = self.get_items_from_sales_order(sales_order_name)
            tripsandsales = self.sales_order_and_tripsheets_table(items, sales_order_name)
            self.tripsandsalesitem_insert(tripsandsales)
            self.clear_trip_id_in_items(sales_order_name,items)
        else:
            frappe.throw("Sales Order is Empty")
                    
            
    def get_trip_id(self,given_trips): 
        trips=""       
        for every_trip in given_trips:
            if every_trip == given_trips[-1]:
                trips += str(every_trip.name)
                print(every_trip)
            else:
                trips += str(every_trip.name)+","
        return trips

    
    
    def sales_order_and_tripsheets_table(self, items, sales_order_name):
        item_trip_id=[]
        list_of_items=[]
        item_trip_id.clear()
        count = 0
        for every_item in items:
            print("trip_ids in every_item", every_item.trip_id)
            item_trips = every_item.trip_id
            item_trip_id = item_trips.split(",")
            for each_trip in item_trip_id:
                if each_trip != "0":
                    tripsheet = frappe.get_doc("Tripsheets", each_trip)
                    tripitems = ({                      "title": sales_order_name,
                                                        "sales_order_item_name": every_item.name,
                                                        # "running_km": tripsheet.running_km, to do work on running km being the same as the running km in the sales order item 
                                                        "trip_name": each_trip,
                                                        "item_code": every_item.item_code})
                    list_of_items.append(tripitems)
        return(list_of_items)
                    
                    
    def tripsandsalesitem_insert(self, list_of_items):
                    order_trip_id = frappe.get_doc({ "doctype":"Trips and Sales Item",
                                                    "link_sales_order_item_and_tripsheet": list_of_items
                                                    })
                    order_trip_id.insert()
                
                
    def clear_trip_id_in_items(self, sales_order_name, items):
            sales_order = frappe.get_doc("Sales Order", sales_order_name)
            sales_order_items = sales_order.items
            for every_sales_order_items in sales_order_items:
                every_sales_order_items.trip_id = ""
            sales_order.save()
            
            
    def get_items_from_sales_order(self,sales_order_id):
        sales_order = frappe.get_doc("Sales Order", sales_order_id)
        if sales_order and sales_order.items:
            return sales_order.items
        else:
            return None
        
        
    def get_price(self):
        item_code = "TRANSPORT CHARGES - MONTHLY"
        item_price_list =[]
        
        item_prices = frappe.db.get_list("Item Price",
                    filters={
                    "customer": self.customer,
                    "price_list" : "Standard Selling",
                    "item_code" : item_code ,
                    "valid_from" : ["<=", self.bill_from_date]
                    #"valid_upto" : ["<=", self.bill_to_date]
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
        vehicles = frappe.db.get_list('Tripsheets',
            filters={
                'customer': ['=', self.customer],
                'price_list':["=", "Standard Selling"], 
                #'location' : ['=', self.item_name],
                "load_date" : ['between',[self.bill_from_date,self.bill_to_date]]
                # 'truck_no':  ['=', self.truck_no]
            },
            fields=['distinct truck_no as truck_no',"original_truck_no","ref_no","load_date"],
            group_by='truck_no')
        if vehicles:
            return vehicles
        else:
            return None
    
    
    def bill_vehicle(self, vehicle):
        excess_trips, cumulative_km = self.get_assorted_trips(vehicle)
        print("Vehicle_Truck_no", vehicle.truck_no)
        print("Cumulative_Km", cumulative_km)
        print("Cumulatice_Toll_Charges", self.cumulative_toll_charges)
        print("Cumulative_Loading_Unloading_Charges", self.cumulative_loading_unloading_charges)
        cost_center = (f'{vehicle.truck_no} - DL')

        if excess_trips:
            trips = self.get_trip_id(excess_trips)
            excess_routes = list(map(lambda t:t.location, excess_trips))
            for excess_route in set(excess_routes):
                print("Route", excess_route)
                print("QTY", excess_routes.count(excess_route))
                item = "TRANSPORT CHARGES - TRIPS"
                self.uom = "Trip"
                hsn_code = self.get_hsn_code(item)
                # print(excess_route)
                self.add_item_auto_price(excess_route, item, vehicle.truck_no, excess_routes.count(excess_route),cost_center, hsn_code,self.uom,trips)
        if self.cumulative_toll_charges > 0:
            item = "TOLL_CHARGES"
            hsn_code = self.get_hsn_code(item)
            self.add_item(item, item, vehicle.truck_no, 1, self.cumulative_toll_charges,cost_center,hsn_code,self.uom,0)
        if self.halting_charges > 0:
            item = "HALTING_CHARGE"
            hsn_code = self.get_hsn_code(item)
            self.add_item(item, item, vehicle.truck_no, 1, self.halting_charges,cost_center,hsn_code,self.uom,0)
        # if self.customer == "UNITECH PLASTO COMPONANTS PVT LTD":
        #     self.add_item_auto_price("MONTHLY_FOOD_CHARGES", "MONTHLY_FOOD_CHARGES", "Monthly Food Charges"+" "+vehicle.truck_no ,len(self.original_truck_no))
        if self.cumulative_loading_unloading_charges > 0:
            item = "LOADING/UNLOADING_CHARGES"
            hsn_code = self.get_hsn_code(item)
            self.add_item_auto_price("LOADING/UNLOADING_CHARGES","LOADING/UNLOADING_CHARGES", "loading and unloading charge for the vehicle", 1 ,cost_center,hsn_code,self.uom,0)
        
        print("***************************************************Next vehicle********************************************")
    
    def get_assorted_trips(self, vehicle): 
        trips = self.get_trips(vehicle)
        if trips == None:
            frappe.throw("Tripsheet Not Found")  
        cumulative_km = 0
        excess_trips = []

        for trip in trips:
            if trips == None:
                frappe.throw("Trips Not Found")
                
            self.trip_count += 1
            if trip.halting_charges == None:
                trip.halting_charges = 0
            self.halting_charges += int(trip.halting_charges)
            # print(self.trip_count)
            self.cumulative_loading_unloading_charges = self.get_loading_charges(trip)
            cumulative_km += trip.running_km
            # print("+", trip.truck_no, trip.load_date, trip.location, trip.running_km, cumulative_km)
            excess_trips.append(trip)
        return excess_trips, cumulative_km
    
    def get_total_kms(self, cumulative_km, trip):
        trip_km =  int(trip.closing_km) - int(trip.starting_km)
        self.cumulative_km += trip_km
        # print("cumulative_km: ", self.cumulative_km)
        return self.cumulative_km , self.cumulative_toll_charges
    
    
    def get_trip_id(self,given_trips): 
        trips=""       
        for every_trip in given_trips:
            if every_trip == given_trips[-1]:
                trips += str(every_trip.name)
                print(every_trip)
            else:
                trips += str(every_trip.name)+","
        return trips
    
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
        
    def get_hsn_code(self,item):
        hsn_code = frappe.db.get_list('Item',
                                      filters={
                                          "item_code": item,
                                      }, fields=['hsn_sac'])
        if hsn_code:
            return hsn_code[0].hsn_sac
        else:
            return None
    
    def get_loading_charges(self, trip):
        if (trip.loading_charges == None):
            trip.loading_charges = 0
        self.cumulative_loading_unloading_charges += trip.loading_charges
        return self.cumulative_loading_unloading_charges


    def get_trips(self, vehicle):
        trips = frappe.db.get_list('Tripsheets',
            filters={
                'customer': ['=', self.customer],
                'price_list': ['=', "Standard Selling"],
                # 'route_name' : ['=', self.item_name],
                'truck_no' : ['=', vehicle.truck_no],
                "load_date" : ['between',[self.bill_from_date,self.bill_to_date]]
            },
            fields=["name", 'price_list', 'load_date', 'truck_no', 'location', 'starting_km', 'closing_km', 'running_km', 'bill_type', 'lr_no', 'halt_days', 'pod_rec_date', 'driver', 'halting_charges'],
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
    def add_item(self, code, name, description, qty, rate, cost_center,hsn_code,uom,trip_id):
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
            "cost_center": cost_center,
            "hsn_sac": hsn_code,
            "uom": uom,
            "trip_id": trip_id
        })    
    def add_item_auto_price(self, code, name, description, qty, cost_center,hsn_code,uom,trip_id):
        # description_of_vehicle = description
        self.items.append({
            "item_code": code,
            "item_name": name,
            "delivery_date": "2023-07-15",
            "description": description,
            "qty": qty,
            "doc_type": "Sales Order Item",
            "cost_center": cost_center,
            "hsn_sac": hsn_code,
            "uom": uom,
            "trip_id": trip_id
        })            