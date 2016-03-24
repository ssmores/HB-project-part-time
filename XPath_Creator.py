"""
Project: XPath generator for XML schema. 

The schema will have to be used/accessed/saved locally (not uploaded to GitHub).

There are a handful of namespaces used in this program.  They are referenced in this program by the following abbreviations:
	tns
	mismo
	xs


This version will capture the attribute's enumerations.  You can build this yourself.  You got this.

"""

# Open the schema, read each line as a list. 
with open("ComplianceAnalyzer-request.xsd") as my_schema:
	lines = my_schema.readlines()

# Iterate over each line in the list, and write them into a text file. 
with open('lines2.txt', 'w') as target:
	for line in lines:
		target.write(line)

	# Each element line has its actual element name, and its type.  The name is the key and the type is the value in the ElementTypeToItsElementName dictionary.
	# For example, <xs:element name="_APPLICATION" type="tns:LOAN_APPLICATIONType" .../>, will have a key and a value pair in this dictionary.   
	ElementTypeToItsElementName = {}

	# Each element generally has a parent complexType.  The complexType line will have a name.  The element name is the key, the complextType will be the value.
	# In the snippet below, the value of "LOAN" will be the key, and the value of ACS_REQUESTType will be the value in the ElementNameToItsParentComplexType dictariony.
		# <xs:complexType name="ACS_REQUESTType">
		# <xs:sequence ... >
		# 	<xs:element name="LOAN" type="tns:LOANType" .../>.  
	ElementNameToItsParentComplexType = {}

	# 
	AttributeNameToItsElementType = {}
	AttributeDataTypeToItsAttributeName = {}
	AttributeNameToItsAttributeType = {}
	AttributeNameToItsXpath = {}
	SimpleTypeToItsEnumerations = {}
	EnumerationValueToItsAttributeName = {}
	currentComplexTypeName = None
	currentAttributeName = None
	currentSimpleTypeName = None


	# This will build the dictionaries based on all the information in the schema.
	for line in lines:
		complexTypeIndex = line.find("<xs:complexType")
		elementTagIndex = line.find("<xs:element")
		attributeTagIndex = line.find("<xs:attribute")
		datatypeTagIndex = line.find("<mismo:DATATYPE>")
		simpleTypeTagIndex = line.find("<xs:simpleType")
		enumerationTagIndex = line.find("<xs:enumeration")

		if complexTypeIndex >= 0:
			# Parse the line for the name & set the name value as the currentComplexTypeName
			complexName_split = line.split(" ")
			currentComplexTypeName = complexName_split[1].split('"')[1]
		elif elementTagIndex >= 0:
			# Parse the line for the type (starts with tns:), which will be set as the key in ElementTypeToItsElementName dictionary
			# Parse the line for the name, which will be the value in ElementTypeToItsElementName dictionary
			elementName_split = line.split(" ")
			ElementTypeToItsElementName_key = elementName_split[2].split('"')[1].split("tns:")[1]
			ElementTypeToItsElementName_value = elementName_split[1].split('"')[1]
			ElementTypeToItsElementName[ElementTypeToItsElementName_key] = ElementTypeToItsElementName_value 
			# Parse the line for the name, which will also be the key in ElementNameToItsParentComplexType dictionary
			# Set the currentComplexType as the value in ElementNameToItsParentComplexType dictionary
			ElementNameToItsParentComplexType[ElementTypeToItsElementName_value] = currentComplexTypeName
		elif attributeTagIndex >= 0:
			# Parse the line for the name, which will be the key for AttributeNameToItsElementType dictionary
			# Set the currentComplexTypeName as the value in AttributeNameToItsElementType dictionary
			attributeName_split = line.split(" ")
			currentAttributeName = attributeName_split[1].split('"')[1]
			if currentAttributeName in AttributeNameToItsElementType: 
				AttributeNameToItsElementType[currentAttributeName].append(currentComplexTypeName)
			else: 
				AttributeNameToItsElementType[currentAttributeName] = [currentComplexTypeName]

			# This split would be needed in order to get the attribute's enumeration type.  

			# Right now this does the attribute name to its enumerate type.  
			# I can also change it around, OR make another library, where you go enumeration to attribute name... 
			# THINK ABUOT IT LATER WHEN YOU DO THE OTHER METHOD... 
			# As I slowly think about this, I think I like this the attribute name to its enumerated type... 

			attributeEnumerationTagIndex = line.find("type=")
			if attributeEnumerationTagIndex >= 0:
				attributeType_split = line.split(" ")
				attributeType = attributeType_split[2].split('"')[1].split(":")[1]
				if attributeType in AttributeNameToItsAttributeType:
					AttributeNameToItsAttributeType[currentAttributeName].append(attributeType)
				else:
					AttributeNameToItsAttributeType[currentAttributeName] = [attributeType]


		elif simpleTypeTagIndex >= 0:
			# Parse the lines for the simpletype lines.  
			# The simpleType lines have a name attribute afterwards, which are part of the attribute enumeration type.  These should be the key in a new library, and the enumerations should be in a list for the values.
			simpleTypeNameIndex = line.find("name=")
			if simpleTypeNameIndex >= 0:
				simpleTypeName_split = line.split(" ")
				currentSimpleTypeName = simpleTypeName_split[1].split('"')[1]
				SimpleTypeToItsEnumerations[currentSimpleTypeName] = []
				

		elif enumerationTagIndex >= 0:
			enumerationValue_split = line.split(" ")
			# The simpleType lines that don't have a name attribute afterwards, their enumerations follow in their own enumeration lines.  These should use the currentAttributeName as the key.
			if enumerationTagIndex >= 0:
				enumerationValue_split = line.split(" ")
				enumerationValue = enumerationValue_split[1].split('"')[1]
				if currentAttributeName in EnumerationValueToItsAttributeName:
					EnumerationValueToItsAttributeName[currentAttributeName].append(enumerationValue)
				else:
					EnumerationValueToItsAttributeName[currentAttributeName] = [enumerationValue]

				# if currentSimpleTypeName in SimpleTypeToItsEnumerations.keys():
				# 	SimpleTypeToItsEnumerations[currentSimpleTypeName].append(enumerationValue)






			




		elif datatypeTagIndex >= 0:
			# Parse the line for the name, which will be the key for AttributeDataTypeToItsAttributeName dictionary
			# Set the currentAttributeName as the value in AttributeDataTypeToItsAttributeName dictionary
			dataTypeToItsAttributeName_key = line.split("<mismo:DATATYPE>")[1].split('</mismo:DATATYPE')[0]
			if dataTypeToItsAttributeName_key in AttributeDataTypeToItsAttributeName:
				AttributeDataTypeToItsAttributeName[dataTypeToItsAttributeName_key].append(currentAttributeName)
			else:
				AttributeDataTypeToItsAttributeName[dataTypeToItsAttributeName_key] = [currentAttributeName]



	for attribute_name_from_dictionary in AttributeNameToItsElementType:

		build1 = AttributeNameToItsElementType[attribute_name_from_dictionary]

		# There needs to be a loop between the element type and the element name.  The element name needs to be added to the xpath_print variable. 
		
		for elementNameInList in build1: 
			build2 = ElementTypeToItsElementName[elementNameInList]


			xpath_print = "/%s/@%s" % (build2, attribute_name_from_dictionary)
			
			while build2 != "ACS_REQUEST":
				build3 = ElementNameToItsParentComplexType[build2]
				build2 = ElementTypeToItsElementName[build3]

				xpath_print = "/%s%s" % (build2, xpath_print) 

			else:
				if attribute_name_from_dictionary in AttributeNameToItsXpath: 
					AttributeNameToItsXpath[attribute_name_from_dictionary].append(xpath_print)
				else: 
					AttributeNameToItsXpath[attribute_name_from_dictionary] = [xpath_print]



