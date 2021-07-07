from sqlalchemy import *
from sqlalchemy.sql import *
engine=create_engine('mysql://root:divyasrd30501@@127.0.0.1:3306/hackathon',echo=True)

class First:
    def __init__(self):
        self.meta=MetaData()
        self.user=Table("user",self.meta,autoload=True,autoload_with=engine)
        self.therapist=Table("therapist",self.meta,autoload=True,autoload_with=engine)
        self.booking_details=Table("booking_details",self.meta,autoload=True,autoload_with=engine)


    def get_email_user(self,email):
        s=self.user.select().where(self.user.c.Email==email)
        res=engine.execute(s)
        results=[dict(r) for r in res] if res else None
        if results:
            return results[0]
        else:
            return None

    def get_email_therapist_login(self,email):
        s=self.therapist.select().where(self.therapist.c.Email==email)
        res=engine.execute(s)
        results=[dict(r) for r in res] if res else None
        if results:
            return results[0]
        else:
            return None

    def insert_info_user(self,data):
        res=engine.execute(self.user.insert(),data)
        if res:
            return res

    def get_info_therapist(self,Gender,Area,Mode):
        s=self.therapist.select().where(            
                and_(
                self.therapist.c.Gender==Gender,
                self.therapist.c.Area==Area,
                self.therapist.c.Mode==Mode,
                
                )           
        )
        res=engine.execute(s)
        results=[dict(r) for r in res] if res else None
        if results:                        
            return results
        else:
            return None


    def get_email_therapist(self,therapist_id):
        s=self.therapist.select().where(self.therapist.c.TherapistId==therapist_id)
        res=engine.execute(s)
        results=[dict(r) for r in res] if res else None
        if results:                        
            return results[0]
        else:
            return None 

    def get_info_user(self,userid):
        s=self.user.select().where(self.user.c.UserID==userid)
        res=engine.execute(s)
        results=[dict(r) for r in res] if res else None
        if results:                        
            return results[0]
        else:
            return None       

    def insert_booking_details(self,data):
        res=engine.execute(self.booking_details.insert(),data)
        if res:
            return res
        else:
            return None
    
    def get_booking_details(self,userid):
        s=self.booking_details.select().where(self.booking_details.c.UserID==userid)
        res=engine.execute(s)
        results=[dict(r) for r in res] if res else None
        if results:
            return results
        else:
            return None

    
    def get_therapist_appointment(self,therapistid):
        s=self.booking_details.select().where(self.booking_details.c.Therapist_id==therapistid)
        res=engine.execute(s)
        results=[dict(r) for r in res] if res else None
        if results:
            return results
        else:
            return None

    
    def get_therapist_appointment_frontline(self,therapistid,type):
        s=self.booking_details.select().where(            
                and_(
                self.booking_details.c.Therapist_id==therapistid,
                self.booking_details.c.Type==type
                )
        )
        res=engine.execute(s)
        results=[dict(r) for r in res] if res else None
        if results:
            return results
        else:
            return None


    def insert_info_therapist(self,areas,data):
        modes=['Video','Voice','Chat']
        for i in areas:
            for j in modes:
                res=engine.execute(self.therapist.insert(),data)
                stmt=self.therapist.update().where(self.therapist.c.Area.is_(None)).values(Area= i)
                engine.execute(stmt)
                stmt1=self.therapist.update().where(self.therapist.c.Mode.is_(None)).values(Mode = j)
                engine.execute(stmt1)        
        if res:
            return res

    def cancel_appointment(self,BookingID):
        s=self.booking_details.update().where(self.booking_details.c.BookingID==BookingID).values(Status="Cancelled")
        res=engine.execute(s)
        return res
    