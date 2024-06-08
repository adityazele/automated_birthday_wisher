import datetime as dt
import pandas, random, smtplib, os

my_email = "marshhectar@gmail.com"
password = os.environ["PASSWORD"]

now = dt.datetime.now()
month = now.month
date = now.day

# Check if today matches a birthday in the birthdays.csv
data_file = pandas.read_csv("birthdays.csv")
i = 0
name_list = []
to_email_list = []
for data_month in data_file["month"]:
    if data_month == month:
        name_data = data_file["name"][i]
        to_email_data = data_file["email"][i]

        name_list.append(name_data)
        to_email_list.append(to_email_data)
    i += 1

# If above step is true, pick a random letter from letter templates and replace the [NAME] with the person's actual
# name from birthdays.csv. Do it for all the eligible people.
num = random.randint(1, 3)
if len(name_list) == 0:
    print("Skip")
else:
    birthday_messages_list = []
    for name in name_list:
        with open(f"letter_templates/letter_{num}.txt", "r") as file:
            file_data = file.read()
            updated_file_data = file_data.replace("[NAME]", f"{name}")
            birthday_messages_list.append(updated_file_data)

    # Send the letterS generated to people's email address.
    for i in range(len(birthday_messages_list)):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs=to_email_list[i], msg=f"Subject:Happy Birthday!\n\n{birthday_messages_list[i]}")
