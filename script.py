#%pip install bs4
#%pip install lxml
import requests
#Allow to parse(analyse) the page or HTML page:
from bs4 import BeautifulSoup
#to write into the csv file:
import csv
from itertools import zip_longest
import re

#____________________________________________________________
#                   < for loop using urloop >
#____________________________________________________________

urloop = ["https://laurentferrier.ch/collections/classic",
                     "https://laurentferrier.ch/collections/square",
                     "https://laurentferrier.ch/collections/grand-sport",
                    "https://laurentferrier.ch/collections/sport"]
watch_url = []
parent_model =[]
specific_model = []
nickname = []
for url in urloop:
    html = requests.get(url)

    soup_html = BeautifulSoup(html.content,'html.parser' )
    #loop = slop.find_all('div',{'class':'ProductListWrapper'})
    link = soup_html.find_all('div',{'class':"ProductItem__Info ProductItem__Info--center"})

    for div in link :
        a = div.find('a')
        b = 'https://laurentferrier.ch'+a.attrs['href']
        #print(b)
        watch_url.append(b)

    product_name = soup_html.find_all('h2',{'class':"ProductItem__Title Heading"})
    for category in product_name:
        category = category.find('a')
        x1 = category.text.split(' ')
        parent_model.append(x1[0])
        x2 = category.text.split('  ')
        specific_model.append(x2[0])
        x3 = x2[1].split('\n')
        nickname.append(x3[0])


print(r"\n\nwatch_url:",watch_url)

#___________________________________________________________
#________________________ find_case ________________________
#___________________________________________________________
def find_case (list,case_material,case_diamete,case_thickness,case_water_resistance):
  start_inx_case = list.find("CASE")
  end_inx_case = list.find("MOVEMENT")
  case = list[start_inx_case:end_inx_case]

  #---------------
  #_Find MATERIAL:
  str_mat = case.find("Material")
  end_mat = case.find("Di")
  material = (case[str_mat:end_mat]).split(":")[1].replace(u'\xa0', u' ')
  #print(material)
  case_material.append(material)#(material.split(":")[1]).replace(u'\xa0', u' '))

  #---------------
  #_Find DIAMETE:
  s_diam = case.find("Di")
  e_diam = case.find("Thickness")
  diameter =  (case[s_diam:e_diam]).split(":")[1].replace(u'\xa0', u' ')
  case_diamete.append(diameter)

  #---------------
  #_Find THICKNESS:
  s_thick = case.find("Thickness")
  if "Water resistance" in case :
    e_thick = case.find("Water resistance")
  elif "Features"in case :
    e_thick = case.find("Features")

  thickness = (case[s_thick:e_thick]).split(":")[1].replace(u'\xa0', u' ')
  case_thickness.append(thickness)

  #---------------
  #_Find the WATER RESISTANCE:
  #_The name of category wrote in 2 ways :

  #_1.Water resistance:
  if "Water resistance" in case :
    s_waterR = case.find("Water resistance")
    e_waterR = len(case)
    waterResistance =  (case[s_waterR:e_waterR]).split(":")[1].replace(u'\xa0', u' ').replace(u'\n',u'')

  #_2.Features:
  #_It contain a descrption, so we cut data[ after (Features:) -->  the end of word (meters)]
  elif "Features"in case :
    f = case.find("Features")
    s_waterR = (case.find("meters"))-5  # the index of start range, ==> s_water is index of 1 in 120.
    #_use (cut_case)to find the range, instead of (case)
    cut_case = case[f:s_waterR].split(":")[1] #.replace(u'\xa0', u' ') # ==> output as [asdfghj 120 meters]
    #print(cut_case) # print all things BETWEEN ['Features , 120'] to check
    e_waterR = (case.find("meters"))+6  # the last index we want to stop into. ==> e_water is last index meters.
    waterResistance =  (case[s_waterR:e_waterR])


  case_water_resistance.append(waterResistance)


  return case_material,case_diamete, case_thickness, case_water_resistance

#___________________________________________________________
#______________________ find_movement ______________________
#___________________________________________________________

