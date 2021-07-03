from flask import *   
from flask_mail import *
from random import *
from model.model import First  
app = Flask(__name__) #creating the Flask class object  
app.secret_key="div"

app.config['MAIL_SERVER']='smtp.gmail.com'  
app.config['MAIL_PORT']=465  
app.config['MAIL_USERNAME'] = 'hackaholics4@gmail.com'  
app.config['MAIL_PASSWORD'] = 'DaggUs4#'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/',methods=["POST","GET"])
def Home():
    f=First()
    if request.method=="GET":
        return render_template('new_user_home.html')

@app.route('/user_home/<userid>',methods=["POST","GET"])
def User_home(userid):
    f=First()
    if request.method=="GET":
        return render_template('home.html',userid=userid)

@app.route('/login',methods=["POST","GET"])
def Login():
    f=First()
    if request.method=="GET":
        return render_template('login.html')
    if request.method=="POST":
        email=request.form["Email"]
        password=request.form["Password"]
        out=f.get_email_user(email)
        if out:
            if out['Password']==password:
                return render_template("home.html",name=out['User_name'],userid=out['UserID'])            
            else:
                flash("Password is wrong.Please enter correct password")
                return render_template("login.html",email=out['Email'])
        else:
            flash("Email you have entered has not been registered. Please register")
            return render_template("login.html")

@app.route('/logout')
def Logout():
    session.pop('User_name',None)
    return redirect(url_for('Home'))


@app.route('/register',methods=["POST","GET"])
def Register():
    f=First()
    if request.method=="GET":
        return render_template('register.html')
    if request.method=="POST":
            data={
                'User_name':request.form['User_name'],
                'Email':request.form['Email'],
                'Password':request.form['Password'],
            }
            out=f.insert_info_user(data)
            flash("You've been registered successfully!")
            return render_template("new_user_home.html")


@app.route('/find/<userid>',methods=["POST","GET"])
def Find(userid):
    f=First()
    if request.method=="GET":
        return render_template('booking.html',userid=userid)
    if request.method=="POST":
        Area=request.form['Area']
        Gender=request.form['Gender']
        Mode=request.form['Mode']
        
        
        out=f.get_info_therapist(Gender,Area,Mode)
        
        return render_template("booking.html",out=out,userid=userid)

@app.route('/booking_direct/<area>/<userid>',methods=["POST","GET"])
def Booking_direct(area,userid):
    f=First()
    if request.method=="GET":
        return render_template('booking.html',area=area,userid=userid)

@app.route('/booking_and_insert/<userid>/<therapist_id>',methods=["POST","GET"])
def Booking_and_insert(userid,therapist_id):
    f=First()
    if request.method=="GET":
        return render_template('new_booking.html',userid=userid,therapist_id=therapist_id)
    if request.method=="POST":
        data={
            
            'Therapist_name':request.form['name'],
            'Area':request.form['area'],
            'Mode':request.form['mode'],
            'Fees':request.form['fees'],
            'Date':request.form['date'],            
            'Description':request.form['description'],
            'Time_slot':request.form['slot'],
            'UserID':userid
        }
        mode=request.form['mode']
        date=request.form['date']
        slot=request.form['slot']
        
        reci=f.get_email_therapist(therapist_id)
        user=f.get_info_user(userid)
        out=f.insert_booking_details(data)
        if out:
            flash("Your Appointment has reached us !!!")
            msg_to_doc = Message('subject', sender = 'divyasudha305@gmail.com', recipients=[reci['Email']])  
            msg_to_doc.html = "<h3>Hi "+reci['Therapist_name'] +",</h3>"+"<br>This is <em><b>WE4YOU</b><em>, You have an appointment requesting a counselling session by "+user['User_name'] +" on "+date+" at a time slot "+slot+" through "+mode+" mode.<br><br> For further communications with your client contact using the Client's Email : <b>"+user['Email']+"</b>. Thank you !!!<br><br>Regards,<br>WE 4 YOU."  
            # return "Mail Sent, Please check the mail id"
            msg_to_client = Message('subject', sender = 'divyasudha305@gmail.com', recipients=[user['Email']])  
            msg_to_client.html = "<h3>Hi "+user['User_name'] +",</h3>"+"<br>This is <em><b>WE4YOU</b><em>, You have booked an appointment requesting a counselling session with Dr."+reci['Therapist_name']+" on "+date+" at a time slot "+slot+" through "+ mode +" mode.<br><br> For further communications with your Therapist in case of Delay contact using the Therapist's Email :<b>"+ user['Email']+"</b>. Thank you !!!<br><br>Regards,<br>WE 4 YOU."  
            mail.send(msg_to_doc)
            mail.send(msg_to_client)    
            return render_template('new_booking.html',userid=userid,therapist_id=therapist_id)

@app.route('/Booking_and_send/<therapist_id>/<name>/<area>/<mode>/<fees>/<userid>',methods=["POST","GET"])
def Booking_and_send(therapist_id,name,area,mode,fees,userid):
    f=First()

    if request.method=="GET":
        return render_template('new_booking.html',therapist_id=therapist_id,name=name,area=area,mode=mode,fees=fees,userid=userid)
    

@app.route('/self_assess/<userid>',methods=["POST","GET"])
def Self_assess(userid):
    f=First()
    if request.method=="GET":
        return render_template('self_assessment.html',userid=userid)

@app.route('/depression/<userid>',methods=["POST","GET"])
def Depression(userid):
    f=First()
    if request.method=="GET":
        return render_template('depression.html',userid=userid)
    if request.method=="POST":
        ans=[]
        score=0 
             
        ans.append(request.form['example1'])
        ans.append(request.form['example2'])
        ans.append(request.form['example3'])
        ans.append(request.form['example4'])
        ans.append(request.form['example5'])
        for i in range(0,5):
            if(ans[i]=='Never'):score+=36
            elif(ans[i]=='Sometimes'):score+=27
            elif(ans[i]=='Fairly Often'):score+=18
            else:score+=9
        print(score)
        return render_template('score.html',score=score,area="Depression",userid=userid)

