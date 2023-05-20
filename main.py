import configparser
import json



simtime = 5



class FantasyLandEconomy:
    
    
    def __init__(self, config_section):
        self.bank = int(config_section['bank'])
        self.population = int(config_section['population'])
        self.workforce = int(config_section['workforce'])
        self.production = int(config_section['production'])
        self.resources = int(config_section['resources'])
        self.resource_extraction_rate = float(config_section['resource_extraction_rate'])
        self.investment_rate = float(config_section['investment_rate'])
        self.export = int(config_section['export'])
        self.import_ = int(config_section['import'])
        self.tax_rate = float(config_section['tax_rate'])
        self.government_spending_p = int(config_section['government_spending']) / 100
        self.price_level = float(config_section['price_level'])
        self.inflation_rate = float(config_section['inflation_rate'])
        self.transfer_payments = int(config_section['transfer_payments'])
        self.consumption_p = int(config_section['consumption_p']) / 100
        self.minconsume = int(config_section['min_consume'])



    def calculate_gdp(self):
        self.gdp = self.production - self.import_ + self.export



    def calculate_income(self):
        self.income = self.gdp - (self.gdp * self.tax_rate) + self.transfer_payments



    def calculate_unemployment_rate(self):
        self.unemployment_rate = (self.population - self.workforce) / self.population



    def calculate_investment(self):
        self.investment = self.investment_rate * self.gdp



    def calculate_trade_balance(self):
        self.trade_balance = self.export - self.import_



    def calculate_total_consumption(self):
        self.total_consumption = (self.consumption_p * self.income) + (self.government_spending_p * self.income)
        if self.total_consumption <= self.minconsume:
            self.total_consumption = self.minconsume


    def calculate_inflation(self):
        self.price_level += self.inflation_rate



    def simulate_year(self, year, outtmp):
        self.year = year
        self.outtmp = outtmp
        
        
        self.calculate_gdp()
        self.calculate_income()
        self.calculate_unemployment_rate()
        self.calculate_investment()
        self.calculate_trade_balance()
        self.calculate_total_consumption()
        self.calculate_inflation()
            
        if self.year >= 1:
            last_year = self.outtmp[self.year - 1]
            self.bank = (
                (last_year["bank"]) + (self.income -
                last_year["total_consumption"]))
        elif self.year == 0:
            self.bank += self.income
                
        self.consumption = (
            self.consumption_p *
            self.income)
                
        self.gov_spend = (
            self.government_spending_p *
            self.income)


        print("Year:", self.year)
        print("Bank:", self.bank)
        print("GDP:", self.gdp)
        print("Income:", self.income)
        print("Unemployment Rate:", self.unemployment_rate)
        print("Investment:", self.investment)
        print("Trade Balance:", self.trade_balance)
        print("Total Consumption:", self.total_consumption)
        print("Inflation Rate:", self.inflation_rate)
        
        outdict = {
            "bank": self.bank,
            "gdp": self.gdp,
            "income": self.income,
            "unemployment": self.unemployment_rate,
            "invest": self.investment,
            "trade": self.trade_balance,
            "total_consumption": self.total_consumption,
            "inflation": self.inflation_rate
            }
            
        return outdict





def read_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config





# Beispielaufruf
config = read_config('config.ini')
out = {}





for section in config.sections():
    fantasy_land = FantasyLandEconomy(config[section])
    outtmp = []
    out[str(section)] = []
    for i in range(0, simtime):
        tmp = fantasy_land.simulate_year(i, outtmp)
        tmp["year"] = i
        print(tmp)
        outtmp.append(tmp)
        
    out[str(section)] = outtmp
        
   
    
     
      
        
print("----------------------\n----------------------\n")
print(json.dumps(out, sort_keys=True, indent=4))

