from upload_drivers import update_dim_drivers
from upload_payments import update_fact_payments
from upload_waybills import update_fact_waybills
from upload_cars import update_dim_cars


# 1. payments
print('fact_payments start update')
if update_fact_payments() == []:
    print('fact_payments succesfully updated')
    
# 2. clients

# 3. drivers
print('Dim_drivers start update')
if update_dim_drivers() == 'OK':
    print('Dim_drivers succesfully updated')

# 4. cars
print('dim_cars start update')
if update_dim_cars() == 'OK':
    print('dim_cars succesfully updated')
    
# 5. waybills
print('fact_waybills start update')
if update_fact_waybills() == 'OK':
    print('fact_waybills succesfully updated')
    
# 6. rides