@app.route('/stress/<userid>',methods=["POST","GET"])
def Stress(userid):
    f=First()
    if request.method=="GET":
        return render_template('stress.html',userid=userid)
    if request.method=="POST":
        ans=[]
        score=0 
             
        ans.append(request.form['example1'])
        ans.append(request.form['example2'])
        ans.append(request.form['example3'])
        ans.append(request.form['example4'])
        ans.append(request.form['example5'])
        for i in range(0,5):
            if(ans[i]=='Never'):score+=36
            elif(ans[i]=='Sometimes'):score+=27
            elif(ans[i]=='Fairly Often'):score+=18
            else:score+=9
        print(score)
        return render_template('score.html',score=score,area="Stress",userid=userid)


            


@app.route('/ocd/<userid>',methods=["POST","GET"])
def Ocd(userid):
    f=First()
    if request.method=="GET":
        return render_template('ocd.html',userid=userid)
    if request.method=="POST":
        ans=[]
        score=0 
             
        ans.append(request.form['example1'])
        ans.append(request.form['example2'])
        ans.append(request.form['example3'])
        ans.append(request.form['example4'])
        ans.append(request.form['example5'])
        for i in range(0,5):
            if(ans[i]=='Never'):score+=36
            elif(ans[i]=='Sometimes'):score+=27
            elif(ans[i]=='Fairly Often'):score+=18
            else:score+=9
        print(score)
        return render_template('score.html',score=score,area="OCD",userid=userid)

    

@app.route('/relationship/<userid>',methods=["POST","GET"])
def Relationship(userid):
    f=First()
    if request.method=="GET":
        return render_template('relationship.html')
    if request.method=="POST":
        ans=[]
        score=0 
             
        ans.append(request.form['example1'])
        ans.append(request.form['example2'])
        ans.append(request.form['example3'])
        ans.append(request.form['example4'])
        ans.append(request.form['example5'])
        for i in range(0,5):
            if(ans[i]=='Never'):score+=36
            elif(ans[i]=='Sometimes'):score+=27
            elif(ans[i]=='Fairly Often'):score+=18
            else:score+=9
        print(score)
        return render_template('score.html',score=score,area="Relationship",userid=userid)



@app.route('/bipolar_disorder/<userid>',methods=["POST","GET"])
def Bipolar_disorder(userid):
    f=First()
    if request.method=="GET":
        return render_template('bipolar_disorder.html',userid=userid)
    if request.method=="POST":
        ans=[]
        score=0 
             
        ans.append(request.form['example1'])
        ans.append(request.form['example2'])
        ans.append(request.form['example3'])
        ans.append(request.form['example4'])
        ans.append(request.form['example5'])
        for i in range(0,5):
            if(ans[i]=='Never'):score+=36
            elif(ans[i]=='Sometimes'):score+=27
            elif(ans[i]=='Fairly Often'):score+=18
            else:score+=9
        print(score)
        return render_template('score.html',score=score,area="Bipolar Disorder",userid=userid)


@app.route('/sleep/<userid>',methods=["POST","GET"])
def Sleep(userid):
    f=First()
    if request.method=="GET":
        return render_template('sleep.html',userid=userid)
    if request.method=="POST":
        ans=[]
        score=0 
             
        ans.append(request.form['example1'])
        ans.append(request.form['example2'])
        ans.append(request.form['example3'])
        ans.append(request.form['example4'])
        ans.append(request.form['example5'])
        for i in range(0,5):
            if(ans[i]=='Never'):score+=36
            elif(ans[i]=='Sometimes'):score+=27
            elif(ans[i]=='Fairly Often'):score+=18
            else:score+=9
        print(score)
        return render_template('score.html',score=score,area="Sleep",userid=userid)



@app.route('/anxiety/<userid>',methods=["POST","GET"])
def Anxiety(userid):
    f=First()
    if request.method=="GET":
        return render_template('anxiety.html',userid=userid)
    if request.method=="POST":
        ans=[]
        score=0 
             
        ans.append(request.form['example1'])
        ans.append(request.form['example2'])
        ans.append(request.form['example3'])
        ans.append(request.form['example4'])
        ans.append(request.form['example5'])
        for i in range(0,5):
            if(ans[i]=='Never'):score+=36
            elif(ans[i]=='Sometimes'):score+=27
            elif(ans[i]=='Fairly Often'):score+=18
            else:score+=9
        print(score)
        return render_template('score.html',score=score,area="Anxiety",userid=userid)



@app.route('/addiction/<userid>',methods=["POST","GET"])
def Addiction(userid):
    f=First()
    if request.method=="GET":
        return render_template('addiction.html',userid=userid)
    if request.method=="POST":
        ans=[]
        score=0 
             
        ans.append(request.form['example1'])
        ans.append(request.form['example2'])
        ans.append(request.form['example3'])
        ans.append(request.form['example4'])
        ans.append(request.form['example5'])
        for i in range(0,5):
            if(ans[i]=='Never'):score+=36
            elif(ans[i]=='Sometimes'):score+=27
            elif(ans[i]=='Fairly Often'):score+=18
            else:score+=9
        print(score)
        return render_template('score.html',score=score,area="Addiction",userid=userid)

    

@app.route('/grief_and_loss/<userid>',methods=["POST","GET"])
def Grief_and_loss(userid):
    f=First()
    if request.method=="GET":
        return render_template('grief_and_loss.html',userid=userid)
    if request.method=="POST":
        ans=[]
        score=0 
             
        ans.append(request.form['example1'])
        ans.append(request.form['example2'])
        ans.append(request.form['example3'])
        ans.append(request.form['example4'])
        ans.append(request.form['example5'])
        for i in range(0,5):
            if(ans[i]=='Never'):score+=36
            elif(ans[i]=='Sometimes'):score+=27
            elif(ans[i]=='Fairly Often'):score+=18
            else:score+=9
        print(score)
        return render_template('score.html',score=score,area="Grief and Loss",userid=userid)



@app.route('/frontline_workers/<userid>',methods=["POST","GET"])
def Frontline_workers(userid):
    f=First()
    if request.method=="GET":
        return render_template('frontline_workers.html',userid=userid)






