import mysql.connector
import smtplib
from smtplib import SMTP       
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment       

def send_mail(name,TO,message,auto_complete_count,geo_code_count,reverse_geo_code_count,distance_count,nearby_count):

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
margin-left: 45px;
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
margin-left: 45px;
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
</style>
</head>
<body>
<header>
<center>
   </center>
</header>
<br><br>
<p style="font-size:15px;">Hi <b>{{name}}</b></p>
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
        </center>
</body>
</html> 
    """  
    msg = MIMEText(
    Environment().from_string(TEMPLATE).render(
       name = name,msg = message,autocomplete = auto_complete_count,geocode = geo_code_count, reverse_geo = reverse_geo_code_count,nearby = nearby_count, distance = distance_count
    ), "html"
    )
    FROM = "mail_address"
    msg['Subject'] = "API Usages"
    msg['From'] = FROM
    msg['To'] = TO

    server = smtplib.SMTP('smtp.zoho.com:587')
    password = "password"
    server.starttls()
    server.login(FROM,password)
    server.sendmail(FROM, [TO], msg.as_string().encode('utf8'))
    server.quit()

if __name__ == "__main__":
    
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="database_name",
        )
    query = "select user_id,autocomplete_count,geo_code_count,reverse_geo_code_count,distance_count,nearby_count from tokens where isActive=1 and user_id=1486 or user_id=1481 or user_id=1 or user_id=17 or user_id=12"
    cursor = mydb.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    for i in records:
        auto_complete_count = i[1]
        geo_code_count = i[2]
        reverse_geo_code_count =  i[3]
        distance_count = i[4]
        nearby_count = i[5]
        query = "select name,email from users where id="+str(i[0])
        cursor = mydb.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        for j in record:
            name = j[0]
            email = j[1]
        if auto_complete_count == 0 and geo_code_count == 0 and reverse_geo_code_count == 0 and distance_count == 0 and nearby_count == 0 :
              message = "You have not use any API yet."
              send_mail(name,email,message,auto_complete_count,geo_code_count,reverse_geo_code_count,distance_count,nearby_count)

        else:
              message = "Here is your total API usages."
              send_mail(name,email,message,auto_complete_count,geo_code_count,reverse_geo_code_count,distance_count,nearby_count)
          

        
        
