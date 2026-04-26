hrs = float(input("Enter Hours: "))
rte = float(input("Enter Rate: "))

total_pay = 0
if hrs > 40:
    overtime_rate = rte * 1.5
    overtime_hours = hrs - 40

    total_pay = (40 * rte) + (overtime_hours * overtime_rate)
else:
    total_pay = rte * hrs

print(total_pay)

