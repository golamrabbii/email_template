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
<header>
   <a href="https://barikoi.com"><img src="https://barikoi.com/views/assets/img/logo2.png" ></a>
</header>
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
    query = "select id,name,email from users where id=1481 or id=1486 or id=17 or id=12 or id=1"
    cursor = mydb.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    for i in records:

      user_id = str(i[0])
      day = '7'
      name = i[1]
      email = i[2]

      autocomlpete_sum,reverse_geo_sum,geocode_sum,distance_sum,nearby_sum=0,0,0,0,0

      url = "http://13.251.2.198:8080/bkoi/apilog/showDayUsage?day="+day+"&id="+user_id
      r = requests.get(url = url)
      log = r.json()
      if log:
        for i in log:
          autocomlpete_sum+=log[i]['autocomplete']
          reverse_geo_sum+=log[i]['reverse_geocode']
          geocode_sum+=log[i]['geocode']
          distance_sum+=log[i]['distance']
          nearby_sum+=log[i]['nearby']

        send_mail(name,email,autocomlpete_sum,geocode_sum,reverse_geo_sum,distance_sum,nearby_sum)