def find_movement (list,mov_jewels,mov_frequency,mov_power_reserve,mov_movement,mov_caliber):
  #extract the items that related to MOVEMENT Menu
  start_mov = list.find("MOVEMENT")     #_it the start index that contains in movement
  if "STRAP" in list:
    end_mov = list.find("STRAP")        #_it the last index in movement stop before STRAP, Mov(--save in mov--)Strap
  elif "BRACELET" in list:
    end_mov = list.find("BRACELET")     #_Mov|--only save in mov--|Bracelet
  movement = list[start_mov+8:end_mov]  #_all item of movement save here
  #print(movement)

  #_______________ Jewels _______________
  #_Find the number of jewels:
  #1_Before, there is 2 words of "Frequency"
  #  --> we need another substring from jewels to the end of Movement part.
  sub = movement.find('jewels:')
  #print(f"start inx feature: {sub}")
  sub_onlyJewels = movement[sub:len(movement)]
  #print(sub_onlyJewels)
  #--------------
  #2_Find the number of jewels: 196  98
  #_(s_jew) = start index of substring
  #_(e_jew) = last index of substring
  s_jew = sub_onlyJewels.find('jewels:')
  if "Frequency" in sub_onlyJewels:
    e_jew = sub_onlyJewels.find("Frequency")  #jewels:(--save in jewels--)Frequency
  elif "Additional" in sub_onlyJewels:
    e_jew = sub_onlyJewels.find("Additional") #jewels:(--save in jewels--)Additional

  #print(f"end inx feature: {e_jew}")
  jewels = sub_onlyJewels[s_jew+7:e_jew].replace(u'\xa0', u' ') # the number of jewels save here
  #print(f"num Jewels = {jewels}")
  mov_jewels.append(jewels)

  #_______________ Frequency _______________
  s_freq = list.find('Frequency:') #start index
  e_freq = list.find('Power')      #end(last) index
  frequency = list[s_freq+11: e_freq]  # the value of feature saved here
  mov_frequency.append(frequency.replace(u'\xa0', u' '))

  #_______________ Power Reserve _______________
  s_power = movement.find('Power') #start index
  if "Components" in movement :
    e_power = movement.find("Components")
  else:
    e_power = len(movement)  #end(last) index
  power_reserve = movement[s_power+14: e_power] # the value of feature saved here
  mov_power_reserve.append(power_reserve.replace(u'\xa0' , u' ').replace(u'\n' , u''))
  #print(mov_power_reserve)

  #_______________ Mov Calibre _______________
  if "Additional Features" not in movement:
    s_mov_feature = movement.find("Features:") # start index feaaure
    e_mov_feature = movement.find("Di") # last index feature
    mov_features = movement[s_mov_feature+9:e_mov_feature] .replace(u'\xa0', u' ') #.split(". ")
    #print(mov_features)

    if "Calibre" or "calibre" in mov_features :
      calibre = mov_features.split(". ")[1]
      #print(calibre)
      mov_caliber.append(calibre)
    elif "Caliber" or "caliber" in mov_features :
      caliber = mov_features.split(". ")[1]
      #print(caliber)
      mov_caliber.append(caliber)

  elif "Model" in movement :
    s_mov_model = movement.find("Model") # start index feaaure
    e_mov_model = movement.find("Type") # last index feature
    mov_model = movement[s_mov_model+6:e_mov_model] .replace(u'\xa0', u' ')
    mov_caliber.append(mov_model)

  else:
    mov_caliber.append(" ")

  #_______________ Mov Movement "Winding" _______________
  if "Additional Features" not in movement:
    #print(mov_features)
    mov_movement.append(mov_features)
  elif "Additional Features" in movement:
    s_mov_type = movement.find("Type") # start index feaaure
    e_mov_type = movement.find("Di") # last index feature
    mov_type_winding = movement[s_mov_type+5:e_mov_type] .replace(u'\xa0', u' ') #.split(". ")
    #print(mov_type_winding)
    mov_movement.append(mov_type_winding)

  return mov_jewels ,mov_frequency , mov_power_reserve ,mov_caliber, mov_movement


#___________________________________________________________
#________________________ find_dial ________________________
#___________________________________________________________

