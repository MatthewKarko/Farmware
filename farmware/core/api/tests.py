from django.test import TestCase
from .models import Organisation, Team,AreaCode,Produce,Stock,Supplier,Customer,Order,OrderStockStock,ProduceVariety,ProduceQuantitySuffix,StockPickers
from django_test_migrations.migrator import Migrator

# Create your tests here.
class OrganisationTestCases(TestCase):
    def setUp(self):
        Organisaton.objects.create(name="Farmone",logo="goat")
        Organisaton.objects.create(name="Farmtwo",logo="sheep")
    def test_organisation_(self):
        farmone = Organisation.objects.get(name="Farmone")
        farmtwo = Organisation.objects.get(name="Farmtwo")
        self.assertEqual(farmone.name, "Farmone")
        self.assertEqual(farmone.logo, "goat")
        self.assertEqual(farmone.name, "Farmtwo")
        self.assertEqual(farmone.logo, "sheep")
class   UserTestCases(TestCase):
    def setUp(self):
        User.objects.create(email="example@gmail.com",first_name="first_name",last_name="last_name",organisation="organisation",password="password")
    def test_User(self):
        user = User.objects.get(name="first_name")
        self.assertEqual(user.email, "example@gmail.com")
        self.assertEqual(user.last_name,"last_name")
        self.assertEqual(user.organisation,"organisation")
        self.assertEqual(user.password,"password")
class   AreaCodeTestCases(TestCase):
    def setUp(self):
        AreaCode.objects.create( area_code=204,description="just another area code")
    def test_AreaCode(self):
        areacode = AreaCode.objects.get(area_code=204)
        self.assertEqual(areacode.description,"just another area code")
class  CustomerTestCases(TestCase):
    def setUp(self):
        Customer.objects.create(name = "Henry",phone_number="9191223445" )
    def test_Customer(self):
        customer = Customer.objects.get(name = "Henry")
        self.assertEqual(customer.phone_number,"9191223445")
class  SupplierTestCases(TestCase):
    def setUp(self):
        Supplier.objects.create(name = "john",phone_number = "1234567891")
    def test_Supplier(self):
        supplier = Supplier.objects.get(name = "Henry")
        self.assertEqual(supplier.phone_number,"1234567891")
class ProduceVarietyTestCases(TestCase):
    def setUp(self):
        produce=Produce.objects.create(name="eggs")
        ProduceVariety.objects.create(produce_id=produce,variety="brown")
    def test_ProduceVariety(self):
        producevariety=ProduceVariety.objects.get(variety="brown")
        self.assertEqual(producevariety.variety,"brown")
class ProduceQuantitySuffixTestCases(TestCase):
    def setUp(self):
        produce=Produce.objects.create(name="eggs")
        ProduceQuantitySuffix.objects.create(produce_id=produce,suffix="lorem ipsum",base_equivalent=5.0)
    def test_ProduceQuantitySuffix(self):
        producequantitysuffix=ProduceQuantitySuffix.objects.get(suffix="lorem ipsum")
        self.assertEqual(producequantitysuffix.base_equivalent,5.0)
class StockTestCases(TestCase):
    def setUp(self):
        produce=Produce.objects.create(name="eggs")
        producequantitysuffix=ProduceQuantitySuffix.objects.create(produce_id=produce,suffix="lorem ipsum",base_equivalent=5.0)
        producevariety=ProduceVariety.objects.create(produce_id=produce,variety="brown")
        supplier=Supplier.objects.create(name = "john",phone_number = "1234567891")
        areacode=AreaCode.objects.create( area_code=204,description="just another area code")
        Stock.objects.create(produce_id =produce,
    variety_id =producevariety,
    quantity = 6.0,
    quantity_suffix_id =producequantitysuffix,
    supplier_id =supplier,
    date_seeded = "2022-10-25",
    date_planted = "2022-10-26",
    date_picked = "2022-10-27",
    ehd = "2022-10-28" ,
    date_completed ="2022-10-29",
    area_code =areacode )
    def test_(self):
        stock.objects.get(area_code =areacode)
        self.assertEqual(stock.ehd,"2022-10-28")
class  OrderStockTestCases(TestCase):
    def setUp(self):
        produce=Produce.objects.create(name="eggs")
        producequantitysuffix=ProduceQuantitySuffix.objects.create(produce_id=produce,suffix="lorem ipsum",base_equivalent=5.0)
        producevariety=ProduceVariety.objects.create(produce_id=produce,variety="brown")
        supplier=Supplier.objects.create(name = "john",phone_number = "1234567891")
        areacode=AreaCode.objects.create( area_code=204,description="just another area code")
        stock=Stock.objects.create(produce_id =produce,
    variety_id =producevariety,
    quantity = 6.0,
    quantity_suffix_id =producequantitysuffix,
    supplier_id =supplier,
    date_seeded = "2022-10-25",
    date_planted = "2022-10-26",
    date_picked = "2022-10-27",
    ehd = "2022-10-28" ,
    date_completed ="2022-10-29",
    area_code =areacode )
        customer=Customer.objects.create(name = "Henry",phone_number="9191223445" )
        order=Order.objects.create(customer_id= customer)
        OrderStock.objects.create( order_id =order,
    stock_id =stock ,quantity = 10.0,quantity_suffix_id =producequantitysuffix,invoice_number="7584")
    def test_OrderStock(self):
        orderstock = OrderStock.objects.get(invoice_number="7584")
        self.assertEqual(orderstock.invoice_number,"7584")
class TeamTestCases(TestCase):
    def setUp(self):
        organisation=Organisaton.objects.create(name="Farmone",logo="goat")
        Team.objects.create(category ="j",name = "jack",organisation = organisation)
    def test_Team(self):
        team=Team.objects.get(category ="j")
        self.assertEqual(team.name,"jack")
###class StockPickersTestCases(TestCase):
    #def setUp(self):
    #    produce=Produce.objects.create(name="eggs")
    #    producequantitysuffix=ProduceQuantitySuffix.objects.create(produce_id=produce,suffix="lorem ipsum",base_equivalent=5.0)
    #    producevariety=ProduceVariety.objects.create(produce_id=produce,variety="brown")
    #    supplier=Supplier.objects.create(name = "john",phone_number = "1234567891")
    #    areacode=AreaCode.objects.create( area_code=204,description="just another area code")
    #    stock=Stock.objects.create(produce_id =produce,
    #variety_id =producevariety,
    #quantity = 6.0,
    #quantity_suffix_id =producequantitysuffix,
    #supplier_id =supplier,
    #date_seeded = "2022-10-25",
    #date_planted = "2022-10-26",
    #date_picked = "2022-10-27",
    #ehd = "2022-10-28" ,
    #date_completed ="2022-10-29",
    #area_code =areacode )
    #    customer=Customer.objects.create(name = "Henry",phone_number="9191223445" )

    #    user=User.objects.create(email="example@gmail.com",first_name="first_name",last_name="last_name",organisation="organisation",password="password")
    #     stocks = models.ManyToManyField(stock)
    #    StockPickers.objects.create(stock_id=stocks,user_id=user)

    #def test_Team(self):
    #    stockpickers=StockPickers.objects.get()
    #    self.assertEqual()
###