# print ElementTypeToItsElementName
# print ElementNameToItsParentComplexType
# print AttributeNameToItsXpath
# print AttributeNameToItsXpath["_IncludedInAPRIndicator"]
# print AttributeDataTypeToItsAttributeName['Money']
# print AttributeNameToItsAttributeType
# print AttributeNameToItsAttributeType.keys()
print AttributeNameToItsAttributeType.values()
# print AttributeNameToItsAttributeType["ChangedCircumstanceReason"]
# print AttributeNameToItsAttributeType["AlternateARMIndexValuePercent"]
# print currentComplexTypeName
# print currentSimpleTypeName
# print SimpleTypeToItsEnumerations
# print EnumerationValueToItsAttributeName










# def menu_options():
# 	print "If you'd like to print all the Xpaths, type 'print all'."
# 	print "If you'd like to find an Xpath of an attribute, type 'Xpath'."
# 	print "If you'd like to find the attribute's datatype, type, 'datatype'."
# 	print "If you want to exit, type exit.\n"

# # Prompt user with options to find an Xpath for an attribute, or exit. 
# print "Hello. You can print all available Xpaths in the schema to a CSV file, you can find an Xpath of an attribute, or you can exit."
# menu_options()


# desired_action = raw_input("What would you like to do now? ")
# attribute_name = ""
# while desired_action.lower() != "exit":