@app.route('/delivery/<userid>',methods=["POST","GET"])
def Delivery(userid):
    f=First()
    if request.method=="GET":
        return render_template('delivery.html',userid=userid)
    if request.method=="POST":
        ans=[]
                     
        ans.append(request.form['example1'])
        ans.append(request.form['example2'])
        ans.append(request.form['example3'])
        ans.append(request.form['example4'])
        ans.append(request.form['example5'])
        ans.append(request.form['example6'])
        ans.append(request.form['example7'])
        ans.append(request.form['example8'])
        ans.append(request.form['example9'])
        ans.append(request.form['example10'])
        ans.append(request.form['example11'])
        ans.append(request.form['example12'])
        dep=0
        for i in range(0,2):
            if(ans[i] =='Never'):dep+=15
            elif(ans[i]=='Sometimes'):dep+=11.5
            elif(ans[i]=='Fairly Often'):dep+=7.5
            else:dep+=3.5
        dep_score=dep
        
        ang=dep
        for i in range(2,4):
            if(ans[i] =='Never'):ang+=15
            elif(ans[i]=='Sometimes'):ang+=11.5
            elif(ans[i]=='Fairly Often'):ang+=7.5
            else:ang+=3.5   
        ang_score=ang-dep
        
        anx=ang
        for i in range(4,6):
            if(ans[i] =='Never'):anx+=15
            elif(ans[i]=='Sometimes'):anx+=11.5
            elif(ans[i]=='Fairly Often'):anx+=7.5
            else:anx+=3.5 
        anx_score=anx-ang
        
        stress=anx
        for i in range(6,8):
            if(ans[i] =='Never'):stress+=15
            elif(ans[i]=='Sometimes'):stress+=11.5
            elif(ans[i]=='Fairly Often'):stress+=7.5
            else:stress+=3.5
        stress_score=stress-anx

        grief=stress
        for i in range(8,10):
            if(ans[i] =='Never'):grief+=15
            elif(ans[i]=='Sometimes'):grief+=11.5
            elif(ans[i]=='Fairly Often'):grief+=7.5
            else:grief+=3.5
        grief_score=grief-stress

        sleep=grief
        for i in range(10,12):
            if(ans[i] =='Never'):sleep+=15
            elif(ans[i]=='Sometimes'):sleep+=11.5
            elif(ans[i]=='Fairly Often'):sleep+=7.5
            else:sleep+=3.5
        sleep_score=sleep-grief

        each_score=[dep_score,ang_score,anx_score,stress_score,grief_score,sleep_score]
        mini=min(each_score)

        if(mini==dep_score):area="Depression"
        elif(mini==ang_score):area="Anger"
        elif(mini==anx_score):area="Anxiety"
        elif(mini==stress_score):area="Stress"
        elif(mini==grief_score):area="Grief and Loss"
        else:area="Sleep"

        return render_template('frontline_score.html',dep=dep,ang=ang,anx=anx,stress=stress,
        grief=grief,sleep=sleep,score=sleep,dep_score=dep_score,ang_score=ang_score,
        anx_score=anx_score,stress_score=stress_score,grief_score=grief_score,
        sleep_score=sleep_score,area=area,userid=userid)

@app.route('/it/<userid>',methods=["POST","GET"])
def It(userid):
    f=First()
    if request.method=="GET":
        return render_template('it.html',userid=userid)
    if request.method=="POST":
        ans=[]
                     
        ans.append(request.form['example1'])
        ans.append(request.form['example2'])
        ans.append(request.form['example3'])
        ans.append(request.form['example4'])
        ans.append(request.form['example5'])
        ans.append(request.form['example6'])
        ans.append(request.form['example7'])
        ans.append(request.form['example8'])
        ans.append(request.form['example9'])
        ans.append(request.form['example10'])
        ans.append(request.form['example11'])
        ans.append(request.form['example12'])
        dep=0
        for i in range(0,2):
            if(ans[i] =='Never'):dep+=15
            elif(ans[i]=='Sometimes'):dep+=11.5
            elif(ans[i]=='Fairly Often'):dep+=7.5
            else:dep+=3.5
        dep_score=dep
        
        ang=dep
        for i in range(2,4):
            if(ans[i] =='Never'):ang+=15
            elif(ans[i]=='Sometimes'):ang+=11.5
            elif(ans[i]=='Fairly Often'):ang+=7.5
            else:ang+=3.5   
        ang_score=ang-dep
        
        anx=ang
        for i in range(4,6):
            if(ans[i] =='Never'):anx+=15
            elif(ans[i]=='Sometimes'):anx+=11.5
            elif(ans[i]=='Fairly Often'):anx+=7.5
            else:anx+=3.5 
        anx_score=anx-ang
        
        stress=anx
        for i in range(6,8):
            if(ans[i] =='Never'):stress+=15
            elif(ans[i]=='Sometimes'):stress+=11.5
            elif(ans[i]=='Fairly Often'):stress+=7.5
            else:stress+=3.5
        stress_score=stress-anx

        grief=stress
        for i in range(8,10):
            if(ans[i] =='Never'):grief+=15
            elif(ans[i]=='Sometimes'):grief+=11.5
            elif(ans[i]=='Fairly Often'):grief+=7.5
            else:grief+=3.5
        grief_score=grief-stress

        sleep=grief
        for i in range(10,12):
            if(ans[i] =='Never'):sleep+=15
            elif(ans[i]=='Sometimes'):sleep+=11.5
            elif(ans[i]=='Fairly Often'):sleep+=7.5
            else:sleep+=3.5
        sleep_score=sleep-grief

        each_score=[dep_score,ang_score,anx_score,stress_score,grief_score,sleep_score]
        mini=min(each_score)

        if(mini==dep_score):area="Depression"
        elif(mini==ang_score):area="Anger"
        elif(mini==anx_score):area="Anxiety"
        elif(mini==stress_score):area="Stress"
        elif(mini==grief_score):area="Grief and Loss"
        else:area="Sleep"

        return render_template('frontline_score.html',dep=dep,ang=ang,anx=anx,stress=stress,
        grief=grief,sleep=sleep,score=sleep,dep_score=dep_score,ang_score=ang_score,
        anx_score=anx_score,stress_score=stress_score,grief_score=grief_score,
        sleep_score=sleep_score,area=area,userid=userid)

