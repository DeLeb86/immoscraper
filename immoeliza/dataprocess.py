from scrapy.item import Item
from scrapy import Field
import json,re


#mapping={
#    "PropertyId": lambda x :x["id"],
#    "TypeOfProperty":lambda x : 1 if x["property"]["type"].lower().strip()=="house" else 2,
#    "SubtypeOfProperty":lambda x : x["property"]["subtype"].lower().strip(),
#    "PostalCode": lambda x : int(str(x["property"]["location"]["postalCode"].strip().lower())) \
#        if str(x["property"]["location"]["postalCode"].strip().lower()).isdigit() else None,
#    "TypeOfSale": lambda x: x["price"]["type"] if "price" in x else None,
#    "Price": lambda x : int(x["price"]["mainValue"]) if x["price"] in x else None,
#    "MonthlyCharges":lambda x:int(x["price"]["additionalValue"]) if "price" in x and x["price"]["additionalValue"] is not None else None,
#    "Kitchen": lambda x : x["type"].strip().lower() if len(x["type"].strip())>0 else None},
#    "building" : {"StateOfBuilding": lambda x : x["condition"].strip().lower() if len(x["condition"].strip())>1 else None},
#    "energy" : {"Heating": lambda x : x["heatingType"].strip().lower() if len(x["heatingType"].strip())>0 else None},
#    "bedroom" : {"Bedrooms": lambda x : int(x["count"].strip()) if str(x["count"].strip()).isdigit() else None},
#    "land": {"SurfaceOfGood": lambda x : float(x) if  str(x).replace(".","").isdigit() else None},
#    "outdoor" : {"Terrace" : lambda x : "exists" in x["terrace"] and "true" in str(x["terrace"]["exists"].strip())},
#    "wellnessEquipment": {"SwimmingPool": lambda x : ("true" in x["hasSwimmingPool"] or "yes" in x["hasSwimmingPool"])},
#    "land" : {"SurfaceOfGood" : lambda x : float(x["surface"]) if  str(x["surface"]).replace(".","").isdigit() else None }
#}


class ImmoItem(Item):
    """
    Item object that represent a real estate property
    it defines all the interesting information we want to keep from the website for the real estate properties

    Args:
        Item: Scrapy default item type
    """
    js=Field()
    #html_elems=Field()
    Url=Field()
    PostalCode=Field()
    Country=Field()
    Locality = Field()
    Region=Field()
    Province=Field()
    District=Field()
    PropertyId  = Field()
    Price=Field()
    MonthlyCharges = Field()
    TypeOfProperty=Field()
    SubtypeOfProperty=Field()
    TypeOfSale=Field()
    BedroomCount=Field()
    BathroomCount=Field()
    ShowerCount=Field()
    ToiletCount=Field()
    RoomCount=Field()
    LivingArea=Field()
    SurfaceOfPlot=Field()
    Terrace=Field()
    Garden=Field()
    GardenArea=Field()
    Kitchen=Field()
    Fireplace=Field()
    NumberOfFacades=Field()
    StateOfBuilding=Field()
    ConstructionYear=Field()
    FloodingZone = Field()
    SwimmingPool=Field()
    Heating=Field()
    Furnished=Field()
    PEB = Field()
    
    
    
    
    def init_all(self,value=None):
        for k, v in self.fields.items():
            self[k]=value
            
    
    def transform(self):
        """
            Update the object with the values that are in the js and html
        """
        for field in self.fields:
            self.setdefault(field,None)
        data=self["js"]
        
        self["PropertyId"]=data["id"]
        self["TypeOfProperty"]=1 if data["property"]["type"].lower().strip()=="house" else 2
        self["SubtypeOfProperty"]=data["property"]["subtype"].lower().strip() \
            if data["property"] is not None else None
        if "price" in data :
            self["TypeOfSale"]=data["price"]["type"]
            self["Price"] = int(data["price"]["mainValue"]) if "mainValue" in data["price"] and data["price"]["mainValue"] is not None else None
            self["MonthlyCharges"] = int(data["price"]["additionalValue"]) \
                if "additionalValue" in data["price"] and data["price"]["additionalValue"] is not None else None 
            
        if "property" in data:
            if "location" in data["property"]:
                self["PostalCode"]=int(str(data["property"]["location"]["postalCode"].strip().lower())) \
                    if str(data["property"]["location"]["postalCode"].strip().lower()).isdigit() else None
                self["Locality"]=data["property"]["location"]["locality"]
                self["Country"]=data["property"]["location"]["country"]
                self["Region"]=data["property"]["location"]["region"]
                self["Province"]=data["property"]["location"]["province"]
                self["District"]=data["property"]["location"]["district"]
        
            if "energy" in data["property"]:
                if "heatingType" in data["property"]["energy"]: self["Heating"]=data["property"]["energy"]["heatingType"]
                if "hasHeatingPump" in data["property"]["energy"] and data["property"]["energy"]["hasHeatingPump"] == True : self["Heating"]="HeatingPump"
            if "kitchen" in data["property"].keys() and data["property"]["kitchen"] is not None:
                self["Kitchen"] = data["property"]["kitchen"]["type"]
            
            if "netHabitableSurface" in data["property"] : 
                self["LivingArea"]=data["property"]["netHabitableSurface"]
            if "hasTerrace" in data["property"]: self["Terrace"]=data["property"]["hasTerrace"]
            if "hasGarden" in data["property"] : self["Garden"]=data["property"]["hasGarden"]
            if "gardenSurface" in data["property"] : self["GardenArea"]=data["property"]["gardenSurface"]
            if "bedroomCount" in data["property"] : self["BedroomCount"]=data["property"]["bedroomCount"]
            if "roomCount" in data["property"] : self["RoomCount"]=data["property"]["roomCount"]
            if "bathroomCount" in data["property"] : self["BathroomCount"]=data["property"]["bathroomCount"]   
            if "showerRoomCount" in data["property"] : self["ShowerCount"]=data["property"]["showerRoomCount"]   
            if "toiletCount" in data["property"] : self["ToiletCount"]=data["property"]["toiletCount"]   
            if "fireplaceCount" in data["property"] : self["Fireplace"]=True if data["property"]["fireplaceCount"] is not None and  data["property"]["fireplaceCount"]>0 else None
            if "constructionPermit" in data["property"] : self["FloodingZone"]=data["property"]["constructionPermit"]["floodZoneType"]
            if "building" in data["property"] and data["property"]["building"]: 
                self["NumberOfFacades"] = data["property"]["building"]["facadeCount"] 
                self["StateOfBuilding"] = data["property"]["building"]["condition"]
                self["ConstructionYear"] = data["property"]["building"]["constructionYear"]
        
            if "land" in data["property"] and data["property"]["land"] is not None : self["SurfaceOfPlot"]=data["property"]["land"]["surface"] if data["property"]["land"]["surface"] is not None else None
            if "hasSwimmingPool" in data["property"] : self["SwimmingPool"]=data["property"]["hasSwimmingPool"]
        if "transaction" in data:
            if "certificates" in data["transaction"] and data["transaction"]["certificates"] is not None:
                self["PEB"]=data["transaction"]["certificates"]["epcScore"] if "epcScore" in data["transaction"]["certificates"] else None
            if "sale" in data["transaction"] and data["transaction"]["sale"] is not None :
                self["Furnished"]=data["transaction"]["sale"]["isFurnished"]
                
        
        
        
                    