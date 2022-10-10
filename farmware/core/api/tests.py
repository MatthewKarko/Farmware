from django.test import TestCase
#from . import models
from .models.organisation import *
from .models.team import *
from .models.areacode import *
from .models.produce import *
from .models.stock import *
from .models.supplier import *
from .models.customer import *
from .models.order import *
from django_test_migrations.migrator import Migrator
from django.db import IntegrityError
from django.core.exceptions import ValidationError

# Create your tests here.
class OrganisationTestCases(TestCase):
    def setUp(self):
        Organisation.objects.create(name="Farmone",logo="goat")
        Organisation.objects.create(name="Farmtwo",logo="sheep")
    def test_organisation_(self):
        farmone = Organisation.objects.get(name="Farmone")
        farmtwo = Organisation.objects.get(name="Farmtwo")
        self.assertEqual(farmone.name, "Farmone")
        self.assertEqual(farmone.logo, "goat")
        self.assertEqual(farmtwo.name, "Farmtwo")
        self.assertEqual(farmtwo.logo, "sheep")
    def test_organisation2(self):
        with self.assertRaises(Exception):
            self.assertRaises(Organisation.objects.create(name=4,logo="sheep"))
    def test_organisation3(self):
        with self.assertRaises(ValidationError):
            Organisation.objects.create(name="anotherna",logo=5.0)
            raise ValidationError("error")
    def test_organisation4(self):
        with self.assertRaises(ValidationError):
            Organisation.objects.create(name="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas commodo cursus condimentum. Donec pulvinar odio sed enim tristique, sit amet tristique dolor volutpat. Proin nec mauris gravida libero scelerisque consectetur non at sapien. Nam et felis nibh. Morbi eget augue sit amet nisl elementum congue. Nulla vel laoreet velit. Nullam est neque, efficitur sodales suscipit ac, vulputate eget velit. Donec.",logo="i")
            raise ValidationError("Error")
    def test_organisation5(self):
        with self.assertRaises(ValidationError):
            Organisation.objects.create(name="a",logo="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas commodo cursus condimentum. Donec pulvinar odio sed enim tristique, sit amet tristique dolor volutpat. Proin nec mauris gravida libero scelerisque consectetur non at sapien. Nam et felis nibh. Morbi eget augue sit amet nisl elementum congue. Nulla vel laoreet velit. Nullam est neque, efficitur sodales suscipit ac, vulputate eget velit. Donec.")
            raise ValidationError("error")