@app.route('/govt_emp/<userid>',methods=["POST","GET"])
def Govt_emp(userid):
    f=First()
    if request.method=="GET":
        return render_template('govt_emp.html',userid=userid)
    if request.method=="POST":
        ans=[]
                     
        ans.append(request.form['example1'])
        ans.append(request.form['example2'])
        ans.append(request.form['example3'])
        ans.append(request.form['example4'])
        ans.append(request.form['example5'])
        ans.append(request.form['example6'])
        ans.append(request.form['example7'])
        ans.append(request.form['example8'])
        ans.append(request.form['example9'])
        ans.append(request.form['example10'])
        ans.append(request.form['example11'])
        ans.append(request.form['example12'])
        dep=0
        for i in range(0,2):
            if(ans[i] =='Never'):dep+=15
            elif(ans[i]=='Sometimes'):dep+=11.5
            elif(ans[i]=='Fairly Often'):dep+=7.5
            else:dep+=3.5
        dep_score=dep
        
        ang=dep
        for i in range(2,4):
            if(ans[i] =='Never'):ang+=15
            elif(ans[i]=='Sometimes'):ang+=11.5
            elif(ans[i]=='Fairly Often'):ang+=7.5
            else:ang+=3.5   
        ang_score=ang-dep
        
        anx=ang
        for i in range(4,6):
            if(ans[i] =='Never'):anx+=15
            elif(ans[i]=='Sometimes'):anx+=11.5
            elif(ans[i]=='Fairly Often'):anx+=7.5
            else:anx+=3.5 
        anx_score=anx-ang
        
        stress=anx
        for i in range(6,8):
            if(ans[i] =='Never'):stress+=15
            elif(ans[i]=='Sometimes'):stress+=11.5
            elif(ans[i]=='Fairly Often'):stress+=7.5
            else:stress+=3.5
        stress_score=stress-anx

        grief=stress
        for i in range(8,10):
            if(ans[i] =='Never'):grief+=15
            elif(ans[i]=='Sometimes'):grief+=11.5
            elif(ans[i]=='Fairly Often'):grief+=7.5
            else:grief+=3.5
        grief_score=grief-stress

        sleep=grief
        for i in range(10,12):
            if(ans[i] =='Never'):sleep+=15
            elif(ans[i]=='Sometimes'):sleep+=11.5
            elif(ans[i]=='Fairly Often'):sleep+=7.5
            else:sleep+=3.5
        sleep_score=sleep-grief

        each_score=[dep_score,ang_score,anx_score,stress_score,grief_score,sleep_score]
        mini=min(each_score)

        if(mini==dep_score):area="Depression"
        elif(mini==ang_score):area="Anger"
        elif(mini==anx_score):area="Anxiety"
        elif(mini==stress_score):area="Stress"
        elif(mini==grief_score):area="Grief and Loss"
        else:area="Sleep"

        return render_template('frontline_score.html',dep=dep,ang=ang,anx=anx,stress=stress,
        grief=grief,sleep=sleep,score=sleep,dep_score=dep_score,ang_score=ang_score,
        anx_score=anx_score,stress_score=stress_score,grief_score=grief_score,
        sleep_score=sleep_score,area=area,userid=userid)

@app.route('/customer_care/<userid>',methods=["POST","GET"])
def Customer_care(userid):
    f=First()
    if request.method=="GET":
        return render_template('customer_care.html',userid=userid)
    if request.method=="POST":
        ans=[]
                     
        ans.append(request.form['example1'])
        ans.append(request.form['example2'])
        ans.append(request.form['example3'])
        ans.append(request.form['example4'])
        ans.append(request.form['example5'])
        ans.append(request.form['example6'])
        ans.append(request.form['example7'])
        ans.append(request.form['example8'])
        ans.append(request.form['example9'])
        ans.append(request.form['example10'])
        ans.append(request.form['example11'])
        ans.append(request.form['example12'])
        dep=0
        for i in range(0,2):
            if(ans[i] =='Never'):dep+=15
            elif(ans[i]=='Sometimes'):dep+=11.5
            elif(ans[i]=='Fairly Often'):dep+=7.5
            else:dep+=3.5
        dep_score=dep
        
        ang=dep
        for i in range(2,4):
            if(ans[i] =='Never'):ang+=15
            elif(ans[i]=='Sometimes'):ang+=11.5
            elif(ans[i]=='Fairly Often'):ang+=7.5
            else:ang+=3.5   
        ang_score=ang-dep
        
        anx=ang
        for i in range(4,6):
            if(ans[i] =='Never'):anx+=15
            elif(ans[i]=='Sometimes'):anx+=11.5
            elif(ans[i]=='Fairly Often'):anx+=7.5
            else:anx+=3.5 
        anx_score=anx-ang
        
        stress=anx
        for i in range(6,8):
            if(ans[i] =='Never'):stress+=15
            elif(ans[i]=='Sometimes'):stress+=11.5
            elif(ans[i]=='Fairly Often'):stress+=7.5
            else:stress+=3.5
        stress_score=stress-anx

        grief=stress
        for i in range(8,10):
            if(ans[i] =='Never'):grief+=15
            elif(ans[i]=='Sometimes'):grief+=11.5
            elif(ans[i]=='Fairly Often'):grief+=7.5
            else:grief+=3.5
        grief_score=grief-stress

        sleep=grief
        for i in range(10,12):
            if(ans[i] =='Never'):sleep+=15
            elif(ans[i]=='Sometimes'):sleep+=11.5
            elif(ans[i]=='Fairly Often'):sleep+=7.5
            else:sleep+=3.5
        sleep_score=sleep-grief

        each_score=[dep_score,ang_score,anx_score,stress_score,grief_score,sleep_score]
        mini=min(each_score)

        if(mini==dep_score):area="Depression"
        elif(mini==ang_score):area="Anger"
        elif(mini==anx_score):area="Anxiety"
        elif(mini==stress_score):area="Stress"
        elif(mini==grief_score):area="Grief and Loss"
        else:area="Sleep"

        return render_template('frontline_score.html',dep=dep,ang=ang,anx=anx,stress=stress,
        grief=grief,sleep=sleep,score=sleep,dep_score=dep_score,ang_score=ang_score,
        anx_score=anx_score,stress_score=stress_score,grief_score=grief_score,
        sleep_score=sleep_score,area=area,userid=userid)

