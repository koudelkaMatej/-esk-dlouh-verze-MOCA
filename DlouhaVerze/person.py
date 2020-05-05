# -*- coding: utf-8 -*-

import os

class Person:
	def __init__(self, **kwargs):
            self.name = kwargs["name"]
            self.edu = kwargs["edu"]
            self.age = kwargs["age"]
            self.sex = kwargs["sex"]
            self.study = kwargs["study"]

	def info(self):
            return self.__dict__

        def save_results(self, tests):
            csv_name_file = open("/sdcard/vysledky/{2}/{0}_{1}.csv".format(self.name.replace(" ","_"), 
                                                                   self.age, self.study), "w")
            if os.path.exists("/sdcard/vysledky/{0}/komplet.csv".format(self.study)):
                csv_all_file = open("/sdcard/vysledky/{0}/komplet.csv".format(self.study), "a")
            else:
                csv_all_file = open("/sdcard/vysledky/{0}/komplet.csv".format(self.study), "w")
                csv_all_file.write("\t".join(["Jméno", "Pohlaví", "Věk", "Vzdělání"]) + "\t")
                for desc, test_list in tests.values():
                    csv_all_file.write(desc + "\t")

                csv_all_file.write("\n")

            
            csv_name_file.write("\t".join(["Jméno", "Pohlaví", "Věk", "Vzdělání"]) + "\n")
            csv_name_file.write("\t".join([self.name, self.sex, self.age, self.edu]) + "\n")
            csv_name_file.write("\t\t\t\n")
            
            csv_all_file.write("\t".join([self.name, self.sex, self.age, self.edu]) + "\t")
            
            for desc, test_list in tests.values():
                csv_name_file.write("\t".join([desc, "Celkem: ", 
                               str(sum([t.points for t in test_list]))]) + "\n")
                csv_all_file.write(str(sum([t.points for t in test_list])) + "\t")
                for test in test_list:
                    if test.desc != None:
                        csv_name_file.write("\t".join([test.desc, str(test.result())]) + "\n")
                                     
                csv_name_file.write("\t\t\t\n")

            
            csv_all_file.write("\n")
            csv_all_file.close()
            csv_name_file.close()



    