def find_dial (lst, dial_feature ,dial_color ):
  #extract the items that related to DIAL Menu
  start_inx_dial = lst.find("DIAL")
  end_inx_dial = lst.find("CASE")
  dial = lst[start_inx_dial:end_inx_dial]
  #print(dial)

  #____________ Feature ___________
  s_feature = dial.find("Indications:")
  if "Finishing:" in dial:
    e_feature = dial.find("Finishing:")
  elif "Material:" in dial:
    e_feature = dial.find("Material:")
  #_features var include the only dial features part
  features = dial[s_feature + 13:e_feature]
  dial_feature.append(features)
  #print(features)

  #____________ Dial color ____________
  #_Extract the color from dial menu
  #_If statements for the starting index
  if "Finishing" in dial:
    s_color = dial.find("Finishing:")
  elif "Material" in dial:
    s_color = dial.find("Material:")

  # IF statements for the ending index
  if 'Indices:' in dial:
    e_color = dial.find('Indices:')
  elif 'Hours markers:' in dial:
    e_color = dial.find('Hours markers:')
  elif 'Indexes:' in dial:
    e_color = dial.find('Indexes:')

  color = dial[s_color+10:e_color].replace("\xa0"," ")  # all item of dial_color
  dial_color.append(color)



  return dial_feature, dial_color


#____________________________________________________________
#                 < for loop using watch_url > 
#____________________________________________________________
images_url = []
refrences_watches = []
salary_watches = []
currency_watches = []
#-----------------------
type_w = []
brand_w = []
year_introduced_w =[]
short_description_w = []
marketing_name= []
style = []
made_in = []
case_shape = []
case_finish = []
caseback = []
between_lugs = []
lug_to_lug = []
bezel_material = []
bezel_color = []
crystal = []
weight = []
img_url_watches = []
#-----------------------
description =[]

case_material = []
case_diamete = []
case_thickness = []
case_water_resistance = []

mov_jewels =[]
mov_frequency =[]
mov_power_reserve =[]
mov_movement =[]
mov_caliber =[]

dial_feature = []
dial_color = []
dial_numerals = []

bracelet_material = []
bracelet_color = []
clasp_type = []
#----------------------------------------------------------
#I need a line to clear all things if we run again and again ??
for link in watch_url:
  result = requests.get(link)
  src = result.content
  soup_lxml = BeautifulSoup(src,"lxml")
  soup_html = BeautifulSoup(result.content, 'html.parser')

  noscript = soup_html.find_all("noscript")
  for img_url in noscript:
    try:
      x = 'https:'+ img_url.find('img').attrs['src']
      images_url.append(x)
      break
    except:
      pass


  #Find the refrence:
  refrence = (soup_lxml.find('span',{'class':'ProductMeta__SkuNumber'})).text
  refrences_watches.append(refrence)
  #rint(refrence.text)

  #Find the salary:
  salary_currency = (soup_lxml.find('span',{'class':'money'})).text.split(" ")
  salary = salary_currency[0]
  salary_watches.append(salary)

  #Find the currency:
  currency = salary_currency[1]
  currency_watches.append(currency)

  #Store empty string for some cloumns:
  brand_w.append("Laurent Ferrier")
  made_in.append("Switzerland")
  type_w.append(" ")
  year_introduced_w.append(" ")
  short_description_w.append(" ")
  short_description_w.append(" ")
  marketing_name.append(" ")
  style.append(" ")
  case_shape.append(" ")
  case_finish.append(" ")
  caseback.append(" ")
  between_lugs.append(" ")
  lug_to_lug.append(" ")
  bezel_material.append(" ")
  bezel_color.append(" ")
  crystal.append(" ")
  weight.append(" ")
  img_url_watches.append(" ")


#-----------------------------------------------------------------------
  #_Find all <h6> elements and <p> after it:
  strong_elements = soup_lxml.find_all('h6')
  #print(strong_elements)

  #_Find parent elements of <strong> elements
  parent_elements = [strong_element.parent for strong_element in strong_elements]

  #_Print the text content of the parent elements & store them in list
  lst=[]
  for index, parent_element in enumerate(parent_elements, start=1):
      lst = parent_element.text.strip()
#--------------------------------------------------
#-------------------------------------------------------------------------------
#_Extract Description for each watch:
  dindex_end = lst.find("DIAL")
  des = lst[0:dindex_end]
  description.append(des)
  #print(description)


#_Extract from Case (material , diameter, thickness ,water_resistance):
  case = find_case(lst,case_material,case_diamete,case_thickness,case_water_resistance)
  #print(case_water_resistance)
  #print(f"\nmaterial :{case_material}")