@app.route('/journalists/<userid>',methods=["POST","GET"])
def Journalists(userid):
    f=First()
    if request.method=="GET":
        return render_template('journalists.html',userid=userid)
    if request.method=="POST":
        ans=[]
                     
        ans.append(request.form['example1'])
        ans.append(request.form['example2'])
        ans.append(request.form['example3'])
        ans.append(request.form['example4'])
        ans.append(request.form['example5'])
        ans.append(request.form['example6'])
        ans.append(request.form['example7'])
        ans.append(request.form['example8'])
        ans.append(request.form['example9'])
        ans.append(request.form['example10'])
        ans.append(request.form['example11'])
        ans.append(request.form['example12'])
        dep=0
        for i in range(0,2):
            if(ans[i] =='Never'):dep+=15
            elif(ans[i]=='Sometimes'):dep+=11.5
            elif(ans[i]=='Fairly Often'):dep+=7.5
            else:dep+=3.5
        dep_score=dep
        
        ang=dep
        for i in range(2,4):
            if(ans[i] =='Never'):ang+=15
            elif(ans[i]=='Sometimes'):ang+=11.5
            elif(ans[i]=='Fairly Often'):ang+=7.5
            else:ang+=3.5   
        ang_score=ang-dep
        
        anx=ang
        for i in range(4,6):
            if(ans[i] =='Never'):anx+=15
            elif(ans[i]=='Sometimes'):anx+=11.5
            elif(ans[i]=='Fairly Often'):anx+=7.5
            else:anx+=3.5 
        anx_score=anx-ang
        
        stress=anx
        for i in range(6,8):
            if(ans[i] =='Never'):stress+=15
            elif(ans[i]=='Sometimes'):stress+=11.5
            elif(ans[i]=='Fairly Often'):stress+=7.5
            else:stress+=3.5
        stress_score=stress-anx

        grief=stress
        for i in range(8,10):
            if(ans[i] =='Never'):grief+=15
            elif(ans[i]=='Sometimes'):grief+=11.5
            elif(ans[i]=='Fairly Often'):grief+=7.5
            else:grief+=3.5
        grief_score=grief-stress

        sleep=grief
        for i in range(10,12):
            if(ans[i] =='Never'):sleep+=15
            elif(ans[i]=='Sometimes'):sleep+=11.5
            elif(ans[i]=='Fairly Often'):sleep+=7.5
            else:sleep+=3.5
        sleep_score=sleep-grief

        each_score=[dep_score,ang_score,anx_score,stress_score,grief_score,sleep_score]
        mini=min(each_score)

        if(mini==dep_score):area="Depression"
        elif(mini==ang_score):area="Anger"
        elif(mini==anx_score):area="Anxiety"
        elif(mini==stress_score):area="Stress"
        elif(mini==grief_score):area="Grief and Loss"
        else:area="Sleep"

        return render_template('frontline_score.html',dep=dep,ang=ang,anx=anx,stress=stress,
        grief=grief,sleep=sleep,score=sleep,dep_score=dep_score,ang_score=ang_score,
        anx_score=anx_score,stress_score=stress_score,grief_score=grief_score,
        sleep_score=sleep_score,area=area,userid=userid)

@app.route('/teachers/<userid>',methods=["POST","GET"])
def Teachers(userid):
    f=First()
    if request.method=="GET":
        return render_template('teachers.html',userid=userid)
    if request.method=="POST":
        ans=[]
                     
        ans.append(request.form['example1'])
        ans.append(request.form['example2'])
        ans.append(request.form['example3'])
        ans.append(request.form['example4'])
        ans.append(request.form['example5'])
        ans.append(request.form['example6'])
        ans.append(request.form['example7'])
        ans.append(request.form['example8'])
        ans.append(request.form['example9'])
        ans.append(request.form['example10'])
        ans.append(request.form['example11'])
        ans.append(request.form['example12'])
        dep=0
        for i in range(0,2):
            if(ans[i] =='Never'):dep+=15
            elif(ans[i]=='Sometimes'):dep+=11.5
            elif(ans[i]=='Fairly Often'):dep+=7.5
            else:dep+=3.5
        dep_score=dep
        
        ang=dep
        for i in range(2,4):
            if(ans[i] =='Never'):ang+=15
            elif(ans[i]=='Sometimes'):ang+=11.5
            elif(ans[i]=='Fairly Often'):ang+=7.5
            else:ang+=3.5   
        ang_score=ang-dep
        
        anx=ang
        for i in range(4,6):
            if(ans[i] =='Never'):anx+=15
            elif(ans[i]=='Sometimes'):anx+=11.5
            elif(ans[i]=='Fairly Often'):anx+=7.5
            else:anx+=3.5 
        anx_score=anx-ang
        
        stress=anx
        for i in range(6,8):
            if(ans[i] =='Never'):stress+=15
            elif(ans[i]=='Sometimes'):stress+=11.5
            elif(ans[i]=='Fairly Often'):stress+=7.5
            else:stress+=3.5
        stress_score=stress-anx

        grief=stress
        for i in range(8,10):
            if(ans[i] =='Never'):grief+=15
            elif(ans[i]=='Sometimes'):grief+=11.5
            elif(ans[i]=='Fairly Often'):grief+=7.5
            else:grief+=3.5
        grief_score=grief-stress

        sleep=grief
        for i in range(10,12):
            if(ans[i] =='Never'):sleep+=15
            elif(ans[i]=='Sometimes'):sleep+=11.5
            elif(ans[i]=='Fairly Often'):sleep+=7.5
            else:sleep+=3.5
        sleep_score=sleep-grief

        each_score=[dep_score,ang_score,anx_score,stress_score,grief_score,sleep_score]
        mini=min(each_score)

        if(mini==dep_score):area="Depression"
        elif(mini==ang_score):area="Anger"
        elif(mini==anx_score):area="Anxiety"
        elif(mini==stress_score):area="Stress"
        elif(mini==grief_score):area="Grief and Loss"
        else:area="Sleep"

        return render_template('frontline_score.html',dep=dep,ang=ang,anx=anx,stress=stress,
        grief=grief,sleep=sleep,score=sleep,dep_score=dep_score,ang_score=ang_score,
        anx_score=anx_score,stress_score=stress_score,grief_score=grief_score,
        sleep_score=sleep_score,area=area,userid=userid)

