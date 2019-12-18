import mysql.connector
import smtplib
from smtplib import SMTP       
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment 
import requests      

def send_mail(name,TO,autocomlpete_sum,geocode_sum,reverse_geo_sum,distance_sum,nearby_sum):

    TEMPLATE = """
   <!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="ie=edge">
<title>Barikoi API Usage</title>
<link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
<style>
    header img {
        margin-top: 5px;
        max-width: 200px;
    }
table {
position: relative;
font-family: 'Open Sans', sans-serif;
border-collapse: collapse;
margin-left: 75px;
width: 727px;
}
td, th {
border: 1px solid #dddddd;
text-align: left;
padding: 8px;
}
th{
padding-top: 12px;
padding-bottom: 12px;
text-align: left;
background-color: #4CAF50;
color: white;
}
tr:nth-child(even) {
background-color: #dddddd;
}
p{
margin-left: 75px;
}
body{
  position: relative;
  margin-left: 250px;
  margin-right: 250px;
  border-style: 5px solid;
  border-color: white;
  box-shadow:5px 6px 100px 100px whitesmoke;
  border-radius: 5px;
  background-color: white;
  font-family:'Open Sans',sans-serif;
}
img{
  position: relative;
  left: 300px;
}
</style>
</head>
<body>
<center>
<header>
   <a href="https://barikoi.com"><img src="https://barikoi.com/views/assets/img/logo2.png" ></a>
</header>
</center>
<br><br>
<p style="font-size:15px;">Hi <b>{{name}}</b></p>
<p style="font-size:15px;">Greetings from <b>Barikoi Technologies Limited</b></p>
<p style="font-size:15px;">Thanking you for using Barikoi API. Here is your total API usage of last 7 Days</p>
          <br>
          <table>
            <thead>
              <tr>
                  <th>Autocomplete</th>
                  <th>Geocode</th>
                  <th>Reverse Geocode</th>
                  <th>Nearby</th>
                  <th>Distance</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{{autocomplete}}</td>
                <td>{{geocode}}</td>
                <td>{{reverse_geo}}</td>
                <td>{{nearby}}</td>
                <td>{{distance}}</td>
              </tr>
            </tbody>
          </table>
          <br>
          <p style="font-size:14px;">Best Wishes</p> 
          <p style="font-size:15px;"><b>Team Barikoi</b></p>
<center>
      <br>
        <b> &copy; 2019 Barikoi Technologies Limited </b>
</center>
</body>
</html> 
    """  
    msg = MIMEText(
    Environment().from_string(TEMPLATE).render(
       name = name,autocomplete = autocomlpete_sum,geocode = geocode_sum, reverse_geo = reverse_geo_sum,nearby = nearby_sum, distance = distance_sum
    ), "html"
    )
    FROM = "hello@barikoi.com"
    msg['Subject'] = "Barikoi API Usages"
    msg['From'] = FROM
    msg['To'] = TO

    server = smtplib.SMTP('smtp.zoho.com:587')
    password = "mirpur1216barikoi"
    server.starttls()
    server.login(FROM,password)
    server.sendmail(FROM, [TO], msg.as_string().encode('utf8'))
    server.quit()

if __name__ == "__main__":
    
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="ethikana",
        )
query = "select `user_id`,`key` from tokens where isActive=1 and (user_id=1486 or user_id=1481 or user_id=1 or user_id=17 or user_id=12)"

cursor = mydb.cursor()
cursor.execute(query)
records = cursor.fetchall()


for i in records:
    user_id=i[0]
    api_key=i[1]

    query = "select name,email from users where id ="+str(user_id)

    cursor = mydb.cursor()
    cursor.execute(query)
    user_data = cursor.fetchall()

    for j in user_data:
        name = j[0]
        email = j[1]

    api = 'https://admin.barikoi.xyz:8080/bkoi/logreader/CheckUsage?key='+api_key+'&day=6'

    connection = requests.get(url = api)

    autocomlpete_sum,reverse_geo_sum,geocode_sum,distance_sum,nearby_sum=0,0,0,0,0

    data = connection.json()
    if data:
      for i in data:
          autocomlpete_sum+=i['autocomplete']
          reverse_geo_sum+=i['reverse_geocode']
          geocode_sum+=i['geocode']
          distance_sum+=i['distance']
          nearby_sum+=i['nearby']
    send_mail(name,email,autocomlpete_sum,geocode_sum,reverse_geo_sum,distance_sum,nearby_sum)