#_Extract from Movement (jewels, frequency, power reserve ,feature(winding), feature(calibre))
  movement = find_movement(lst,mov_jewels,mov_frequency,mov_power_reserve,mov_movement,mov_caliber)

#_Extract from Dial (feature, dial color, numerals(indicate))
  #print(link)
  dial = find_dial(lst, dial_feature ,dial_color)

#__ . __ . __ . __ . __ . __ . __ . __ . __ .
 # extract the Numerals from DIAL Menu:
  start = lst.find("DIAL")
  end = lst.find("CASE")
  Indices = lst[start:end]

  # start index
  if 'Indices:' in Indices:
    s = Indices.find('Indices:')
  elif 'Indexes:' in Indices:
    s = Indices.find('Indexes:')

  # end index
  if 'Hour and minute hands' in Indices:
    e = Indices.find('Hour and minute hands:')

  elif ' Hour markers' in Indices:
    e = Indices.find('Hour markers:')

  dial_numerals.append(Indices[s+9:e].replace("\xa0"," "))
  #print(dial_numerals)

#__ . __ . __ . __ . __ . __ . __ . __ . __ .
# Find bracelet_material &  bracelet_color:

  if 'STRAP' in lst:
    start_index1 = lst.find('STRAP') #[1279]
  elif 'BRACELET' in lst:
    start_index1 = lst.find('BRACELET')  # [1279]

  if 'CARE' in lst:
    end_index1 = lst.find('CARE')#[1393]
  else:
    end_index1 = len(lst)

  strap = lst[start_index1:end_index1]
  start_index2 = strap.find('Material:')
  end_index2 = strap.find('Buckle')
  extract_data = strap[start_index2+9:end_index2]
  bracelet_material.append(extract_data.replace('\xa0',' '))
  bracelet_color.append(extract_data.replace('\xa0',' '))

#__ . __ . __ . __ . __ . __ . __ . __ . __ .
  if 'STRAP' in lst:
    start_index1 = lst.find('STRAP') #[1279]
  if 'BRACELET' in lst:
    start_index1 = lst.find('BRACELET')  # [1279]

  if 'CARE' in lst:
    end_index1 = lst.find('CARE')#[1393]
  else:
    end_index1 = len(lst)

  BRACELET = lst[start_index1:end_index1]
    # start_index2 = BRACELET.find('Material:')
  start_index2 = BRACELET.find('Buckle')
  extract_data = BRACELET[start_index2+14:end_index1]
    # print(len(extract_data))
    # print(url)
    # print('-----')
  clasp_type.append(extract_data.replace('\xa0',' ').replace('\n',''))


  print("------------------")

#____________________________________________________________
#                        < CSV Files >
#____________________________________________________________

file_list= [refrences_watches, watch_url,type_w,brand_w,year_introduced_w
            ,parent_model, specific_model, nickname
            ,marketing_name, style
            ,currency_watches, salary_watches , images_url
            ,made_in
            ,case_shape ,case_material, case_finish , caseback , case_diamete,
            between_lugs , lug_to_lug , case_thickness , bezel_material ,
            bezel_color , crystal ,case_water_resistance, weight, dial_color,
            dial_numerals ,bracelet_material,bracelet_color, clasp_type
            ,mov_movement,mov_caliber,mov_power_reserve, mov_frequency, mov_jewels,
            dial_feature,description , short_description_w]

exported = zip_longest(*file_list)
#----------------------------------
with open("project_webScraping_Group2.csv", "w", newline='') as myFile:
  wr = csv.writer(myFile)
  wr.writerow(["reference_number","watch_URL", "type","brand","year_introduced",
                "parent_model","specific_model", "nickname",
                "marketing_name","style",
                "currency","price","image_URL",
                "made_in","case_shape", "case_material" ,
                "case_finish","caseback","diameter","between_lugs","lug_to_lug",
                "case_thickness","bezel_material","bezel_color","crystal",
                "water_resistance","weight","dial_color","numerals","bracelet_material",
                "bracelet_color","clasp_type","movement","caliber","power_reserve",
                "frequency","jewels","features","description" ,"short_description" ])
  wr.writerows(exported)