# 	if desired_action.lower() == "print all":
# 		import csv
# 		print_the_xpath = open('AllXpathNames.csv', 'w')
# 		xpath_writer = csv.writer(print_the_xpath)
# 		for attribute_name_from_dictionary in AttributeNameToItsXpath.values():
# 			for item in attribute_name_from_dictionary:
# 				xpath_writer.writerow([item])
# 		print_the_xpath.close()
# 		print "The 'AllXpathsNames' CSV file has been created for you!\n"

# 	elif desired_action.lower() == "xpath":
# 		attribute_name = raw_input("Enter the attribute name (or 'exit') here: ")
# 		while attribute_name.lower() != "exit":
# 			# Find the raw input attribute name from user, and search for it as a key in AttributeNameToItsElementType dictionary.
# 			if attribute_name in AttributeNameToItsElementType:
# 				# This is where the XPath will need to be constructioned.  It starts with a back slash, and then an @ symbol, and then the attribute_name.   
# 				for item in AttributeNameToItsXpath[attribute_name]:
# 					print item + "\n"
# 				attribute_name = raw_input("If you'd like to continue, enter another attribute.  If you're done, type exit. ") 
# 			else:
# 				print "Your attribute does not exist. Please input a new attribute.\n"
# 				attribute_name = raw_input("If you'd like to continue, enter another attribute.  If you're done, type exit. ") 
# 	elif desired_action.lower() == "datatype":
# 		# This can find attribute names that have a specific datatype.
# 		datatype_name = raw_input("Enter the datatype to find (or 'exit') here: ")
# 		while datatype_name.lower() != "exit":
# 			# Find the raw input datatype name from user, and search for it as a key in the AttributeDataTypeToItsAttributeName dictionary.
# 			if datatype_name in AttributeDataTypeToItsAttributeName:
# 				for item in AttributeDataTypeToItsAttributeName[datatype_name]:
# 					print item + "\n"
# 				datatype_name = raw_input("If you'd like to continue, enter another datatype.  If you're done, type exit. ") 
# 			else:
# 				print "Your datatype does not exist. Please input a new datatype.\n"
# 				datatype_name = raw_input("If you'd like to continue, enter another datatype.  If you're done, type exit. ") 
				
	
# 	menu_options()
# 	desired_action = raw_input("What would you like to do now? ")


# else:
# 	print "Thanks for stopping by!"

