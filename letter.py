import mysql.connector
import smtplib
from smtplib import SMTP       
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment       

def send_mail(name,TO,auto_complete_count,geo_code_count,reverse_geo_code_count,distance_count,nearby_count):
    
    TEMPLATE = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Barikoi API Usage</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
    <style>
        header img {
            max-width: 200px;
        }
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
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
  font-size: large;
}
</style>
</head>
<body>
<header>
<center>
    <div class="container">
        <div class="row">
            <div class="col s12 l12 m12">
                <img src="https://barikoi.com/views/assets/img/logo2.png" >
            </div>
        </div>
    </div>
</center>
</header>
<div class="container">
        <div class="row">
            <div class="col s12 l12 m12">
                <p style = "font-family:courier,arial,helvetica;">Hi <b>{{name}}</b></p>
                <p>Greetings from Barikoi Technologies Limited</p>
            </div>
          </div>
          <div class="row">
              <h4>This weeks usage</h4>
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
                    <td> {{ autocomplete }} </td>
                    <td>{{ geocode }}</td>
                    <td>{{ reverse_geo }}</td>
                    <td>{{ nearby }}</td>
                    <td>{{ distance }}</td>
                  </tr>
                </tbody>
              </table>
          </div>
      </div>
<center>
      <footer class="">
        <div class="container">
          <div class="row">
            <div class="col l12 s12">
              <div class="center">
              </div>
            </div>
          </div>
        </div>
        <div class="footer-copyright">
          <div class="container">
          <div class="center">
          <br>
            <b> &copy; 2019 Barikoi Technologies Limited </b>
          </div>
          </div>
        </div>
      </footer>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>

</body>
</html> 
    """  
    msg = MIMEText(
    Environment().from_string(TEMPLATE).render(
       name = name,autocomplete = auto_complete_count,geocode = geo_code_count, reverse_geo = reverse_geo_code_count,nearby = nearby_count, distance = distance_count
    ), "html"
    )
    FROM = "sender_email_address"
    msg['Subject'] = "Barikoi API Usages"
    msg['From'] = FROM
    msg['To'] = TO

    server = smtplib.SMTP('smtp.gmail.com:587')
    password = "sender_email_password"
    server.starttls()
    server.login(FROM,password)
    server.sendmail(FROM, [TO], msg.as_string().encode('utf8'))
    server.quit()

if __name__ == "__main__":
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="12345",
            database="test_db_",
        )
    query = "select user_id,autocomplete_count,geo_code_count,reverse_geo_code_count,distance_count,nearby_count from tokens where isActive=1"
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
        send_mail(name,email,auto_complete_count,geo_code_count,reverse_geo_code_count,distance_count,nearby_count)