class   AreaCodeTestCases(TestCase):
    def setUp(self):
        AreaCode.objects.create( area_code="204",description="just another area code")
    def test_AreaCode1(self):
        areacodee = AreaCode.objects.get(area_code="204")
        self.assertEqual(areacodee.description,"just another area code")
    def test_AreaCode2(self):
        areacode = AreaCode.objects.get(area_code="204")
        with self.assertRaises(IntegrityError):
            AreaCode.objects.create( area_code="204",description="just another area code")
    def  test_AreaCode3(self):
        areacode = AreaCode.objects.get(area_code="204")
        with self.assertRaises(ValidationError):
            AreaCode.objects.create( area_code="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque egestas, leo in mattis suscipit, ante arcu gravida sapien, sit amet varius quam mi vitae lectus. Nullam in aliquam odio. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. In quis imperdiet purus. Curabitur quis laoreet tellus. Quisque gravida vitae arcu molestie interdum. Phasellus dictum urna est, ut feugiat turpis gravida sed. Pellentesque ut consectetur ante. Sed scelerisque mauris quis mi condimentum, a consectetur massa ullamcorper. Ut condimentum tellus ac lorem luctus ultrices. In nibh est, placerat ac dignissim sit amet, dapibus in libero. Quisque lobortis lacus et laoreet hendrerit. Quisque vel placerat mi. Suspendisse vitae sodales justo, sed dapibus sapien. Vestibulum bibendum fermentum fringilla. Aliquam vitae neque orci.Aenean euismod lacus id orci rutrum suscipit. In sit amet tortor vel mauris luctus lacinia. Suspendisse potenti. Mauris lorem sem, ornare in justo commodo, vulputate condimentum urna. Nam fermentum ipsum vestibulum vehicula cursus. Mauris iaculis ut risus a imperdiet. Suspendisse porttitor, sem sed laoreet luctus, est tellus bibendum felis, a dignissim justo velit a ante. Sed placerat justo eros, at viverra ex imperdiet ac. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Donec id odio nunc. Nulla tincidunt rhoncus tellus, sit amet maximus lectus blandit sit amet. Donec interdum vitae sapien sit amet varius. Proin imperdiet mauris eget cursus rhoncus. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent id libero erat.Pellentesque gravida, lectus vitae porttitor dapibus, nisl nunc suscipit ante, eu varius sem dolor id ante. Pellentesque porta feugiat ipsum, eget pharetra dolor dapibus vitae. Donec gravida eleifend sem, ac dictum augue elementum eget. Ut accumsan maximus purus, sed aliquet tellus interdum vel. Praesent iaculis diam et neque rhoncus placerat. Mauris consectetur vel leo nec suscipit. Praesent placerat, felis facilisis.",description="ss")
            raise ValidationError("error")
    def  test_AreaCode4(self):
        areacode = AreaCode.objects.get(area_code="204")
        with self.assertRaises(ValidationError):
            AreaCode.objects.create( area_code="203", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque egestas, leo in mattis suscipit, ante arcu gravida sapien, sit amet varius quam mi vitae lectus. Nullam in aliquam odio. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. In quis imperdiet purus. Curabitur quis laoreet tellus. Quisque gravida vitae arcu molestie interdum. Phasellus dictum urna est, ut feugiat turpis gravida sed. Pellentesque ut consectetur ante. Sed scelerisque mauris quis mi condimentum, a consectetur massa ullamcorper. Ut condimentum tellus ac lorem luctus ultrices. In nibh est, placerat ac dignissim sit amet, dapibus in libero. Quisque lobortis lacus et laoreet hendrerit. Quisque vel placerat mi. Suspendisse vitae sodales justo, sed dapibus sapien. Vestibulum bibendum fermentum fringilla. Aliquam vitae neque orci.Aenean euismod lacus id orci rutrum suscipit. In sit amet tortor vel mauris luctus lacinia. Suspendisse potenti. Mauris lorem sem, ornare in justo commodo, vulputate condimentum urna. Nam fermentum ipsum vestibulum vehicula cursus. Mauris iaculis ut risus a imperdiet. Suspendisse porttitor, sem sed laoreet luctus, est tellus bibendum felis, a dignissim justo velit a ante. Sed placerat justo eros, at viverra ex imperdiet ac. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Donec id odio nunc. Nulla tincidunt rhoncus tellus, sit amet maximus lectus blandit sit amet. Donec interdum vitae sapien sit amet varius. Proin imperdiet mauris eget cursus rhoncus. Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent id libero erat.Pellentesque gravida, lectus vitae porttitor dapibus, nisl nunc suscipit ante, eu varius sem dolor id ante. Pellentesque porta feugiat ipsum, eget pharetra dolor dapibus vitae. Donec gravida eleifend sem, ac dictum augue elementum eget. Ut accumsan maximus purus, sed aliquet tellus interdum vel. Praesent iaculis diam et neque rhoncus placerat. Mauris consectetur vel leo nec suscipit. Praesent placerat, felis facilisis.")
            raise ValidationError("error")
class  CustomerTestCases(TestCase):
    def setUp(self):
        Customer.objects.create(name = "Henry",phone_number="9191223445" )

    def test_Customer1(self):
        customer = Customer.objects.get(name = "Henry")
        self.assertEqual(customer.phone_number,"9191223445")
    def test_Customer2(self):
        customer = Customer.objects.get(name = "Henry")
        with self.assertRaises(IntegrityError):
            Customer.objects.create(name = "Henr",phone_number="91912234452" )
            raise IntegrityError("error")
    def test_Customer3(self):
        customer = Customer.objects.get(name = "Henry")
        with self.assertRaises(ValidationError):
            Customer.objects.create(name = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas commodo cursus condimentum. Donec pulvinar odio sed enim tristique, sit amet tristique dolor volutpat. Proin nec mauris gravida libero scelerisque consectetur non at sapien. Nam et felis nibh. Morbi eget augue sit amet nisl elementum congue. Nulla vel laoreet velit. Nullam est neque, efficitur sodales suscipit ac, vulputate eget velit. Donec.",phone_number="9191223445")
            raise ValidationError("error")
class  SupplierTestCases(TestCase):
    def setUp(self):
        Supplier.objects.create(name = "john",phone_number = "1234567891")
    def test_Supplier1(self):
        supplier = Supplier.objects.get(name = "john")
        self.assertEqual(supplier.phone_number,"1234567891")
    def test_Supplier2(self):
        with self.assertRaises(ValidationError):
            Supplier.objects.create(name = "john",phone_number = "12345678911")
            raise ValidationError("error")

    def test_Supplier3(self):
        with self.assertRaises(ValidationError):
            Supplier.objects.create(name ="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean et justo ut turpis suscipit mattis ac ac lorem. Aenean molestie nisi et ullamcorper condimentum. Integer at congue nulla, quis elementum mauris. Mauris luctus nisl elementum massa vehicula, ut maximus purus pellentesque. Curabitur consectetur tincidunt malesuada. Sed dignissim ipsum nec urna tincidunt lobortis. Vestibulum porta finibus tincidunt. Nunc a odio porta, aliquam odio ut, commodo risus. Duis quis risus in nulla accumsan tempus dapibus et elit. Integer sed est at ligula commodo tristique.Sed et pulvinar mauris. Vivamus fringilla odio a ex porttitor, nec dapibus nisi vestibulum. Phasellus sed nisi velit. Vestibulum tempus justo dolor, et pellentesque urna molestie ut. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Curabitur viverra tincidunt hendrerit. Maecenas accumsan est vitae est faucibus facilisis. Sed nec quam in orci vehicula varius in ut urna. Proin lacus nibh, suscipit a elementum nec.",phone_number = "1234567891")
            raise ValidationError("error")
    def test_Supplier4(self):
         with self.assertRaises(ValidationError):
             Supplier.objects.create(name = 2,phone_number = "1234567891")
             raise ValidationError("error")
    def test_Supplier5(self):
         with self.assertRaises(ValidationError):
             Supplier.objects.create(name = "name2",phone_number = 1234567891)
             raise ValidationError("error")
    def test_Supplier6(self):
        try:
             supplier = Supplier.objects.create(name = 2,phone_number = 12345678919)
             supplier.clean_fields()
        except ValidationError:
             raise ValidationError("error")

class ProduceVarietyTestCases(TestCase):
    def setUp(self):
        produce=Produce.objects.create(name="eggs")
        ProduceVariety.objects.create(produce_id=produce,variety="brown")
    def test_ProduceVariety(self):
        producevariety=ProduceVariety.objects.get(variety="brown")
        produce2=Produce.objects.create(name="chicken")
        self.assertEqual(producevariety.variety,"brown")
        with self.assertRaises(ValidationError):
            ProduceVariety.objects.create(produce_id=produce2,variety="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean et justo ut turpis suscipit mattis ac ac lorem. Aenean molestie nisi et ullamcorper condimentum. Integer at congue nulla, quis elementum mauris. Mauris luctus nisl elementum massa vehicula, ut maximus purus pellentesque. Curabitur consectetur tincidunt malesuada. Sed dignissim ipsum nec urna tincidunt lobortis. Vestibulum porta finibus tincidunt. Nunc a odio porta, aliquam odio ut, commodo risus. Duis quis risus in nulla accumsan tempus dapibus et elit. Integer sed est at ligula commodo tristique.Sed et pulvinar mauris. Vivamus fringilla odio a ex porttitor, nec dapibus nisi vestibulum. Phasellus sed nisi velit. Vestibulum tempus justo dolor, et pellentesque urna molestie ut. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Curabitur viverra tincidunt hendrerit. Maecenas accumsan est vitae est faucibus facilisis. Sed nec quam in orci vehicula varius in ut urna. Proin lacus nibh, suscipit a elementum nec")
            raise ValidationError("error")

class ProduceQuantitySuffixTestCases(TestCase):
    def setUp(self):
        produce=Produce.objects.create(name="eggs")
        ProduceQuantitySuffix.objects.create(produce_id=produce,suffix="lorem ipsum",base_equivalent=5.0)
    def test_ProduceQuantitySuffix(self):
        producequantitysuffix=ProduceQuantitySuffix.objects.get(suffix="lorem ipsum")
        self.assertEqual(producequantitysuffix.base_equivalent,5.0)
        produce2=Produce.objects.create(name="eggs")
        with self.assertRaises(ValidationError):
            ProduceQuantitySuffix.objects.create(produce_id=produce2,suffix="ipsumLorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur cursus lectus id est dignissim dapibus. Integer mollis sodales urna, quis consectetur enim aliquam nec. Fusce nec velit nec lacus sollicitudin bibendum a ut augue. Fusce commodo lacus vel enim vulputate finibus. Integer aliquam quam at lorem imperdiet dignissim. Suspendisse volutpat.",base_equivalent=5.0)
            raise ValidationError("error")
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
    def test_Stock1(self):
        stock=Stock.objects.get(quantity=6.0)
        #d=new Date("2022-10-28")
        #self.assertEqual(stock.ehd,d)
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
        organisation=Organisation.objects.create(name="Farmone",logo="goat")
        Team.objects.create(category ="j",name = "jack",organisation = organisation)
    def test_Team(self):
        team=Team.objects.get(category ="j")
        self.assertEqual(team.name,"jack")
        organisation2=Organisation.objects.create(name="Farmon",logo="goa")
        with self.assertRaises(ValidationError):
            Team.objects.create(category ="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis euismod gravida. Vestibulum quam lacus, faucibus ac dui nec, hendrerit lobortis arcu. Ut vel lorem at enim dignissim porttitor in nec neque. Mauris lobortis justo lorem, id venenatis dui laoreet vel. Quisque egestas neque quis erat porttitor fermentum. Proin cursus, lorem non auctor aliquam, turpis neque tincidunt sem, vitae maximus massa dolor ut diam. Nam euismod urna sed leo vestibulum ultrices. Donec tempus fringilla feugiat. Nullam faucibus mattis diam, in sagittis lacus aliquam eget. Mauris eu ligula fermentum, bibendum enim id, sodales turpis. Praesent sed risus felis. Vivamus ut ultrices nisl.Ut luctus purus neque, eget blandit augue consectetur at. Etiam eleifend cursus tortor, ut venenatis lectus laoreet sollicitudin. Nunc at elementum magna. Integer ut scelerisque arcu, ac pellentesque lorem. Donec rutrum porttitor consectetur. Nunc nunc enim, sollicitudin mollis maximus non, lacinia at neque. Curabitur ultrices tincidunt pharetra. Vestibulum vitae.",name = "jack",organisation = organisation2)
            raise ValidationError("error")
    def test_team2(self):
        organisation2=Organisation.objects.create(name="Farmon",logo="goa")
        with self.assertRaises(ValidationError):
            Team.objects.create(category ="Jack",name = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi convallis euismod gravida. Vestibulum quam lacus, faucibus ac dui nec, hendrerit lobortis arcu. Ut vel lorem at enim dignissim porttitor in nec neque. Mauris lobortis justo lorem, id venenatis dui laoreet vel. Quisque egestas neque quis erat porttitor fermentum. Proin cursus, lorem non auctor aliquam, turpis neque tincidunt sem, vitae maximus massa dolor ut diam. Nam euismod urna sed leo vestibulum ultrices. Donec tempus fringilla feugiat. Nullam faucibus mattis diam, in sagittis lacus aliquam eget. Mauris eu ligula fermentum, bibendum enim id, sodales turpis. Praesent sed risus felis. Vivamus ut ultrices nisl.Ut luctus purus neque, eget blandit augue consectetur at. Etiam eleifend cursus tortor, ut venenatis lectus laoreet sollicitudin. Nunc at elementum magna. Integer ut scelerisque arcu, ac pellentesque lorem. Donec rutrum porttitor consectetur. Nunc nunc enim, sollicitudin mollis maximus non, lacinia at neque. Curabitur ultrices tincidunt pharetra. Vestibulum vitae.",organisation = organisation2)
            raise ValidationError("error")

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