@app.route('/public_safety/<userid>',methods=["POST","GET"])
def Public_safety(userid):
    f=First()
    if request.method=="GET":
        return render_template('public_safety.html',userid=userid)
    if request.method=="POST":
        ans=[]
                     
        ans.append(request.form['example1'])
        ans.append(request.form['example2'])
        ans.append(request.form['example3'])
        ans.append(request.form['example4'])
        ans.append(request.form['example5'])
        ans.append(request.form['example6'])
        ans.append(request.form['example7'])
        ans.append(request.form['example8'])
        ans.append(request.form['example9'])
        ans.append(request.form['example10'])
        ans.append(request.form['example11'])
        ans.append(request.form['example12'])
        dep=0
        for i in range(0,2):
            if(ans[i] =='Never'):dep+=15
            elif(ans[i]=='Sometimes'):dep+=11.5
            elif(ans[i]=='Fairly Often'):dep+=7.5
            else:dep+=3.5
        dep_score=dep
        
        ang=dep
        for i in range(2,4):
            if(ans[i] =='Never'):ang+=15
            elif(ans[i]=='Sometimes'):ang+=11.5
            elif(ans[i]=='Fairly Often'):ang+=7.5
            else:ang+=3.5   
        ang_score=ang-dep
        
        anx=ang
        for i in range(4,6):
            if(ans[i] =='Never'):anx+=15
            elif(ans[i]=='Sometimes'):anx+=11.5
            elif(ans[i]=='Fairly Often'):anx+=7.5
            else:anx+=3.5 
        anx_score=anx-ang
        
        stress=anx
        for i in range(6,8):
            if(ans[i] =='Never'):stress+=15
            elif(ans[i]=='Sometimes'):stress+=11.5
            elif(ans[i]=='Fairly Often'):stress+=7.5
            else:stress+=3.5
        stress_score=stress-anx

        grief=stress
        for i in range(8,10):
            if(ans[i] =='Never'):grief+=15
            elif(ans[i]=='Sometimes'):grief+=11.5
            elif(ans[i]=='Fairly Often'):grief+=7.5
            else:grief+=3.5
        grief_score=grief-stress

        sleep=grief
        for i in range(10,12):
            if(ans[i] =='Never'):sleep+=15
            elif(ans[i]=='Sometimes'):sleep+=11.5
            elif(ans[i]=='Fairly Often'):sleep+=7.5
            else:sleep+=3.5
        sleep_score=sleep-grief

        each_score=[dep_score,ang_score,anx_score,stress_score,grief_score,sleep_score]
        mini=min(each_score)

        if(mini==dep_score):area="Depression"
        elif(mini==ang_score):area="Anger"
        elif(mini==anx_score):area="Anxiety"
        elif(mini==stress_score):area="Stress"
        elif(mini==grief_score):area="Grief and Loss"
        else:area="Sleep"

        return render_template('frontline_score.html',dep=dep,ang=ang,anx=anx,stress=stress,
        grief=grief,sleep=sleep,score=sleep,dep_score=dep_score,ang_score=ang_score,
        anx_score=anx_score,stress_score=stress_score,grief_score=grief_score,
        sleep_score=sleep_score,area=area,userid=userid)


@app.route('/transport/<userid>',methods=["POST","GET"])
def Transport(userid):
    f=First()
    if request.method=="GET":
        return render_template('transport.html',userid=userid)
    if request.method=="POST":
        ans=[]
                     
        ans.append(request.form['example1'])
        ans.append(request.form['example2'])
        ans.append(request.form['example3'])
        ans.append(request.form['example4'])
        ans.append(request.form['example5'])
        ans.append(request.form['example6'])
        ans.append(request.form['example7'])
        ans.append(request.form['example8'])
        ans.append(request.form['example9'])
        ans.append(request.form['example10'])
        ans.append(request.form['example11'])
        ans.append(request.form['example12'])
        dep=0
        for i in range(0,2):
            if(ans[i] =='Never'):dep+=15
            elif(ans[i]=='Sometimes'):dep+=11.5
            elif(ans[i]=='Fairly Often'):dep+=7.5
            else:dep+=3.5
        dep_score=dep
        
        ang=dep
        for i in range(2,4):
            if(ans[i] =='Never'):ang+=15
            elif(ans[i]=='Sometimes'):ang+=11.5
            elif(ans[i]=='Fairly Often'):ang+=7.5
            else:ang+=3.5   
        ang_score=ang-dep
        
        anx=ang
        for i in range(4,6):
            if(ans[i] =='Never'):anx+=15
            elif(ans[i]=='Sometimes'):anx+=11.5
            elif(ans[i]=='Fairly Often'):anx+=7.5
            else:anx+=3.5 
        anx_score=anx-ang
        
        stress=anx
        for i in range(6,8):
            if(ans[i] =='Never'):stress+=15
            elif(ans[i]=='Sometimes'):stress+=11.5
            elif(ans[i]=='Fairly Often'):stress+=7.5
            else:stress+=3.5
        stress_score=stress-anx

        grief=stress
        for i in range(8,10):
            if(ans[i] =='Never'):grief+=15
            elif(ans[i]=='Sometimes'):grief+=11.5
            elif(ans[i]=='Fairly Often'):grief+=7.5
            else:grief+=3.5
        grief_score=grief-stress

        sleep=grief
        for i in range(10,12):
            if(ans[i] =='Never'):sleep+=15
            elif(ans[i]=='Sometimes'):sleep+=11.5
            elif(ans[i]=='Fairly Often'):sleep+=7.5
            else:sleep+=3.5
        sleep_score=sleep-grief

        each_score=[dep_score,ang_score,anx_score,stress_score,grief_score,sleep_score]
        mini=min(each_score)

        if(mini==dep_score):area="Depression"
        elif(mini==ang_score):area="Anger"
        elif(mini==anx_score):area="Anxiety"
        elif(mini==stress_score):area="Stress"
        elif(mini==grief_score):area="Grief and Loss"
        else:area="Sleep"

        return render_template('frontline_score.html',dep=dep,ang=ang,anx=anx,stress=stress,
        grief=grief,sleep=sleep,score=sleep,dep_score=dep_score,ang_score=ang_score,
        anx_score=anx_score,stress_score=stress_score,grief_score=grief_score,
        sleep_score=sleep_score,area=area,userid=userid)


