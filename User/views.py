from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def register(request):
    if request.method=="POST":
        first=request.POST['fname']
        last=request.POST['lname']
        u=request.POST['uname']
        e=request.POST['email']
        p1=request.POST['password']
        p2=request.POST['password1']
        if p1==p2:
            if User.objects.filter(username=u).exists():
                messages.info(request,"Username Available")
                return render(request,"register.html")
            elif User.objects.filter(email=e).exists():
                messages.info(request,"Email Exists")
                return render(request,"register.html")
            else:
                #To store value in database
                user=User.objects.create_user(first_name=first,last_name=last,
                username=u,email=e,password=p2)
                user.save()
                return redirect('login')
        else:
            messages.info(request,"Password Not Matching")
            return render(request,"register.html")
    else:
        return render(request,"register.html")

    return render(request,"register.html")


def login(request):
    if request.method=="POST":
        u=request.POST['uname']
        p=request.POST['password']
        user=auth.authenticate(username=u,password=p)
        if user is not None:
            auth.login(request,user)
            return redirect('data')
        else:
            messages.info(request,"Invalid Credentials")
            return render(request,"login.html")
    return render(request,"login.html")

def logout(request):
    auth.logout(request)
    return redirect('/')

def data(request):
    return render(request,"data.html")

def predict(request):
    if request.method == 'POST':
        n=int(request.POST['nitrogen'])
        p=int(request.POST['phosphorous'])
        k=int(request.POST['potassium'])
        t=float(request.POST['temp'])
        h=float(request.POST['humidity'])
        ph=float(request.POST['ph'])
        rain=float(request.POST['rainfall'])
        import pandas as pd
        df=pd.read_csv(r"static/Crop_recommendation.csv")
        import matplotlib.pyplot as plt
        import seaborn as sns

        sns.heatmap(df.isnull())
        plt.show()
        print("**")
        print(df.shape)
        print("**")
        print(df.isnull().sum)
        print("**")
        print(df.dropna(inplace=True))
        print("**")
        sns.violinplot(df["temperature"])
        plt.show()
        plt.bar(df["N"],df["K"])
        plt.show()

        X_train=df[["N","P","K","temperature","humidity","ph","rainfall"]]
        y_train=df["label"]

        from sklearn.linear_model import LogisticRegression
        log=LogisticRegression()
        log.fit(X_train,y_train)
        import numpy as np
        crop=np.array([[n,p,k,t,h,ph, rain]],dtype=object)
        predicted_crop=log.predict(crop)
        print("Predicted Crop:",predicted_crop)
        return render(request,"predict.html",{"n":n,"p":p,"k":k,"ph":ph,"h":h,"t":t,"rain":rain,"crop":predicted_crop})
       

    return render(request,"predict.html")