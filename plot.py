import matplotlib.pyplot as plt
import json

with open('aggregated_data.json') as file:
    aggregated_data = json.load(file)

gender_data = aggregated_data['gender']

labels = gender_data.keys()
values = gender_data.values()

plt.pie(values, labels=labels, autopct='%1.1f%%')
plt.title('Number of Appointments by Gender')


plt.show()