@app.route('/lawyers/<userid>',methods=["POST","GET"])
def Lawyers(userid):
    f=First()
    if request.method=="GET":
        return render_template('lawyers.html',userid=userid)
    if request.method=="POST":
        ans=[]
                     
        ans.append(request.form['example1'])
        ans.append(request.form['example2'])
        ans.append(request.form['example3'])
        ans.append(request.form['example4'])
        ans.append(request.form['example5'])
        ans.append(request.form['example6'])
        ans.append(request.form['example7'])
        ans.append(request.form['example8'])
        ans.append(request.form['example9'])
        ans.append(request.form['example10'])
        ans.append(request.form['example11'])
        ans.append(request.form['example12'])
        dep=0
        for i in range(0,2):
            if(ans[i] =='Never'):dep+=15
            elif(ans[i]=='Sometimes'):dep+=11.5
            elif(ans[i]=='Fairly Often'):dep+=7.5
            else:dep+=3.5
        dep_score=dep
        
        ang=dep
        for i in range(2,4):
            if(ans[i] =='Never'):ang+=15
            elif(ans[i]=='Sometimes'):ang+=11.5
            elif(ans[i]=='Fairly Often'):ang+=7.5
            else:ang+=3.5   
        ang_score=ang-dep
        
        anx=ang
        for i in range(4,6):
            if(ans[i] =='Never'):anx+=15
            elif(ans[i]=='Sometimes'):anx+=11.5
            elif(ans[i]=='Fairly Often'):anx+=7.5
            else:anx+=3.5 
        anx_score=anx-ang
        
        stress=anx
        for i in range(6,8):
            if(ans[i] =='Never'):stress+=15
            elif(ans[i]=='Sometimes'):stress+=11.5
            elif(ans[i]=='Fairly Often'):stress+=7.5
            else:stress+=3.5
        stress_score=stress-anx

        grief=stress
        for i in range(8,10):
            if(ans[i] =='Never'):grief+=15
            elif(ans[i]=='Sometimes'):grief+=11.5
            elif(ans[i]=='Fairly Often'):grief+=7.5
            else:grief+=3.5
        grief_score=grief-stress

        sleep=grief
        for i in range(10,12):
            if(ans[i] =='Never'):sleep+=15
            elif(ans[i]=='Sometimes'):sleep+=11.5
            elif(ans[i]=='Fairly Often'):sleep+=7.5
            else:sleep+=3.5
        sleep_score=sleep-grief

        each_score=[dep_score,ang_score,anx_score,stress_score,grief_score,sleep_score]
        mini=min(each_score)

        if(mini==dep_score):area="Depression"
        elif(mini==ang_score):area="Anger"
        elif(mini==anx_score):area="Anxiety"
        elif(mini==stress_score):area="Stress"
        elif(mini==grief_score):area="Grief and Loss"
        else:area="Sleep"

        return render_template('frontline_score.html',dep=dep,ang=ang,anx=anx,stress=stress,
        grief=grief,sleep=sleep,score=sleep,dep_score=dep_score,ang_score=ang_score,
        anx_score=anx_score,stress_score=stress_score,grief_score=grief_score,
        sleep_score=sleep_score,area=area,userid=userid)


@app.route('/child_care/<userid>',methods=["POST","GET"])
def Child_care(userid):
    f=First()
    if request.method=="GET":
        return render_template('child_care.html',userid=userid)
    if request.method=="POST":
        ans=[]
                     
        ans.append(request.form['example1'])
        ans.append(request.form['example2'])
        ans.append(request.form['example3'])
        ans.append(request.form['example4'])
        ans.append(request.form['example5'])
        ans.append(request.form['example6'])
        ans.append(request.form['example7'])
        ans.append(request.form['example8'])
        ans.append(request.form['example9'])
        ans.append(request.form['example10'])
        ans.append(request.form['example11'])
        ans.append(request.form['example12'])
        dep=0
        for i in range(0,2):
            if(ans[i] =='Never'):dep+=15
            elif(ans[i]=='Sometimes'):dep+=11.5
            elif(ans[i]=='Fairly Often'):dep+=7.5
            else:dep+=3.5
        dep_score=dep
        
        ang=dep
        for i in range(2,4):
            if(ans[i] =='Never'):ang+=15
            elif(ans[i]=='Sometimes'):ang+=11.5
            elif(ans[i]=='Fairly Often'):ang+=7.5
            else:ang+=3.5   
        ang_score=ang-dep
        
        anx=ang
        for i in range(4,6):
            if(ans[i] =='Never'):anx+=15
            elif(ans[i]=='Sometimes'):anx+=11.5
            elif(ans[i]=='Fairly Often'):anx+=7.5
            else:anx+=3.5 
        anx_score=anx-ang
        
        stress=anx
        for i in range(6,8):
            if(ans[i] =='Never'):stress+=15
            elif(ans[i]=='Sometimes'):stress+=11.5
            elif(ans[i]=='Fairly Often'):stress+=7.5
            else:stress+=3.5
        stress_score=stress-anx

        grief=stress
        for i in range(8,10):
            if(ans[i] =='Never'):grief+=15
            elif(ans[i]=='Sometimes'):grief+=11.5
            elif(ans[i]=='Fairly Often'):grief+=7.5
            else:grief+=3.5
        grief_score=grief-stress

        sleep=grief
        for i in range(10,12):
            if(ans[i] =='Never'):sleep+=15
            elif(ans[i]=='Sometimes'):sleep+=11.5
            elif(ans[i]=='Fairly Often'):sleep+=7.5
            else:sleep+=3.5
        sleep_score=sleep-grief

        each_score=[dep_score,ang_score,anx_score,stress_score,grief_score,sleep_score]
        mini=min(each_score)

        if(mini==dep_score):area="Depression"
        elif(mini==ang_score):area="Anger"
        elif(mini==anx_score):area="Anxiety"
        elif(mini==stress_score):area="Stress"
        elif(mini==grief_score):area="Grief and Loss"
        else:area="Sleep"

        return render_template('frontline_score.html',dep=dep,ang=ang,anx=anx,stress=stress,
        grief=grief,sleep=sleep,score=sleep,dep_score=dep_score,ang_score=ang_score,
        anx_score=anx_score,stress_score=stress_score,grief_score=grief_score,
        sleep_score=sleep_score,area=area,userid=userid)


@app.route('/social_workers/<userid>',methods=["POST","GET"])
def Social_workers(userid):
    f=First()
    if request.method=="GET":
        return render_template('social_workers.html',userid=userid)
    if request.method=="POST":
        ans=[]
                     
        ans.append(request.form['example1'])
        ans.append(request.form['example2'])
        ans.append(request.form['example3'])
        ans.append(request.form['example4'])
        ans.append(request.form['example5'])
        ans.append(request.form['example6'])
        ans.append(request.form['example7'])
        ans.append(request.form['example8'])
        ans.append(request.form['example9'])
        ans.append(request.form['example10'])
        ans.append(request.form['example11'])
        ans.append(request.form['example12'])
        dep=0
        for i in range(0,2):
            if(ans[i] =='Never'):dep+=15
            elif(ans[i]=='Sometimes'):dep+=11.5
            elif(ans[i]=='Fairly Often'):dep+=7.5
            else:dep+=3.5
        dep_score=dep
        
        ang=dep
        for i in range(2,4):
            if(ans[i] =='Never'):ang+=15
            elif(ans[i]=='Sometimes'):ang+=11.5
            elif(ans[i]=='Fairly Often'):ang+=7.5
            else:ang+=3.5   
        ang_score=ang-dep
        
        anx=ang
        for i in range(4,6):
            if(ans[i] =='Never'):anx+=15
            elif(ans[i]=='Sometimes'):anx+=11.5
            elif(ans[i]=='Fairly Often'):anx+=7.5
            else:anx+=3.5 
        anx_score=anx-ang
        
        stress=anx
        for i in range(6,8):
            if(ans[i] =='Never'):stress+=15
            elif(ans[i]=='Sometimes'):stress+=11.5
            elif(ans[i]=='Fairly Often'):stress+=7.5
            else:stress+=3.5
        stress_score=stress-anx

        grief=stress
        for i in range(8,10):
            if(ans[i] =='Never'):grief+=15
            elif(ans[i]=='Sometimes'):grief+=11.5
            elif(ans[i]=='Fairly Often'):grief+=7.5
            else:grief+=3.5
        grief_score=grief-stress

        sleep=grief
        for i in range(10,12):
            if(ans[i] =='Never'):sleep+=15
            elif(ans[i]=='Sometimes'):sleep+=11.5
            elif(ans[i]=='Fairly Often'):sleep+=7.5
            else:sleep+=3.5
        sleep_score=sleep-grief

        each_score=[dep_score,ang_score,anx_score,stress_score,grief_score,sleep_score]
        mini=min(each_score)

        if(mini==dep_score):area="Depression"
        elif(mini==ang_score):area="Anger"
        elif(mini==anx_score):area="Anxiety"
        elif(mini==stress_score):area="Stress"
        elif(mini==grief_score):area="Grief and Loss"
        else:area="Sleep"

        return render_template('frontline_score.html',dep=dep,ang=ang,anx=anx,stress=stress,
        grief=grief,sleep=sleep,score=sleep,dep_score=dep_score,ang_score=ang_score,
        anx_score=anx_score,stress_score=stress_score,grief_score=grief_score,
        sleep_score=sleep_score,area=area,userid=userid)


@app.route('/doctors/<userid>',methods=["POST","GET"])
def Doctors(userid):
    f=First()
    if request.method=="GET":
        return render_template('doctors.html',userid=userid)
    if request.method=="POST":
        ans=[]
                     
        ans.append(request.form['example1'])
        ans.append(request.form['example2'])
        ans.append(request.form['example3'])
        ans.append(request.form['example4'])
        ans.append(request.form['example5'])
        ans.append(request.form['example6'])
        ans.append(request.form['example7'])
        ans.append(request.form['example8'])
        ans.append(request.form['example9'])
        ans.append(request.form['example10'])
        ans.append(request.form['example11'])
        ans.append(request.form['example12'])
        dep=0
        for i in range(0,2):
            if(ans[i] =='Never'):dep+=15
            elif(ans[i]=='Sometimes'):dep+=11.5
            elif(ans[i]=='Fairly Often'):dep+=7.5
            else:dep+=3.5
        dep_score=dep
        
        ang=dep
        for i in range(2,4):
            if(ans[i] =='Never'):ang+=15
            elif(ans[i]=='Sometimes'):ang+=11.5
            elif(ans[i]=='Fairly Often'):ang+=7.5
            else:ang+=3.5   
        ang_score=ang-dep
        
        anx=ang
        for i in range(4,6):
            if(ans[i] =='Never'):anx+=15
            elif(ans[i]=='Sometimes'):anx+=11.5
            elif(ans[i]=='Fairly Often'):anx+=7.5
            else:anx+=3.5 
        anx_score=anx-ang
        
        stress=anx
        for i in range(6,8):
            if(ans[i] =='Never'):stress+=15
            elif(ans[i]=='Sometimes'):stress+=11.5
            elif(ans[i]=='Fairly Often'):stress+=7.5
            else:stress+=3.5
        stress_score=stress-anx

        grief=stress
        for i in range(8,10):
            if(ans[i] =='Never'):grief+=15
            elif(ans[i]=='Sometimes'):grief+=11.5
            elif(ans[i]=='Fairly Often'):grief+=7.5
            else:grief+=3.5
        grief_score=grief-stress

        sleep=grief
        for i in range(10,12):
            if(ans[i] =='Never'):sleep+=15
            elif(ans[i]=='Sometimes'):sleep+=11.5
            elif(ans[i]=='Fairly Often'):sleep+=7.5
            else:sleep+=3.5
        sleep_score=sleep-grief

        each_score=[dep_score,ang_score,anx_score,stress_score,grief_score,sleep_score]
        mini=min(each_score)

        if(mini==dep_score):area="Depression"
        elif(mini==ang_score):area="Anger"
        elif(mini==anx_score):area="Anxiety"
        elif(mini==stress_score):area="Stress"
        elif(mini==grief_score):area="Grief and Loss"
        else:area="Sleep"

        return render_template('frontline_score.html',dep=dep,ang=ang,anx=anx,stress=stress,
        grief=grief,sleep=sleep,score=sleep,dep_score=dep_score,ang_score=ang_score,
        anx_score=anx_score,stress_score=stress_score,grief_score=grief_score,
        sleep_score=sleep_score,area=area,userid=userid)

@app.route('/booking_details/<userid>',methods=["POST","GET"])
def Booking_details(userid):
    f=First()
    if request.method=="GET":        
        out=f.get_booking_details(userid)
        print(out)
        if out:
            return render_template('booking_details.html',out=out,userid=userid)
        else:
            return render_template('booking_details.html',userid=userid)
    


if __name__ =='__main__':  
    app.run(debug = True) 